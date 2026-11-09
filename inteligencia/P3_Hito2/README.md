# 🏛️ Entregables Hito 2 — Persona 3: Arquitecto de Datos y Modelador Dimensional
## Proyecto Final de Business Intelligence (2012–2026) — Región Metropolitana
**Integrante Evaluado:** **Angel Pino (Persona 3)**  
**Ponderación Pauta Hito 2:** 10 Puntos Grupales (Modelo Dimensional 6 pts + DataMart y Cuadre 4 pts)  
**Preparación Individual:** 15 Puntos Individuales de Defensa Oral  

---

## 📁 Estructura del Módulo `P3_MODELO_DIMENSIONAL_Y_ARQUITECTURA/`

```text
P3_MODELO_DIMENSIONAL_Y_ARQUITECTURA/
├── README.md                                  # Este documento explicativo del módulo
├── schema_dimensional_star.sql                # Script DDL canónico formal (CREATE TABLE, PK, FK, Índices, Vistas)
│
├── diagramas/                                 # Diagramas formales del Modelo Dimensional (Esquema Estrella)
│   ├── diagrama_modelo_dimensional_estrella.svg # Diagrama vectorial escalable de alta definición
│   ├── diagrama_modelo_dimensional_estrella.png # Render de alta resolución (300 DPI) para informes y diapositivas
│   └── diagrama_modelo_dimensional_estrella.mmd # Código fuente Mermaid para visualización en Markdown
│
├── scripts/                                   # Scripts reproducibles de automatización y auditoría
│   ├── generate_star_diagram.py               # Generador programático de diagramas SVG, PNG y Mermaid
│   └── audit_architecture_and_integrity_p3.py # Auditoría formal de 0 huérfanos, grano y benchmarks de performance
│
└── docs/                                      # Informes técnicos formales y guías de defensa
    ├── informe_hito2_persona3_arquitectura.pdf  # Informe técnico en PDF (compilable en LaTeX)
    ├── informe_hito2_persona3_arquitectura.tex  # Código fuente LaTeX del informe con estilo ejecutivo
    ├── informe_hito2_persona3_arquitectura.md   # Informe técnico en Markdown con tablas y fórmulas
    ├── guia_defensa_oral_persona3.md            # Banco de 10 preguntas y respuestas para la defensa individual (15 pts)
    ├── reporte_arquitectura_p3.md               # Reporte técnico generado automáticamente por el script de auditoría
    └── auditoria_arquitectura_p3.json           # Datos estructurados JSON de la auditoría de integridad
```

---

## 🚀 Cómo Reproducir y Auditar el Trabajo de Persona 3

Todo el trabajo es 100% reproducible y auditable mediante scripts en Python y SQL ANSI:

### 1. Ejecutar la Auditoría Técnica de Arquitectura e Integridad:
```bash
python "Avance Hito 2/P3_MODELO_DIMENSIONAL_Y_ARQUITECTURA/scripts/audit_architecture_and_integrity_p3.py"
```
* **Qué valida:**
  - Existencia y estructura de las 5 tablas dimensionales y la tabla de hechos.
  - Verificación matemática de **0 registros huérfanos** (100% integridad referencial).
  - Unicidad absoluta de claves primarias.
  - Clasificación de medidas aditivas y control de rango PAES (100 a 1000).
  - Medición de tiempos de respuesta de consultas analíticas para Power BI (< 25 ms).

### 2. Regenerar los Diagramas Vectoriales y de Alta Resolución:
```bash
python "Avance Hito 2/P3_MODELO_DIMENSIONAL_Y_ARQUITECTURA/scripts/generate_star_diagram.py"
```

---

## 📊 Resumen de Resultados Técnicos Certificados (Persona 3)

| Componente | Resultado Técnico | Cumplimiento Pauta |
| :--- | :--- | :---: |
| **Topología Relacional** | **Esquema Estrella Puro** (1 Fact + 4 Dimensiones canónicas + 1 Externa INE) | **6.0 / 6.0 pts** |
| **Grano Declarado** | Oferta institucional por programa, sede física, jornada y año cronológico | **Aprobado** |
| **Gobernanza Temporal** | **SCD Tipo 2** en `dim_institucion` (1.994 fotografías históricas con `id_institucion_sk`) | **Aprobado** |
| **Integridad Referencial** | **0 huérfanos** en 158.211 filas en todas las relaciones de claves foráneas | **4.0 / 4.0 pts** |
| **Latencia Power BI** | Consultas analíticas multidimensionales resueltas en **menos de 25 ms** | **Aprobado** |
