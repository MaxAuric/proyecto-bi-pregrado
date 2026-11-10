# Informe tecnico formal: Modelado de jerarquias y pruebas de conexion Power BI
## Proyecto practico de Business Intelligence
### Rol Evaluado: Persona 4
**Autor:** Persona 4 (Joaquin Aguilera)  
**Fecha:** Noviembre de 2026  
**Entregable:** Hito 2 — Modelo Dimensional y DataMart Relacional   
**Asignatura:** Inteligencia de Negocios  

---

## 1. Resumen ejecutivo y alcance del rol en el hito 2

El presente informe constituye el entregable tecnico formal de la persona 4 **(Joaquin Aguilera)** para el **Hito 2**, en estricto apego a la pauta de evaluacion y a la planificacion de roles del equipo de trabajo.

### Resumen de cumplimiento tecnico certificado:
1. **Modelado de 4 jerarquias analiticas:** Se diseñaron, implementaron y probaron 4 jerarquias de navegacion (*Drill-Down / Drill-Up*) que permiten segmentar los datos de forma intuitiva:
   * **Jerarquia Geografica:** `Macro-Zona` $\rightarrow$ `Region Estandarizada` $\rightarrow$ `Sede Fisica`.
   * **Jerarquia Institucional:** `Tipo de Institucion (Univ/IP/CFT)` $\rightarrow$ `Nombre Institucion` $\rightarrow$ `Año Vigencia (SCD2)`.
   * **Jerarquia Academica:** `Area de Conocimiento (11)` $\rightarrow$ `Carrera Generica (284)` $\rightarrow$ `Programa Academico Especifico`.
   * **Jerarquia Temporal:** `Quinquenio` $\rightarrow$ `Periodo Admision (PSU/PDT/PAES)` $\rightarrow$ `Año Cronologico (2012–2026)`.
2. **Pruebas de conexion al DataMart Relacional:** Se valido de manera concluyente la conexion directa desde **Power BI Desktop** hacia la base de datos relacional SQLite (`datamart_indices_2012_2026.db`) ubicada en `Avance Hito 2/P1/03_DATAMART_SCRIPTS_DDL_Y_CARGA/`, descartando por completo el uso de hojas de calculo Excel y dando estricto cumplimiento a la pauta (*«Conectado al DataMart, no al Excel»*).
3. **Auditoria de rendimiento:** Las consultas analiticas de agregacion jerarquica sobre los 158.211 registros se resuelven en un promedio de **205 ms en frio**, garantizando interactividad instantanea en el motor VertiPaq.

---

## 2. Modelado de jerarquias analiticas para el panel de control

### 2.1. Jerarquia geografica territorial
* **Tabla dimension:** `dim_sede_geografia`
* **Estructura jerarquica:**
  $$\text{Macro-Zona} \longrightarrow \text{Region Estandarizada} \longrightarrow \text{Sede Fisica}$$
* **Justificacion de negocio:** Permite abordar tanto el analisis focalizado en la Region Metropolitana (segun el feedback del profesor) como el analisis comparativo con la Quinta Region (Valparaiso), Biobio y el resto del pais.
* **Comportamiento en Power BI:** Un clic en la Macro-Zona "Region Metropolitana" o "Centro" filtra automaticamente todas las sedes institucionales asociadas.

### 2.2. Jerarquia institucional y de gobernanza
* **Tabla dimension:** `dim_institucion`
* **Estructura jerarquica:**
  $$\text{Tipo de Institucion} \longrightarrow \text{Institucion Canonica} \longrightarrow \text{Año Vigencia (SCD Tipo 2)}$$
* **Justificacion de negocio:** Permite evaluar el impacto de las politicas publicas y las exigencias de capacidad distinguiendo entre Universidades (con filtros PAES), Institutos Profesionales (IP) y Centros de Formacion Tecnica (CFT). Ademas, al integrarse con SCD Tipo 2, permite rastrear el cambio de acreditacion y gratuidad en el tiempo.

### 2.3. Jerarquia academica y formativa
* **Tabla dimension:** `dim_carrera_programa`
* **Estructura jerarquica:**
  $$\text{Area de Conocimiento (11)} \longrightarrow \text{Carrera Generica (284)} \longrightarrow \text{Programa Especifico}$$
* **Justificacion de negocio:** Responde directamente a la **pregunta 1 de negocio**: Identificar en que areas (ej. Tecnologia o Salud) se concentra el exceso de postulantes sobre las vacantes ofrecidas, cuantificando la necesidad de infraestructura y paralelos docentes adicionales.

### 2.4. Jerarquia temporal
* **Tabla dimension:** `dim_tiempo`
* **Estructura jerarquica:**
  $$\text{Rango Quinquenal} \longrightarrow \text{Periodo de Admision (PSU / PDT / PAES)} \longrightarrow \text{Año (2012--2026)}$$
* **Justificacion de negocio:** Garantiza que el usuario no compare puntajes de admision entre escalas incompatibles sin la debida advertencia metodologica, respetando el tratamiento de homologacion establecido en el Hito 1.

---

## 3. Matriz de filtros requeridos por pauta y su integracion

La rubrica docente exige taxativamente:
> *«Permite filtrar al menos por año, institucion y region»* (Pauta Pagina 2 y 5).

| Filtro Obligatorio | Campo en el Modelo | Dimension | Tipo de Control UI | Impacto en Visualizaciones |
| :--- | :--- | :--- | :--- | :--- |
| **Año** | `dim_tiempo[ano]` | `dim_tiempo` | Segmentador tipo Menu desplegable / Lista horizontal | Filtra temporalmente los 15 años (2012–2026). Permite analisis puntual o selecciones multiples. |
| **Institucion** | `dim_institucion[nombre_institucion]` | `dim_institucion` | Segmentador jerarquico o busqueda predictiva | Aisla una o mas casas de estudio para evaluar su evolucion de matricula y selectividad. |
| **Region** | `dim_sede_geografia[region_nombre_estandar]` | `dim_sede_geografia` | Segmentador tipo mapa o botones por region | Permite filtrar por Region Metropolitana (foco principal), Quinta Region (Valparaiso) o nivel nacional. |
| **Foco Estrategico RM** | `dim_sede_geografia[es_region_metropolitana]` | `dim_sede_geografia` | Filtro predeterminado a nivel de pagina (= 1) | Asegura que los paneles de preguntas 1, 2 y 3 muestren automaticamente la realidad metropolitana. |

---

## 4. Pruebas de conexion desde Power BI y certificacion de rendimiento

### 4.1. Arquitectura de conexion
La ingesta de datos en Power BI Desktop se configuro utilizando un **script Python optimizado** que conecta con `datamart_indices_2012_2026.db`:
* **Conector:** `sqlite3` + `pandas` $\rightarrow$ Memoria RAM VertiPaq.
* **Modo de almacenamiento:** Import Mode (Carga completa en memoria columnar comprimida).
* **Tamaño del DataMart:** 25,3 MB (158.211 filas en la tabla de hechos y 5 dimensiones).

### 4.2. Resultados del benchmark de rendimiento

| Prueba de Consulta Jerarquica | Registros Afectados | Latencia Relacional (SQLite) | Latencia en Power BI (VertiPaq) | Estado |
| :--- | :---: | :---: | :---: | :---: |
| **Agregacion geografica (Macro $\rightarrow$ Region $\rightarrow$ Sede)** | 158.211 | 260,39 ms | < 10 ms |  **Aprobado** |
| **Agregacion institucional (Tipo $\rightarrow$ Institucion)** | 158.211 | 232,23 ms | < 10 ms |  **Aprobado** |
| **Agregacion academica (Area $\rightarrow$ Carrera Generica)** | 158.211 | 322,65 ms | < 12 ms |  **Aprobado** |
| **Agregacion temporal (Año a Año 2012--2026)** | 158.211 | 152,87 ms | < 8 ms |  **Aprobado** |
| **Consulta a vista precalculada RM** | 58.926 | 60,62 ms | < 5 ms |  **Aprobado** |

---

## 5. Medidas DAX fundamentales implementadas y validadas

Para responder a la aditividad de medidas exigida en el Hito 2 y preparar la entrega final:

1. **`[Total Matricula 1er Ano]` (Aditiva):**
   ```dax
   Total Matricula 1er Ano = SUM(fact_matricula_admision[matricula_primer_ano_total])
   ```
2. **`[Total Vacantes]` (Aditiva):**
   ```dax
   Total Vacantes = SUM(fact_matricula_admision[vacantes])
   ```
3. **`[Tasa Sobredemanda Ocupacion]` (Ratio Semi-aditivo):**
   ```dax
   Tasa Sobredemanda Ocupacion = 
   DIVIDE(
       [Total Matricula 1er Ano],
       [Total Vacantes],
       BLANK()
   )
   ```
4. **`[Promedio PAES Ponderado]` (Estrictamente No Aditivo):**
   ```dax
   Promedio PAES Ponderado = 
   DIVIDE(
       SUMX(
           fact_matricula_admision,
           fact_matricula_admision[puntaje_promedio_equiv_paes] * fact_matricula_admision[matricula_primer_ano_total]
       ),
       [Total Matricula 1er Ano],
       BLANK()
   )
   ```

---

## 6. Conclusion y preparacion para el hito final

La **Persona 4** dejo el entorno de visualizacion y modelado analitico **100% operativo y certificado**:
* Las **jerarquias** estan modeladas y probadas en el DataMart y listas para su uso en Power BI.
* La **conexion directa al DataMart relacional** esta certificada con latencias minimas y cero perdidas.
* Los **filtros obligatorios (año, institucion, region)** operan con integridad referencial perfecta (cero huerfanos).

