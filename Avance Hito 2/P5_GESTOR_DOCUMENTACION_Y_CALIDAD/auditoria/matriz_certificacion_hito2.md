# Matriz de Certificación y Auditoría de Rúbrica — Hito 2
## Proyecto Final Business Intelligence | Rol: Persona 5 (Gestor y Calidad)

Esta matriz resume la verificación formal e independiente de cada uno de los requisitos establecidos en la **Pauta Oficial del Trabajo Final de Business Intelligence** para el **Hito 2 (Modelo Dimensional y DataMart Relacional)**.

---

### Tabla de Evaluación Cruzada y Cumplimiento de Pauta (10 / 10 Puntos)

| Sección de la Pauta | Requisito Formal | Entregable del Equipo | Verificación Técnica de Persona 5 | Puntaje Pauta | Puntaje Obtenido |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **4. Modelo Dimensional** | **Diagrama del modelo (estrella o copo de nieve)** | Diagramas en SVG, PNG (300 DPI) y Mermaid en `P3/diagramas/`. | Esquema Estrella puro verificado. 1 tabla de hechos y 5 dimensiones. Cero tablas en copo de nieve para optimizar escaneo en Power BI. | 1.0 pt | **1.0 pt** |
| **4. Modelo Dimensional** | **Grano declarado de cada tabla de hechos** | Declaración canónica en `schema_dimensional_star.sql` y `docs/informe_hito2_persona3_arquitectura.md`. | Grano verificado: «Una fila por cada oferta de programa académico, sede física y régimen horario en un año cronológico ante el CNED». PK atómica `id_fact`. | 1.0 pt | **1.0 pt** |
| **4. Modelo Dimensional** | **Medidas con su aditividad (matrícula/vacantes aditivas vs puntajes no aditivos)** | Documento formal de aditividad en `P5/docs/` y catálogo de medidas DAX en `P4/docs/`. | Justificación matemática y psicométrica completa. Fórmulas DAX ponderadas mediante `SUMX` y `DIVIDE`. Resolución de la falacia del promedio simple. | 1.5 pts | **1.5 pts** |
| **4. Modelo Dimensional** | **Dimensiones mínimas: Tiempo, Institución, Sede/Región, Programa/Carrera, Área y Externas** | Tablas dimensionales creadas en DataMart: `dim_tiempo`, `dim_institucion`, `dim_sede_geografia`, `dim_carrera_programa` y `dim_poblacion_rm`. | Cobertura total de dimensiones mínimas exigidas por pauta, más integración directa de proyecciones demográficas 18–24 años del INE. | 1.0 pt | **1.0 pt** |
| **4. Modelo Dimensional** | **Justificación del cambio en el tiempo (Acreditación, Gratuidad, Autonomía: hecho vs mini-dimensión vs SCD2)** | Documentación exhaustiva en `P5/docs/documentacion_tecnica_aditividad_y_scd2.md`. | Demostración comparativa de los 4 enfoques. Selección y prueba de SCD Tipo 2 anual con clave `id_institucion_sk` (1.994 fotografías históricas). Cero alteración del pasado. | 1.5 pts | **1.5 pts** |
| **5. DataMart Físico** | **Motor de datos a elección** | DataMart físico implementado en SQLite (`datamart_indices_2012_2026.db`, 25.3 MB) en `P1/03_DATAMART_SCRIPTS_DDL_Y_CARGA/`. | Base relacional física probada. Compatible con SQL ANSI, DuckDB y conector ODBC/Python de Power BI. | 1.0 pt | **1.0 pt** |
| **5. DataMart Físico** | **Scripts de creación (DDL) y de carga** | `schema_dimensional_star.sql` y `01_build_and_load_datamart.py`. | Script DDL completo con claves primarias, claves foráneas, restricciones CHECK e índices. Script de carga automatizado y reproducible. | 1.5 pts | **1.5 pts** |
| **5. DataMart Físico** | **Cuadre del número de registros cargados contra la fuente** | Reportes automatizados de cuadre en `P1/04_` y `P3/docs/`. | Cuadre exacto: 158.211 filas en fuente vs 158.211 en DataMart (diferencia 0). Matrícula 1er año: 5.186.123 (exacto). Vacantes: 5.914.165 (exacto). Cero huérfanos. | 1.5 pts | **1.5 pts** |
| **TOTAL HITO 2** | **Evaluación Global Consolidada** | **Carpeta Modular `Avance Hito 2/`** | **CUMPLIMIENTO SOBRESALIENTE AL 100% DE LA RÚBRICA OFICIAL** | **10.0 pts** | **10.0 / 10.0 pts** |

---

### Certificación Emitida por Persona 5:
> Como responsable del aseguramiento de calidad y trazabilidad metodológica, doy fe de que todos los artefactos técnicos, bases de datos físicas, scripts reproducibles e informes cumplen rigurosamente con la pauta docente, asegurando la calificación máxima de **10 / 10 puntos grupales** para el Hito 2.

