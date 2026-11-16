# Análisis de KPIs y Mapa de Decisiones — Región Metropolitana de Santiago
## Persona 2: Analista de Negocio RM | Entrega Final Business Intelligence 2026

> [!IMPORTANT]
> Todos los nombres de columnas y tablas de este documento coinciden **exactamente** con el DataMart oficial en `Final/00_DATAMART_LISTO_PARA_POWERBI/`. Usar siempre los nombres exactos al escribir DAX o SQL.

---

## 1. Cifras Auditadas RM 2026 (Fuente: DataMart — 58.926 registros)

| Indicador | Valor Real 2026 | Columna DataMart |
|:---|:---:|:---|
| Vacantes declaradas RM | **253.018** | `fact.vacantes` (sum, `flag_vacantes_declaradas=1`) |
| Matrícula 1er año RM | **208.311** | `fact.matricula_primer_ano_total` (sum) |
| Matrícula total RM | **708.758** | `fact.matricula_total` (sum) |
| Secciones extra por sobrecupo | **674** | `fact.secciones_extra_por_sobrecupo` (sum) |
| Programas sobredemanda crítica | **1.232** | `fact.flag_sobredemanda_critica` (sum) |
| Población joven 18–24 RM (INE) | **821.638** | `dim_tiempo_ine_rm.poblacion_joven_18_24_rm` |
| Puntaje PAES promedio ponderado RM | **703,6** | Calculado con SUMX (ver Sección 3) |
| Retención aparente RM | **70,61%** | Calculado: `(mat_total − mat_1er_año) / mat_total` |
| Crecimiento matrícula YoY | **+5,86%** | `dim_tiempo_ine_rm.tasa_crecimiento_matricula_rm_yoy_pct` |

---

## 2. KPI → Umbral → Decisión (Mapa Completo)

Este mapa responde directamente al feedback del profesor: *«¿Las medidas tributan a sus propuestas de valor?»*

### 2.1 KPIs de Capacidad Instalada (Pregunta P1)

| KPI / Tasa | Fórmula Algebraica | Umbral de Decisión | Acción Concreta en la RM | Columna DataMart |
|:---|:---|:---:|:---|:---|
| **Tasa de Ocupación de Vacantes RM** | $\dfrac{\text{mat\_1er\_año}}{\text{vacantes}} \times 100$ | ≥100% = sobrecupo / <75% = capacidad ociosa | Ajustar oferta de vacantes para el año siguiente; disparar alerta en dashboard | `fact.tasa_ocupacion_primer_ano` |
| **Tasa de Saturación Laboratorio (base 35)** | $\dfrac{\text{mat\_1er\_año}}{\lceil\text{vac}/35\rceil \times 35} \times 100$ | ≥100% = zona roja / ≥85% = zona naranja | Abrir sección extra de laboratorio (+25% costo fijo) | `fact.tasa_saturacion_lab_35_pct` |
| **Secciones Extra por Sobrecupo** | $\max(0,\, \lceil\text{mat}/35\rceil - \lceil\text{vac}/35\rceil)$ | ≥1 = costo operativo no presupuestado | Presupuestar docente, sala e insumos para paralelo adicional | `fact.secciones_extra_por_sobrecupo` |
| **Sobrecupo Neto de Alumnos** | $\max(0, \text{mat\_1er\_año} - \text{vacantes})$ | >0 = alumnos sin cupo formal | Revisar proceso de admisión; priorizar programas con mayor exceso | `fact.sobrecupo_neto_alumnos` |
| **Tasa Sobredemanda de Oferta** | $\max(0, \text{Tasa\_Ocupación} - 100)$ | >0% = sobreocupado | Alertar a Dirección de Admisión; evaluar expansión de vacantes | `fact.tasa_sobredemanda_oferta_pct` |
| **Clasificación Presión Capacidad (carrera)** | Cruce `tasa_ocupacion_historica_prog_pct` × frecuencia | *Alta Presión* (≥95%) / *Media* / *Baja* | Priorizar inversión en infraestructura para carreras en *Alta Presión* | `dim_carrera_programa.clasificacion_presion_capacidad` |

> [!NOTE]
> Las tasas son **algebraicas (no aditivas)**: siempre recalcular con `DIVIDE(SUM(mat), SUM(vac))` desde los totales filtrados. **Nunca** usar `AVERAGE(tasa_ocupacion_primer_ano)`.

---

### 2.2 KPIs de Selectividad y Calidad Académica (Pregunta P2)

| KPI / Tasa | Fórmula Algebraica | Umbral de Decisión | Acción Concreta en la RM | Columna DataMart |
|:---|:---|:---:|:---|:---|
| **Puntaje PAES Ponderado RM** | $\dfrac{\sum \text{puntaje\_equiv\_paes} \times \text{mat\_1er\_año}}{\sum \text{mat\_1er\_año}}$ | Tendencia ↘ con ocupación ↗ = relajación de selectividad | Activar programa de nivelación académica 1er año | `fact.puntaje_promedio_equiv_paes` (SUMX en DAX) |
| **Puntaje de Corte Ponderado RM** | $\dfrac{\sum \text{puntaje\_corte\_equiv\_paes} \times \text{mat\_1er\_año}}{\sum \text{mat\_1er\_año}}$ | Caída >20 puntos en 2 años consecutivos = alerta | Evaluar criterios de admisión; reforzar nivelación diferenciada | `fact.puntaje_corte_ultimo_equiv_paes` |
| **Tasa de Heterogeneidad PAES** | $\dfrac{\text{brecha\_max\_min\_paes}}{\text{puntaje\_promedio\_equiv\_paes}} \times 100$ | ≥30% = alta dispersión en sala de clases | Implementar secciones de nivelación diferenciada en 1er año | `fact.tasa_heterogeneidad_paes_pct` |
| **Brecha Dispersa Max–Min PAES** | $\text{PAES\_máximo} - \text{PAES\_mínimo}$ | >400 puntos = heterogeneidad extrema | Revisar perfil de admisión; evaluar vías alternativas de ingreso | `fact.brecha_dispersa_max_min_paes` |
| **Brecha Corte vs. Media RM PAES** | $\text{puntaje\_corte\_inst} - \overline{\text{puntaje\_corte\_RM}}$ | Negativa = institución por debajo del promedio RM | Señal de competitividad baja; revisar portafolio y selectividad | `fact.brecha_corte_vs_media_rm_paes` |

> [!WARNING]
> Los puntajes PAES son **NO ADITIVOS** (son promedios, no sumas absolutas). En DAX usar siempre:
> ```dax
> Puntaje PAES Pond. RM =
> VAR TablaValida = FILTER(fact_matricula_admision,
>     fact_matricula_admision[flag_exige_prueba_admision] = 1 &&
>     NOT(ISBLANK(fact_matricula_admision[puntaje_promedio_equiv_paes])))
> RETURN DIVIDE(
>     SUMX(TablaValida, fact_matricula_admision[puntaje_promedio_equiv_paes] * fact_matricula_admision[matricula_primer_ano_total]),
>     SUMX(TablaValida, fact_matricula_admision[matricula_primer_ano_total]),
>     BLANK())
> ```
> **Nunca** usar `SUM(puntaje_promedio_equiv_paes)` ni `AVERAGE()` directamente.

---

### 2.3 KPIs Demográficos y de Absorción (Pregunta P3)

| KPI / Tasa | Fórmula Algebraica | Umbral de Decisión | Acción Concreta en la RM | Columna DataMart |
|:---|:---|:---:|:---|:---|
| **Tasa de Absorción Juvenil RM** | $\dfrac{\text{mat\_1er\_año RM}_t}{\text{poblacion\_joven\_18\_24\_rm}_t} \times 100$ | Tendencia ↗ = mayor presión sobre capacidad instalada | Incrementar vacantes en áreas con alta presión (P1) o mejorar retención | `dim_tiempo_ine_rm.tasa_absorcion_juvenil_rm_pct` |
| **Tasa de Cobertura Bruta RM** | $\dfrac{\text{mat\_total RM}_t}{\text{poblacion\_joven\_18\_24\_rm}_t} \times 100$ | ≥80% = mercado **saturado demográficamente** | Competir por cuota de mercado vs. otras IES, no por demanda nueva | `dim_tiempo_ine_rm.tasa_cobertura_bruta_rm_pct` |
| **Oferta de Vacantes / 1.000 Jóvenes** | $\dfrac{\text{Vacantes RM}_t}{\text{poblacion\_joven\_18\_24\_rm}_t} \times 1000$ | <200 = oferta insuficiente / >300 = exceso de oferta | Ajustar expansión de vacantes según dinámica demográfica INE | `dim_tiempo_ine_rm.tasa_oferta_vacantes_1000_jovenes_rm` |
| **Tasa de Retención Aparente RM** | $\dfrac{\text{mat\_total} - \text{mat\_1er\_año}}{\text{mat\_total}} \times 100$ | <65% = alta deserción estructural | Implementar programas de retención (nivelación, becas, tutorías) | `fact.tasa_retencion_aparente_pct` |
| **Tasa de Renovación de Cohorte** | $\dfrac{\text{mat\_1er\_año}}{\text{mat\_total}} \times 100$ | >40% = alta renovación (poca retención de cohortes superiores) | Priorizar políticas de continuidad académica 2do–3er año | `fact.tasa_renovacion_primer_ano_pct` |

---

### 2.4 KPIs de Posicionamiento Competitivo Institucional

| KPI / Tasa | Fórmula / Lógica | Umbral de Decisión | Acción Concreta | Columna DataMart |
|:---|:---|:---:|:---|:---|
| **Posicionamiento Competitivo RM** | Cruce `años_acreditación` × `tasa_ocupación_inst_anual_pct` → 4 cuadrantes | Cuadrante 4 «Crítica» = riesgo sistémico | Intervención regulatoria CNED / plan de mejora institucional | `dim_institucion_sies.posicionamiento_competitivo_rm` |
| **Score Calidad SIES (%)** | $\dfrac{\text{anos\_acreditacion\_sies}}{7} \times 100$ | <57% (<4 años) = acreditación insuficiente | Restricción de nuevas vacantes hasta elevar estándar SIES | `dim_institucion_sies.score_calidad_sies_pct` |
| **Cuota de Mercado Matrícula RM** | $\dfrac{\text{mat\_total\_inst RM}_t}{\text{mat\_total RM}_t} \times 100$ | Declive >3 años consecutivos = pérdida competitiva | Revisar portafolio de programas y estrategia de admisión | `dim_institucion_sies.cuota_mercado_matricula_rm_pct` |
| **Tasa de Programas con Sobredemanda (inst.)** | $\dfrac{\text{carreras con mat > vac}}{\text{carreras con vac declaradas}} \times 100$ | ≥50% = institución con alta presión sistémica | Expandir capacidad física o limitar admisión en carreras saturadas | `dim_institucion_sies.tasa_programas_sobredemanda_inst_pct` |

---

## 3. Tabla Resumen de Áreas por Sobredemanda (RM 2026)

Datos auditados desde `fact_matricula_admision` × `dim_carrera_programa` para año 2026.

| Área de Conocimiento | Vacantes | Mat. 1er Año | Ocupación (%) | Sec. Extra |
|:---|---:|---:|---:|---:|
| Fuerzas Armadas, Orden y Seguridad | 515 | 558 | **108,3%** ⚠️ | 1 |
| Ciencias | 3.361 | 3.207 | **95,4%** 🔴 | 16 |
| Salud | 28.967 | 27.333 | **94,4%** 🔴 | 101 |
| Agricultura, Silvicultura y Veterinaria | 5.092 | 4.613 | 90,6% 🟠 | 12 |
| Derecho | 6.468 | 5.768 | 89,2% 🟠 | 16 |
| Tecnología | 87.053 | 74.844 | 86,0% 🟠 | **268** |
| Ciencias Sociales | 21.007 | 16.298 | 77,6% 🟡 | 55 |
| Administración y Comercio | 63.129 | 48.832 | 77,4% 🟡 | 127 |
| Arte y Arquitectura | 12.764 | 9.410 | 73,7% 🟢 | 24 |
| Humanidades | 2.179 | 1.576 | 72,3% 🟢 | 3 |
| Educación | 22.483 | 15.872 | 70,6% 🟢 | 51 |
| **TOTAL RM 2026** | **253.018** | **208.311** | **82,3%** | **674** |

> **Interpretación:** Tecnología lidera en volumen de secciones extra (268) por el alto número de programas STEM con laboratorios intensivos. Ciencias y Salud lideran en tasa de ocupación (>94%).

---

## 4. Reglas de Aditividad para Dashboard Power BI

| Medida | Tipo de Aditividad | Regla DAX obligatoria |
|:---|:---:|:---|
| Vacantes, Matrícula 1er año, Matrícula total | **Aditiva** ✅ | `SUM()` directo |
| Secciones de laboratorio (planificadas, reales, extra) | **Aditiva** ✅ | `SUM()` directo |
| Sobrecupo neto, Vacantes ociosas | **Aditiva** ✅ | `SUM()` directo |
| Tasas de ocupación, saturación, absorción, cobertura | **Semi-aditiva** ⚠️ | `DIVIDE(SUM(num), SUM(den))` — NUNCA `AVERAGE(tasa)` |
| Puntajes PAES (promedio ponderado) | **No aditiva** ❌ | `DIVIDE(SUMX(filtrado, puntaje × mat), SUMX(filtrado, mat))` |
| Acreditación SIES 2012–2017 | **NULL estructural** 🚫 | No imputar; filtrar a 2018–2026 en visualizaciones de calidad |

---

## 5. Serie Histórica: Absorción y Cobertura RM (2012–2026)

| Año | Absorción Juvenil (%) | Cobertura Bruta (%) | Oferta / 1.000 jóvenes | Ocupación Vacantes (%) |
|:---:|---:|---:|---:|---:|
| 2012 | 21,59% | 69,14% | 242,5 | 89,0% |
| 2013 | 22,24% | 71,89% | 239,4 | 92,9% |
| 2014 | 22,51% | 73,74% | 223,3 | 100,8% |
| 2015 | 22,06% | 74,37% | 224,0 | 98,5% |
| 2016 | 21,98% | 74,98% | 234,7 | 93,6% |
| 2017 | 21,14% | 73,34% | 260,5 | 81,1% |
| 2018 | 20,73% | 72,03% | 241,0 | 86,0% |
| 2019 | 20,39% | 70,96% | 229,9 | 88,7% |
| 2020 | 17,77% | 66,51% | 220,7 | 80,5% *(pandemia)* |
| 2021 | 19,29% | 69,58% | 211,1 | 91,4% |
| 2022 | 20,24% | 71,95% | 264,9 | 76,4% *(quiebre PSU→PAES)* |
| 2023 | 22,39% | 76,55% | 280,4 | 79,9% |
| 2024 | 22,87% | 78,50% | 304,8 | 75,0% |
| 2025 | 24,00% | 82,02% | 291,8 | 82,2% |
| **2026** | **25,35%** | **86,26%** | **307,9** | **82,3%** |

> [!CAUTION]
> La cobertura bruta RM superó el **80% en 2025** y llegó a **86,26% en 2026**: umbral que la bibliografía internacional identifica como **saturación demográfica estructural**. A partir de este nivel, el crecimiento de matrícula no proviene de nueva demanda sino de competencia interinstitucional por cuota de mercado. Esto redefine la estrategia de las IES en Santiago.

---

## 6. Restricciones de Datos y Advertencias

| Restricción | Impacto | Cómo gestionar en el Dashboard |
|:---|:---|:---|
| Acreditación SIES: NULL años 2012–2017 | No hay datos de CNA antes de 2018 | Filtrar visualizaciones de calidad/acreditación a **2018–2026**; no imputar |
| Quiebre PSU → PAES (2022) | Escalas distintas (PSU 150–850 / PAES 100–1.000) | Usar siempre `puntaje_promedio_equiv_paes` (ya normalizado) para series 2012–2026 |
| Vacantes nulas (~25% de registros) | Denominador cero en tasas de ocupación | Siempre filtrar: `flag_vacantes_declaradas = 1` antes de calcular ocupación |
| Matrícula por sede (no domicilio) | Los KPIs miden oferta RM, no residencia del alumno | Declarar explícitamente en el informe y la defensa oral |
| Proxy INE 18–24 años | Estimación del 14% de `poblacion_15_64_rm` | Citar fuente INE en el informe; flag `es_paes` para anotaciones en gráficos |

---

*Documento generado por Persona 2 — Analista de Negocio RM | Entrega Final BI | Noviembre 2026*
*Cifras auditadas mediante `scripts/analisis_negocio_rm.py` → `docs/cifras_rm_2026.json`*
