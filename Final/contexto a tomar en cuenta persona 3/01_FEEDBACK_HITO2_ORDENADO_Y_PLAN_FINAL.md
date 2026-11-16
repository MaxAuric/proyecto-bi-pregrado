# Feedback Ordenado del Hito 2 y Plan de Acción para la Entrega Final (18 de Noviembre)

> **Alcance Oficial del Proyecto:** **100% Región Metropolitana de Santiago (`region_codigo_subdere == '13'`)**  
> **Cifras Clave Auditadas RM:** **58.926** registros históricos de oferta académica (2012–2026) | **164** instituciones históricas en la RM | **69 Instituciones de Educación Superior activas en Santiago en 2026** (**35 Universidades**, **19 Institutos Profesionales**, **11 Centros de Formación Técnica** y **4 Instituciones de las FF.AA. y Orden**).

---

## 1. Ordenamiento e Interpretación del Feedback del Profesor (Hito 2)

Los mensajes enviados durante la evaluación del Hito 2 se agrupan en **3 ejes técnicos y de negocio** que debemos resolver y demostrar en la **Entrega Final (Dashboard Power BI + Informe Ejecutivo + Presentación PPT de 15 min)**:

### Eje 1: Uso de Tasas y KPIs que Tributen a la Propuesta de Valor y Toma de Decisiones
> **Feedback literal:**
> - *"Mejorar y ver el uso de tasas"*
> - *"Los KPI se calculan de alguna forma"*
> - *"Y las medidas tributan a sus propuestas de valor"*
> - *"Está tratando de aportar un valor para tomar una decisión"*
> - *(Comentario adicional en sala):* *"En las tablas `dim` faltan más tasas y KPI que le den más poder y explicación coherente a nuestra propuesta de valor."*

**¿Qué significa y cómo lo resolvimos?**
1. **Mostrar solo conteos brutos (ej. "hay 140 matriculados" o "hay 120 vacantes") NO es un KPI de negocio.** Una tasa relaciona dos magnitudes ($\text{Tasa} = \frac{A}{B} \times 100$) y se compara contra un umbral para **tomar una decisión** (abrir una nueva sección de laboratorio, reasignar presupuesto docente, subir el puntaje mínimo de postulación o ajustar vacantes en una sede de Santiago).
2. **Se agregaron tasas y KPIs directamente en las tablas de dimensión (`dim_*`) y en la tabla de hechos (`fact_matricula_admision`):**
   - En **`dim_tiempo_ine_rm`**: Tasa de Absorción de 1er Año sobre Jóvenes de 18–24 años en la RM (`tasa_absorcion_juvenil_rm_pct`), Tasa de Cobertura Bruta RM (`tasa_cobertura_bruta_rm_pct`), Tasa de Oferta de Vacantes por 1.000 jóvenes (`tasa_oferta_vacantes_1000_jovenes_rm`), Tasa de Ocupación Anual de Vacantes RM (`tasa_ocupacion_anual_rm_pct`) y Variación Interanual (`tasa_crecimiento_matricula_rm_yoy_pct`).
   - En **`dim_institucion_sies`**: Años y Tramo de Acreditación SIES (`anos_acreditacion_sies`, `tramo_acreditacion_sies`), Score de Calidad SIES (`score_calidad_sies_pct`, `0%–100%`), Cuota de Mercado en Santiago (`cuota_mercado_matricula_rm_pct`), Tasa de Ocupación Institucional Anual (`tasa_ocupacion_inst_anual_pct`), Tasa de Permanencia de Cohortes Superiores (`tasa_permanencia_cohortes_sup_pct`) y **Posicionamiento Competitivo RM** (`posicionamiento_competitivo_rm`, que clasifica a cada institución en 4 cuadrantes de decisión).
   - En **`dim_sede_geografia`**: Participación de la Sede en la RM (`participacion_matricula_rm_sede_pct`), Tasa de Ocupación Histórica de la Sede (`tasa_ocupacion_historica_sede_pct`), Tasa de Sobredemanda de Sede (`tasa_sobredemanda_sede_pct`) y Nivel de Saturación de Sede (`nivel_saturacion_sede`).
   - En **`dim_carrera_programa`**: Tasa de Ocupación Histórica del Programa (`tasa_ocupacion_historica_prog_pct`), Frecuencia de Sobredemanda (`tasa_frecuencia_sobredemanda_prog_pct`), **Tasa de Presión de Laboratorio Base 35 (`tasa_presion_lab_base35_prog_pct`)** y Clasificación de Presión de Capacidad (`clasificacion_presion_capacidad`).
   - En **`fact_matricula_admision`** (100% numérica, cero columnas `VARCHAR` según `Clase 4 - DW.pdf` pág. 62): Tasa de Ocupación de Vacantes (`tasa_ocupacion_primer_ano`), Tasa de Sobredemanda (`tasa_sobredemanda_oferta_pct`), Tasa de Renovación de Cohorte (`tasa_renovacion_primer_ano_pct`), Tasa de Retención Aparente (`tasa_retencion_aparente_pct`), **Tasa de Saturación de Secciones de Laboratorio Base 35 (`tasa_saturacion_lab_35_pct`)** y **Secciones Extra por Sobrecupo (`secciones_extra_por_sobrecupo`)** (que modela exactamente el caso expuesto por el profesor de pasar de **120 a 140 alumnos** cuando cada laboratorio soporta **35 estudiantes**).

---

### Eje 2: Transformación 100% Terminada en Python (No se puede cargar el CSV crudo directo)
> **Feedback literal:**
> - *"Transformación no terminada"*
> - *"No podría hacerlo del CSV directo porque habían datos desordenados y con script se ordenaron"*

**¿Qué significa y cómo lo resolvimos?**
1. En el Hito 2 quedaron abreviaturas crudas dentro de las dimensiones (`'Univ.'`, `'I.P.'`, `'C.F.T.'`, `'F.F.A.A.'`), lo cual contradice la regla explícita de **`Clase 4 - DW.pdf` (pág. 62)**: *"Evite códigos o descripciones abreviadas en las tablas de dimensión"*. Además, los 2 CSV de fuentes externas (`rm_ext_ine_poblacion.csv` y `rm_ext_sies_acreditacion.csv`) no estaban integrados dentro de las dimensiones del DataMart.
2. Tampoco era posible conectar Power BI al CSV crudo original porque los archivos históricos 2012–2026 tenían cambios de escala psicométrica (PSU 150–850 vs. PAES 100–1000), códigos de región y comunas desalineados y duplicidades de nombres de sedes.
3. **Solución lista en `Final/P1_INGENIERO_DATOS_ETL_Y_DATAMART/scripts/01_build_final_datamart_rm.py`:** El script de Python deja **el 100% de la transformación terminada**:
   - Expande todos los textos (`'Universidad'`, `'Instituto Profesional'`, `'Centro de Formación Técnica'`, `'Institución de las FF.AA. y Orden'`).
   - Cruza e integra físicamente el INE RM en `dim_tiempo_ine_rm` y SIES en `dim_institucion_sies`.
   - Filtra exclusivamente la **Región Metropolitana de Santiago (`58.926` registros)** para que todo el modelo sea 100% coherente con nuestro alcance geográfico.

---

### Eje 3: Exportación desde Python a Excel Estrella para Importación Instantánea en Power BI
> **Feedback literal:**
> - *"Importación de una tabla en Excel a Power BI es menos tiempo"*
> - *"Y de Python se exporta"*

**¿Qué significa y cómo lo resolvimos?**
1. En el Hito 2 se intentó usar `Python.Execute()` dentro de Power Query en Power BI, lo que demoraba la recarga del panel y generaba problemas de rutas entre computadores.
2. Tal como indicó el profesor, la forma óptima es **procesar y ordenar todo en Python y desde Python exportar las tablas finales a Excel (`.xlsx`)**, además de mantener el `.db` SQLite de respaldo.
3. **Solución lista en `Final/00_DATAMART_LISTO_PARA_POWERBI/`:**
   - Python ya generó el archivo **`DataMart_Estrella_RM_PowerBI.xlsx`**, que contiene en hojas separadas las 5 dimensiones (`dim_tiempo_ine_rm`, `dim_institucion_sies`, `dim_ubicacion_rm`, `dim_programa_academico`, `dim_modalidad_jornada`), la tabla de hechos (`fact_matricula_rm`) y 3 hojas resumen ejecutivas.
   - **Persona 4** solo debe ir a Power BI $\rightarrow$ *Obtener datos de Libro de Excel* $\rightarrow$ seleccionar `DataMart_Estrella_RM_PowerBI.xlsx`, marcar las 6 tablas del Esquema Estrella y cargar en menos de 3 segundos.

---

## 2. Entregables Obligatorios para la Entrega Final (Miércoles 18 de Noviembre)

Según la `Pauta_Trabajo_Final_BI.pdf`, nos jugamos el **83% de la nota del proyecto** en tres elementos que deben hablar **exclusivamente de la Región Metropolitana de Santiago**:

1. **Dashboard Interactivo en Power BI (`.pbix`) — 8 puntos grupales:**
   - Conectado a `DataMart_Estrella_RM_PowerBI.xlsx` (y respaldado por `datamart_estrella_rm_final.db`).
   - Con medidas DAX calculadas con `DIVIDE()` que reflejen las tasas de ocupación, sobredemanda, saturación de laboratorios (base 35 alumnos), retención aparente, absorción demográfica juvenil INE RM y acreditación SIES.
   - Con filtros interactivos sin abreviaturas: Año (`2012–2026`), Tipo de Institución (`Universidad`, `Instituto Profesional`, `Centro de Formación Técnica`), Institución (`69` activas en RM en 2026), Sede/Comuna RM y Tramo de Acreditación SIES.

2. **Informe Ejecutivo Final (`.pdf`) — 5 puntos grupales:**
   - Documento ejecutivo completo que consolida:
     - **Sección 1 (P2):** Problema de negocio en la Región Metropolitana, Canvas BI RM y cómo cada tasa/KPI tributa a una decisión real (incluyendo el caso de capacidad de laboratorios 120 $\rightarrow$ 140 alumnos).
     - **Sección 2 (P1):** Pipeline ETL 100% finalizado en Python, integración de fuentes externas (INE RM y SIES), eliminación de abreviaturas, cuadre exacto (`58.926` registros RM) y exportación a `DataMart_Estrella_RM_PowerBI.xlsx`.
     - **Sección 3 (P3):** Modelo Dimensional Estrella RM enriquecido con tasas y KPIs en dimensiones y hechos, justificación de aditividad y SCD Tipo 2.
     - **Sección 4 (P4):** Diseño del Dashboard Power BI, catálogo de medidas DAX y análisis visual de las 3 preguntas de negocio en Santiago.
     - **Sección 5 (P5):** Conclusiones y recomendaciones ejecutivas para la toma de decisiones en instituciones de la RM.

3. **Presentación PPT (`.pptx`) y Defensa Oral de 15 Minutos — 10 pts Dominio Grupal + 15 pts Defensa Individual + 5 pts Exposición Individual:**
   - Presentación ejecutiva de **12 a 15 diapositivas** (3 minutos por integrante) más demostración en vivo del Dashboard en Power BI.
   - Ronda de preguntas individuales del profesor donde cada integrante debe defender tanto su rol como la lógica de las tasas, KPIs, ETL y modelo estrella en Santiago.
