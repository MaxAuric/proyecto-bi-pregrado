# Entregables Hito 2 — Modelo Dimensional y DataMart Relacional
## Proyecto Práctico Final de Business Intelligence (2012–2026)

Este directorio contiene la solución formal, reproducible y verificada para el **Hito 2** del proyecto, reorientado estratégicamente hacia la **Región Metropolitana de Santiago (RM)** según la retroalimentación del profesor.

---

## 📁 Estructura Modular de `Avance Hito 2/`

```text
Avance Hito 2/
├── P1/                                         # Entregables de Persona 1: Ingeniero de Datos
│   ├── 00_DOCUMENTOS_PARA_PRESENTAR_Y_DEFENDER/
│   │   ├── Informe_Hito2_Persona1_DataMart.pdf     # Informe técnico formal de Persona 1
│   │   ├── Informe_Hito2_Persona1_DataMart.tex     # Código fuente LaTeX del informe
│   │   └── RESUMEN_FEEDBACK_Y_REORIENTACION_HITO2.md # Síntesis ejecutiva de la reorientación a RM
│   ├── 03_DATAMART_SCRIPTS_DDL_Y_CARGA/           # DataMart físico y scripts de carga
│   │   ├── schema_datamart.sql                     # Script DDL formal (CREATE TABLE, PK, FK, Índices)
│   │   ├── 01_build_and_load_datamart.py           # Pipeline de carga masiva automatizada en Python
│   │   ├── datamart_indices_2012_2026.db           # Base de datos relacional SQLite (DataMart físico)
│   │   └── vistas_analiticas_rm.sql                # Vistas optimizadas para la Región Metropolitana
│   ├── 04_CERTIFICACION_CUADRE_Y_AUDITORIA/       # Certificación de cuadre contra la fuente (4 Pts Pauta)
│   │   ├── 02_verify_cuadre_datamart.py            # Script automatizado de auditoría matemática
│   │   ├── reporte_cuadre_datamart.md              # Tabla de Control Totals y certificación formal
│   │   └── reporte_cuadre_datamart.json            # Reporte estructurado para evaluación automatizada
│   └── 05_CONEXION_POWERBI_Y_PRUEBAS/             # Conexión directa DataMart -> Power BI (Persona 4)
│       └── guia_conexion_powerbi_datamart.md       # Guía paso a paso para cumplir "Conectado al DataMart, no a Excel"
│
├── P2_PROPUESTA_VALOR_Y_CANVAS_BI_RM/          # Entregables de Persona 2: Analista de Negocio
│   └── 01_PROPUESTA_VALOR_Y_CANVAS_BI_RM/
│       ├── data_rm/                                # Conjuntos de datos filtrados para la RM e integración externa
│       │   ├── rm_ext_ine_poblacion.csv            # Proyecciones demográficas INE (2002–2035) RM
│       │   ├── rm_ext_sies_acreditacion.csv        # Acreditación institucional SIES RM
│       │   ├── rm_kpi_p1_sobredemanda.csv          # KPIs Pregunta 1
│       │   ├── rm_kpi_p2_puntajes_paes.csv         # KPIs Pregunta 2
│       │   └── rm_kpi_p3_absorcion_demografica.csv # KPIs Pregunta 3
│       ├── docs/                                   # Documentación formal y Canvas BI RM
│       │   ├── diccionario_fuentes_rm_hito2.md     # Diccionario de fuentes externas
│       │   └── informe_hito2_persona2.tex          # Informe técnico Canvas BI y Preguntas de Negocio
│       └── scripts/                                # Scripts de extracción y validación de llaves RM
│           ├── 08_extract_rm_data.py               # Extracción y filtrado
│           └── 09_validate_rm_keys.py              # Validación de integridad de llaves
│
└── P3_MODELO_DIMENSIONAL_Y_ARQUITECTURA/       # Entregables de Persona 3: Arquitecto de Datos (Angel Pino)
    ├── README.md                                  # Guía del módulo de arquitectura
    ├── schema_dimensional_star.sql                # Script DDL canónico formal del Esquema Estrella
    ├── diagramas/                                 # Diagramas del modelo dimensional
    │   ├── diagrama_modelo_dimensional_estrella.svg # Diagrama vectorial SVG
    │   ├── diagrama_modelo_dimensional_estrella.png # Render PNG alta resolución (300 DPI)
    │   └── diagrama_modelo_dimensional_estrella.mmd # Código fuente Mermaid
    ├── scripts/                                   # Scripts reproducibles de arquitectura
    │   ├── generate_star_diagram.py               # Generador programático de diagramas
    │   └── audit_architecture_and_integrity_p3.py # Auditoría de 0 huérfanos, grano y benchmarks (< 25 ms)
    └── docs/                                      # Documentación e informes técnicos
        ├── informe_hito2_persona3_arquitectura.tex  # Informe formal en LaTeX (estilo ejecutivo)
        ├── informe_hito2_persona3_arquitectura.md   # Informe técnico en Markdown con tablas y fórmulas
        ├── guia_defensa_oral_persona3.md            # Banco de 10 preguntas y respuestas para la defensa oral (15 pts)
        ├── reporte_arquitectura_p3.md               # Reporte técnico generado por el script de auditoría
        └── auditoria_arquitectura_p3.json           # Datos estructurados JSON de la auditoría
```

---

## 🚀 Cómo Reproducir y Auditar el DataMart Completo

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

---

## 📊 Resumen de Resultados Técnicos Certificados (Hito 2)

1. **Cuadre Perfecto contra la Fuente (0 Pérdidas, 0 Duplicados):**
   * Registros en fuente original consolidada: **158.211 filas**.
   * Registros en `fact_matricula_admision`: **158.211 filas**.
   * Diferencia neta: **0 registros**.
   * Integridad referencial: **100,0%** (**0 registros huérfanos** en todas las claves foráneas).

2. **Universo de la Región Metropolitana:**
   * La RM concentra **58.926 ofertas / 82.348 registros totales** de pregrado (más del 52% de la base nacional).
   * Vistas especializadas (`vw_rm_sobredemanda_y_capacidad`, `vw_rm_evolucion_selectividad_paes`, `vw_rm_absorcion_demografica_ine`) para alimentar Power BI Desktop.

3. **Arquitectura Dimensional Formal (Kimball):**
   * **Tabla de Hechos Central:** `fact_matricula_admision` (Grano atómico: oferta de programa, sede, horario y año).
   * **Dimensiones:** `dim_tiempo`, `dim_sede_geografia`, `dim_institucion` (con historial SCD Tipo 2 anual), `dim_carrera_programa` y `dim_poblacion_rm` (INE).
   * **Aditividad:** Matrícula y vacantes completamente aditivas; puntajes PAES estrictamente no aditivos (promedios ponderados por matrícula en DAX).
