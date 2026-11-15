# Entrega Final BI — DataMart Estrella Región Metropolitana (Santiago) 2012–2026

> **Alcance Geográfico:** **100% focalizado en la Región Metropolitana de Santiago (`region_codigo_subdere == '13'`)**, correspondiente a **58.926 registros históricos de oferta académica (2012–2026)** y **69 Instituciones de Educación Superior activas en 2026** (35 Universidades, 19 Institutos Profesionales, 11 Centros de Formación Técnica y 4 Instituciones de las Fuerzas Armadas y de Orden).

---

## Estructura del Directorio `Final/`

```text
Final/
├── 00_DATAMART_LISTO_PARA_POWERBI/
│   ├── DataMart_Estrella_RM_PowerBI.xlsx      <-- [RECOMENDADO P4] Libro Excel Estrella listo para importar en 1 clic a Power BI
│   ├── datamart_estrella_rm_final.db          <-- Base relacional SQLite con el Esquema Estrella RM + Vista Maestra + Tabla Agregada
│   └── tablas_estrella_csv/                   <-- Tablas dim_*, fact_* y puente en CSV UTF-8-SIG (nombres idénticos a SQLite)
│       ├── dim_tiempo_ine_rm.csv
│       ├── dim_sede_geografia.csv
│       ├── dim_institucion_sies.csv
│       ├── dim_carrera_programa.csv
│       ├── fact_matricula_admision.csv
│       ├── agg_resumen_anual_institucion_rm.csv
│       └── puente_institucion_sies.csv
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

## Cumplimiento de Pauta Oficial y Buenas Prácticas de Clases (`Clase 3`, `Clase 4`, `Clase 5`, `Clase 6`)

1. **Transformación 100% Terminada en Python (Cero Abreviaturas ni Prefijos Crudos en Dimensiones — `Clase 4 DW`, pág. 62):**
   - Se eliminaron todas las abreviaturas (`'Univ.'` $\rightarrow$ `'Universidad'`, `'I.P.'` $\rightarrow$ `'Instituto Profesional'`, `'C.F.T.'` $\rightarrow$ `'Centro de Formación Técnica'`, `'F.F.A.A.'` $\rightarrow$ `'Institución de las Fuerzas Armadas y de Orden'`, `'M/'` $\rightarrow$ `'con Mención en'`) y todos los prefijos crudos (`'(a)'`, `'(b)'`, `'(c)'`, etc.) en `subtipo_institucion`, `acreditacion_cned`, `autonomia` y `gratuidad`.
   - **Cero columnas de texto (`VARCHAR`) en la tabla de hechos (`fact_matricula_admision`)**, cumpliendo estrictamente el primer mandamiento de `Clase 4 - DW.pdf` (pág. 62): *"Errores: Incluir atributos de texto en una tabla de hechos"*.
   - Las **2 fuentes externas** (Proyecciones Demográficas **INE RM** y Acreditación Institucional **SIES/CNA**) están integradas directamente dentro de `dim_tiempo_ine_rm` y `dim_institucion_sies`, acompañadas de la tabla puente `puente_institucion_sies` (`Pauta Oficial`, pág. 3).

2. **Tablas Agregadas y Exportación Directa a Power BI (`Clase 4 DW`, pág. 63 y `Clase 5 ETL`, slide 10):**
   - Se incluye la tabla agregada `agg_resumen_anual_institucion_rm` para acelerar consultas ejecutivas OLAP.
   - Tanto `datamart_estrella_rm_final.db` como `DataMart_Estrella_RM_PowerBI.xlsx` comparten exactamente los mismos nombres de tablas y columnas.

3. **Nuevas Tasas y KPIs en Tablas `dim_*` y `fact_matricula_admision` que Tributan a la Propuesta de Valor:**
   - **`dim_tiempo_ine_rm`:** `tasa_absorcion_juvenil_rm_pct`, `tasa_cobertura_bruta_rm_pct`, `tasa_oferta_vacantes_1000_jovenes_rm`, `tasa_ocupacion_anual_rm_pct`, `tasa_crecimiento_matricula_rm_yoy_pct`.
   - **`dim_institucion_sies`:** `anos_acreditacion_sies`, `score_calidad_sies_pct`, `tramo_acreditacion_sies`, `tasa_ocupacion_inst_anual_pct`, `tasa_programas_sobredemanda_inst_pct`, `cuota_mercado_matricula_rm_pct`, `tasa_permanencia_cohortes_sup_pct`, `posicionamiento_competitivo_rm`.
   - **`dim_sede_geografia`:** `tasa_ocupacion_historica_sede_pct`, `tasa_sobredemanda_sede_pct`, `participacion_matricula_rm_sede_pct`, `nivel_saturacion_sede`.
   - **`dim_carrera_programa`:** `tasa_ocupacion_historica_prog_pct`, `tasa_frecuencia_sobredemanda_prog_pct`, `tasa_presion_lab_base35_prog_pct`, `clasificacion_presion_capacidad`.
   - **`fact_matricula_admision`:** `tasa_ocupacion_primer_ano`, `tasa_sobredemanda_oferta_pct`, `tasa_renovacion_primer_ano_pct`, `tasa_retencion_aparente_pct`, `secciones_lab_planificadas_35`, `secciones_lab_reales_35`, `secciones_extra_por_sobrecupo`, `tasa_saturacion_lab_35_pct`, `brecha_dispersa_max_min_paes`, `tasa_heterogeneidad_paes_pct`.
