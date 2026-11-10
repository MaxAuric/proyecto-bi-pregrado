# Entregables Hito 2 — Modelo Dimensional y DataMart Relacional
## Proyecto Practico Final de Business Intelligence (2012–2026)

Este directorio contiene la solucion formal, reproducible y verificada para el **Hito 2** del proyecto, reorientado estratégicamente hacia la **Region Metropolitana de Santiago (RM)** segun la retroalimentacion del profesor.

---

## Estructura Modular de `Avance Hito 2/`

```text
Avance Hito 2/
├── P1/                                         # Entregables de Persona 1: Ingeniero de Datos
│   ├── 00_DOCUMENTOS_PARA_PRESENTAR_Y_DEFENDER/
│   │   ├── Informe_Hito2_Persona1_DataMart.pdf     # Informe técnico formal de Persona 1
│   │   ├── Informe_Hito2_Persona1_DataMart.tex     # Codigo fuente LaTeX del informe
│   │   └── RESUMEN_FEEDBACK_Y_REORIENTACION_HITO2.md # Sintesis ejecutiva de la reorientacion a RM
│   ├── 03_DATAMART_SCRIPTS_DDL_Y_CARGA/           # DataMart fisico y scripts de carga
│   │   ├── schema_datamart.sql                     # Script DDL formal (CREATE TABLE, PK, FK, Indices)
│   │   ├── 01_build_and_load_datamart.py           # Pipeline de carga masiva automatizada en Python
│   │   ├── datamart_indices_2012_2026.db           # Base de datos relacional SQLite (DataMart fisico)
│   │   └── vistas_analiticas_rm.sql                # Vistas optimizadas para la Region Metropolitana
│   ├── 04_CERTIFICACION_CUADRE_Y_AUDITORIA/       # Certificacion de cuadre contra la fuente (4 Pts Pauta)
│   │   ├── 02_verify_cuadre_datamart.py            # Script automatizado de auditoria matematica
│   │   ├── reporte_cuadre_datamart.md              # Tabla de Control Totals y certificacion formal
│   │   └── reporte_cuadre_datamart.json            # Reporte estructurado para evaluacion automatizada
│   └── 05_CONEXION_POWERBI_Y_PRUEBAS/             # Conexion directa DataMart -> Power BI (Persona 4)
│       └── guia_conexion_powerbi_datamart.md       # Guia paso a paso para cumplir "Conectado al DataMart, no a Excel"
│
├── P2_PROPUESTA_VALOR_Y_CANVAS_BI_RM/          # Entregables de Persona 2: Analista de Negocio
│   └── 01_PROPUESTA_VALOR_Y_CANVAS_BI_RM/
│       ├── data_rm/                                # Conjuntos de datos filtrados para la RM e integracion externa
│       │   ├── rm_ext_ine_poblacion.csv            # Proyecciones demograficas INE (2002–2035) RM
│       │   ├── rm_ext_sies_acreditacion.csv        # Acreditacion institucional SIES RM
│       │   ├── rm_kpi_p1_sobredemanda.csv          # KPIs Pregunta 1
│       │   ├── rm_kpi_p2_puntajes_paes.csv         # KPIs Pregunta 2
│       │   └── rm_kpi_p3_absorcion_demografica.csv # KPIs Pregunta 3
│       ├── docs/                                   # Documentacion formal y Canvas BI RM
│       │   ├── diccionario_fuentes_rm_hito2.md     # Diccionario de fuentes externas
│       │   └── informe_hito2_persona2.tex          # Informe técnico Canvas BI y Preguntas de Negocio
│       └── scripts/                                # Scripts de extraccion y validacion de llaves RM
│           ├── 08_extract_rm_data.py               # Extraccion y filtrado
│           └── 09_validate_rm_keys.py              # Validacion de integridad de llaves
│
├── P3_MODELO_DIMENSIONAL_Y_ARQUITECTURA/       # Entregables de Persona 3: Arquitecto de Datos (Angel Pino)
│   ├── README.md                                  # Guia del modulo de arquitectura
│   ├── schema_dimensional_star.sql                # Script DDL canonico formal del Esquema Estrella
│   ├── diagramas/                                 # Diagramas del modelo dimensional
│   │   ├── diagrama_modelo_dimensional_estrella.svg # Diagrama vectorial SVG
│   │   ├── diagrama_modelo_dimensional_estrella.png # Render PNG alta resolucion (300 DPI)
│   │   └── diagrama_modelo_dimensional_estrella.mmd # Codigo fuente Mermaid
│   ├── scripts/                                   # Scripts reproducibles de arquitectura
│   │   ├── generate_star_diagram.py               # Generador programatico de diagramas
│   │   └── audit_architecture_and_integrity_p3.py # Auditoria de 0 huérfanos, grano y benchmarks (< 25 ms)
│   └── docs/                                      # Documentacion e informes técnicos
│       ├── informe_hito2_persona3_arquitectura.tex  # Informe formal en LaTeX (estilo ejecutivo)
│       ├── informe_hito2_persona3_arquitectura.md   # Informe técnico en Markdown con tablas y formulas
│       └── auditoria_arquitectura_p3.json           # Datos estructurados JSON de la auditoria
│
└── P4_DESARROLLADOR_BI/                       # Entregables de Persona 4: Desarrollador BI
    ├── README.md                                  # Guía del módulo y resumen de resultados
    ├── powerbi_templates/                         # Plantillas de conexión y scripts M/Python
    │   └── conexion_powerquery_m.pq               # Script de conexión directa DataMart -> Power BI
    ├── scripts/                                   # Scripts reproducibles de auditoría y conexión
    │   └── audit_and_test_connections_p4.py       # Suite de pruebas de jerarquías y latencias
    └── docs/                                      # Documentación formal e informes técnicos
        ├── informe_hito2_persona4_desarrollador_bi.md # Informe técnico formal de Persona 4
        ├── modelado_jerarquias_y_filtros_p4.md    # Especificación exhaustiva de las 4 jerarquías
        ├── protocolo_pruebas_conexion_datamart_p4.md # Protocolo de pruebas de conexión
        └── certificacion_conexion_jerarquias_p4.json # Certificación y benchmarks estructurados

└── P5_GESTOR_DOCUMENTACION_Y_CALIDAD/         # Entregables de Persona 5: Gestor de Proyecto, Documentador y Calidad
    ├── README.md                                  # Guía del módulo y matriz de certificación
    ├── docs/                                      # Informes técnicos, justificaciones y guías de defensa
    │   ├── informe_hito2_persona5_calidad_gobernanza.pdf # Informe técnico formal en PDF (compilado)
    │   ├── informe_hito2_persona5_calidad_gobernanza.tex # Código fuente LaTeX del informe de calidad
    │   ├── informe_hito2_persona5_calidad_gobernanza.md  # Informe técnico en Markdown
    │   ├── documentacion_tecnica_aditividad_y_scd2.md    # Fundamentación formal de Kimball y SCD2
    │   └── Guia_Estudio_Defensa_Hito2_BI.pdf             # Guía maestra de estudio para presentar y defender
    ├── auditoria/                                 # Matrices de evaluación y certificación oficial
    │   ├── matriz_certificacion_hito2.md                 # Matriz de cumplimiento ítem por ítem
    │   └── auditoria_cumplimiento_rubrica_hito2.json     # Datos estructurados JSON de la rúbrica (10/10)
    └── scripts/                                   # Pipeline automatizado de calidad y compilación
        └── 12_audit_and_generate_p5_hito2.js             # Generador de reportes, PDFs y auditoría integral
```

---

##  Como Reproducir y Auditar el DataMart Completo

Todo el pipeline es 100% reproducible y automatizado:

1. **Construir y Poblar el DataMart Relacional (Persona 1):**
   ```bash
   python "Avance Hito 2/P1/03_DATAMART_SCRIPTS_DDL_Y_CARGA/01_build_and_load_datamart.py"
   ```
2. **Auditar y Certificar el Cuadre Estricto de Filas (Persona 1):**
   ```bash
   python "Avance Hito 2/P1/04_CERTIFICACION_CUADRE_Y_AUDITORIA/02_verify_cuadre_datamart.py"
   ```
3. **Auditar la Arquitectura Dimensional, Integridad y Latencias (Persona 3):**
   ```bash
   python "Avance Hito 2/P3_MODELO_DIMENSIONAL_Y_ARQUITECTURA/scripts/audit_architecture_and_integrity_p3.py"
   ```
4. **Regenerar Diagramas Vectoriales del Esquema Estrella (Persona 3):**
   ```bash
   python "Avance Hito 2/P3_MODELO_DIMENSIONAL_Y_ARQUITECTURA/scripts/generate_star_diagram.py"
   ```
5. **Auditar la Gobernanza, Certificar Rúbrica y Generar PDFs (Persona 5):**
   ```bash
   node "Avance Hito 2/P5_GESTOR_DOCUMENTACION_Y_CALIDAD/scripts/12_audit_and_generate_p5_hito2.js"
   ```

---

##  Resumen de Resultados Técnicos Certificados (Hito 2)

1. **Cuadre Perfecto contra la Fuente (0 Pérdidas, 0 Duplicados):**
   * Registros en fuente original consolidada: **158.211 filas**.
   * Registros en `fact_matricula_admision`: **158.211 filas**.
   * Diferencia neta: **0 registros**.
   * Integridad referencial: **100,0%** (**0 registros huérfanos** en todas las claves foraneas).

2. **Universo de la Region Metropolitana:**
   * La RM concentra **58.926 ofertas / 82.348 registros totales** de pregrado (mas del 52% de la base nacional).
   * Vistas especializadas (`vw_rm_sobredemanda_y_capacidad`, `vw_rm_evolucion_selectividad_paes`, `vw_rm_absorcion_demografica_ine`) para alimentar Power BI Desktop.

3. **Arquitectura Dimensional Formal (Kimball):**
   * **Tabla de Hechos Central:** `fact_matricula_admision` (Grano atomico: oferta de programa, sede, horario y año).
   * **Dimensiones:** `dim_tiempo`, `dim_sede_geografia`, `dim_institucion` (con historial SCD Tipo 2 anual), `dim_carrera_programa` y `dim_poblacion_rm` (INE).
   * **Aditividad:** Matricula y vacantes completamente aditivas; puntajes PAES estrictamente no aditivos (promedios ponderados por matricula en DAX).
