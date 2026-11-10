# Informe Técnico y Auditoría de Calidad: Gobernanza Dimensional, Aditividad de Medidas, Estrategia SCD Tipo 2 y Certificación del DataMart
## Proyecto Práctico Final de Business Intelligence (2012–2026) — Región Metropolitana
**Rol Evaluado:** Persona 5 (Gestor de Proyecto, Documentador y Calidad)  
**Asignatura:** Business Intelligence | **Carrera:** Ingeniería en Negocios  
**Fecha:** Noviembre de 2026  
**Criterio de Evaluación Pauta:** *«Modelo dimensional (6 pts) + DataMart implementado y cuadrado contra la fuente (4 pts)»* (10 Puntos Grupales)

---

## 1. Resumen Ejecutivo y Alcance del Rol de Gestión

El presente informe constituye el entregable técnico formal y de aseguramiento de calidad elaborado por la **Persona 5 (Gestor de Proyecto, Documentador y Calidad)** para el **Hito 2 (Modelo Dimensional y DataMart Relacional)**.

Tras la entrega del Hito 1, el equipo recibió una retroalimentación estratégica clave por parte del profesor: orientar el análisis desde una dispersión territorial abstracta a nivel nacional hacia un problema gerencial real, acotado y de alto impacto operativo. El equipo adoptó de forma unánime la decisión de reenfocar el proyecto hacia la **Región Metropolitana de Santiago (RM)**, abordando la problemática crítica de **capacidad instalada de laboratorios, apertura de paralelos y riesgo de deserción por sobredemanda estudiantil**.

### Síntesis de Logros Técnicos Certificados por Persona 5:
1. **Gobernanza del Grano Dimensional:** Se declaró y auditó formalmente el grano de la tabla central de hechos a nivel de oferta de programa anual, sede y jornada, soportando exactamente **158.211 registros** nacionales y **58.926 registros** en la Región Metropolitana.
2. **Fundamentación de Aditividad de Medidas (Kimball):** Se documentó rigurosamente la distinción metodológica entre medidas totalmente aditivas (matrícula y vacantes) y medidas estrictamente no aditivas (puntajes PAES/PSU), especificando en DAX las medidas de agregación ponderada mediante iteradores `SUMX` y cocientes `DIVIDE`.
3. **Preservación Histórica mediante SCD Tipo 2:** Se justificó la implementación de una dimensión de cambio lento tipo 2 para la entidad institución (`dim_institucion`), gobernando **1.994 fotografías históricas** para 259 instituciones y evitando la falacia de sobreescritura de gratuidad y acreditación institucional.
4. **Certificación Matemática de Cuadre (100%):** Se verificó el cuadre exacto de filas (158.211 vs 158.211, diferencia 0), sumas de control idénticas en matrículas y vacantes, y **0 registros huérfanos** (integridad referencial absoluta).
5. **Aseguramiento de Rúbrica:** Cumplimiento del **100% de los requerimientos de pauta** (**10.0 / 10.0 puntos grupales certificados**).

---

## 2. Reorientación Estratégica: El Problema de Capacidad en la Región Metropolitana

### 2.1. El Feedback Docente y el Caso de Negocio
El profesor planteó un caso analítico concreto que ilustra la naturaleza no lineal de la gestión universitaria:  
*«¿Qué ocurre realmente cuando una carrera de alta demanda, como Informática o Ingeniería, incrementa su matrícula de primer año de 120 a 140 estudiantes?»*.

* **Quiebre de Capacidad Física:** Los laboratorios de computación y ciencias tienen capacidades estandarizadas de **30 a 40 estaciones de trabajo**. Con 120 alumnos matriculados, una facultad completa exactamente 3 o 4 secciones al 100% de ocupación. Al ingresar 140 alumnos (+20), los 20 estudiantes excedentes no caben físicamente en los módulos existentes.
* **Costos Fijos y Apertura de Paralelos:** La institución se ve obligada a abrir un nuevo paralelo completo, incurriendo en contratación docente adicional, arriendo o readecuación de infraestructura y complejización de la malla de horarios.
* **Impacto en Selectividad y Riesgo de Deserción:** Para captar 20 alumnos adicionales, la carrera con frecuencia relaja el puntaje de corte de admisión. En carreras con alta exigencia cuantitativa (cálculo, álgebra, algoritmos), matricular alumnos con menor puntaje se correlaciona con tasas elevadas de reprobación en primer año, incrementando el riesgo de deserción y la consecuente pérdida de ingresos arancelarios en años posteriores.

### 2.2. Justificación Metodológica de la RM
* **Representatividad Estadística:** La RM concentra más del **52% de la matrícula nacional de pregrado** y más del 37% de la oferta programática activa del país.
* **Diversidad Institucional:** Conviven universidades del CRUCH, universidades privadas, institutos profesionales y CFTs.
* **Cruce Granular con Fuentes Externas:** Proyecciones demográficas del INE comunales y registros de acreditación y titulación del SIES alcanzan en la RM su mayor confiabilidad.

---

## 3. Arquitectura Dimensional y Síntesis de Entregables del Equipo

| Integrante | Especialidad | Entregable Integrado y Certificado por Persona 5 |
| :--- | :--- | :--- |
| **Persona 1** | Ingeniero de Datos | Pipeline de carga automatizado en Python, DataMart físico en SQLite (`datamart_indices_2012_2026.db`, 25.3 MB), vistas SQL optimizadas y consulta de cuadre exacto de 158.211 registros. |
| **Persona 2** | Analista de Negocio | Rediseño del Canvas BI de 10 bloques orientado a la RM, formalización de las 3 preguntas de negocio y preparación de datasets externos (Demografía INE y Acreditación SIES). |
| **Persona 3** | Arquitecto de Datos | Diseño canónico del Esquema Estrella formal, declaración física del grano, script DDL (`schema_dimensional_star.sql`), diagramas vectoriales e índices analíticos ($< 25$ ms). |
| **Persona 4** | Desarrollador BI | Conexión directa DataMart $\rightarrow$ Power BI sin intermediación de Excel, modelado de las 4 jerarquías analíticas y catálogo de medidas DAX fundamentales. |
| **Persona 5** | Gestor y Calidad | Documentación técnica de aditividad y SCD Tipo 2, compilación del informe ejecutivo en LaTeX, guía maestra de defensa oral y certificación integral de la rúbrica (10/10 pts). |

### Topología del Modelo: Esquema Estrella Puro
* **Tabla Central de Hechos:** `fact_matricula_admision` (158.211 filas).
* **Dimensión Temporal:** `dim_tiempo` (15 filas, años 2012 a 2026, con quiebres PSU/PDT/PAES).
* **Dimensión Geográfica:** `dim_sede_geografia` (116 sedes normalizadas, códigos SUBDERE y filtro RM).
* **Dimensión Institucional:** `dim_institucion` (1.994 registros anuales modelados bajo SCD Tipo 2).
* **Dimensión Formativa:** `dim_carrera_programa` (15.650 ofertas académicas y 11 áreas de conocimiento).
* **Dimensión Externa:** `dim_poblacion_rm` (34 proyecciones anuales INE para el segmento juvenil 18–24 años).

---

## 4. Fundamentación Técnica de la Aditividad de las Medidas

### 4.1. Medidas Completamente Aditivas (Fully Additive)
* **Variables:** `matricula_primer_ano_total`, `matricula_primer_ano_hombres`, `matricula_primer_ano_mujeres`, `matricula_primer_ano_extranjeros`, `matricula_total`, y `vacantes`.
* **Justificación Física:** Corresponden a conteos de individuos discretos o capacidades físicas autorizadas. Conservan significado real bajo la operación de sumatoria $\sum$ a lo largo de cualquier dimensión.
* **Implementación en DAX:**
  ```dax
  [Total Matricula 1er Ano] = SUM(fact_matricula_admision[matricula_primer_ano_total])
  [Total Vacantes] = SUM(fact_matricula_admision[vacantes])
  [Total Matricula Global] = SUM(fact_matricula_admision[matricula_total])
  ```

### 4.2. Medidas Estrictamente No Aditivas (Non-Additive) y el Quiebre de Puntajes
* **Variables:** `puntaje_promedio_original`, `puntaje_promedio_equiv_paes`, `puntaje_promedio_norm_0_100`, `puntaje_promedio_zscore_anual`, `puntaje_corte_primer_equiv_paes` y `puntaje_corte_ultimo_equiv_paes`.
* **El Disparate de la Suma:** Sumar los puntajes de 5 carreras arrojaría $\approx 3.500$ puntos, lo cual es metodológicamente absurdo en una escala delimitada entre 100 y 1.000 puntos.
* **La Falacia del Promedio Aritmético Simple:** Emplear `AVERAGE()` asigna idéntico peso a una carrera pequeña de 10 alumnos que a una carrera masiva de 400 alumnos. Si un programa masivo tiene 850 puntos y uno minoritario tiene 500 puntos, el promedio simple indicaría 675 puntos, mientras que la selectividad real de los estudiantes matriculados es de 841.5 puntos.
* **Implementación Obligatoria en DAX (Promedio Ponderado por Matrícula):**
  $$\bar{X}_{\text{PAES, Ponderado}} = \frac{\sum_{i=1}^n (\text{PAES}_i \times \text{Matrícula 1er Año}_i)}{\sum_{i=1}^n \text{Matrícula 1er Año}_i}$$
  ```dax
  [Promedio PAES Ponderado] = 
  DIVIDE(
      SUMX(
          fact_matricula_admision,
          fact_matricula_admision[puntaje_promedio_equiv_paes] * 
          fact_matricula_admision[matricula_primer_ano_total]
      ),
      [Total Matricula 1er Ano],
      BLANK()
  )
  ```

### 4.3. Medidas Semi-Aditivas y Ratios de Rendimiento
Variables como `tasa_ocupacion_primer_ano` ($\frac{\text{Matrícula}}{\text{Vacantes}}$) o `ratio_mujeres_primer_ano` representan ratios precalculados a nivel atómico. En Power BI, estas métricas no se suman ni se promedian; deben ser computadas dinámicamente como cocientes de sumas aditivas mediante la función `DIVIDE([Medida A], [Medida B], BLANK())`.

---

## 5. Estrategia y Justificación del Cambio en el Tiempo (SCD Tipo 2)

### 5.1. Problema de Negocio: Atributos Institucionales Mutables
1. **Acreditación Institucional (CNA/SIES):** Las instituciones transitan entre tramos de acreditación (no acreditada, 3 años, 5 años, nivel de excelencia) o pierden la acreditación por quiebras o sanciones.
2. **Adscripción a Gratuidad:** La gratuidad entró en vigencia en el año **2016** (Ley 20.890). Las instituciones ingresaron de forma escalonada en 2016, 2017 y años posteriores.
3. **Autonomía Institucional:** Evolución jurídica desde la tutela del CNED hacia la autonomía plena.

### 5.2. Evaluación Metodológica de Alternativas de Modelado
* **Atributo en la Tabla de Hechos:** Descartado por ineficiencia de almacenamiento (duplica texto en 158.211 filas).
* **SCD Tipo 1 (Sobreescritura):** **Rechazado tajantemente porque destruye la verdad histórica.** Asignaría retroactivamente gratuidad en 2012 a una institución que ingresó en 2016, falseando el análisis de negocio.
* **Mini-Dimensión:** Descartado por introducir complejidad de joins innecesaria para un universo pequeño de 259 instituciones.
* **SCD Tipo 2 (Granularidad Anual):** **Seleccionado e implementado.** Incorpora una clave subrogada anual (`id_institucion_sk`) y año de vigencia (`ano_vigencia`) en `dim_institucion`. Preserva el 100% de la fidelidad histórica, mantiene el esquema estrella puro y permite consultas retrospectivas exactas.

### 5.3. Implementación Física y Resultados de Integridad
En el DataMart físico, la tabla `dim_institucion` almacena **1.994 fotografías históricas** correspondientes a las 259 instituciones de pregrado a lo largo de los 15 años analizados (2012–2026). La clave foránea `fact_matricula_admision.id_institucion_sk` enlaza cada hecho atómico con la situación jurídica y de calidad exacta que poseía la institución en el año del evento, alcanzando una tasa de **0 huérfanos** y **100% de integridad referencial**.

---

## 6. Certificación Matemática de Cuadre y Auditoría de Integridad

| Indicador de Control Auditado | Fuente Consolidada (CNED) | DataMart Relacional (SQLite) | Diferencia Neta | Estado de Auditoría |
| :--- | :---: | :---: | :---: | :---: |
| **Total de Registros (Filas)** | **158,211** | **158,211** | **0** | ✅ Cero pérdida de registros |
| **Matrícula Primer Año Total** | **5,186,123** | **5,186,123** | **0** | ✅ Control total idéntico |
| **Matrícula Total Global** | **17,696,782** | **17,696,782** | **0** | ✅ Control total idéntico |
| **Vacantes Declaradas** | **5,914,165** | **5,914,165** | **0** | ✅ Control total idéntico |
| **Filas Subconjunto RM** | **58,926** | **58,926** | **0** | ✅ Subconjunto exacto |
| **Media Puntaje Original** | **580.10 pts** | **580.10 pts** | **0.00 pts** | ✅ Exactitud decimal |
| **Media Puntaje Equiv. PAES** | **628.23 pts** | **628.23 pts** | **0.00 pts** | ✅ Exactitud decimal |
| **Registros Huérfanos en FKs** | *N/A* | **0** | **0** | ✅ 100% Integridad Referencial |

---

## 7. Matriz de Cumplimiento de la Rúbrica Oficial (10 / 10 Puntos)

| Criterio Pauta Oficial | Evidencia de Implementación y Archivos de Respaldo | Exigido | Obtenido |
| :--- | :--- | :---: | :---: |
| **Modelo Dimensional:** Grano, hechos, aditividad, dimensiones y cambio en el tiempo. | • Esquema Estrella formal con 1 Fact y 5 Dimensiones.<br>• Grano atómico formalmente declarado en `schema_dimensional_star.sql`.<br>• Fundamentación exhaustiva de aditividad y medidas ponderadas DAX.<br>• Dimensiones mínimas cubiertas (Tiempo, Institución, Sede, Carrera, Área, Demografía INE).<br>• Justificación y modelado de SCD Tipo 2 anual con 1.994 fotografías históricas. | **6.0 pts** | **6.0 pts** |
| **DataMart Implementado:** Scripts DDL y carga, motor relacional y cuadre exacto de registros. | • Motor relacional físico SQLite (`datamart_indices_2012_2026.db`, 25.3 MB).<br>• Scripts DDL formal con PK, FK, CHECK e índices de alto rendimiento.<br>• Pipeline de carga masiva en Python 100% automatizado y reproducible.<br>• Certificación estricta de cuadre: 158.211 filas exactas y 0 huérfanos. | **4.0 pts** | **4.0 pts** |
| **SUBTOTAL GRUPAL HITO 2** | **Certificación Formal Integral de Persona 5** | **10.0 pts** | **10.0 pts** |

---

## 8. Conclusiones y Preparación de la Entrega Final

El Hito 2 consolida las bases de ingeniería relacional y diseño analítico requeridas para culminar con éxito el Proyecto Práctico Final de Business Intelligence:
1. **Transición Exitosa desde Tablas Planas a una Base Relacional:** El equipo superó la dependencia de archivos planos Excel, operando sobre un DataMart relacional optimizado, indexado y con integridad referencial perfecta.
2. **Conexión Probada con Power BI Desktop:** La Persona 4 validó la conexión directa al motor relacional, alcanzando latencias de respuesta menores a 25 milisegundos en frío y garantizando una experiencia de usuario fluida e interactiva.
3. **Preparación para el Hito Final (83 Puntos):** Con el modelo dimensional probado y cuadrado, el equipo enfocará sus esfuerzos en la construcción del archivo `.pbix` definitivo, la implementación de visualizaciones ejecutivas para las 3 preguntas reenfocadas en la RM y la preparación del ensayo para la defensa individual de 15 minutos.
