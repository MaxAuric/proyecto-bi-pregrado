# Guía Técnica Persona 1: Auditoría de Rúbrica, Buenas Prácticas de Clases y Catálogo del DataMart Estrella RM

**Rol:** Persona 1 — Ingeniero de Datos (ETL, Integración de Fuentes Externas, Cálculo de Tasas/KPIs y Carga del DataMart)  
**Alcance Geográfico:** **Exclusivamente Región Metropolitana de Santiago (`region_codigo_subdere == '13'`)**  
**Volumen Auditado RM:** `58.926` registros históricos de oferta académica (2012–2026) | `69` IES activas en 2026 (`35` Universidades, `19` Institutos Profesionales, `11` Centros de Formación Técnica, `4` FF.AA. y Orden).

---

## 1. Verificación de Cumplimiento contra la Rúbrica Oficial (`Pauta_Trabajo_Final_BI.pdf`)

| Requisito de la Pauta Oficial | Estado en `Final/` (Persona 1) | Evidencia Técnica Implementada |
| :--- | :---: | :--- |
| **Integración 2023–2026 a la base 2012–2022 y Cuadre Exacto** (Etapa 2 y 5) | **100% Cumplido** | Consolidación auditada de `158.211` registros nacionales y filtrado físico de los **`58.926` registros de la Región Metropolitana de Santiago** en `fact_matricula_admision`, con cuadre exacto certificado en `reporte_cuadre_y_kpis_final.json`. |
| **Homologación de Puntajes (PSU 2012–2020, PDT 2021–2022, PAES 2023–2026)** (Etapa 2) | **100% Cumplido** | Se entregan las 4 variantes numéricas en `fact_matricula_admision`: `puntaje_promedio_original`, `puntaje_promedio_norm_0_100`, `puntaje_promedio_equiv_paes` (escala unificada 100–1000) y `puntaje_promedio_zscore_anual`. |
| **Tratamiento Justificado de Nulos (~80% en puntajes y ~25% en vacantes)** (Etapa 2) | **100% Cumplido** | Jamás se imputan con cero (evita sesgar promedios y tasas). Se preservan como `NULL` en SQLite/Excel y se gobiernan con los flags binarios `flag_exige_prueba_admision` (`0/1`) y `flag_vacantes_declaradas` (`0/1`). |
| **Integración de 2 Fuentes Externas, Tabla Puente y Tasa de Coincidencia** (Etapa 3, Pág. 3) | **100% Cumplido** | 1. **INE RM** integrada en `dim_tiempo_ine_rm` (`100%` coincidencia en los 15 años).<br>2. **SIES Acreditación** integrada en `dim_institucion_sies` mediante la tabla puente `puente_institucion_sies` (incluida dentro del `.db` y `.xlsx`), con reporte explícito de tasa de coincidencia y tratamiento de instituciones cerradas pre-2018. |
| **Scripts de Creación (DDL) y de Carga Reproducibles** (Etapa 5) | **100% Cumplido** | DDL formal en `sql/schema_final_estrella_rm.sql` y pipeline automatizado en `scripts/01_build_final_datamart_rm.py`. |

---

## 2. Verificación contra las Buenas Prácticas del Material de Clases (`Material_extra_clases`)

| Documento de Clase | Regla / Buena Práctica Enseñada por el Profesor | Cómo la Cumple Nuestro DataMart Final |
| :--- | :--- | :--- |
| **`Clase 4 - DW.pdf` (Pág. 62 - Error 1)** | *"Errores: Incluir atributos de texto en una tabla de hechos, si se hace con la intención de filtrar o agrupar."* | **`fact_matricula_admision` tiene CERO columnas `VARCHAR`**. Solo contiene claves foráneas enteras (`INTEGER`), flags binarios (`0/1`), código numérico de estado (`1..4`), conteos enteros y tasas/medidas reales (`REAL`). |
| **`Clase 4 - DW.pdf` (Pág. 62 - Error 2)** | *"Errores: Abreviar las descripciones en las tablas de dimensión con la intención de reducir el espacio requerido."* | Se eliminó el 100% de abreviaturas (`'Univ.'` $\rightarrow$ `'Universidad'`, `'I.P.'` $\rightarrow$ `'Instituto Profesional'`, `'C.F.T.'` $\rightarrow$ `'Centro de Formación Técnica'`, `'F.F.A.A.'` $\rightarrow$ `'Institución de las Fuerzas Armadas y de Orden'`, `'M/'` $\rightarrow$ `'con Mención en'`) y se limpiaron todos los prefijos `'(a)'`, `'(b)'`, `'(c)'` en `subtipo_institucion`, `acreditacion_cned`, `autonomia` y `gratuidad`. |
| **`Clase 4 - DW.pdf` (Pág. 62 - Error 3)** | *"Dividir las jerarquías en múltiples dimensiones vs. Modelo en Estrella donde una única tabla contiene toda la información de la jerarquía."* | Cada dimensión consolida su jerarquía completa en una sola tabla desnormalizada: `dim_sede_geografia` (`macro_zona` $\rightarrow$ `region_nombre_estandar` $\rightarrow$ `nombre_sede`), `dim_carrera_programa` (`area_conocimiento` $\rightarrow$ `carrera_generica` $\rightarrow$ `nombre_programa` $\rightarrow$ `horario`), `dim_institucion_sies` (`tipo_institucion` $\rightarrow$ `subtipo_institucion` $\rightarrow$ `nombre_institucion`). |
| **`Clase 4 - DW.pdf` (Pág. 29)** | *"Medidas del cubo de datos: Distributivas (`sum`, `count`), Algebraicas (`avg`, tasas/razones) y Holísticas (`median`, `rank`)."* | Se separan explícitamente las medidas **Distributivas/Aditivas** (matrícula, vacantes, secciones de laboratorio) de las **Algebraicas/No Aditivas** (tasas de ocupación, tasas de sobredemanda, puntajes ponderados), las cuales se recalculan con `DIVIDE()` en DAX. |
| **`Clase 4 - DW.pdf` (Pág. 52, 57 y 62)** | *"Agregar claves sustitutas (`Surrogate Keys`), evitar 'smart keys' y afrontar las dimensiones lentamente cambiantes (SCD)."* | Se usan claves subrogadas enteras (`id_institucion_sk`, `id_sede_geografia`, `id_carrera_programa_sk`) y se modela **SCD Tipo 2** en `dim_institucion_sies` para capturar los cambios anuales de Acreditación, Gratuidad y Autonomía. |
| **`Clase 4 - DW.pdf` (Pág. 63) y `Clase 5 - ETLv2.pptx` (Slide 10)** | *"No omitir las tablas agregadas para afrontar problemas de rendimiento"* y 5 tareas ETL (*Selección, Dividir/Unir, Conversión, Resumen, Enriquecimiento*). | El pipeline ejecuta las 5 tareas de transformación y construye la tabla agregada **`agg_resumen_anual_institucion_rm`** dentro del DataMart. |
| **`Clase 3 - Arquitectura BI.pdf` (Pág. 18–20 y 29)** | *"Data Franchising (Disponibilizar los datos hacia Data Marts orientados a la herramienta de explotación)."* | Desde Python se disponibiliza el mismo Esquema Estrella tanto en motor relacional SQLite (`datamart_estrella_rm_final.db`) como en libro Excel multi-hoja (`DataMart_Estrella_RM_PowerBI.xlsx`) para importación instantánea en Power BI. |
