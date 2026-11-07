# 📋 Resumen Ejecutivo de Feedback y Reorientación Estratégica (Hito 2)
## Proyecto Final de Business Intelligence — Ingeniería en Negocios

---

> **Objetivo de este documento:**  
> Alinear a todo el equipo de trabajo (Personas 1 a 5) tras la retroalimentación del profesor en el Hito 1, formalizar la reorientación temática hacia la **Región Metropolitana (RM)** y definir las tareas y entregables exactos de cada integrante para el **Hito 2 (Modelo Dimensional y DataMart - 10 Puntos)**.

---

## 1. 🔍 ¿Qué nos dijo el profesor en el Feedback?

El profesor fue sumamente claro y constructivo en tres puntos críticos:

1. **Nuestra propuesta de valor original era demasiado amplia y difusa:**  
   Intentar responder *"la equidad territorial de todo Chile"* abarcando las 16 regiones, todos los niveles y todas las instituciones generaba un análisis superficial. En analítica de negocios, **el valor está en la profundidad de la decisión**, no en la amplitud geográfica abstracta.
2. **Recomendación explícita:**  
   *«Céntrense en una región y aborden un problema real que una institución o autoridad deba resolver»*.
3. **El ejemplo práctico del profesor (¿Qué significa pasar de 120 a 140 matriculados?):**  
   El profesor puso el caso de carreras con alta demanda (como Informática o Ingeniería). Muchos piensan que matricular a 20 alumnos más es simplemente un número, pero para una universidad representa un **quiebre operativo y financiero**:
   * **Tope de infraestructura:** Los laboratorios de computación o ciencias tienen capacidades fijas de **30 a 40 puestos**. Con 120 alumnos se llenan exactamente 3 o 4 secciones. Con **140 alumnos (+20)**, los estudiantes ya no caben físicamente en un aula estándar.
   * **Costos fijos adicionales:** Obliga a abrir un paralelo nuevo completo, contratar nuevos profesores jornada/hora y descalabrar los bloques de horarios.
   * **Impacto en Selectividad y Deserción:** Si la universidad sobrecupa vacantes aceptando alumnos con menores puntajes, aumenta drásticamente el riesgo de reprobación en ramos de primer año (cálculo, programación), lo que deriva en deserción estudiantil y pérdida del arancel/gratuidad en los años siguientes.

---

## 2. 🎯 Nuestra Decisión: Focalización en la Región Metropolitana (RM)

Para capitalizar el feedback docente, el equipo reorientará el proyecto hacia la **Región Metropolitana de Santiago (RM)**:

### ¿Por qué la Región Metropolitana y no otra?
1. **Mayor volumen y calidad de datos:** La RM concentra más del **52% de la matrícula nacional de educación superior** (más de 80.000 registros en la serie consolidada). No sufre los problemas de datos dispersos o campus rurales vacíos.
2. **Ecosistema educativo completo:** Conviven universidades del CRUCH, universidades privadas, institutos profesionales (IP) y centros de formación técnica (CFT), lo que permite contrastar selectividad universitaria vs. matrícula abierta técnica.
3. **Granularidad de fuentes externas:** Tanto el INE (proyecciones demográficas comunales) como el SIES (acreditación, titulación y retención) poseen el más alto nivel de detalle en Santiago.

### Nuevo Título del Proyecto:
> **«Sistema de Inteligencia de Negocios para la Planificación de Capacidad Instalada, Sobredemanda y Selectividad de la Educación Superior en la Región Metropolitana (2012–2026)»**

---

## 3. ❓ Las 3 Nuevas Preguntas de Negocio (Reenfocadas en la RM)

Estas son las tres preguntas que alimentarán el Canvas BI, el DataMart y el Panel final en Power BI:

1. **Pregunta 1 (Presión de Vacantes y Sobredemanda en la RM):**  
   *¿Qué áreas de conocimiento (ej. Tecnología, Salud, Administración) y carreras críticas en la RM presentan tasas de sobreocupación ($\text{Matrícula 1er Año} > \text{Vacantes}$) sistemáticas, y qué esfuerzo de paralelos e infraestructura docente exige a las instituciones?*
2. **Pregunta 2 (Selectividad y Puntajes de Admisión PAES/PSU):**  
   *¿Cómo reaccionan los puntajes de corte y promedios de admisión en la RM ante los picos de sobredemanda? ¿Las instituciones más demandadas elevan sus requisitos de ingreso o relajan la selectividad para capturar matrícula?*
3. **Pregunta 3 (Capacidad Regional y Absorción Juvenil Externa):**  
   *¿La oferta de vacantes de pregrado en la RM es suficiente para absorber a la población en edad típica de ingreso (18-24 años, según proyecciones INE), o se detecta saturación frente a instituciones con baja acreditación institucional (SIES)?*

---

## 4. 📊 ¿Qué exige la Pauta Oficial para el Hito 2? (10 Puntos)

El Hito 2 es estrictamente técnico y de modelado dimensional. La pauta califica dos entregables:

| Criterio | Puntos | Requisito Formal de la Pauta |
| :--- | :---: | :--- |
| **Modelo Dimensional** | **6 pts** | Diagrama formal (Estrella/Copo de nieve), declaración explícita del grano de cada tabla de hechos, aditividad de medidas y justificación del cambio en el tiempo (SCD Tipo 2). |
| **DataMart Físico y Cuadre** | **4 pts** | Motor de base de datos relacional implementado, scripts DDL (`CREATE TABLE`), pipeline de carga y **certificación matemática de cuadre de registros contra la fuente**. |

---

## 5. 👥 Asignación de Tareas por Rol para el Hito 2

Para asegurar una calificación sobresaliente y que todos tengan insumos para trabajar, esta es la distribución de responsabilidades:

```text
                                 [HITO 2: WORKFLOW DEL EQUIPO]
                                 
   Persona 2 (Negocio)           Persona 3 (Arquitecto)          Persona 1 (Tú - Ing. Datos)
   Rediseña Canvas RM     ──►    Diseña Diagrama Estrella  ──►   Ejecuta carga física al DataMart
   Ajusta 3 Preguntas            Declara Grano y DDL SQL         Certifica Cuadre (Cero pérdidas)
           │                                │                                │
           ▼                                ▼                                ▼
   Persona 5 (Documentador) ◄─────────────────────────────────   Persona 4 (Dev Power BI)
   Documenta Aditividad y SCD Tipo 2                             Conecta Power BI al DataMart
   Compila Informe LaTeX Hito 2                                  Modela Jerarquías y Medidas DAX
```

### 🔹 Persona 1: Ingeniero de Datos (ETL y DataMart) — *Tu Rol*
1. **Auditoría de consistencia de la base limpia:** Validar tipos de datos y nulos para la inserción relacional.
2. **Implementación física del DataMart:** Configurar el motor relacional (SQLite / DuckDB / PostgreSQL) para que el equipo no dependa de archivos planos.
3. **Pipeline de Carga Masiva:** Script en Python que puebla automáticamente las tablas de dimensiones y la tabla de hechos a partir de la base consolidada (158.211 registros).
4. **Certificación de Cuadre de Registros (Exigencia Pauta):** Generar el reporte automatizado que demuestre que el total de filas, la suma de matrículas y los promedios de puntaje en el DataMart coinciden exactamente con la fuente original (0 registros duplicados, 0 registros perdidos).
5. **Vistas de la Región Metropolitana:** Crear vistas SQL optimizadas (`vw_rm_analisis_capacidad`) para que Power BI cargue velozmente.

### 🔹 Persona 2: Analista de Negocio y Fuentes Externas
1. Rediseñar el **Canvas BI de 10 bloques** enfocándolo en la Región Metropolitana.
2. Formalizar las 3 preguntas de negocio descritas en la sección 3.
3. Asegurar que las fuentes externas (Población INE RM y Acreditación SIES) tengan las llaves listas para integrarse como dimensiones complementarias en el modelo.

### 🔹 Persona 3: Arquitecto de Bases de Datos
1. Dibujar el **Diagrama del Modelo Dimensional (Esquema Estrella)** identificando dimensiones (`Dim_Tiempo`, `Dim_Institucion`, `Dim_Sede_Comuna`, `Dim_Carrera_Programa`, `Dim_Area_Conocimiento`) y la tabla de hechos (`Fact_Matricula_Admision`).
2. Declarar el **Grano formal** (ej. *«Una fila por cada programa académico, en una sede y horario específico, reportado en un año cronológico determinado»*).
3. Redactar los scripts DDL (`CREATE TABLE`) con tipos de datos, llaves primarias (`PK`) y foráneas (`FK`).

### 🔹 Persona 4: Desarrollador BI
1. Configurar la conexión directa en Power BI Desktop apuntando al motor del DataMart (cumpliendo la regla: *«Conectado al DataMart, no al Excel»*).
2. Configurar las relaciones y jerarquías dimensionales (`Tiempo: Año`, `Geografía: Región > Comuna > Sede`, `Académica: Área > Carrera > Programa`).
3. Crear el borrador de medidas DAX preliminares (Tasa de ocupación de vacantes, ratio de género, puntaje equivalente promedio).

### 🔹 Persona 5: Gestor del Proyecto y Documentador
1. Documentar técnicamente la **aditividad de las medidas**:
   * Matrícula y vacantes son **completamente aditivas** (se pueden sumar a través de todas las dimensiones).
   * Los puntajes de admisión son **no aditivos** (son promedios; sumarlos destruye el significado matemático y deben agregarse con promedios ponderados en DAX).
2. Justificar la estrategia de **cambio en el tiempo (Slowly Changing Dimensions - SCD Tipo 2)**:
   * Demostrar cómo atributos mutables como los años de *Acreditación Institucional* y la política de *Gratuidad* cambian en el tiempo para una misma institución sin sobreescribir la historia.
3. Compilar el informe técnico del Hito 2 en formato LaTeX.

---

> 💡 **Nota para el equipo:**  
> Este documento resume el plan acordado. La carpeta `Avance Hito 2/` contiene toda la estructura modular ordenada lista para comenzar el desarrollo técnico.
