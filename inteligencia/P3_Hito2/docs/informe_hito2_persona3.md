# Informe Técnico Hito 2 - Arquitectura Dimensional y DataMart
## Rol Evaluado: Persona 3 (Arquitecto de Bases de Datos)
**Asignatura:** Business Intelligence  
**Proyecto:** Demanda, Capacidad y Equidad Territorial de la Educación Superior Chilena (2012–2026)  
**Fecha de Entrega:** 4 de Noviembre de 2026

---

## 1. Resumen Ejecutivo
El presente informe documenta el diseño conceptual, lógico y físico del **DataMart Relacional Dimensional** construido para responder a las preguntas estratégicas planteadas en el Canvas BI.

El DataMart integra la base oficial consolidada limpia del CNED (158.211 registros, 2012–2026) procesada por la Persona 1, junto con las dos fuentes externas procesadas por la Persona 2: (i) Proyecciones Regionales de Población del INE (2002–2035) y (ii) Listados Oficiales de IES Vigentes y Acreditación del SIES/MINEDUC (2018–2026).

El DataMart fue implementado en SQLite (motor relacional ligero y estándar ANSI SQL) y cuenta con una exportación relacional directa en CSV (`data/tablas_csv_powerbi/`) para habilitar la conexión transparente e inmediata de la **Persona 4 (Desarrollador BI)** en Power BI Desktop.

---

## 2. Declaración Formal del Grano (Kimball 4-Step Process)

En concordancia con las mejores prácticas de Ralph Kimball, la arquitectura implementa una **Constelación de Hechos (Fact Constellation)** con dimensiones conformadas:

### 2.1. Grano de la Tabla de Hechos Principal (`fact_matricula_oferta`)
- **Declaración del Grano:** *Un registro individual por cada combinación única de Programa Académico, Sede Geográfica, Régimen Horario y Año Calendario.*
- **Unidad de Análisis Atómica:** Corresponde exactamente a una oferta académica específica impartida por una institución en un campus y año determinado.
- **Cardinalidad Resultante:** **158.211 registros** (cuadre al 100% con la base fuente).

### 2.2. Grano de la Tabla de Hechos Secundaria (`fact_poblacion_regional` - INE)
- **Declaración del Grano:** *Un registro por Región Geográfica (Código SUBDERE 01 a 16) y Año Calendario (2012 a 2026).*
- **Cardinalidad Resultante:** **240 registros** ($16 \text{ regiones} \times 15 \text{ años}$).
- **Propósito:** Soportar de forma nativa la **Pregunta de Negocio 1 (Equidad Territorial)** calculando la tasa de matrícula de 1er año por cada 1.000 habitantes en edad de estudiar/trabajar (15–64 años), compartiendo las dimensiones conformadas `dim_tiempo` y `dim_geografia`.

---

## 3. Matriz de Clasificación y Aditividad de Medidas

La pauta exige explicitar la aditividad de las medidas para prevenir errores de agregación en los tableros de BI:

| Tabla | Medida / Atributo | Tipo de Medida | Comportamiento de Agregación | Justificación Técnica |
| :--- | :--- | :--- | :--- | :--- |
| `fact_matricula_oferta` | `matricula_primer_ano_total` | **Totalmente Aditiva** | `SUM` a través de todas las dimensiones | Representa personas físicas que ingresan por primera vez. Es sumable en tiempo, espacio e institución. |
| `fact_matricula_oferta` | `matricula_total` | **Totalmente Aditiva** | `SUM` a través de todas las dimensiones | Stock total de alumnos matriculados en ese año y programa. |
| `fact_matricula_oferta` | `vacantes` | **Totalmente Aditiva** | `SUM` (cuando `flag_vacantes_declaradas=1`) | Cupos de admisión ofrecidos. Los nulos (25,4%) se preservan para no simular cierre de carreras. |
| `fact_matricula_oferta` | `puntaje_promedio_original` | **No Aditiva (Intensiva)** | `AVERAGE` (requiere ponderación por matrícula) | Los puntajes son promedios psicométricos; su suma carece de sentido matemático. |
| `fact_matricula_oferta` | `puntaje_promedio_equiv_paes`| **No Aditiva (Intensiva)** | `AVERAGE` (requiere ponderación por matrícula) | Proyección unificada escala [100-1000]. Debe promediarse ponderado por matrícula. |
| `fact_matricula_oferta` | `tasa_ocupacion_primer_ano` | **Derivada / No Aditiva** | Medida calculada: $\frac{\sum \text{Matrícula 1er año}}{\sum \text{Vacantes}} \times 100$ | Ratio que nunca debe sumarse ni promediarse directamente. Se calcula a nivel agregado en DAX/SQL. |
| `fact_poblacion_regional` | `poblacion_total` / `poblacion_15_64` | **Semi-Aditiva** | `SUM` entre regiones; **NO sumable** a través del tiempo | La población es una medición de stock censal al 30 de junio. Sumar años diferentes duplicaría artificialmente a los habitantes. |

---

## 4. Justificación del Modelado del Cambio en el Tiempo (SCD)

La pauta establece:
> *"Acreditación, Gratuidad y Autonomía cambian de un año a otro en la misma institución. El equipo decide y justifica si las modela como atributo del hecho, como mini-dimensión o como dimensión de cambio lento tipo 2."*

### 4.1. Análisis Comparativo de Opciones
1. **Opción A - Atributo en la Tabla de Hechos:**
   - *Ventajas:* Simple de consultar.
   - *Desventajas:* Desnormaliza la tabla de hechos inflando el tamaño de fila (158.211 registros) y mezcla atributos descriptivos categóricos de la entidad institucional dentro de una tabla diseñada puramente para transacciones numéricas.
2. **Opción B - Dimensión de Cambio Lento Tipo 2 Estándar (SCD Tipo 2 con fechas de vigencia):**
   - *Ventajas:* Mantiene trazabilidad histórica completa mediante `fecha_inicio`, `fecha_fin` y `flag_actual`.
   - *Desventajas:* Requiere búsquedas complejas con operadores de rango temporal (`BETWEEN fecha_inicio AND fecha_fin`) que degradan fuertemente el rendimiento analítico en Power BI y dificultan las relaciones $1 \text{ a } N$.
3. **Opción C (Adoptada) - Dimensión de Estado / Snapshot Anual Institucional (`dim_institucion_calidad_anual`):**
   - *Fundamento:* Como la acreditación, autonomía y gratuidad operan en ciclos anuales discretos (los listados SIES se publican una vez al año y los presupuestos de gratuidad rigen por año fiscal), modelar una tabla de **Snapshot Anual de Institución** ($1.994$ filas: $259 \text{ instituciones} \times \text{años activos}$) ofrece lo mejor de ambos mundos:
     - Preserva la condición histórica exacta que tenía cada institución en cada año (SCD Tipo 2 discreto por año).
     - Permite a Power BI conectar la tabla mediante una relación $1 \text{ a } N$ limpia o vincularla directamente por `(id_institucion, id_tiempo)` sin joins no equi-relacionales.
     - Resuelve directamente la **Pregunta de Negocio 3 (Calidad y Competencia)**, permitiendo graficar la evolución de la matrícula en instituciones acreditadas frente a los años de acreditación.

---

## 5. Tratamiento de Miembros Desconocidos y Gobernanza

Para asegurar que **ningún registro de la tabla de hechos se pierda** por falta de cruce o dato no informado (principio de Integridad Referencial de Kimball):
- Todas las dimensiones incorporan un registro especial con clave sustituta `-1`:
  - `dim_geografia`: `id_geografia = -1` ('Sin Dato / Desconocido').
  - `dim_sede`: `id_sede = -1` ('Sin Dato / Desconocida').
  - `dim_institucion`: `id_institucion = -1` ('No Informado / Desconocido').
  - `dim_programa`: `id_programa = -1` ('Programa No Informado').
- Las **19 instituciones de la base CNED que no tienen código SIES** (identificadas por la Persona 2) se cargan en `dim_institucion` con `codigo_ies = NULL` y `metodo_cruce_sies = 'sin_coincidencia'`. En la tabla de calidad anual quedan asignadas a la categoría `'Sin Información'`, lo que permite a la Persona 4 visualizarlas o filtrarlas sin provocar errores en las sumas totales.

---

## 6. Resultados de Auditoría y Certificación de Cuadre

El script automatizado `verify_cuadre.py` certifica los siguientes resultados oficiales:

```text
==================================================================
=== AUDITORIA Y CUADRE EXACTO DEL DATAMART (PERSONA 3) ===
==================================================================

[1] CUADRE DE REGISTROS:
  Fuente CSV:      158,211 filas
  DataMart DB:     158,211 filas
  Diferencia:      0 -> OK EXACTO (100% Coincidencia)

[2] CUADRE DE MATRICULA 1ER ANO:
  Fuente CSV:      5,186,123
  DataMart DB:     5,186,123
  Diferencia:      0 -> OK EXACTO (Zero Data Loss)

[3] CUADRE DE MATRICULA TOTAL:
  Fuente CSV:      17,696,782
  DataMart DB:     17,696,782
  Diferencia:      0 -> OK EXACTO (Zero Data Loss)

[4] CUADRE DE VACANTES DECLARADAS:
  Fuente CSV:      5,914,165
  DataMart DB:     5,914,165
  Diferencia:      0 -> OK EXACTO (Zero Data Loss)

[5] INTEGRIDAD REFERENCIAL:
  Total Huérfanos: 0 -> OK (Integridad Referencial Absoluta)
==================================================================
```

---

## 7. Entregables Físicos Generados en el Repositorio

| Archivo | Ubicación | Descripción |
| :--- | :--- | :--- |
| `01_ddl_datamart.sql` | `P3_Hito2/sql/` | Script DDL de creación de tablas, llaves primarias, foráneas e índices. |
| `02_views_powerbi.sql` | `P3_Hito2/sql/` | Vistas analíticas semánticas para responder P1, P2 y P3. |
| `03_audit_and_reconciliation.sql` | `P3_Hito2/sql/` | Consultas SQL de auditoría y verificación. |
| `load_datamart.py` | `P3_Hito2/scripts/` | Pipeline Python de carga masiva automatizada y generación de surrogate keys. |
| `verify_cuadre.py` | `P3_Hito2/scripts/` | Script de conciliación matemática fuente vs DataMart. |
| `datamart_educacion_superior.db` | `P3_Hito2/data/` | Base de datos SQLite compilada con los 158.211 registros cargados. |
| `tablas_csv_powerbi/` | `P3_Hito2/data/` | Tablas exportadas individualmente en CSV para importación directa en Power BI. |
| `modelo_dimensional.md` | `P3_Hito2/diagrams/` | Diagrama Entidad-Relación en formato Mermaid y definición de jerarquías. |
| `guia_conexion_powerbi_persona4.md` | `P3_Hito2/docs/` | Manual de integración para la Persona 4. |
