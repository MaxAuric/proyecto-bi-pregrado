# Guión de Defensa Oral y Contenido de Diapositivas — Persona 2
## Rol: Analista de Negocio RM | Entrega Final Business Intelligence 2026

> [!IMPORTANT]
> **Tiempo asignado a Persona 2:** **3 minutos** de exposición continua + ronda de preguntas individuales del profesor (15 pts Defensa Individual + 5 pts Exposición Individual = **20 puntos personales**).
> Este documento contiene el libreto exacto palabra por palabra, el diseño de diapositivas que debe usar Persona 5 y el banco de preguntas difíciles del profesor con sus respuestas técnicas fundamentadas.

---

## 1. Estructura de las Diapositivas de Persona 2 (Slides 1 a 3 de la PPT)

### Slide 1: Propuesta de Valor y Canvas BI de 10 Bloques (Foco 100% RM)
- **Título:** Propuesta de Valor y Canvas BI — Región Metropolitana de Santiago
- **Subtítulo:** Decisiones de Planificación de Vacantes, Capacidad de Laboratorios y Selectividad (2012–2026)
- **Elementos visuales clave:**
  - El Canvas BI de 10 bloques sintetizado.
  - Cifras auditadas en tarjetas: **58.926** registros históricos RM | **69** IES activas 2026 (35 Univ, 19 IP, 11 CFT, 4 FF.AA.) | **253.018** vacantes vs. **208.311** matriculados en 2026 (82,3% ocupación).
  - Los 2 usuarios clave: Directores de Admisión/Planificación IES y Subsecretaría de Educación Superior / CNED.
- **Mensaje central:** *«No analizamos datos por curiosidad; cada dato responde a: ¿cuántos cupos abrimos el próximo año sin que colapsen nuestras salas ni caiga la calidad?»*

### Slide 2: El Quiebre Operativo — Caso de Capacidad de Laboratorios (120 $\to$ 140 Alumnos)
- **Título:** Del Dato a la Decisión: El Caso de Saturación de Laboratorios (Módulo 35 Puestos)
- **Elementos visuales clave:**
  - Esquema comparativo de 3 escenarios:
    1. **120 vacantes:** $\lceil 120 / 35 \rceil = 4$ secciones planificadas $\to$ Capacidad 140 puestos $\to$ **85,7% saturación** (20 puestos de holgura).
    2. **140 matriculados (Sobrecupo):** $\lceil 140 / 35 \rceil = 4$ secciones reales $\to$ **100,0% saturación** (cero holgura para repitentes, `secciones_extra = 0`).
    3. **141 matriculados:** $\lceil 141 / 35 \rceil = 5$ secciones reales $\to$ `secciones_extra_por_sobrecupo = 1` $\to$ **+25% de costo fijo** (docente, sala, insumos) para atender a **1 solo alumno**.
  - Tarjeta con cifra real 2026: **674 secciones de laboratorio extra por sobrecupo** en la RM (268 solo en Tecnología).
  - Efecto dominó: Mayor sobrecupo $\to$ relajación de corte PAES $\to$ alta dispersión en sala (`tasa_heterogeneidad_paes_pct` $\ge$ 30%) $\to$ aumento de reprobación y deserción en 2do año.

### Slide 3: Las 3 Preguntas de Negocio y el Mapa de KPIs de Decisión
- **Título:** 3 Preguntas de Negocio, Tasas Derivadas y Umbrales de Acción
- **Elementos visuales clave:**
  - Tabla de 3 preguntas con sus KPIs y umbrales semafóricos:
    - **P1 (Capacidad):** Tasa de Ocupación ($\ge$100% sobrecupo / <75% ociosa) y Secciones Extra ($\ge$1).
    - **P2 (Selectividad):** Puntaje PAES Ponderado (medida no aditiva, escala continua 100–1000) y Tasa de Heterogeneidad ($\ge$30%).
    - **P3 (Absorción INE):** Tasa de Absorción Juvenil (**25,35%**) y Tasa de Cobertura Bruta (**86,26%** $\ge$ 80% mercado saturado).
  - Regla de oro metodológica: *"Las tasas no se promedian; se recalculan desde los totales aditivos usando `DIVIDE()`"*.

---

## 2. Guión Palabra por Palabra para la Exposición Oral (3 Minutos Exactos)

*(Práctica recomendada: leer a ritmo pausado, seguro y con contacto visual con el profesor).*

> **[0:00 – 0:45] Minuto 1: Introducción, Alcance y Propuesta de Valor**
>
> *"Buenas tardes profesor y compañeros. Como **Analista de Negocio**, mi responsabilidad en este proyecto fue estructurar la **Propuesta de Valor y el Canvas BI de 10 bloques**, enfocándonos de manera estricta y al 100% en la **Región Metropolitana de Santiago** para el periodo 2012 a 2026.*
>
> *Para responder directamente al feedback que usted nos entregó en el Hito 2: no queríamos un tablero que solo mostrara totales descriptivos de 'cuántos alumnos hay'. Una cifra bruta no permite tomar decisiones. Nuestro sistema está diseñado para que los **Directores de Planificación y Admisión de las 69 IES activas de Santiago**, así como los reguladores del **CNED y la Subsecretaría**, puedan responder a una pregunta crítica: **¿cómo planificar las vacantes del próximo año sin generar un quiebre de capacidad física ni sacrificar la selectividad académica?** Todos los análisis que verán hoy se basan en **58.926 registros históricos auditados** de nuestra región."*

---

> **[0:45 – 1:45] Minuto 2: El Quiebre Operativo (Caso 120 a 140 alumnos)**
>
> *"Para ilustrar cómo cada indicador tributa a una decisión real, tomemos el caso concreto de capacidad de laboratorios que usted nos planteó: consideremos una carrera en Santiago que ofrece **120 vacantes**, donde cada módulo de laboratorio admite un máximo de **35 alumnos**.*
>
> *Inicialmente, la institución planifica $\lceil 120 / 35 \rceil = 4$ secciones de laboratorio, lo que entrega una capacidad física instalada de 140 puestos. Con los 120 alumnos planificados, la tasa de saturación es de un saludable **85,7%**, dejando 20 cupos de holgura para estudiantes repitentes.*
>
> *Sin embargo, si por presiones de matrícula la carrera acepta a **140 estudiantes**, la saturación llega exactamente al **100%**: la holgura desaparece por completo. Y si ingresa **un solo estudiante adicional —el alumno 141—**, la fórmula de secciones reales $\lceil 141 / 35 \rceil$ salta a 5. Esto dispara la métrica `secciones_extra_por_sobrecupo = 1`. ¿Qué significa esto en el negocio? Que la universidad se ve forzada a contratar un profesor extra, reservar un laboratorio adicional y duplicar insumos: un incremento inmediato del **25% en costos fijos** para capturar el arancel de un solo alumno.*
>
> *En nuestro DataMart demostramos que este no es un caso teórico: en 2026, la Región Metropolitana registró **674 secciones extra de laboratorio no presupuestadas**, concentradas principalmente en el área de Tecnología con 268 secciones."*

---

> **[1:45 – 3:00] Minuto 3: Las 3 Preguntas de Negocio, Integración INE/SIES y Reglas Técnicas**
>
> *"Para gobernar este problema, formulamos tres preguntas de negocio conectadas directamente con el modelo dimensional:*
>
> *Primero, en **Presión de Demanda**, monitoreamos la tasa de ocupación: áreas como Ciencias y Salud operan al **95,4% y 94,4% de ocupación**, en zona crítica.*
>
> *Segundo, en **Selectividad Institucional**, analizamos cómo reaccionan los puntajes PAES ante la sobredemanda. Aquí aplicamos una regla técnica fundamental: **los puntajes PAES son holísticos y no aditivos**. Jamás usamos `SUM` ni `AVERAGE` simple; implementamos un promedio ponderado por matrícula mediante `SUMX` en escala normalizada 100 a 1.000, evidenciando un promedio RM de **703,6 puntos** en 2026.*
>
> *Y tercero, en **Absorción y Demografía**, integramos las proyecciones del **INE** y la acreditación de **SIES**. En 2026, la tasa de absorción juvenil es del **25,35%**, lo que significa que uno de cada cuatro jóvenes de 18 a 24 años de Santiago entra a primer año. Pero más relevante aún: la **tasa de cobertura bruta llegó al 86,26%**. Al superar el umbral internacional del 80%, el sistema entra en **saturación demográfica estructural**. Las instituciones de la RM ya no pueden crecer esperando nueva demanda juvenil; ahora deben competir por cuota de mercado o fidelizar mediante retención.*
>
> *A continuación, mis compañeros presentarán cómo el pipeline ETL, el modelo estrella y el dashboard interactivo materializan estas decisiones. Muchas gracias."*

---

## 3. Banco de Preguntas Difíciles del Profesor (Defensa Individual — 15 Puntos)

### Pregunta 1: *"¿Por qué la tasa de saturación de laboratorio usa la función techo (`CEILING`) y el módulo de 35 puestos?"*
**Respuesta técnica del alumno:**
> *"Profesor, en la gestión física universitaria las aulas y laboratorios son **bienes indivisibles y discretos**: no es posible abrir '4,2 secciones' de laboratorio. Si tengo 141 alumnos y cada módulo soporta 35 puestos, matemáticamente $\frac{141}{35} = 4,028$. La institución no puede dejar a ese 0,028 de alumnos sin laboratorio; está obligada por estándar docente y acreditación CNA a abrir la 5ta sección completa mediante $\lceil 141 / 35 \rceil = 5$. Por eso la columna `secciones_extra_por_sobrecupo = MAX(0, CEILING(mat/35) - CEILING(vac/35))` refleja el verdadero costo marginal de infraestructura que la contabilidad tradicional oculta en los promedios globales."*

---

### Pregunta 2: *"¿Por qué no puedo simplemente promediar la columna `tasa_ocupacion_primer_ano` en Power BI con un `AVERAGE()`?"*
**Respuesta técnica del alumno:**
> *"Porque la tasa de ocupación es una **medida derivada o no aditiva de tipo algebraica** (`Clase 4 DW`, pág. 29). Si promediamos directamente con `AVERAGE()`, estaríamos dándole el mismo peso estadístico a un programa pequeño de 10 vacantes que a una carrera masiva de 500 vacantes (efecto de la 'paradoja de Simpson' o sesgo por tamaño). La regla de negocio exige que al subir de nivel en la jerarquía (por ejemplo, a nivel de Institución, Área o Región), la tasa se recalcule dividiendo la suma total de matriculados entre la suma total de vacantes declaradas: `DIVIDE(SUM(matricula), SUM(vacantes))`. Ese cálculo dinámico lo garantizamos en DAX filtrando además por `flag_vacantes_declaradas = 1` para no distorsionar el denominador con valores nulos."*

---

### Pregunta 3: *"¿Cómo manejaron el cambio de la PSU a la PAES en 2022 para que la serie de selectividad sea válida?"*
**Respuesta técnica del alumno:**
> *"Ese fue uno de los desafíos centrales de la transformación en Python realizada por Persona 1. Hasta el proceso de admisión 2021 regía la escala PSU de 150 a 850 puntos; desde 2022 opera la escala PAES de 100 a 1.000 puntos. Si graficáramos los datos crudos, veríamos un salto artificial de casi 150 puntos en 2022 que arruinaría cualquier análisis de tendencia.*
>
> *Para solucionarlo, el DataMart contiene la columna `puntaje_promedio_equiv_paes`, donde toda la serie histórica 2012–2021 fue convertida a la métrica equivalente PAES mediante la tabla de conversión oficial del DEMRE/SIES. Además, en `dim_tiempo_ine_rm` incluimos la columna booleana `es_paes` para que en el Dashboard de Power BI se marque una línea vertical divisoria que advierte visualmente al usuario del cambio de instrumento, asegurando rigor metodológico."*

---

### Pregunta 4: *"¿Qué significa en la práctica que la Tasa de Cobertura Bruta de la RM sea de 86,26% en 2026?"*
**Respuesta técnica del alumno:**
> *"La tasa de cobertura bruta relaciona la **matrícula total de pregrado en la RM (708.758 estudiantes)** con la **población joven de 18 a 24 años estimada por el INE (821.638 jóvenes)**. Que alcance un 86,26% tiene dos lecturas de negocio cruciales:*
>
> *1. **Efecto de atracción interregional:** Significa que Santiago actúa como polo educativo nacional: miles de jóvenes de otras regiones viajan a estudiar a la RM, elevando la matrícula por sobre la cohorte local.*
> *2. **Saturación demográfica estructural:** En economía de la educación superior, cuando la cobertura bruta supera el 80%, el mercado entra en fase de madurez. Las instituciones de la RM ya no pueden basar sus planes de negocios en que 'habrá más jóvenes el próximo año'. Para crecer, las opciones son dos: o le quitan cuota de mercado a otras IES (vía calidad y acreditación), o retienen mejor a sus alumnos evitando la deserción en cursos superiores (`tasa_retencion_aparente_pct`, que en 2026 se situó en 70,61%)."*

---

### Pregunta 5: *"En la dimensión institución tienen datos de acreditación SIES, pero ¿por qué tienen nulos entre 2012 y 2017?"*
**Respuesta técnica del alumno:**
> *"Los registros nulos entre 2012 y 2017 son un **nulo estructural verídico**: la base oficial SIES de acreditación institucional estandarizada comienza su serie pública comparable en 2018. Siguiendo las mejores prácticas de Data Warehousing (`Clase 4 DW`), **no inventamos ni imputamos datos retrospectivos hacia atrás**, porque estaríamos falseando la historia regulatoria de las instituciones (por ejemplo, proyectando acreditaciones actuales a épocas donde ciertas IES no estaban acreditadas).*
>
> *Para respetar la integridad del negocio, en el informe y en las visualizaciones de Power BI que involucran acreditación y posicionamiento competitivo, establecimos como regla explícita acotar el filtro temporal al periodo válido **2018–2026**, mientras que para matrícula y vacantes se utiliza la serie completa **2012–2026**."*

---

### Pregunta 6: *"¿Qué es el Posicionamiento Competitivo RM y para qué le sirve a un rector?"*
**Respuesta técnica del alumno:**
> *"Es una clasificación estratégica en 4 cuadrantes generada en `dim_institucion_sies`, que cruza la **calidad institucional (Acreditación SIES: $\ge$4 años vs. <4 años)** contra la **demanda real del mercado (Tasa de ocupación de vacantes: $\ge$85% vs. <85%)**:*
>
> - *Cuadrante 1: **Líder Acreditada con Alta Demanda** ($\ge$4 años y $\ge$85% ocupación).*
> - *Cuadrante 2: **Acreditada con Capacidad Disponible** ($\ge$4 años y <85% ocupación).*
> - *Cuadrante 3: **En Riesgo de Calidad con Demanda Activa** (<4 años y $\ge$85% ocupación).*
> - *Cuadrante 4: **Crítica: Baja Acreditación y Subocupación** (<4 años y <85% ocupación).*
>
> *A un rector de una IES en el Cuadrante 2 le indica que su cuello de botella no es la calidad sino su estrategia de captación y marketing. En cambio, a un regulador del CNED o la Subsecretaría le permite encender alarmas sobre las 18 instituciones en el Cuadrante 4, donde se combinan baja acreditación y baja captación, señalando inviabilidad financiera o académica."*

---

## 4. Checklist de Preparación Final para Persona 2

- [x] **Cifras de memoria:** 58.926 registros | 69 IES 2026 | 253.018 vacantes | 208.311 matriculados 1er año | 82,3% ocupación | 674 secciones extra | 25,35% absorción juvenil | 86,26% cobertura bruta | 703,6 PAES ponderado.
- [x] **Caso 120 $\to$ 140 alumnos memorizado:** 4 secciones base (140 cupos) $\to$ 85,7% con 120 $\to$ 100% con 140 $\to$ alumno 141 abre 5ta sección (+25% costo fijo).
- [x] **Reglas DAX claras:** `DIVIDE()` para tasas, `SUMX()` para ponderar PAES, nunca `SUM` directo en puntajes ni promedios de tasas.
- [x] **Enfoque geográfico indiscutible:** Todo es Región Metropolitana (`region_codigo_subdere == '13'`), sede física en Santiago.

---

*Guión elaborado para la Persona 2 — Analista de Negocio RM | Entrega Final BI | 18 de Noviembre de 2026*
