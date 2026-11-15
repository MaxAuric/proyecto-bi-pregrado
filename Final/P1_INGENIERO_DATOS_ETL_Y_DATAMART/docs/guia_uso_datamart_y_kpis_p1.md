# Guía Técnica Persona 1: DataMart Estrella RM (2012–2026), Transformaciones Finalizadas y Nuevas Tasas/KPIs

**Rol:** Persona 1 — Ingeniero de Datos (ETL, Integración de Fuentes Externas, Cálculo de Tasas/KPIs y Carga del DataMart)  
**Alcance Geográfico:** **Exclusivamente Región Metropolitana de Santiago (`region_codigo_subdere == '13'`)**  
**Volumen Auditado RM:** `58.926` registros históricos de oferta académica (2012–2026) | `69` IES activas en 2026 (`35` Universidades, `19` Institutos Profesionales, `11` Centros de Formación Técnica, `4` FF.AA. y Orden).

---

## 1. Respuesta Técnica al Feedback del Hito 2

Durante la revisión del Hito 2, el profesor planteó tres observaciones estructurales que quedaron **100% resueltas en esta versión final**:

### A. "Transformación no terminada / No podría hacerlo del CSV directo porque había datos desordenados y con script se ordenaron"
- **Problema detectado en Hito 2:** En la versión anterior, `dim_institucion` mantenía abreviaturas crudas del archivo original (`'Univ.'`, `'I.P.'`, `'C.F.T.'`, `'F.F.A.A.'`), contraviniendo la regla de `Clase 4 - DW (pág. 62)` (*"Evite códigos o descripciones abreviadas en las tablas de dimensión"*). Además, las 2 fuentes externas (`rm_ext_ine_poblacion.csv` y `rm_ext_sies_acreditacion.csv`) habían quedado sueltas fuera del modelo estrella.
- **Solución implementada en Python (`01_build_final_datamart_rm.py`):**
  1. Se expandieron todas las descripciones institucionales y académicas en Python antes de poblar las dimensiones:
     - `'Univ.'` $\rightarrow$ **`'Universidad'`**
     - `'I.P.'` $\rightarrow$ **`'Instituto Profesional'`**
     - `'C.F.T.'` $\rightarrow$ **`'Centro de Formación Técnica'`**
     - `'F.F.A.A.'` $\rightarrow$ **`'Institución de las FF.AA. y Orden'`**
  2. Se integró la demografía **INE RM** dentro de `dim_tiempo_ine_rm` y la acreditación **SIES/CNA** dentro de `dim_institucion_sies`.
  3. Se filtró físicamente el DataMart principal para que contenga **únicamente la Región Metropolitana de Santiago (`58.926` filas)**, eliminando el ruido de otras regiones y dejando el caso nacional (`158.211` filas) únicamente como referencia de auditoría.

### B. "Importación de una tabla en Excel a Power BI es menos tiempo / Y de Python se exporta"
- **Problema detectado en Hito 2:** Ejecutar un script de Python dentro del conector de Power Query en Power BI tardaba demasiado y dependía del entorno local de Python en el PC donde se abriera el `.pbix`.
- **Solución implementada:** El script `01_build_final_datamart_rm.py` ejecuta todo el procesamiento pesado en Python y **exporta directamente**:
  1. **`Final/00_DATAMART_LISTO_PARA_POWERBI/DataMart_Estrella_RM_PowerBI.xlsx`**: Un libro Excel multi-hoja donde cada pestaña es una tabla del Esquema Estrella (`dim_tiempo_ine_rm`, `dim_institucion_sies`, `dim_ubicacion_rm`, `dim_programa_academico`, `dim_modalidad_jornada`, `fact_matricula_rm` + 3 vistas ejecutivas). Power BI lo importa nativamente en menos de 3 segundos.
  2. **`Final/00_DATAMART_LISTO_PARA_POWERBI/tablas_estrella_csv/*.csv`**: Las mismas tablas del esquema estrella en CSV limpio (`UTF-8-SIG`).
  3. **`Final/00_DATAMART_LISTO_PARA_POWERBI/datamart_estrella_rm_final.db`**: El motor relacional SQLite con claves primarias, claves foráneas e índices optimizados.

### C. "Mejorar y ver el uso de tasas / Los KPI se calculan de alguna forma / Y las medidas tributan a sus propuestas de valor / Está tratando de aportar un valor para tomar una decisión"
- **Problema detectado en Hito 2:** Las dimensiones solo tenían nombres descriptivos y la tabla de hechos solo tenía conteos brutos (`matricula_primer_anio`, `vacantes`). Un conteo bruto no permite decidir si abrir o cerrar una sección o laboratorio.
- **Solución implementada:** Se enriquecieron **todas las tablas `dim_*` y `fact_matricula_rm`** con tasas porcentuales, brechas operativas y tramos de decisión que responden directamente a la propuesta de valor en Santiago (incluyendo el caso real de capacidad de laboratorios de **35 alumnos por sección** para evaluar saltos como pasar de **120 a 140 matriculados**).

---

## 2. Catálogo de Tasas y KPIs Incorporados en el Esquema Estrella RM

### 2.1. Tasas y KPIs en Tablas de Dimensión (`dim_*`)

| Tabla Dimensión | Columna (Tasa / KPI) | Fórmula / Lógica de Cálculo | Cómo Tributa a la Toma de Decisiones en Santiago (RM) |
| :--- | :--- | :--- | :--- |
| **`dim_tiempo_ine_rm`** | `tasa_absorcion_1er_anio_sobre_jovenes_rm_pct` | $\frac{\text{Matrícula 1er Año RM}_t}{\text{Población 18–24 RM (INE)}_t} \times 100$ | Mide qué porcentaje de la cohorte juvenil de Santiago ingresa cada año a primer año de educación superior (`22,63%` en 2026). |
| **`dim_tiempo_ine_rm`** | `tasa_cobertura_bruta_rm_pct` | $\frac{\text{Matrícula Total RM}_t}{\text{Población 18–24 RM (INE)}_t} \times 100$ | Evalúa la saturación demográfica estructural en la RM (`80,45%` en 2026): demuestra que el crecimiento en Santiago ya no depende de bonos demográficos sino de quitar cuota de mercado o mejorar retención. |
| **`dim_tiempo_ine_rm`** | `tasa_ocupacion_vacantes_rm_anual_pct` | $\frac{\sum \text{Matrícula 1er Año RM}_t}{\sum \text{Vacantes RM}_t} \times 100$ | Termómetro macro de eficiencia de llenado de cupos en la Región Metropolitana año a año. |
| **`dim_tiempo_ine_rm`** | `variacion_interanual_mat_1er_anio_pct` | $\frac{\text{Mat. 1er Año}_t - \text{Mat. 1er Año}_{t-1}}{\text{Mat. 1er Año}_{t-1}} \times 100$ | Permite detectar contracciones o expansiones anuales de ingreso nuevo en Santiago (ej. impacto post-pandemia o PAES). |
| **`dim_institucion_sies`** | `anios_acreditacion_sies` y `tramo_acreditacion_sies` | Cruce con `rm_ext_sies_acreditacion.csv` (0 a 7 años) | Clasifica a las IES de Santiago en **Excelencia (6–7 años)**, **Avanzada (4–5 años)**, **Básica (1–3 años)** o **Sin Acreditación (0 años)**. |
| **`dim_institucion_sies`** | `score_calidad_sies_pct` | $\frac{\text{Años Acreditación SIES}}{7} \times 100$ | Estandariza la calidad institucional en escala `0%–100%` para cruzar calidad vs. selectividad y ocupación de vacantes. |
| **`dim_institucion_sies`** | `cuota_mercado_rm_2026_pct` | $\frac{\text{Matrícula Total Inst. RM}_{2026}}{\text{Matrícula Total RM}_{2026}} \times 100$ | Identifica el peso real de mercado de cada una de las 69 IES activas en Santiago. |
| **`dim_institucion_sies`** | `tasa_ocupacion_inst_rm_2026_pct` | $\frac{\sum \text{Mat. 1er Año Inst.}_{2026}}{\sum \text{Vacantes Inst.}_{2026}} \times 100$ | Diagnostica si una institución de la RM sufre de **Sobredemanda (>100%)** o **Capacidad Ociosa (<70%)**. |
| **`dim_institucion_sies`** | `indice_posicionamiento_competitivo_rm` | Categorización combinada de `anios_acreditacion_sies` + `tasa_ocupacion_inst_rm_2026_pct` | Segmenta las IES de Santiago en 4 cuadrantes estratégicos para vicerrectorías: *Líder Acreditada con Alta Demanda*, *Acreditada con Capacidad Disponible*, *En Riesgo de Calidad con Demanda Activa* y *Crítica: Baja Acreditación y Subocupación*. |
| **`dim_ubicacion_rm`** | `participacion_sede_en_rm_2026_pct` y `tasa_ocupacion_sede_2026_pct` | Participación sobre matrícula RM y razón Matrícula 1er Año / Vacantes por sede | Permite decidir en qué campus/sede de Santiago ampliar infraestructura física y en cuál consolidar o cerrar secciones. |
| **`dim_programa_academico`** | `tasa_ocupacion_programa_2026_pct` y `tasa_presion_laboratorio_base35_pct` | Ocupación de vacantes y presión de tamaño de cohorte respecto al módulo de 35 puestos por laboratorio | Identifica qué carreras (ej. Ingeniería Civil Informática, Medicina, Psicología, Derecho) requieren desdoblar paralelos de laboratorio en Santiago. |

---

### 2.2. Tasas, KPIs y Modelo de Capacidad Operativa (Caso 120 $\rightarrow$ 140) en `fact_matricula_rm`

| Columna en `fact_matricula_rm` | Fórmula / Regla | Decisión de Negocio que Habilita |
| :--- | :--- | :--- |
| **`tasa_ocupacion_vacantes_pct`** | $\frac{\text{matricula\_primer\_anio}}{\text{vacantes}} \times 100$ | Indicador primario de llenado de cupos por carrera/sede/jornada. |
| **`tasa_sobredemanda_pct`** | $\max\left(0, \frac{\text{matricula\_primer\_anio} - \text{vacantes}}{\text{vacantes}} \times 100\right)$ | Cuantifica el exceso porcentual de alumnos matriculados por sobre las vacantes planificadas. |
| **`brecha_vacantes_neta`** | $\text{matricula\_primer\_anio} - \text{vacantes}$ | Si es $>0$, hay sobrecupo; si es $<0$, quedaron vacantes sin llenar (costo hundido). |
| **`secciones_lab_planificadas_35`** | $\lceil \text{vacantes} / 35 \rceil$ | Número de secciones de laboratorio (módulo estándar de 35 puestos) presupuestadas según las vacantes ofrecidas. |
| **`secciones_lab_requeridas_35`** | $\lceil \text{matricula\_primer\_anio} / 35 \rceil$ | Número real de secciones de laboratorio necesarias para atender a los matriculados de 1er año. |
| **`secciones_lab_adicionales_requeridas`** | $\text{secciones\_lab\_requeridas\_35} - \text{secciones\_lab\_planificadas\_35}$ | Si es $\ge 1$, alerta que el incremento de matrícula rompió el umbral de capacidad instalada y obliga a contratar docentes y habilitar nuevos laboratorios. |
| **`tasa_saturacion_secciones_lab_pct`** | $\frac{\text{matricula\_primer\_anio}}{\text{secciones\_lab\_planificadas\_35} \times 35} \times 100$ | **Ejemplo del Profesor (120 $\rightarrow$ 140 alumnos):** Con 4 secciones planificadas ($4 \times 35 = 140$ puestos máximos), pasar de 120 alumnos (`85,7%` de saturación) a 140 alumnos lleva el laboratorio al **`100%` de saturación crítica** (0 puestos de holgura para rezagados) y el alumno 141 obliga a abrir una 5ta sección (`+25%` en costo fijo de laboratorio). |
| **`tasa_renovacion_cohorte_pct`** | $\frac{\text{matricula\_primer\_anio}}{\text{matricula\_total}} \times 100$ | Mide qué fracción del alumnado total corresponde a ingreso nuevo. |
| **`tasa_retencion_aparente_pct`** | $\frac{\text{matricula\_total} - \text{matricula\_primer\_anio}}{\text{matricula\_total}} \times 100$ | Mide la permanencia estructural de cohortes superiores en la carrera. |
| **`brecha_dispersion_puntaje_pt`** | $\text{puntaje\_max\_homologado} - \text{puntaje\_corte\_homologado}$ | Mide la brecha en puntos entre el primer y el último matriculado; si supera 150 puntos, requiere nivelación académica en 1er semestre. |
| **`tasa_heterogeneidad_academica_pct`** | $\frac{\text{brecha\_dispersion\_puntaje\_pt}}{\text{puntaje\_prom\_homologado}} \times 100$ | Tasa relativa de dispersión académica de la cohorte entrante. |
