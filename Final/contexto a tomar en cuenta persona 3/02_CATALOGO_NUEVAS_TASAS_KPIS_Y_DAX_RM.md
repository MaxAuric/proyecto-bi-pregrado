# Catálogo Maestro de Tasas, KPIs y Medidas DAX — Región Metropolitana de Santiago (RM)

> **Importante:** Todos los nombres de tablas y columnas de este catálogo coinciden **exactamente** tanto con el libro Excel [`DataMart_Estrella_RM_PowerBI.xlsx`](file:///c:/Users/Shila/Documents/Otros/Proy%20IN/Final/00_DATAMART_LISTO_PARA_POWERBI/DataMart_Estrella_RM_PowerBI.xlsx) como con la base SQLite [`datamart_estrella_rm_final.db`](file:///c:/Users/Shila/Documents/Otros/Proy%20IN/Final/00_DATAMART_LISTO_PARA_POWERBI/datamart_estrella_rm_final.db).

---

## 1. Tablas del Esquema Estrella RM Exportadas desde Python

| Nombre Exacto de la Tabla / Hoja Excel | Filas (RM) | Rol en el Modelo Estrella |
| :--- | :---: | :--- |
| **`fact_matricula_admision`** | `58.926` | Tabla de hechos central (100% numérica, cero columnas `VARCHAR` según `Clase 4 DW` Pág. 62). |
| **`dim_tiempo_ine_rm`** | `15` | Dimensión temporal (`2012–2026`) integrada con proyecciones demográficas **INE RM** y tasas anuales. |
| **`dim_institucion_sies`** | `1.298` | Dimensión institucional SCD Tipo 2 en la RM (`69` IES activas en 2026) integrada con **SIES Acreditación** y KPIs competitivos. |
| **`dim_sede_geografia`** | `22` | Dimensión geográfica de sedes en la Región Metropolitana con tasas de ocupación y saturación. |
| **`dim_carrera_programa`** | `5.108` | Dimensión académica de carreras/programas en la RM con tasas de presión de cupos y laboratorios. |
| **`agg_resumen_anual_institucion_rm`** | `1.298` | Tabla agregada anual por institución en la RM (para consultas rápidas de resumen según `Clase 4 DW` Pág. 63). |
| **`puente_institucion_sies`** | `259` | Tabla puente oficial de auditoría entre nombres CNED y códigos SIES (`Pauta Oficial` Pág. 3). |

---

## 2. Nuevas Tasas y KPIs en las Tablas de Dimensión (`dim_*`)

### A. `dim_tiempo_ine_rm` (Dimensión Temporal + Demografía Juvenil INE RM)
| Columna Exacta en `dim_tiempo_ine_rm` | Fórmula Matemática | Decisión de Negocio que Habilita en Santiago |
| :--- | :--- | :--- |
| **`tasa_absorcion_juvenil_rm_pct`** | $\frac{\text{Matrícula 1er Año RM}_t}{\text{poblacion\_joven\_18\_24\_rm}_t} \times 100$ | Mide qué porcentaje de los jóvenes de 18 a 24 años de Santiago ingresa cada año a primer año de educación superior. |
| **`tasa_cobertura_bruta_rm_pct`** | $\frac{\text{Matrícula Total RM}_t}{\text{poblacion\_joven\_18\_24\_rm}_t} \times 100$ | Evalúa la saturación demográfica estructural en la RM (>80%): demuestra que crecer en Santiago exige capturar cuota de mercado o mejorar retención. |
| **`tasa_oferta_vacantes_1000_jovenes_rm`** | $\frac{\text{Vacantes RM}_t}{\text{poblacion\_joven\_18\_24\_rm}_t} \times 1000$ | Mide cuántos cupos de 1er año ofrecen las instituciones de Santiago por cada 1.000 jóvenes de 18–24 años. |
| **`tasa_ocupacion_anual_rm_pct`** | $\frac{\text{Matrícula 1er Año RM}_t}{\text{Vacantes RM}_t} \times 100$ | Benchmark anual de llenado de vacantes en la Región Metropolitana. |
| **`tasa_crecimiento_matricula_rm_yoy_pct`** | $\frac{\text{Mat. 1er Año}_t - \text{Mat. 1er Año}_{t-1}}{\text{Mat. 1er Año}_{t-1}} \times 100$ | Variación porcentual interanual de ingreso nuevo en Santiago. |

---

### B. `dim_institucion_sies` (Dimensión Institucional + Calidad SIES + Competitividad RM)
*Cumplimiento `Clase 4 DW` Pág. 62:* Cero abreviaturas (`Universidad`, `Instituto Profesional`, `Centro de Formación Técnica`, `Institución de las Fuerzas Armadas y de Orden`) y cero prefijos `(a)/(b)`.

| Columna Exacta en `dim_institucion_sies` | Fórmula / Regla | Cómo Tributa a la Propuesta de Valor en Santiago |
| :--- | :--- | :--- |
| **`anos_acreditacion_sies`** y **`tramo_acreditacion_sies`** | Cruce oficial SIES (`0` a `7` años) | Clasifica en `1. Excelencia (6 a 7 años)`, `2. Avanzada (4 a 5 años)`, `3. Básica (1 a 3 años)` y `4. No Acreditada (0 años)`. |
| **`score_calidad_sies_pct`** | $\frac{\text{anos\_acreditacion\_sies}}{7} \times 100$ | Estandariza la acreditación institucional en una tasa de `0%` a `100%`. |
| **`tasa_ocupacion_inst_anual_pct`** | $\frac{\sum \text{Mat. 1er Año Inst.}_t}{\sum \text{Vacantes Inst.}_t} \times 100$ | Mide la eficiencia anual de llenado de cupos de la institución. |
| **`tasa_programas_sobredemanda_inst_pct`** | $\frac{\text{Ofertas con Mat. 1er Año > Vacantes}}{\text{Ofertas con Vacantes Declaradas}} \times 100$ | Porcentaje de carreras de la institución que sufren sobrecupo crítico en ese año. |
| **`cuota_mercado_matricula_rm_pct`** | $\frac{\text{Matrícula Total Inst. RM}_t}{\text{Matrícula Total RM}_t} \times 100$ | Market Share anual de la institución dentro de la Región Metropolitana de Santiago. |
| **`tasa_permanencia_cohortes_sup_pct`** | $\frac{\text{Mat. Total} - \text{Mat. 1er Año}}{\text{Mat. Total}} \times 100$ | Tasa de permanencia de alumnos de cursos superiores en la institución. |
| **`posicionamiento_competitivo_rm`** | Cruce `anos_acreditacion_sies` $\times$ `tasa_ocupacion_inst_anual_pct` | Clasifica a cada IES de Santiago en 4 cuadrantes de decisión: *1. Líder Acreditada con Alta Demanda (>=85%)*, *2. Acreditada con Capacidad Disponible (<85%)*, *3. En Riesgo de Calidad con Demanda Activa*, *4. Crítica: Baja Acreditación y Subocupación*. |

---

### C. `dim_sede_geografia` y `dim_carrera_programa`
| Tabla | Columna Exacta (Tasa / KPI) | Fórmula / Lógica | Decisión que Habilita en Santiago |
| :--- | :--- | :--- | :--- |
| **`dim_sede_geografia`** | `tasa_ocupacion_historica_sede_pct`, `tasa_sobredemanda_sede_pct`, `participacion_matricula_rm_sede_pct`, `nivel_saturacion_sede` | Razón Matrícula 1er Año / Vacantes y % de ofertas con sobrecupo por sede | Identifica qué sedes de Santiago están en *1. Sede Saturada / Alta Presión (>=95%)* frente a *3. Sede con Capacidad Ociosa (<80%)*. |
| **`dim_carrera_programa`** | `tasa_ocupacion_historica_prog_pct`, `tasa_frecuencia_sobredemanda_prog_pct`, `tasa_presion_lab_base35_prog_pct`, `clasificacion_presion_capacidad` | Ocupación acumulada y presión media sobre módulos de laboratorio de 35 puestos | Permite decidir qué carreras requieren abrir paralelos adicionales de laboratorio y cuáles deben ajustar vacantes. |

---

## 3. Tasas y KPIs en `fact_matricula_admision` (Incluyendo Caso 120 $\rightarrow$ 140 Alumnos)

| Columna Exacta en `fact_matricula_admision` | Fórmula Matemática | Interpretación para Toma de Decisiones |
| :--- | :--- | :--- |
| **`tasa_ocupacion_primer_ano`** | $\frac{\text{matricula\_primer\_ano\_total}}{\text{vacantes}} \times 100$ | Porcentaje de llenado de vacantes de la oferta académica. |
| **`tasa_sobredemanda_oferta_pct`** | $\max(0, \text{tasa\_ocupacion\_primer\_ano} - 100)$ | Exceso porcentual por sobre el 100% de las vacantes ofrecidas. |
| **`secciones_lab_planificadas_35`** | $\lceil \text{vacantes} / 35 \rceil$ | Secciones de laboratorio de 35 puestos presupuestadas según vacantes. |
| **`secciones_lab_reales_35`** | $\lceil \text{matricula\_primer\_ano\_total} / 35 \rceil$ | Secciones de laboratorio de 35 puestos realmente requeridas por los matriculados. |
| **`secciones_extra_por_sobrecupo`** | $\max(0, \text{secciones\_lab\_reales\_35} - \text{secciones\_lab\_planificadas\_35})$ | Paralelos extra de laboratorio que la institución se ve obligada a abrir por sobredemanda. |
| **`tasa_saturacion_lab_35_pct`** | $\frac{\text{matricula\_primer\_ano\_total}}{\text{secciones\_lab\_planificadas\_35} \times 35} \times 100$ | **Caso 120 $\rightarrow$ 140 alumnos:** Con 120 vacantes se planifican $\lceil 120/35 \rceil = 4$ secciones (capacidad tope = 140 puestos; saturación con 120 alumnos = `85,7%`). Al subir a 140 matriculados, la saturación llega al **`100,0%`** (cero holgura para repitentes) y el alumno 141 exige abrir una 5ta sección (`+25%` costo fijo). |
| **`tasa_renovacion_primer_ano_pct`** | $\frac{\text{matricula\_primer\_ano\_total}}{\text{matricula\_total}} \times 100$ | Peso de la cohorte nueva sobre la matrícula total del programa. |
| **`tasa_retencion_aparente_pct`** | $\frac{\text{matricula\_total} - \text{matricula\_primer\_ano\_total}}{\text{matricula\_total}} \times 100$ | Permanencia de cohortes superiores en la carrera. |
| **`brecha_dispersa_max_min_paes`** y **`tasa_heterogeneidad_paes_pct`** | $\text{Máx PAES} - \text{Mín PAES}$ y $\frac{\text{Brecha}}{\text{Promedio PAES}} \times 100$ | Mide la dispersión de puntajes dentro de la sala de clases para decidir programas de nivelación en 1er año. |

---

## 4. Bloque de Medidas DAX Listo para Copiar en Power BI (Persona 4)

```dax
// =========================================================================
// MEDIDAS DAX OFICIALES — ENTREGA FINAL BI (REGIÓN METROPOLITANA)
// Nombres 100% compatibles con DataMart_Estrella_RM_PowerBI.xlsx y SQLite
// =========================================================================

// 1. Medidas Aditivas / Distributivas (Conteos Base)
Matrícula 1er Año RM = SUM(fact_matricula_admision[matricula_primer_ano_total])

Matrícula Total RM = SUM(fact_matricula_admision[matricula_total])

Vacantes Ofrecidas RM = SUM(fact_matricula_admision[vacantes])

Sobrecupo Neto Alumnos RM = SUM(fact_matricula_admision[sobrecupo_neto_alumnos])

Vacantes Ociosas Netas RM = SUM(fact_matricula_admision[vacantes_ociosas_netas])

// 2. Tasas Algebraicas de Ocupación y Sobredemanda (Con DIVIDE según Clase 4 DW Pág. 29)
Tasa Ocupación Vacantes RM (%) = 
DIVIDE(
    CALCULATE(SUM(fact_matricula_admision[matricula_primer_ano_total]), fact_matricula_admision[flag_vacantes_declaradas] = 1),
    CALCULATE(SUM(fact_matricula_admision[vacantes]), fact_matricula_admision[flag_vacantes_declaradas] = 1),
    BLANK()
) * 100

Tasa Sobredemanda RM (%) = 
VAR Ocupacion = [Tasa Ocupación Vacantes RM (%)]
RETURN IF(ISBLANK(Ocupacion), BLANK(), MAX(0, Ocupacion - 100))

// 3. KPIs de Capacidad de Laboratorios (Caso 120 -> 140 alumnos, módulo 35 puestos)
Secciones Lab Planificadas (Base 35) = SUM(fact_matricula_admision[secciones_lab_planificadas_35])

Secciones Lab Reales Requeridas (Base 35) = SUM(fact_matricula_admision[secciones_lab_reales_35])

Secciones Lab Extra por Sobrecupo = SUM(fact_matricula_admision[secciones_extra_por_sobrecupo])

Tasa Saturación Laboratorios RM (%) = 
DIVIDE(
    CALCULATE(SUM(fact_matricula_admision[matricula_primer_ano_total]), fact_matricula_admision[secciones_lab_planificadas_35] > 0),
    CALCULATE(SUM(fact_matricula_admision[secciones_lab_planificadas_35]) * 35, fact_matricula_admision[secciones_lab_planificadas_35] > 0),
    BLANK()
) * 100

// 4. Tasas de Renovación y Retención Estructural
Tasa Renovación Cohorte RM (%) = 
DIVIDE([Matrícula 1er Año RM], [Matrícula Total RM], BLANK()) * 100

Tasa Retención Aparente RM (%) = 
DIVIDE([Matrícula Total RM] - [Matrícula 1er Año RM], [Matrícula Total RM], BLANK()) * 100

// 5. KPIs de Selectividad Ponderada y Heterogeneidad PAES (Escala 100-1000)
Puntaje PAES Promedio Ponderado RM = 
VAR TablaValida = FILTER(fact_matricula_admision, fact_matricula_admision[flag_exige_prueba_admision] = 1 && NOT(ISBLANK(fact_matricula_admision[puntaje_promedio_equiv_paes])))
RETURN
DIVIDE(
    SUMX(TablaValida, fact_matricula_admision[puntaje_promedio_equiv_paes] * fact_matricula_admision[matricula_primer_ano_total]),
    SUMX(TablaValida, fact_matricula_admision[matricula_primer_ano_total]),
    BLANK()
)

Puntaje PAES Corte Ponderado RM = 
VAR TablaValida = FILTER(fact_matricula_admision, NOT(ISBLANK(fact_matricula_admision[puntaje_corte_ultimo_equiv_paes])) && fact_matricula_admision[matricula_primer_ano_total] > 0)
RETURN
DIVIDE(
    SUMX(TablaValida, fact_matricula_admision[puntaje_corte_ultimo_equiv_paes] * fact_matricula_admision[matricula_primer_ano_total]),
    SUMX(TablaValida, fact_matricula_admision[matricula_primer_ano_total]),
    BLANK()
)

Tasa Heterogeneidad PAES Promedio (%) = 
AVERAGE(fact_matricula_admision[tasa_heterogeneidad_paes_pct])

// 6. Tasas de Cuota de Mercado y Demografía Juvenil INE RM
Cuota Mercado Matrícula RM (%) = 
DIVIDE(
    [Matrícula Total RM],
    CALCULATE([Matrícula Total RM], ALL(dim_institucion_sies), ALL(dim_sede_geografia), ALL(dim_carrera_programa)),
    0
) * 100

Tasa Absorción Juvenil INE RM (%) = 
DIVIDE(
    [Matrícula 1er Año RM],
    AVERAGE(dim_tiempo_ine_rm[poblacion_joven_18_24_rm]),
    BLANK()
) * 100
```
