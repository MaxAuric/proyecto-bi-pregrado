# Guion de Exposición Oral (Slides 6–7) y Banco de Defensa Individual (15 Puntos)
## Proyecto Final de Business Intelligence: Región Metropolitana de Santiago (2012–2026)
**Rol Evaluado:** **Persona 3 — Arquitecto Dimensional y Diccionario de Tasas/KPIs**  
**Autor:** **Angel Pino**  
**Tiempo Asignado en Presentación Oficial:** **Minuto 6:00 a 9:00 (3 minutos exactos)**  
**Ponderación en Pauta Oficial:** 5 pts Exposición Oral + 10 pts Dominio Grupal + 15 pts Defensa Técnica Individual  

---

## 1. Estructura y Contenido de Diapositivas para Persona 5 (Slides 6 y 7)

Persona 5 debe incorporar estas dos diapositivas en la presentación oficial `Presentacion_Defensa_Final_RM.pptx`:

### Slide 6: Arquitectura Dimensional — Esquema Estrella Enriquecido (100% RM)
- **Título de la Diapositiva:** *Arquitectura Dimensional: Esquema Estrella Enriquecido y Gobernanza de Datos (RM)*
- **Subtítulo:** *58.926 Ofertas Académicas (2012–2026) $|$ 69 IES Activas en 2026 $|$ Cumplimiento Estricto Clase 4 DW*
- **Elementos Visuales a Incrustar:**
  - Render central de [`diagrama_modelo_dimensional_estrella_rm.png`](../diagramas/diagrama_modelo_dimensional_estrella_rm.png).
  - 4 tarjetas resumen con métricas auditadas:
    1. **Tabla de Hechos (100% Numérica):** 58.926 filas RM, 43 columnas, **0 columnas VARCHAR** (cumple Clase 4 DW pág. 62).
    2. **Dimensiones Limpias:** Cero abreviaturas (`'Univ.'`, `'I.P.'`, `'C.F.T.'`, `'F.F.A.A.'`) y cero prefijos `(a)/(b)`.
    3. **Integración Externa:** INE RM en `dim_tiempo_ine_rm` y SIES Acreditación en `dim_institucion_sies`.
    4. **SCD Tipo 2 Certificado:** 1.298 fotografías históricas que preservan cambios de acreditación y gratuidad.
- **Grano Declarado:** Una fila por oferta académica de programa, sede física en Santiago, jornada/horario y año cronológico (2012–2026).

---

### Slide 7: Modelado de Tasas/KPIs y la Falacia de la Agregación (DIVIDE en DAX)
- **Título de la Diapositiva:** *Arquitectura de Tasas y Capacidad: Por qué las Tasas son Medidas No Aditivas*
- **Subtítulo:** *Demostración Matemática: Simpson's Paradox $|$ Caso Laboratorios Base 35 (120 $\rightarrow$ 140 Alumnos)*
- **Elementos Visuales a Incrustar:**
  - **Tabla Comparativa de Aditividad (Kimball / Clase 4 DW pág. 29):**
    - *Aditivas:* Vacantes, Matrícula 1er Año, Matrícula Total, Sobrecupo Neto, Secciones Extra.
    - *No Aditivas (Tasas y Puntajes):* Ocupación de Vacantes, Saturación Lab Base 35, Puntaje PAES Ponderado.
  - **Fórmula de Quiebre Operativo (Caso 120 $\rightarrow$ 140 Estudiantes):**
    - Con 120 vacantes: $\lceil 120/35 \rceil = 4$ secciones (140 puestos, 85,7% saturación, 20 cupos de holgura).
    - Con 140 alumnos: $\lceil 140/35 \rceil = 4$ secciones (140 puestos, **100,0% saturación**, cero holgura).
    - Alumno 141: $\lceil 141/35 \rceil = 5$ secciones (**+1 sección extra forzada**, $+25\%$ en costo docente).
  - **Alerta Metodológica:**
    $$\text{Tasa Ocupación Agregada} = \frac{\sum \text{Matrícula 1er Año}}{\sum \text{Vacantes}} \times 100 \neq \text{AVERAGE}(\text{Tasas precalculadas})$$
    Justificación técnica del uso mandatorio de `DIVIDE()` y promedios ponderados en DAX.

---

## 2. Guion Verbal Paso a Paso para la Exposición (3 Minutos Cronometrados)

> **Instrucción:** Hablar con voz firme, técnica y segura. Mirar al profesor y destacar cómo resolvimos cada punto de su feedback del Hito 2.

### Minuto 6:00 a 7:00 — Slide 6: El Esquema Estrella RM y Cero Huérfanos
> *"Buenos días profesor y comisión. Mi nombre es Angel Pino, Persona 3, y como Arquitecto Dimensional del proyecto asumí la responsabilidad de rediseñar nuestro Esquema Estrella para acotarlo 100% a la Región Metropolitana y resolver cada una de las observaciones del Hito 2.*  
>  
> *En primer lugar, auditamos nuestra tabla de hechos central, `fact_matricula_admision`, la cual contiene exactamente **58.926 ofertas académicas** entre 2012 y 2026. Cumpliendo rigurosamente el primer mandamiento de la Clase 4 de Data Warehousing (página 62), **nuestra tabla de hechos es 100% numérica: tiene cero columnas VARCHAR**. Solo almacena claves foráneas enteras, flags binarios de filtrado y métricas cuantitativas.*  
>  
> *Asimismo, eliminamos el 100% de las abreviaturas crudas en las dimensiones: hoy no existen textos como 'Univ.' o 'I.P.', sino etiquetas completas, e integramos directamente las dos fuentes externas: el INE demográfico en la dimensión tiempo y la acreditación SIES en la dimensión institución.*  
>  
> *Para las 69 instituciones activas en Santiago al 2026, implementamos **SCD Tipo 2** con claves subrogadas anuales, garantizando que si una universidad pasó de 3 a 7 años de acreditación, su historia se preserve sin anacronismos. Ejecutamos un script de auditoría automatizado que certifica **cero registros huérfanos** en las cuatro relaciones dimensionales."*

### Minuto 7:00 a 8:00 — Slide 7: Medidas No Aditivas y el Recálculo en DAX
> *"Ahora bien, atendiendo al feedback central del profesor respecto a que 'los conteos brutos no bastan y que las tasas deben tributar a la decisión', clasificamos rigurosamente las medidas bajo la taxonomía de Kimball y Clase 4 (página 29).*  
>  
> *Demostramos técnicamente por qué las tasas de ocupación, la retención y los puntajes PAES son **medidas estrictamente NO ADITIVAS**. Si un analista comete el error de hacer un `SUM` o un `AVERAGE` sobre las tasas precalculadas a nivel de fila, cae en la falacia de promediar promedios o Paradoja de Simpson.*  
>  
> *Por ejemplo, si promediamos una carrera masiva de 600 cupos al 110% con una pequeña de 20 cupos al 20%, el promedio simple daría 65%, sugiriendo una falsa crisis de vacantes. Pero el cociente algebraico real entre la suma de matriculados y la suma de vacantes da un 107,1%, demostrando sobrecupo real. Por ello, diseñamos el catálogo DAX para que Persona 4 programe todas las tasas en Power BI utilizando cocientes dinámicos con `DIVIDE()`, recalculando el numerador y denominador aditivos al filtrar por sede o institución."*

### Minuto 8:00 a 9:00 — Caso Laboratorios 120 $\rightarrow$ 140 Alumnos y Transición a Power BI
> *"Este modelado dimensional cobra vida en el caso de capacidad planteado por la cátedra: ¿qué ocurre cuando una carrera en Santiago pasa de 120 a 140 alumnos si sus laboratorios tienen un tope de 35 puestos?*  
>  
> *En el Esquema Estrella modelamos esto matemáticamente: con 120 vacantes se planifican 4 secciones de 35 puestos, lo que da una capacidad tope de 140 y una saturación del 85,7%, dejando 20 puestos de holgura para repitentes. Pero al subir a 140 matriculados, la saturación llega exactamente al **100,0%**. Ya no cabe ningún alumno reprobado, y el estudiante 141 gatilla la apertura forzada de una quinta sección, encareciendo los costos docentes en un 25%.*  
>  
> *En el DataMart descubrimos que **13.995 ofertas de Santiago han operado con sobredemanda**, forzando la apertura de **7.529 secciones extra de laboratorio**. Con este modelo dimensional cuadrado, limpio y auditado en SQLite y Excel, doy el pase a Persona 4 para ver el Dashboard interactivo en Power BI."*

---

## 3. Banco de 10 Preguntas y Respuestas Técnicas para la Defensa Individual (15 Puntos)

### P1: ¿Por qué eligieron un Esquema Estrella y no un Esquema Copo de Nieve (Snowflake)?
**Respuesta:**  
«Elegimos un Esquema Estrella puro porque, tal como enseña Ralph Kimball y la Clase 4 de DW (págs. 21–25), es la estructura óptima para motores analíticos columnares como VertiPaq en Power BI. El esquema estrella desnormaliza deliberadamente las jerarquías dentro de las dimensiones (por ejemplo, región y comuna dentro de `dim_sede_geografia`, o área y carrera dentro de `dim_carrera_programa`). Esto reduce la cantidad de *joins* a un único salto relacional entre la tabla de hechos y cada dimensión, minimizando el costo computacional de escaneo y asegurando que las consultas se resuelvan en menos de 25 milisegundos, frente a la complejidad y sobrecarga de *joins* que introduce un copo de nieve.»

### P2: ¿Cuál es el grano declarado de su tabla de hechos y por qué no lo agregaron a nivel de institución?
**Respuesta:**  
«El grano de `fact_matricula_admision` es atómico: **una fila por cada oferta académica curricular específica de una institución, en una sede física de la Región Metropolitana, bajo una jornada u horario determinado, en un año cronológico (2012–2026)**.  
No agregamos la tabla de hechos a nivel de institución porque habríamos destruido la variabilidad analítica: impediríamos analizar la sobredemanda por jornada (diurno vs vespertino), por área del conocimiento (carreras STEM vs humanistas) o la saturación de laboratorios por campus. No obstante, para optimizar consultas gerenciales agregadas, construimos la tabla complementaria `agg_resumen_anual_institucion_rm` siguiendo la recomendación de Clase 4 DW (pág. 63).»

### P3: ¿Por qué la tabla de hechos no contiene ninguna columna de texto (VARCHAR)?
**Respuesta:**  
«Porque seguimos al pie de la letra la regla de oro de Clase 4 DW (página 62), que cataloga explícitamente como error arquitectónico incluir atributos de texto en una tabla de hechos. Los textos incrementan exponencialmente el tamaño en bytes por fila y degradan la compresión columnar. En nuestro modelo, las 43 columnas de `fact_matricula_admision` son 100% numéricas: claves foráneas enteras que apuntan a las dimensiones, flags binarios numéricos (0 y 1) para filtrado rápido, y medidas continuas o discretas (INTEGER y REAL). Todo texto descriptivo pertenece exclusivamente a las dimensiones.»

### P4: ¿Cómo gestionaron los cambios en el tiempo de las instituciones (SCD) y por qué usaron Tipo 2?
**Respuesta:**  
«Implementamos **SCD Tipo 2 (Slowly Changing Dimensions)** en `dim_institucion_sies`. Entre 2012 y 2026, las instituciones en Chile cambian radicalmente: aumentan o pierden años de acreditación CNA, obtienen plena autonomía del CNED o se adscriben a la gratuidad desde 2016. Si usáramos SCD Tipo 1 (sobrescritura), generaríamos un grave anacronismo histórico, evaluando las decisiones de 2012 con la acreditación de 2026. Con SCD Tipo 2 generamos una clave subrogada anual (`id_institucion_sk`) con su respectivo `ano_vigencia`, registrando 1.298 fotografías institucionales históricas. Cada oferta de la tabla de hechos apunta exactamente a la fotografía regulatoria que la institución tenía en el año en que se abrió la matrícula.»

### P5: ¿Por qué insisten en que las tasas son medidas no aditivas y qué pasa si las promedio en DAX?
**Respuesta:**  
«Las tasas y porcentajes son medidas no aditivas porque representan razones entre dos cantidades de distinto peso ($\text{Tasa} = A / B$). Promediarlas directamente mediante la función `AVERAGE` en DAX o Excel comete la falacia de ponderación idéntica o Paradoja de Simpson: le asigna el mismo peso a una carrera de 10 alumnos que a una de 1.000 alumnos.  
En el modelo demostramos matemáticamente que promediar tasas precalculadas puede arrojar un 65% de ocupación aparente cuando en realidad la institución opera con un 107% de sobrecupo real. En DAX, la única forma metodológicamente correcta de calcular una tasa es descomponerla en sus sumas aditivas atómicas utilizando `DIVIDE(SUM(Numerador), SUM(Denominador), BLANK()) * 100`.»

### P6: ¿Cómo modelaron técnicamente en el DataMart el caso de capacidad de laboratorios de 120 a 140 alumnos en módulos de 35?
**Respuesta:**  
«Lo modelamos directamente en la tabla de hechos con cuatro métricas de ingeniería de capacidad:
1. `secciones_lab_planificadas_35`: calculada como el techo entero de vacantes dividido por 35 ($\lceil \text{vacantes}/35 \rceil$). Para 120 vacantes, planifica 4 secciones (capacidad 140, saturación 85,7% y 20 puestos libres).
2. `secciones_lab_reales_35`: calculada como $\lceil \text{matrícula 1er año}/35 \rceil$. Al subir a 140 alumnos, requiere 4 secciones, pero la saturación llega al 100,0% y la holgura desaparece.
3. `secciones_extra_por_sobrecupo`: evalúa el exceso de secciones requeridas. Si la matrícula llega a 141 alumnos, esta métrica salta inmediatamente a 1 sección extra.
4. `tasa_saturacion_lab_35_pct`: evalúa el porcentaje de llenado del laboratorio planificado.  
En todo el histórico de Santiago, detectamos 7.529 secciones extra forzadas por sobrecupo.»

### P7: ¿Cómo integraron la Fuente Externa 1 (Proyecciones Demográficas del INE RM) en el Esquema Estrella?
**Respuesta:**  
«Integramos las proyecciones demográficas del INE para la Región Metropolitana directamente dentro de la dimensión temporal `dim_tiempo_ine_rm`. Enriquecimos cada año con la población total de Santiago, la población en edad de trabajar (15–64) y específicamente la cohorte juvenil universitaria de 18 a 24 años. A partir de ello precalculamos la `tasa_absorcion_juvenil_rm_pct` (que relaciona los matriculados de 1er año en Santiago contra los jóvenes de 18–24 años de la RM, promediando 21,64%) y la tasa de cobertura bruta (>80%), permitiendo demostrar que el mercado universitario de Santiago está demográficamente saturado y que crecer exige capturar cuota de mercado.»

### P8: ¿Cómo integraron la Fuente Externa 2 (Acreditación SIES / CNA) y qué porcentaje de cruce obtuvieron?
**Respuesta:**  
«Integramos la acreditación institucional directamente en `dim_institucion_sies`, agregando los años oficiales de acreditación (0 a 7), el tramo de calidad (Excelencia, Avanzada, Básica, No Acreditada) y el `score_calidad_sies_pct`. Además, construimos la tabla puente `puente_institucion_sies` para conciliar la discrepancia de nombres entre INDICES CNED y los códigos de IES del SIES. Logramos un **98,25% de cruce directo** con códigos SIES en las ofertas de la RM (57.892 de 58.926 filas), y el 1,75% restante se preservó sin pérdida de filas mediante `LEFT JOIN` imputando su condición a partir del atributo legal histórico de acreditación.»

### P9: ¿Cómo demostraron que no existen registros huérfanos en la base de datos?
**Respuesta:**  
«Construí un script de auditoría automatizado en Python (`audit_architecture_and_integrity_p3.py`) que ejecuta consultas relacionales `LEFT JOIN` entre las 58.926 filas de `fact_matricula_admision` y las tablas de dimensión buscando claves foráneas nulas. El resultado arrojó **cero registros huérfanos** en `id_tiempo`, cero en `id_sede_geografia`, cero en `id_institucion_sk` y cero en `id_carrera_programa_sk`. Las claves foráneas tienen una integridad del 100,000% y todas las claves primarias de las dimensiones y de los hechos demostraron unicidad absoluta.»

### P10: ¿Para qué sirve la tabla `agg_resumen_anual_institucion_rm` si ya tienen la tabla de hechos atómica?
**Respuesta:**  
«Cumple con la directriz de Clase 4 DW (página 63) y Clase 5 ETL (slide 10) sobre estrategias de resumen y optimización de rendimiento en Data Warehouses. Mientras que la tabla de hechos almacena 58.926 filas para análisis a nivel de carrera y jornada, la tabla agregada precalcula anualmente los totales por institución (1.298 filas). Esto permite que las tarjetas de KPI ejecutivas, los gráficos de cuota de mercado institucional y los análisis de tendencia en Power BI carguen de forma casi instantánea, liberando al motor de recalcular sumatorias de miles de filas cuando el usuario solo requiere una visión corporativa.»
