# Entrega Final BI — DataMart Estrella Región Metropolitana (Santiago) 2012–2026

> **Alcance Geográfico:** **100% focalizado en la Región Metropolitana de Santiago (`region_codigo_subdere == '13'`)**, correspondiente a **58.926 registros históricos de oferta académica (2012–2026)** y **69 Instituciones de Educación Superior activas en 2026** (35 Universidades, 19 Institutos Profesionales, 11 Centros de Formación Técnica y 4 Instituciones de las FF.AA. y Orden).

---

## Estructura del Directorio `Final/`

```text
Final/
├── 00_DATAMART_LISTO_PARA_POWERBI/
│   ├── DataMart_Estrella_RM_PowerBI.xlsx      <-- [RECOMENDADO P4] Libro Excel multi-hoja listo para importar en 1 clic a Power BI
│   ├── datamart_estrella_rm_final.db          <-- Base relacional SQLite con el Esquema Estrella RM + Vistas Analíticas
│   └── tablas_estrella_csv/                   <-- Tablas dim_* y fact_* en CSV UTF-8-SIG (importación directa de carpeta)
│       ├── dim_tiempo_ine_rm.csv
│       ├── dim_institucion_sies.csv
│       ├── dim_ubicacion_rm.csv
│       ├── dim_programa_academico.csv
│       ├── dim_modalidad_jornada.csv
│       └── fact_matricula_rm.csv
├── P1_INGENIERO_DATOS_ETL_Y_DATAMART/         <-- Rol 1: Ingeniería de Datos, ETL 100% Terminado en Python y Tasas/KPIs
│   ├── scripts/01_build_final_datamart_rm.py
│   ├── sql/schema_final_estrella_rm.sql
│   ├── auditoria/
│   │   ├── reporte_cuadre_y_kpis_final.json
│   │   └── reporte_cuadre_y_kpis_final.md
│   └── docs/guia_uso_datamart_y_kpis_p1.md
├── P2_ANALISTA_NEGOCIO_RM/                    <-- Rol 2: Propuesta de Valor, Caso 120->140 y Foco Demográfico/SIES RM
├── P3_ARQUITECTO_MODELO_ESTRELLA/             <-- Rol 3: Modelo Estrella, Diccionario de Tasas/KPIs y Gobierno de Datos
├── P4_DESARROLLADOR_POWERBI_Y_DAX/            <-- Rol 4: Dashboard Power BI (.pbix), Medidas DAX con DIVIDE() y UX
└── P5_INFORME_FINAL_Y_PPT_15MIN/              <-- Rol 5: Informe Ejecutivo Final y Presentación PPT (Defensa 15 min)
```

---

## Mejoras Aplicadas según Feedback del Hito 2

1. **Transformación 100% Terminada en Python (Cero Abreviaturas en Dimensiones):**
   - Siguiendo las buenas prácticas de *Data Warehouse* (`Clase 4 - DW`, pág. 62), todas las descripciones en las tablas de dimensión vienen completamente expandidas desde Python:
     - `'Univ.'` $\rightarrow$ `'Universidad'`
     - `'I.P.'` $\rightarrow$ `'Instituto Profesional'`
     - `'C.F.T.'` $\rightarrow$ `'Centro de Formación Técnica'`
     - `'F.F.A.A.'` $\rightarrow$ `'Institución de las FF.AA. y Orden'`
   - Las **2 fuentes externas** (Proyecciones Demográficas **INE RM** y Acreditación Institucional **SIES/CNA**) fueron integradas directamente dentro de `dim_tiempo_ine_rm` y `dim_institucion_sies`.

2. **Importación Directa y Rápida a Power BI (Excel / CSV / SQLite):**
   - En lugar de ejecutar un script de Python dentro de Power Query o cargar archivos planos crudos desordenados, el script `01_build_final_datamart_rm.py` ordena, limpia, cruza e integra todo en Python y exporta **`DataMart_Estrella_RM_PowerBI.xlsx`** (con las 5 dimensiones, la tabla de hechos y las 3 vistas ejecutivas en hojas separadas), permitiendo que Power BI lo importe nativamente en pocos segundos.

3. **Nuevas Tasas y KPIs en Tablas `dim_*` y `fact_*` que Tributan a la Propuesta de Valor:**
   - **`dim_tiempo_ine_rm`:** `tasa_absorcion_1er_anio_sobre_jovenes_rm_pct`, `tasa_cobertura_bruta_rm_pct`, `tasa_ocupacion_vacantes_rm_anual_pct`, `variacion_interanual_mat_1er_anio_pct`, `indice_crecimiento_base2012_mat_1er_anio`.
   - **`dim_institucion_sies`:** `anios_acreditacion_sies`, `tramo_acreditacion_sies`, `score_calidad_sies_pct`, `cuota_mercado_rm_2026_pct`, `tasa_ocupacion_inst_rm_2026_pct`, `tasa_retencion_estructural_inst_pct`, `indice_posicionamiento_competitivo_rm`.
   - **`dim_ubicacion_rm`:** `participacion_sede_en_rm_2026_pct`, `tasa_ocupacion_sede_2026_pct`, `indice_saturacion_sede_rm`.
   - **`dim_programa_academico`:** `participacion_area_rm_2026_pct`, `tasa_ocupacion_programa_2026_pct`, `tasa_presion_laboratorio_base35_pct`, `nivel_demanda_programa_rm`.
   - **`fact_matricula_rm`:** `tasa_ocupacion_vacantes_pct`, `tasa_sobredemanda_pct`, `tasa_selectividad_ingreso_pct`, `tasa_renovacion_cohorte_pct`, `tasa_retencion_aparente_pct`, `secciones_lab_requeridas_35`, `tasa_saturacion_secciones_lab_pct`, `brecha_alumnos_sin_laboratorio` (modela directamente el caso de pasar de **120 a 140 estudiantes** con capacidad de **35 alumnos por laboratorio**), `brecha_dispersion_puntaje_pt`, `tasa_heterogeneidad_academica_pct`.
