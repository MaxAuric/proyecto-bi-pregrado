# Proyecto Práctico Final — Business Intelligence: Educación Superior en la Región Metropolitana (2012–2026)

> **Alcance Geográfico:** **100% focalizado en la Región Metropolitana de Santiago (`region_codigo_subdere == '13'`)**, correspondiente a **58.926 registros históricos de oferta académica (2012–2026)** (extraídos del consolidado nacional de **158.211 registros**) y **69 Instituciones de Educación Superior activas en 2026** (**35 Universidades**, **19 Institutos Profesionales**, **11 Centros de Formación Técnica** y **4 Instituciones de las Fuerzas Armadas y de Orden**).

---

## Entregables Principales (Acceso Directo en la Raíz)

| Entregable Oficial (Pauta BI) | Archivo en Raíz / Ubicación | Descripción Ejecutiva |
| :--- | :--- | :--- |
| **1. Informe Ejecutivo Final (PDF)** | [`Informe_Ejecutivo_Final_BI_RM.pdf`](./Informe_Ejecutivo_Final_BI_RM.pdf) | Informe completo de **42 páginas** (LaTeX) con resumen ejecutivo, Canvas BI, proceso ETL, modelo estrella, análisis de las 3 vistas del panel y **Anexos A–Ñ** (URLs, SHA-256, mapeo de 59 columnas y diccionario de 150 columnas). |
| **2. Presentación 15 Minutos (PDF)** | [`Presentacion_15_Minutos_BI_RM.pdf`](./Presentacion_15_Minutos_BI_RM.pdf) | Presentación ejecutiva de **12 diapositivas** diseñada para la exposición grupal de 15 minutos y defensa técnica individual. |
| **3. Panel de Control Power BI (`.pbix`)** | [`Dashboard_Final_RM.pbix`](./Dashboard_Final_RM.pbix) | Dashboard interactivo con **3 vistas de decisión** (Capacidad y Secciones de 35 plazas, Puntajes PAES vs. Acreditación SIES, y Oferta vs. Contexto Demográfico INE RM). |
| **4. DataMart Relacional Estrella RM** | [`00_DATAMART_LISTO_PARA_POWERBI/`](./00_DATAMART_LISTO_PARA_POWERBI/) | Motor relacional SQLite (`datamart_estrella_rm_final.db`), libro Excel Estrella (`DataMart_Estrella_RM_PowerBI.xlsx`) y tablas CSV del Esquema Estrella RM. |

---

## Arquitectura del Repositorio por Módulos

```text
.
├── README.md                                      <-- Portada ejecutiva del Proyecto Final BI (RM 2012-2026)
├── Informe_Ejecutivo_Final_BI_RM.pdf              <-- [ENTREGABLE] Informe Ejecutivo Final (42 páginas + Anexos A-Ñ)
├── Presentacion_15_Minutos_BI_RM.pdf              <-- [ENTREGABLE] Presentación Oficial (12 diapositivas - 15 min)
├── Dashboard_Final_RM.pbix                        <-- [ENTREGABLE] Panel interactivo Power BI conectado al DataMart
├── 01_BaseINDICES_Pregrado24.xlsx                 <-- Base histórica original 2012-2022 entregada por la cátedra
│
├── 00_DATAMART_LISTO_PARA_POWERBI/                <-- DataMart Estrella RM listo para explotación OLAP
│   ├── datamart_estrella_rm_final.db              <-- Base relacional SQLite (PKs, FKs, 0 huérfanos + Vista Maestra)
│   ├── DataMart_Estrella_RM_PowerBI.xlsx          <-- Libro Excel multi-hoja del Esquema Estrella RM
│   └── tablas_estrella_csv/                       <-- Tablas dim_*, fact_*, agregada y puente SIES en CSV UTF-8-SIG
│
├── P1_INGENIERO_DATOS_ETL_Y_DATAMART/             <-- Módulo 1: Pipeline ETL en Python, Limpieza, Tasas/KPIs y Carga SQL
│   ├── scripts/01_build_final_datamart_rm.py      <-- Script reproducible de construcción y exportación del DataMart RM
│   ├── sql/schema_final_estrella_rm.sql           <-- DDL relacional del Esquema Estrella RM
│   ├── insumos/                                   <-- Consolidado 2012-2026 (.parquet), INE RM, SIES y Tabla Puente
│   ├── auditoria/                                 <-- Certificación de cuadre (58.926 filas RM / 158.211 nacional)
│   └── docs/guia_uso_datamart_y_kpis_p1.md        <-- Documentación de cumplimiento de rúbrica y buenas prácticas DW
│
├── P2_ANALISTA_NEGOCIO_RM/                        <-- Módulo 2: Propuesta de Valor, Canvas BI 10 bloques y Caso 35 plazas
│   ├── docs/                                      <-- Sección 1 en LaTeX, Canvas BI RM y Análisis de KPIs
│   └── scripts/analisis_negocio_rm.py             <-- Script de validación de indicadores de negocio RM 2026
│
├── P3_ARQUITECTO_MODELO_ESTRELLA/                 <-- Módulo 3: Diseño Dimensional Estrella, Aditividad y SCD
│   ├── diagramas/                                 <-- Diagramas del Esquema Estrella RM en alta resolución (.png, .svg, .mmd)
│   ├── docs/                                      <-- Informe de arquitectura y Diccionario Técnico de Tasas y KPIs
│   ├── scripts/                                   <-- Auditoría automática de integridad referencial (0 huérfanos)
│   └── sql/                                       <-- Esquema DDL canónico
│
├── P4_DESARROLLADOR_POWERBI_Y_DAX/                <-- Módulo 4: Modelo Semántico Power BI y Catálogo de Medidas DAX
│   ├── Dashboard_Final_RM.pbix                    <-- Panel Power BI con las 3 vistas ejecutivas de la RM
│   ├── docs/                                      <-- Catálogo DAX (DIVIDE/SUMX), diseño de vistas e informe técnico
│   └── scripts/validar_modelo_powerbi.py          <-- Script de validación automática del DataMart
│
└── P5_INFORME_FINAL_Y_PPT_15MIN/                  <-- Módulo 5: Consolidación Editorial, Gobernanza, Informe y PPT
    ├── Informe_Ejecutivo_Final_BI_RM.pdf          <-- Informe Ejecutivo Final consolidado (42 páginas)
    └── Presentacion_15_Minutos_BI_RM.pdf          <-- Presentación para defensa grupal e individual (12 slides)
```

---

## Cifras Oficiales Auditadas (Región Metropolitana 2012–2026)

- **Consolidado Nacional (2012–2026):** `158.211` registros (`114.265` base 2012–2022 + `43.946` extensión 2023–2026).
- **Subconjunto Región Metropolitana (`SUBDERE 13`):** `58.926` registros históricos en `15` años (`1.298` fotografías institucionales anuales, `22` etiquetas de sede y `5.184` perfiles curriculares).
- **Fotografía RM 2026:**
  - **Matrícula de primer año:** `208.311` matriculados.
  - **Vacantes declaradas:** `253.018` vacantes (en `3.284` registros con vacantes positivas).
  - **Ocupación comparable:** `82,31%` (`208.251` matriculados en registros con vacantes / `253.018` vacantes).
  - **Presión de capacidad (Escenario de 35 plazas por sección):** `1.232` registros sobreocupados (`>100%`) que generan **`674` secciones adicionales modeladas** (concentradas en un `73,59%` en Tecnología con `268`, Administración y Comercio con `127` y Salud con `101`).
  - **Selectividad PAES 2026:** Promedio ponderado de **`703,59` puntos** y corte ponderado de **`622,89` puntos** (sobre `68.085` matriculados en registros con puntaje válido).
  - **Contexto Demográfico INE RM 2026:** Población publicada de 15 a 64 años de **`5.868.843` habitantes**, con **`35,49` ingresos** y **`43,11` vacantes** por cada 1.000 habitantes (`+5,86%` variación anual de matrícula).
