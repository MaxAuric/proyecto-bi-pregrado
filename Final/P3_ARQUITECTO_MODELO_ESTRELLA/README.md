# Entrega Final — Persona 3: Arquitecto Dimensional y Diccionario de Tasas/KPIs
## Proyecto Final de Business Intelligence: Región Metropolitana de Santiago (2012–2026)
**Integrante Evaluado:** **Angel Pino (Persona 3)**  
**Carrera:** Ingeniería en Negocios  
**Fecha de Entrega y Defensa:** 18 de Noviembre de 2026  
**Alcance Oficial:** **100% Región Metropolitana de Santiago (`region_codigo_subdere == '13'`)**  
**Ponderación Oficial Asociada:** Dashboard Power BI (8 pts grupales) + Informe Ejecutivo Final (5 pts grupales) + Dominio Grupal (10 pts) + Defensa Técnica Individual (15 pts individuales) + Exposición Oral 15 min (5 pts individuales).

---

## Estructura del Módulo P3_ARQUITECTO_MODELO_ESTRELLA/

```text
Final/P3_ARQUITECTO_MODELO_ESTRELLA/
├── README.md                                         # Documento ejecutivo del módulo de Persona 3
│
├── diagramas/                                        # Diagramas formales del Esquema Estrella Enriquecido
│   ├── diagrama_modelo_dimensional_estrella_rm.svg   # Vectorial escalable HD con tasas, PK, FK y fuentes externas
│   ├── diagrama_modelo_dimensional_estrella_rm.png   # Render de alta definición (300 DPI) para informe y slides
│   └── diagrama_modelo_dimensional_estrella_rm.mmd   # Código fuente Mermaid para previsualización directa en Markdown
│
├── docs/                                             # Informes formales, catálogo técnico y guías de defensa
│   ├── informe_final_persona3_arquitectura.md        # Sección técnica completa de Persona 3 para el Informe Final (Markdown)
│   ├── informe_final_persona3_arquitectura.tex       # Código fuente LaTeX con diseño ejecutivo para consolidación de P5
│   ├── diccionario_tecnico_tasas_kpis_rm.md          # Catálogo maestro de tablas, columnas, fórmulas, aditividad y DAX
│   └── guion_defensa_oral_y_slides_p3.md             # Guion de exposición (Slides 6-7) y banco de 10 preguntas para la defensa oral (15 pts)
│
├── scripts/                                          # Scripts reproducibles de automatización y certificación
│   ├── generate_star_diagram_rm.py                   # Generador programático de diagramas SVG, PNG y Mermaid
│   └── audit_architecture_and_integrity_p3.py        # Auditoría formal de 0 huérfanos, unicidad de PKs y reglas DW
│
└── sql/                                              # Script DDL relacional canónico
    └── schema_dimensional_estrella_rm_canonica.sql   # DDL ANSI SQL formal con PKs, FKs, restricciones CHECK, índices y vista OLAP
```

---

## Cómo Reproducir y Auditar el Trabajo de Persona 3

Todo el trabajo desarrollado por Persona 3 es **100% auditable y reproducible mediante Python y SQL**:

### 1. Ejecutar la Auditoría Técnica de Arquitectura e Integridad:
```bash
python "Final/P3_ARQUITECTO_MODELO_ESTRELLA/scripts/audit_architecture_and_integrity_p3.py"
```
* **Qué certifica:**
  - Existencia y correspondencia exacta de filas entre SQLite (`datamart_estrella_rm_final.db`) y Excel (`DataMart_Estrella_RM_PowerBI.xlsx`).
  - Verificación matemática de **0 registros huérfanos** (100% integridad referencial en claves foráneas).
  - Unicidad absoluta de claves primarias (PK) y claves subrogadas (SK).
  - Cumplimiento de **Clase 4 DW (Pág. 62)**: Cero columnas `VARCHAR` en la tabla de hechos y Cero abreviaturas en dimensiones.
  - Cuadre oficial de las **69 instituciones activas en Santiago en 2026** y sus 1.298 fotografías históricas SCD Tipo 2.
  - Benchmarks de latencia analítica para Power BI (**< 25 ms**).

### 2. Regenerar los Diagramas del Esquema Estrella (SVG, PNG, Mermaid):
```bash
python "Final/P3_ARQUITECTO_MODELO_ESTRELLA/scripts/generate_star_diagram_rm.py"
```

---

## Matriz de Cumplimiento del Feedback Docente (Hito 2 -> Entrega Final)

| Observación / Feedback Docente (Hito 2) | Corrección Arquitectónica Implementada por Persona 3 | Archivo de Respaldo | Estado |
| :--- | :--- | :--- | :---: |
| **"Acotarse a un problema claro y ámbito geográfico"** | Foco estricto 100% en la Región Metropolitana de Santiago (**58.926 ofertas académicas** y **69 IES activas en 2026**). | `schema_dimensional_estrella_rm_canonica.sql` | **APROBADO** |
| **"Mejorar y ver el uso de tasas / Los conteos brutos no bastan"** | Modelado formal de tasas relativas ($\text{Tasa} = \frac{A}{B} \times 100$) en dimensiones y hechos (ocupación, sobredemanda, retención, demografía juvenil INE y acreditación SIES). | `diccionario_tecnico_tasas_kpis_rm.md` | **APROBADO** |
| **"Dimensionar capacidad de laboratorios (caso 120 -> 140 alumnos en base 35)"** | Formalización de cuatro métricas de capacidad: secciones planificadas ($\lceil \text{vac}/35 \rceil$), secciones reales, secciones extra por sobrecupo y tasa de saturación. | `informe_final_persona3_arquitectura.md` | **APROBADO** |
| **"Transformación no terminada / Abreviaturas en dimensiones"** | Eliminación de todas las abreviaturas (`Univ.`, `I.P.`, `C.F.T.`, `F.F.A.A.`, `M/`) y prefijos regulatorios `(a)/(b)` cumpliendo Clase 4 DW Pág. 62. | `audit_architecture_and_integrity_p3.py` | **APROBADO** |
| **"Cero VARCHAR en la tabla de hechos"** | `fact_matricula_admision` es 100% numérica: solo claves foráneas enteras, flags numéricos y métricas cuantitativas (Clase 4 DW Pág. 62). | `audit_architecture_and_integrity_p3.py` | **APROBADO** |
| **"Integración de fuentes externas"** | Integración directa de Proyecciones Demográficas **INE RM** en `dim_tiempo_ine_rm` y Acreditación Institucional **SIES/CNA** en `dim_institucion_sies` con tabla puente. | `diagrama_modelo_dimensional_estrella_rm.svg` | **APROBADO** |
| **"Por qué las tasas se recalculan con DIVIDE() al agregar"** | Demostración matemática rigurosa de la no aditividad de tasas y puntajes, evidenciando la Paradoja de Simpson al promediar promedios simples. | `informe_final_persona3_arquitectura.md` | **APROBADO** |
| **"Verificar integridad 1:N entre dimensiones y hechos"** | **0 registros huérfanos** auditados en las 58.926 ofertas académicas de la Región Metropolitana. | `audit_architecture_and_integrity_p3.py` | **APROBADO** |

---

## Resumen de Cifras Clave Certificadas en el Esquema Estrella RM

- **Ofertas Académicas Auditadas en Santiago (2012–2026):** `58.926`
- **Instituciones de Educación Superior Activas en la RM (2026):** `69`
  - Universidades: `35`
  - Institutos Profesionales: `19`
  - Centros de Formación Técnica: `11`
  - Instituciones de las FF.AA. y de Orden: `4`
- **Fotografías Históricas SCD Tipo 2:** `1.298` registros anuales
- **Sedes Físicas en Santiago:** `22`
- **Programas Académicos Únicos:** `5.184`
- **Integridad Referencial de Claves Foráneas:** `100,000%` (0 huérfanos)
- **Columnas VARCHAR en Hechos:** `0` (100% numérica)
- **Ofertas con Sobredemanda Crítica (>100% vacantes):** `13.995`
- **Secciones Extra de Laboratorio (Base 35 puestos) Forzadas por Sobrecupo:** `7.529`
- **Tasa de Absorción Juvenil Promedio RM (INE):** `21,64%`
- **Latencia de Consultas Analíticas OLAP:** `< 25 ms`
