# 🎓 Guía Maestra de Estudio y Defensa Oral Individual (15 Puntos)
## Rol Evaluado: Persona 3 — Arquitecto de Datos y Modelador Dimensional
**Estudiante:** **Angel Pino**  
**Asignatura:** Business Intelligence | **Carrera:** Ingeniería en Negocios  
**Hito Evaluado:** Hito 2 (Modelo Dimensional y DataMart) y Preparación Examen Final  
**Ponderación Defensa Oral:** 15 Puntos Individuales (Escala Pauta Oficial: 15 pts Respuesta correcta y fundamentada, 8 pts incompleta, 0-3 pts incorrecta)

---

## 🎯 Instrucciones de Dominio Escénico para Angel Pino

En la defensa oral individual, el profesor sorteará una pregunta para cada integrante del equipo. Como **Persona 3 (Arquitecto de Datos)**, tu fortaleza es **el diseño conceptual, el grano, el Esquema Estrella, el tratamiento de SCD Tipo 2 y la integridad referencial**.

### Regla de Oro al Responder:
1. **Seguridad y Brevedad (60 a 90 segundos):** Da primero la respuesta conceptual directa y luego cita la evidencia técnica concreta de tu implementación en el DataMart.
2. **Usa Terminología Kimball:** "Desnormalización controlada", "grano atómico", "claves subrogadas (Surrogate Keys)", "aditividad de medidas", "motor VertiPaq en memoria", "cero registros huérfanos".
3. **Conecta con el Problema de Negocio de la RM:** Siempre menciona el feedback docente del caso de los 20 alumnos (120 a 140 matriculados en laboratorios de 30-40 puestos) para justificar por qué diseñaste el modelo a ese nivel de granularidad.

---

## 📚 Banco de Preguntas Docentes Simuladas y Respuestas Modelo

### Pregunta 1: ¿Por qué diseñó un Esquema Estrella y no un Esquema Copo de Nieve (Snowflake)?
> **Respuesta Modelo:**  
> «Profesor, la decisión entre Estrella y Copo de Nieve es el núcleo del diseño analítico. Opté por un **Esquema Estrella Puro** siguiendo la metodología de Ralph Kimball y las características del motor tabular VertiPaq de Power BI.  
> En un esquema copo de nieve, jerarquías como *País $\rightarrow$ Región $\rightarrow$ Comuna $\rightarrow$ Sede* se normalizan en sub-tablas separadas, lo que obliga al motor de base de datos a ejecutar múltiples JOINs en cascada sobre las 158.211 filas de hechos, ralentizando las consultas y complejizando el código DAX.  
> En cambio, en nuestro Esquema Estrella desnormalizamos las jerarquías en tablas dimensionales únicas: `dim_sede_geografia` (116 filas) y `dim_carrera_programa` (15.650 filas). Esto permite relaciones directas de 1 a N hacia la tabla central `fact_matricula_admision`, reduciendo los tiempos de respuesta a menos de 25 milisegundos y eliminando ambigüedades en el filtrado cruzado».

---

### Pregunta 2: ¿Cuál es el grano formal de la tabla de hechos y por qué no usó un grano más agregado?
> **Respuesta Modelo:**  
> «El grano formal declarado de `fact_matricula_admision` es:  
> **"Una fila por cada oferta de programa académico, sede física y régimen horario, reportada por una institución en un año cronológico determinado en las bases INDICES del CNED"**.  
> No utilicé un grano más agregado (como institución por año o carrera genérica) porque destruiría el valor del proyecto para responder a la pregunta de negocio central que usted nos planteó:  
> **El caso de los 20 alumnos y la capacidad instalada en la Región Metropolitana**.  
> El quiebre operativo que ocurre cuando una carrera pasa de 120 a 140 alumnos satura los laboratorios de computación o ciencias (que tienen capacidades fijas de 30 a 40 puestos). Este fenómeno ocurre en una **sede física concreta** y en un **turno específico** (diurno). Si hubiésemos agregado los datos, la sobredemanda de vacantes y la variación de los puntajes de corte se habrían disuelto en promedios globales, haciendo invisible el quiebre de infraestructura».

---

### Pregunta 3: ¿Por qué hay más filas en la tabla de hechos que combinaciones únicas de institución, carrera, sede y año?
> **Respuesta Modelo:**  
> «Excelente observación, profesor. En las 158.211 filas de la base oficial del CNED, detectamos que en 4.410 casos una misma institución ofrece dos o más variantes para un mismo programa en la misma sede y año.  
> Esto ocurre porque las casas de estudio reportan **diferentes vías de ingreso o planes curriculares paralelos** (por ejemplo, el Plan Regular de 12 semestres con cupos ordinarios vía prueba versus planes de continuidad de estudios o programas para trabajadores).  
> Como Arquitecto de Datos, decidí utilizar una clave primaria subrogada atómica (`id_fact INTEGER PRIMARY KEY`) para preservar cada una de las ofertas oficiales sin colapsar ni sumar indebidamente registros que tienen vacantes y puntajes de corte diferenciados. De esta forma aseguramos un cuadre perfecto de 158.211 filas con cero pérdida de datos».

---

### Pregunta 4: ¿Cómo modeló que la Acreditación Institucional, la Gratuidad y la Autonomía cambien en el tiempo?
> **Respuesta Modelo:**  
> «Lo modelé implementando una **Dimensión de Cambio Lento Tipo 2 (SCD Tipo 2)** en `dim_institucion`.  
> En lugar de sobreescribir el estado actual (que sería un SCD Tipo 1), creé una clave subrogada anual llamada `id_institucion_sk` vinculada al campo `ano_vigencia`, generando 1.994 registros que representan la fotografía histórica exacta de cada institución en cada año entre 2012 y 2026.  
> Si hubiésemos usado SCD Tipo 1, habríamos cometido un **grave error anacrónico**: a una universidad que se adscribió a la gratuidad en 2018 y obtuvo acreditación en 2016, el panel le atribuiría gratuidad en 2012, falsificando el impacto real de la política pública. Con SCD Tipo 2, cada matrícula del hecho se une a la situación regulatoria exacta de la universidad en ese año».

---

### Pregunta 5: ¿Por qué descartó modelar la Acreditación como una Mini-Dimensión o como atributo en la tabla de hechos?
> **Respuesta Modelo:**  
> «Evalué rigurosamente las tres alternativas que permite la pauta:  
> 1. **Atributo en la tabla de hechos:** Lo descarté porque saturaría las 158.211 filas con cadenas de texto redundantes ('Acreditada', 'No Acreditada') y desvincularía la acreditación de la dimensión institucional.  
> 2. **Mini-dimensión:** La teoría de Kimball indica que las mini-dimensiones se justifican cuando se tienen millones de filas y atributos que cambian continuamente a lo largo del año (como perfiles de clientes bancarios). En educación superior chilena, las instituciones son 259 entidades jurídicas y sus resoluciones de acreditación se actualizan con frecuencia estrictamente anual.  
> Crear una mini-dimensión habría introducido una tabla intermedia innecesaria sin aportar ningún beneficio de rendimiento. El SCD Tipo 2 anual en `dim_institucion` es la solución metodológicamente más limpia y elegante».

---

### Pregunta 6: ¿Cuáles medidas de la tabla de hechos son aditivas y cuáles no? ¿Cómo deben tratarse en DAX?
> **Respuesta Modelo:**  
> «Clasifiqué las medidas bajo las tres categorías de Ralph Kimball:  
> 1. **Completamente Aditivas:** `vacantes`, `matricula_primer_ano_total`, `matricula_total` y desgloses por género y extranjeros. Son magnitudes acumulativas y se pueden sumar válidamente con `SUM()` a través de cualquier dimensión (Tiempo, Sede, Institución, Carrera).  
> 2. **Estrictamente No Aditivas:** Los puntajes psicométricos (`puntaje_promedio_equiv_paes`, cortes de primer y último matriculado). Sumar puntajes de diferentes carreras es un disparate estadístico. En Power BI Desktop, especifiqué que se deben agregar mediante **promedios ponderados por matrícula de primer año** usando `SUMX()` dividido por el total de alumnos.  
> 3. **Semi-Aditivas / Ratios:** La tasa de ocupación ($\% = \frac{\text{Matrícula}}{\text{Vacantes}} \times 100$). En visualizaciones agrupadas no se deben promediar los porcentajes; se recalculan dinámicamente en DAX mediante la función `DIVIDE([Total Matricula], [Total Vacantes])`».

---

### Pregunta 7: ¿Cómo comprobó que no hay registros huérfanos entre la tabla de hechos y las dimensiones?
> **Respuesta Modelo:**  
> «Desarrollé y ejecuté un script de auditoría automatizada en Python (`audit_architecture_and_integrity_p3.py`) que ejecuta consultas `LEFT JOIN` entre `fact_matricula_admision` y cada una de las dimensiones (`dim_tiempo`, `dim_sede_geografia`, `dim_institucion`, `dim_carrera_programa` y `dim_poblacion_rm`), filtrando por `WHERE dimension.id IS NULL`.  
> El resultado arrojó **estrictamente cero registros huérfanos** en las 158.211 filas (100% de integridad referencial). Esto garantiza que el panel Power BI nunca mostrará valores en blanco ni categorías huérfanas en los segmentadores».

---

### Pregunta 8: ¿Qué índices relacionales creó en el DataMart y qué impacto tienen en Power BI?
> **Respuesta Modelo:**  
> «Construí índices B-Tree específicos en la tabla de hechos para cada una de las cuatro claves foráneas: `idx_fact_tiempo`, `idx_fact_geografia`, `idx_fact_institucion` y `idx_fact_carrera`, además de un índice de filtrado regional `idx_fact_rm`.  
> En las pruebas de benchmark que incluí en el reporte, las consultas típicas enviadas por Power BI (como filtrar por año y región metropolitana o cruzar institución por área de conocimiento) pasaron de requerir un Table Scan completo a ejecutarse en **menos de 22 milisegundos**. Esto asegura que las transiciones visuales en el panel interactivo sean instantáneas».

---

### Pregunta 9: ¿Cómo se integró la fuente externa demográfica del INE en la arquitectura?
> **Respuesta Modelo:**  
> «Diseñé la tabla dimensional complementaria `dim_poblacion_rm`, cargando las proyecciones oficiales del Censo 2017 del INE acotadas a la Región Metropolitana (34 filas, 2002–2035).  
> Su clave primaria es el año (`ano`), que se vincula directamente con `dim_tiempo.id_tiempo`.  
> Esta tabla aporta la población de 15 a 64 años y el proxy documentado del tramo 18 a 24 años (14% de dicho grupo). Gracias a esta dimensión, el equipo puede responder a la **Pregunta de Negocio 3**, contrastando la oferta total de vacantes en Santiago contra el universo real de jóvenes en edad de ingresar a la educación superior».

---

### Pregunta 10: ¿Cuál fue su rol específico como Persona 3 en relación con Persona 1 (Ingeniero de Datos) y Persona 4 (Power BI)?
> **Respuesta Modelo:**  
> «Mi rol como Persona 3 (Arquitecto de Datos) fue diseñar el **contrato conceptual, lógico y físico** del sistema:  
> - Definí el Esquema Estrella, el grano formal atómico, los tipos de datos estrictos, las claves primarias y foráneas, y redacté el script DDL canónico `schema_dimensional_star.sql`.  
> - Con **Persona 1 (Ingeniero de Datos)**, coordiné la carga masiva física en el motor SQLite asegurando que las claves subrogadas cumplieran las restricciones de unicidad y cuadre exacto de 158.211 filas.  
> - Con **Persona 4 (Desarrollador BI)**, le entregué las jerarquías dimensionales pre-calculadas, los índices para consultas rápidas, las vistas analíticas especializadas de la RM y las reglas matemáticas de aditividad para que sus medidas DAX y paneles no presenten errores de agregación».

---

## 💡 Consejos Finales para la Exposición Oral
- Si te preguntan sobre números globales de la base:  
  * Total nacional: **158.211 filas** (2012–2026).
  * Subconjunto RM: **58.926 ofertas / 82.348 registros totales**.
  * Matrícula 1er Año Total: **5.186.123 alumnos**.
  * Vacantes Nacionales: **5.914.165 cupos**.
  * Registros huérfanos: **0**.
- Habla con aplomo y orgullo técnico: este modelo dimensional cumple con el 100% de la pauta y los estándares de ingeniería de datos de la industria.
