# Módulo de Persona 5: Gestor de Proyecto, Documentador y Calidad — Hito 2
## Proyecto Final de Business Intelligence (2012–2026) — Región Metropolitana

Este directorio contiene la solución formal, trazabilidad metodológica, gobernanza dimensional y certificación de rúbrica correspondientes al rol de **Persona 5 (Gestor de Proyecto, Documentador y Calidad)** para el **Hito 2 (Modelo Dimensional y DataMart Relacional)**.

---

## 📌 Responsabilidades Asignadas a Persona 5 (Hito 2)

De acuerdo con el documento oficial de planificación (*Planificación Estratégica y División de Trabajo*, Sección 2.2):

> **Persona 5 (Gestor / Calidad / Documentador):**
> 1. *Documentar técnicamente la aditividad de las medidas: justificar por qué matrícula y vacantes son aditivas, mientras que los puntajes son promedios no aditivos que requieren agregaciones ponderadas en DAX.*
> 2. *Documentar la estrategia de cambio en el tiempo (SCD Tipo 2): justificar cómo se modelan atributos mutables como la Acreditación Institucional y la adscripción a Gratuidad.*
> 3. *Compilar el Informe Técnico del Hito 2 en formato LaTeX y Markdown, adjuntando el diagrama relacional y evidencias de cuadre.*
> 4. *Aseguramiento de la rúbrica oficial (10 / 10 puntos).*
> 5. *Guía de estudio y preparación de la defensa oral del Hito 2.*

---

## 📁 Estructura del Módulo `P5_GESTOR_DOCUMENTACION_Y_CALIDAD/`

```text
P5_GESTOR_DOCUMENTACION_Y_CALIDAD/
├── README.md                                          # Este documento de presentación del módulo
│
├── docs/                                              # Informes técnicos, justificaciones y guías
│   ├── informe_hito2_persona5_calidad_gobernanza.pdf  # Informe técnico ejecutivo compilado en PDF
│   ├── informe_hito2_persona5_calidad_gobernanza.tex  # Código fuente LaTeX corporativo del informe
│   ├── informe_hito2_persona5_calidad_gobernanza.md   # Informe técnico en Markdown con tablas completas
│   ├── informe_hito2_persona5_calidad_gobernanza.html # Versión HTML para visualización web
│   ├── documentacion_tecnica_aditividad_y_scd2.md     # Tratamiento dimensional profundo de Kimball y SCD2
│   ├── Guia_Estudio_Defensa_Hito2_BI.pdf              # Guía maestra de estudio para presentar y defender
│   ├── Guia_Estudio_Defensa_Hito2_BI.md               # Versión Markdown de la guía de estudio
│   └── Guia_Estudio_Defensa_Hito2_BI.html             # Versión interactiva para proyección en clases
│
├── auditoria/                                         # Matrices de evaluación y certificación oficial
│   ├── matriz_certificacion_hito2.md                  # Matriz de verificación ítem por ítem de la pauta
│   └── auditoria_cumplimiento_rubrica_hito2.json      # Reporte estructurado de calidad y 0 huérfanos
│
└── scripts/                                           # Pipeline automatizado de calidad y compilación
    └── 12_audit_and_generate_p5_hito2.js              # Script en Node.js para compilar PDFs y auditar
```

---

## 🚀 Cómo Reproducir y Auditar el Trabajo de Persona 5

Para regenerar todos los artefactos, compilar los informes y guías a PDF y certificar la integridad de todo el Hito 2:

```bash
node "Avance Hito 2/P5_GESTOR_DOCUMENTACION_Y_CALIDAD/scripts/12_audit_and_generate_p5_hito2.js"
```

---

## 📊 Resumen de Resultados Técnicos Certificados (Persona 5)

| Requisito Pauta | Verificación Técnica | Estado | Puntaje |
| :--- | :--- | :---: | :---: |
| **Esquema Estrella** | 1 Fact central + 4 Dimensiones canónicas + 1 Dimensión Externa INE. | Aprobado | 1.0 pt |
| **Grano Declarado** | Oferta institucional por programa, sede, jornada y año ante el CNED. | Aprobado | 1.0 pt |
| **Aditividad de Medidas** | Matrícula y vacantes (SUM) vs Puntajes PAES/PSU (SUMX ponderado en DAX). | Aprobado | 1.5 pts |
| **Dimensiones Mínimas** | Tiempo, Institución, Sede/Región, Programa/Carrera, Área y Demografía INE. | Aprobado | 1.0 pt |
| **Cambio en el Tiempo (SCD2)** | SCD Tipo 2 anual con `id_institucion_sk` (1.994 fotografías históricas). | Aprobado | 1.5 pts |
| **DataMart Físico Implementado** | Base de datos relacional SQLite (`datamart_indices_2012_2026.db`, 25.3 MB). | Aprobado | 1.0 pt |
| **Scripts DDL y Carga** | Script SQL ANSI con PK, FK, CHECK e índices + Pipeline Python automatizado. | Aprobado | 1.5 pts |
| **Certificación de Cuadre** | 158.211 filas exactas (diferencia 0), 0 huérfanos y control totals idénticos. | Aprobado | 1.5 pts |
| **PUNTAJE TOTAL HITO 2** | **CUMPLIMIENTO AL 100% DE LA RÚBRICA OFICIAL** | **CERTIFICADO** | **10.0 / 10.0 pts** |

