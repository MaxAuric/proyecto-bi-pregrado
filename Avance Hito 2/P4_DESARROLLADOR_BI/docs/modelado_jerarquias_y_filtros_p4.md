# Especificacion y modelado de jerarquias de filtro para Power BI
## Rol Evaluado: Persona 4 (Joaquin Aguilera)
### Hito 2: Modelo Dimensional y DataMart Relacional (2012–2026)

---

## 1. Fundamentacion del modelado de jerarquias

De acuerdo con las mejores practicas de arquitectura de Business Intelligence (Ralph Kimball) y los lineamientos de diseño analitico en Microsoft Power BI, las **jerarquias de navegacion (*Drill-Down / Drill-Up*)** son estructuras precalculadas en las tablas de dimensiones que permiten al usuario final explorar los datos desde una vision macroscopica (agregada) hasta el nivel atomico (detallado) sin perder el contexto de negocio ni degradar el rendimiento del motor tabular VertiPaq.

Para la solucion analitica reorientada a la **gestion de capacidad instalada, sobredemanda y selectividad** (con foco especial en la **Region Metropolitana**, preservando la comparabilidad nacional), la **Persona 4** modelo e implemento **4 jerarquias analiticas principales**.

---

## 2. Definicion detallada de jerarquias en el Modelo

### Jerarquia 1: Jerarquia geografica territorial
* **Tabla de origen:** `dim_sede_geografia`
* **Nombre en Power BI:** `Jerarquia Geografia Sede`
* **Niveles de navegacion:**
  1. **Nivel 1 (Macro):** `macro_zona` *(Norte, Centro, Region Metropolitana, Sur, Austral)*
  2. **Nivel 2 (Meso):** `region_nombre_estandar` *(16 regiones politico-administrativas homologadas)*
  3. **Nivel 3 (Micro / Sede Fisica):** `nombre_sede` *(Comuna o campus sede institucional)*

```text
[Macro-Zona] ────────► [Region Estandarizada] ────────► [Sede Fisica]
 (ej. Region Met.)      (ej. Region Met. de Santiago)    (ej. SANTIAGO, SAN JOAQUIN)
 (ej. Centro)           (ej. Region de Valparaiso)       (ej. VALPARAISO, VIÑA DEL MAR)
```

* **Casos de uso en el dashboard:**
  * Permite al usuario iniciar observando la concentracion de matricula en la Region Metropolitana vs el resto del pais, descender a la Quinta Region de Valparaiso o Biobio, y finalmente inspeccionar la sede fisica especifica donde se genera la sobredemanda de vacantes.
  * Habilita el cumplimiento del requisito de segmentacion: *«Permitir filtrar al menos por region»*.

---

### Jerarquia 2: Jerarquia institucional y de subsistema
* **Tabla de origen:** `dim_institucion`
* **Nombre en Power BI:** `Jerarquia Institucional`
* **Niveles de navegacion:**
  1. **Nivel 1 (Tipo de institucion):** `tipo_institucion` *(Universidad, Instituto Profesional - IP, Centro de Formacion Tecnica - CFT)*
  2. **Nivel 2 (Institucion):** `nombre_institucion` *(Nombre canonico de la casa de estudios)*
  3. **Nivel 3 (Vigencia anual SCD2):** `ano_vigencia` *(Permite trazar como cambian Acreditacion, Gratuidad y Autonomia año a año)*

```text
[Tipo de IES] ────────► [Institucion Canonica] ────────► [Año Vigencia SCD2]
 (ej. Universidad)       (ej. P. U. CATOLICA DE CHILE)    (ej. 2024: Acreditada / Gratuidad)
 (ej. Inst. Prof.)       (ej. DUOC UC)                    (ej. 2026: 7 años acreditacion)
```

* **Casos de uso en el dashboard:**
  * Facilita comparar la presion de vacantes entre universidades con examen de admision vs institutos tecnicos con matricula abierta.
  * Responde al requisito: *«Permitir filtrar al menos por institucion»*.

---

### Jerarquia 3: Jerarquia academica y formativa
* **Tabla de origen:** `dim_carrera_programa`
* **Nombre en Power BI:** `Jerarquia Academica`
* **Niveles de navegacion:**
  1. **Nivel 1 (Area de conocimiento):** `area_conocimiento` *(11 areas oficiales CNED: Tecnologia, Salud, Administracion y Comercio, etc.)*
  2. **Nivel 2 (Carrera generica):** `carrera_generica` *(284 familias genericas normalizadas)*
  3. **Nivel 3 (Programa especifico):** `nombre_programa` *(Denominacion especifica del plan de estudios)*

```text
[Area conocimiento] ────► [Carrera generica] ────► [Programa especifico]
 (ej. Tecnologia)          (ej. Ingenieria Civil Inf.)(ej. Ing. Civil en Computacion Diurno)
 (ej. Salud)               (ej. Medicina)             (ej. Medicina plan regular)
```

* **Casos de uso en el dashboard:**
  * Fundamental para responder la **Pregunta 1 de negocio**: Identificar que areas del saber sufren mayor sobrecupo y requieren apertura de nuevas secciones/laboratorios.

---

###  Jerarquia 4: Jerarquia temporal y metodologica
* **Tabla de origen:** `dim_tiempo`
* **Nombre en Power BI:** `Jerarquia Temporal`
* **Niveles de navegacion:**
  1. **Nivel 1 (Quinquenio):** `rango_quinquenio` *(2012–2016, 2017–2021, 2022–2026)*
  2. **Nivel 2 (Periodo metodologico):** `periodo_admision` *(PSU [2012–2020], PDT [2021–2022], PAES [2023–2026])* 
  3. **Nivel 3 (Año cronologico):** `ano` *(2012, 2013, ..., 2026)*

```text
[Quinquenio] ────────► [Periodo Admision] ────────► [Año Cronologico]
 (ej. 2022–2026)        (ej. PAES)                   (ej. 2023, 2024, 2025, 2026)
```

* **Casos de uso en el dashboard:**
  * Alerta visualmente sobre los quiebres de escala de las pruebas de admision antes de comparar puntajes en el tiempo.
  * Responde al requisito: *«Permitir filtrar al menos por año»*.

---

## 3. Matriz de filtros cruzados y relaciones en Power BI

| Filtro / segmentador | Jerarquia o campo vinculado | Tabla DataMart | Cardinalidad con Fact Table | Comportamiento del filtro |
| :--- | :--- | :--- | :---: | :--- |
| **Segmentador de año** | `dim_tiempo[ano]` | `dim_tiempo` | `1 : *` (Direccion unica) | Filtra instantaneamente todas las ofertas academicas de ese año. |
| **Segmentador de institucion** | `dim_institucion[nombre_institucion]` | `dim_institucion` | `1 : *` (Direccion unica) | Restringe el analisis a la universidad, IP o CFT seleccionado. |
| **Segmentador de region** | `dim_sede_geografia[region_nombre_estandar]` | `dim_sede_geografia` | `1 : *` (Direccion unica) | Permite aislar la RM (foco principal) o la Quinta Region / resto del pais. |
| **Filtro de foco RM** | `dim_sede_geografia[es_region_metropolitana]` | `dim_sede_geografia` | `1 : *` | Filtro predeterminado a nivel de informe (= 1) para responder a las preguntas de la RM. |
| **Selector de area** | `dim_carrera_programa[area_conocimiento]` | `dim_carrera_programa` | `1 : *` | Segmenta carreras por facultades y disciplinas. |

---

## 4. Medidas DAX para las jerarquias

Para garantizar que los agregados en cualquier nivel de la jerarquia respeten estrictamente las reglas de aditividad y no-aditividad, se  definio y probo las siguientes formulas DAX:

```dax
// Matricula de primer año
Total Matricula 1er Ano = 
SUM(fact_matricula_admision[matricula_primer_ano_total])

// Vacantes totales ofrecidas
Total Vacantes = 
SUM(fact_matricula_admision[vacantes])

// Tasa de sobredemanda y ocupacion de vacantes 
Tasa Sobredemanda Ocupacion = 
DIVIDE(
    [Total Matricula 1er Ano],
    [Total Vacantes],
    BLANK()
)

// Promedio PAES homologado ponderado 
Promedio PAES Ponderado = 
DIVIDE(
    SUMX(
        fact_matricula_admision,
        fact_matricula_admision[puntaje_promedio_equiv_paes] * fact_matricula_admision[matricula_primer_ano_total]
    ),
    [Total Matricula 1er Ano],
    BLANK()
)

// Presion de infraestructura y paralelos 
// Modela la necesidad de paralelos adicionales cuando las secciones superan los 40 alumnos
Indice Sobrecupo Alumnos = 
[Total Matricula 1er Ano] - [Total Vacantes]
```

