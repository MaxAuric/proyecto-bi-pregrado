# Diccionario de Datos Exhaustivo Maestro - Hito 1
## Proyecto Práctico Final de Business Intelligence - Ingeniería en Negocios

**Documentador y Gestor:** Persona 5  
**Fecha de Entrega:** 21 de Octubre de 2026  
**Cobertura Temporal:** 2012–2026 (158.211 registros consolidados)  

---

### 1. Resumen Estructural de Columnas (Base CNED Consolidada 2012–2026)

La base consolidada integra las 35 variables originales requeridas en la pauta (2012–2022) con las descargas oficiales del repositorio CNED (2023–2026) y 24 atributos técnicos calculados, totalizando **59 columnas gobernadas** sin pérdida de información.

| # | Nombre Final | Nombre Orig. (12-22) | Nombre Orig. (23-26) | Tipo de Dato | Categoría / Rol Dimensional | Regla de Transformación ETL | Tratamiento de Nulos y Justificación |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `ano` | Año | Año | `INTEGER` | Dimensión Temporal | Conversión a entero estándar de 4 dígitos [2012-2026]. | 0% nulos (0/158.211). Clave de particionamiento temporal y trazabilidad histórica. |
| 2 | `nombre_institucion` | Nombre Institución | Nombre Institución | `VARCHAR(150)` | Dimensión Institución | Normalización de espacios (strip), mayúsculas consistentes y homofonía para enlace con tabla puente SIES. | 0% nulos. Clave de entidad institucional (259 grafías normalizadas). |
| 3 | `tipo_institucion` | Tipo Institución | Tipo Institución | `VARCHAR(50)` | Dimensión Institución | Limpieza de caracteres especiales y recorte de espacios. | 0% nulos. Clasificación estructural del sistema terciario. |
| 4 | `clasificacion2` | Clasificación2 | Clasificación2 | `VARCHAR(100)` | Dimensión Institución | Mapeo directo y homogeneización de cadenas alfanuméricas. | Preservación de nulos en tipologías sin régimen secundario aplicable. |
| 5 | `acreditacion` | Acreditación | Clasificación3 | `VARCHAR(50)` | Dimensión Institución | Mapeo estructural de 'Clasificación3' del CNED 2023-2026 a la variable histórica 'acreditacion'. | 0% nulos. En Hito 2 se modela formalmente su variación temporal (SCD Tipo 2). |
| 6 | `autonomia` | Autonomía | Clasificación4 | `VARCHAR(50)` | Dimensión Institución | Mapeo de 'Clasificación4' del CNED 2023-2026 a 'autonomia'. | 0% nulos. Estado legal continuo. |
| 7 | `gratuidad` | Gratuidad | Clasificación5 | `VARCHAR(50)` | Dimensión Institución | Mapeo de 'Clasificación5' del CNED 2023-2026 a 'gratuidad'. | Nulos previos a 2016 reflejan la inexistencia legal de la ley. No se imputa para respetar la verdad histórica. |
| 8 | `nombre_sede` | Nombre de la Sede | Nombre de la Sede | `VARCHAR(100)` | Dimensión Sede | Normalización de cadenas de texto y remoción de espacios redundantes. | 0% nulos. |
| 9 | `nombre_region` | Nombre Region | Nombre Region | `VARCHAR(80)` | Dimensión Geográfica | Normalización ortográfica y compatibilización con estándares territoriales SUBDERE e INE. | 0% nulos. |
| 10 | `region_codigo_subdere` | (Calculado) | (Calculado) | `VARCHAR(2)` | Dimensión Geográfica | Mapeo determinista por diccionario regional oficial a partir de 'nombre_region'. | 0% nulos. Llave canónica de interoperabilidad externa (INE, Casen). |
| 11 | `region_numero_romano` | (Calculado) | (Calculado) | `VARCHAR(5)` | Dimensión Geográfica | Mapeo determinista derivado del código SUBDERE. | 0% nulos. |
| 12 | `region_nombre_estandar` | (Calculado) | (Calculado) | `VARCHAR(100)` | Dimensión Geográfica | Estandarización léxica oficial según norma SUBDERE. | 0% nulos. |
| 13 | `region_orden_geografico` | (Calculado) | (Calculado) | `INTEGER` | Dimensión Geográfica | Mapeo numérico secuencial para garantizar orden visual correcto en paneles Power BI. | 0% nulos. |
| 14 | `flag_quiebre_nuble` | (Calculado) | (Calculado) | `INTEGER (0/1)` | Dimensión Geográfica | 1 si region_codigo_subdere == '16' y ano < 2018; 0 en otro caso. | 0% nulos. Gobierna 1.599 registros históricos previos a la vigencia institucional de la región. |
| 15 | `carrera_generica` | Carrera Genérica | Carrera Genérica | `VARCHAR(120)` | Dimensión Carrera | Limpieza de tildes, caracteres redundantes y mayúsculas. Llave para cruces con mifuturo.cl. | 0% nulos. |
| 16 | `nombre_programa` | Nombre Programa | Nombre Programa | `VARCHAR(200)` | Dimensión Programa | Limpieza de texto, unificación de espacios y normalización a mayúsculas. | 0% nulos. |
| 17 | `horario` | Horario | Horario | `VARCHAR(30)` | Dimensión Programa | Tipificación uniforme y eliminación de caracteres no imprimibles. | 0% nulos. |
| 18 | `tipo_programa` | Tipo Programa | Tipo Programa | `VARCHAR(50)` | Dimensión Programa | Normalización de texto y concordancia de categorías. | 0% nulos. |
| 19 | `area_conocimiento` | Area Conocimiento | Area Conocimiento | `VARCHAR(80)` | Dimensión Programa | Limpieza de caracteres especiales y acentos ortográficos. | 0% nulos. |
| 20 | `tipo_carrera` | Tipo Carrera | Tipo Carrera | `VARCHAR(50)` | Dimensión Carrera | Recorte de espacios y tipificación uniforme. | 0% nulos. |
| 21 | `ingreso_directo` | IngresoDirecto | IngresoDirecto | `VARCHAR(10)` | Dimensión Carrera | Estandarización a valores booleanos/texto homogéneo SI/NO. | 0% nulos. |
| 22 | `ano_inicio_actividades` | Año Inicio Actividades | Año Inicio Actividades | `INTEGER` | Dimensión Programa | Conversión a entero estándar. Preservación de 6 casos nulos de origen (0,01%). | 0.01% nulos justificados por omisión en registro original del CNED. |
| 23 | `duracion_semestres` | Duración (en semestres) | Duración (en semestres) | `INTEGER` | Dimensión Programa | Casting numérico a entero int64. | 0% nulos. |
| 24 | `titulo` | Título | Título | `VARCHAR(200)` | Dimensión Programa | Limpieza tipográfica. Preservación de nulos en planes que conducen únicamente a grado académico. | 1.46% nulos legítimos correspondientes a planes de licenciatura académica sin titulación profesional directa. |
| 25 | `grado_academico` | Grado Académico | Grado Académico | `VARCHAR(100)` | Dimensión Programa | Limpieza tipográfica. Preservación estricta de nulos. | 68.57% nulos legítimos: las carreras técnicas de CFT y carreras de IP por ley no otorgan grado académico. |
| 26 | `tipo_prueba_admision` | (Calculado) | (Calculado) | `VARCHAR(10)` | Atributo de Hecho | Mapeo condicional por año cronológico de ingreso. | 0% nulos. Esencial para segmentar auditorías psicométricas. |
| 27 | `flag_exige_prueba_admision` | (Calculado) | (Calculado) | `INTEGER (0/1)` | Atributo Dim. / Hecho | 1 si puntaje_promedio_original no es nulo; 0 en caso contrario. | 0% nulos. Filtro indispensable en Power BI para aislar carreras con prueba de aquellas de admisión abierta. |
| 28 | `puntaje_promedio_original` | Promedio Puntaje | Promedio Puntaje | `DECIMAL(6,2)` | Hecho / Medida No Aditiva | Casting numérico float. Escalas: PSU/PDT [150-850], PAES [100-1000]. | 80.49% nulos explicados matemáticamente por cobertura: CFT 0.2%, IP 0.1%, Univ 47.4%. Preservados como NULL. Prohibido reemplazar por cero. |
| 29 | `puntaje_promedio_norm_0_100` | (Calculado) | (Calculado) | `DECIMAL(5,2)` | Hecho / Medida No Aditiva | PSU/PDT: ((score-150)/700)*100; PAES: ((score-100)/900)*100. | Preservado como NULL para programas sin requisito de prueba centralizada. |
| 30 | `puntaje_promedio_equiv_paes` | (Calculado) | (Calculado) | `DECIMAL(6,2)` | Hecho / Medida No Aditiva | PSU/PDT: 100 + ((score-150)/700)*900; PAES: score nativo. | Preservado como NULL. |
| 31 | `puntaje_promedio_zscore_anual` | (Calculado) | (Calculado) | `DECIMAL(5,3)` | Hecho / Medida Estandarizada | (score - media_anual) / desv_anual. | Preservado como NULL. |
| 32 | `puntaje_maximo_original` | Máximo Puntaje | Máximo Puntaje | `DECIMAL(6,2)` | Hecho / Medida No Aditiva | Casting numérico float. Preservación estricta de nulos. | 80.48% nulos justificados por cobertura institucional. Preservados como NULL. |
| 33 | `puntaje_maximo_norm_0_100` | (Calculado) | (Calculado) | `DECIMAL(5,2)` | Hecho / Medida No Aditiva | PSU/PDT: ((score-150)/700)*100; PAES: ((score-100)/900)*100. | Preservado como NULL. |
| 34 | `puntaje_maximo_equiv_paes` | (Calculado) | (Calculado) | `DECIMAL(6,2)` | Hecho / Medida No Aditiva | PSU/PDT: 100 + ((score-150)/700)*900; PAES: score nativo. | Preservado como NULL. |
| 35 | `puntaje_minimo_original` | Mínimo Puntaje | Mínimo Puntaje | `DECIMAL(6,2)` | Hecho / Medida No Aditiva | Casting numérico float. Preservación de nulos. | 80.48% nulos justificados. Preservados como NULL. |
| 36 | `puntaje_minimo_norm_0_100` | (Calculado) | (Calculado) | `DECIMAL(5,2)` | Hecho / Medida No Aditiva | PSU/PDT: ((score-150)/700)*100; PAES: ((score-100)/900)*100. | Preservado como NULL. |
| 37 | `puntaje_minimo_equiv_paes` | (Calculado) | (Calculado) | `DECIMAL(6,2)` | Hecho / Medida No Aditiva | PSU/PDT: 100 + ((score-150)/700)*900; PAES: score nativo. | Preservado como NULL. |
| 38 | `puntaje_corte_primer_original` | Puntaje de corte (primer seleccionado) | Puntaje de corte (primer seleccionado) | `DECIMAL(6,2)` | Hecho / Medida No Aditiva | Casting numérico float. | 81.70% nulos justificados por programas sin proceso de selección centralizado. |
| 39 | `puntaje_corte_primer_norm_0_100` | (Calculado) | (Calculado) | `DECIMAL(5,2)` | Hecho / Medida No Aditiva | PSU/PDT: ((score-150)/700)*100; PAES: ((score-100)/900)*100. | Preservado como NULL. |
| 40 | `puntaje_corte_primer_equiv_paes` | (Calculado) | (Calculado) | `DECIMAL(6,2)` | Hecho / Medida No Aditiva | PSU/PDT: 100 + ((score-150)/700)*900; PAES: score nativo. | Preservado como NULL. |
| 41 | `puntaje_corte_promedio_original` | Puntaje de corte (promedio de la carrera) | Puntaje de corte (promedio de la carrera) | `DECIMAL(6,2)` | Hecho / Medida No Aditiva | Casting numérico float. | 81.70% nulos justificados. Preservados como NULL. |
| 42 | `puntaje_corte_promedio_norm_0_100` | (Calculado) | (Calculado) | `DECIMAL(5,2)` | Hecho / Medida No Aditiva | PSU/PDT: ((score-150)/700)*100; PAES: ((score-100)/900)*100. | Preservado como NULL. |
| 43 | `puntaje_corte_promedio_equiv_paes` | (Calculado) | (Calculado) | `DECIMAL(6,2)` | Hecho / Medida No Aditiva | PSU/PDT: 100 + ((score-150)/700)*900; PAES: score nativo. | Preservado como NULL. |
| 44 | `puntaje_corte_ultimo_original` | Puntaje de corte (último seleccionado) | Puntaje de corte (último seleccionado) | `DECIMAL(6,2)` | Hecho / Medida No Aditiva (Corte de Carrera) | Casting numérico float. | 81.67% nulos justificados. Preservados como NULL. |
| 45 | `puntaje_corte_ultimo_norm_0_100` | (Calculado) | (Calculado) | `DECIMAL(5,2)` | Hecho / Medida No Aditiva | PSU/PDT: ((score-150)/700)*100; PAES: ((score-100)/900)*100. | Preservado como NULL. |
| 46 | `puntaje_corte_ultimo_equiv_paes` | (Calculado) | (Calculado) | `DECIMAL(6,2)` | Hecho / Medida No Aditiva | PSU/PDT: 100 + ((score-150)/700)*900; PAES: score nativo. | Preservado como NULL. |
| 47 | `vacantes` | Vacantes | Vacantes | `INTEGER` | Hecho / Medida Aditiva | Casting numérico a entero int64. | 25.35% nulos en carreras con matrícula abierta, vespertinas o sin límite predefinido de cupo. Preservados como NULL. Reemplazar por cero falsearía el cierre de la oferta y provocaría divisiones por cero. |
| 48 | `flag_vacantes_declaradas` | (Calculado) | (Calculado) | `INTEGER (0/1)` | Atributo Dim. / Hecho | 1 si vacantes > 0; 0 si es nulo o no informado. | 0% nulos. Filtro de gobernanza que garantiza la estabilidad matemática de los indicadores de ocupación. |
| 49 | `matricula_primer_ano_hombres` | Matrícula primer año hombres | Matrícula primer año hombres | `INTEGER` | Hecho / Medida Aditiva | Conversión numérica a entero. Imputación de nulos a 0 (ausencia de inscritos del segmento). | 0% nulos. Medida totalmente aditiva. |
| 50 | `matricula_primer_ano_mujeres` | Matrícula primer año mujeres | Matrícula primer año mujeres | `INTEGER` | Hecho / Medida Aditiva | Conversión numérica a entero. Imputación de nulos a 0. | 0% nulos. Medida totalmente aditiva. |
| 51 | `matricula_primer_ano_extranjeros` | Matrícula primer año extranjeros | Matrícula primer año extranjeros | `INTEGER` | Hecho / Medida Aditiva | Conversión numérica a entero. Imputación de nulos a 0. | 0% nulos. Medida totalmente aditiva. |
| 52 | `matricula_primer_ano_total` | Matrícula Primer Año | Matrícula Primer Año | `INTEGER` | Hecho / Medida Aditiva Principal | Conversión numérica a entero. Imputación de nulos a 0. | 0% nulos. Medida aditiva en tiempo, espacio, institución y programa. |
| 53 | `matricula_total_hombres` | Matrícula total hombres | Matrícula total hombres | `INTEGER` | Hecho / Medida Aditiva | Conversión numérica a entero. Imputación de nulos a 0. | 0% nulos. |
| 54 | `matricula_total_mujeres` | Matrícula total mujeres | Matrícula total mujeres | `INTEGER` | Hecho / Medida Aditiva | Conversión numérica a entero. Imputación de nulos a 0. | 0% nulos. |
| 55 | `matricula_total_extranjeros` | Matrícula total extranjeros | Matrícula total extranjeros | `INTEGER` | Hecho / Medida Aditiva | Conversión numérica a entero. Imputación de nulos a 0. | 0% nulos. |
| 56 | `matricula_total` | Matrícula Total | Matrícula Total | `INTEGER` | Hecho / Medida Aditiva Principal | Conversión numérica a entero. Imputación de nulos a 0. | 0% nulos. Medida aditiva central. |
| 57 | `tasa_ocupacion_primer_ano` | (Calculado) | (Calculado) | `DECIMAL(6,2)` | Métrica Analítica / Ratio Intensivo | ((matricula_primer_ano_total / vacantes) * 100). Calculado solo cuando flag_vacantes_declaradas = 1. | Preservado como NULL cuando no hay vacantes declaradas para no sesgar medias. |
| 58 | `ratio_mujeres_primer_ano` | (Calculado) | (Calculado) | `DECIMAL(5,2)` | Métrica Analítica / Ratio Intensivo | ((matricula_primer_ano_mujeres / matricula_primer_ano_total) * 100). | Preservado como NULL si matricula_primer_ano_total == 0. |
| 59 | `ratio_extranjeros_total` | (Calculado) | (Calculado) | `DECIMAL(5,2)` | Métrica Analítica / Ratio Intensivo | ((matricula_total_extranjeros / matricula_total) * 100). | Preservado como NULL si matricula_total == 0. |

---

### 2. Diccionario de Fuentes Externas Integradas

#### ext_ine_poblacion_region_ano.csv (INE (Instituto Nacional de Estadísticas))
- **Descripción:** Estimaciones y proyecciones de población por región y grupos de edad (2002-2035, base Censo 2017).
- **URL Oficial:** [Descarga Oficial](https://www.ine.gob.cl/docs/default-source/proyecciones-de-poblacion/cuadros-estadisticos/base-2017/ine_estimaciones-y-proyecciones-2002-2035_base-2017_region_area_tabulados.xlsx)
- **Fecha de Descarga:** 2026-10-15
- **Grano Declarado:** `region_codigo_subdere x ano`
- **Llave de Cruce:** `region_codigo_subdere + ano`

| Columna | Tipo de Dato | Descripción y Regla de Negocio |
| :--- | :--- | :--- |
| `region_codigo_subdere` | `VARCHAR(2)` | Código oficial SUBDERE de dos dígitos (01-16). |
| `hoja_ine` | `VARCHAR(50)` | Nombre original de la hoja tabular en el libro del INE. |
| `ano` | `INTEGER` | Año cronológico proyectado (2002-2035). |
| `poblacion_total` | `INTEGER` | Población total estimada al 30 de junio, ambos sexos. |
| `poblacion_hombres` | `INTEGER` | Población masculina estimada al 30 de junio. |
| `poblacion_mujeres` | `INTEGER` | Población femenina estimada al 30 de junio. |
| `poblacion_0_14` | `INTEGER` | Población en rango etario de 0 a 14 años. |
| `poblacion_15_64` | `INTEGER` | Población en edad activa de estudiar/trabajar (15 a 64 años). |
| `poblacion_65_mas` | `INTEGER` | Población de 65 años o más. |

#### ext_sies_acreditacion_ies_ano.csv (SIES / Ministerio de Educación)
- **Descripción:** Listados oficiales de Instituciones de Educación Superior vigentes con acreditación y autonomía (2018-2026).
- **URL Oficial:** [Descarga Oficial](https://www.mifuturo.cl/instituciones-de-educacion-superior-en-chile/)
- **Fecha de Descarga:** 2026-10-15
- **Grano Declarado:** `codigo_ies x ano_corte`
- **Llave de Cruce:** `codigo_ies + ano`

| Columna | Tipo de Dato | Descripción y Regla de Negocio |
| :--- | :--- | :--- |
| `codigo_ies` | `INTEGER` | Código numérico institucional oficial otorgado por SIES. |
| `tipo_institucion` | `VARCHAR(50)` | Clasificación oficial (Universidad, IP, CFT, etc.). |
| `nombre_institucion_sies` | `VARCHAR(150)` | Denominación legal registrada ante el Mineduc. |
| `autonomia` | `VARCHAR(50)` | Condición de autonomía institucional (disponible desde corte 2023). |
| `acreditacion` | `VARCHAR(50)` | Estado literal de acreditación según listado SIES. |
| `acreditacion_norm` | `VARCHAR(50)` | Categoría estandarizada (Acreditada, Extendida, Tutela, No Acreditada). |
| `vigencia` | `VARCHAR(100)` | Fecha o periodo de vencimiento del dictamen de la CNA. |
| `anos_acreditacion` | `INTEGER` | Años de acreditación otorgados formalmente (0 a 7 años). |
| `ano_corte` | `INTEGER` | Año del corte censal del listado SIES (2018-2026). |
| `corte` | `VARCHAR(10)` | Etiqueta cronológica AAAA-MM (ej. 2026-09). |
| `nombre_norm` | `VARCHAR(150)` | Nombre sin acentos, signos ni puntuación para búsqueda fonética. |

---

### 3. Documentación Formal de Tablas Puente de Homologación

#### Tabla Puente: `puente_region.csv`
- **Propósito:** Tabla puente determinista para resolución geográfica de sedes y vinculación con proyecciones INE.
- **Granularidad:** `nombre_region (16 regiones)`
- **Llave en Base Primaria:** `nombre_region` | **Llave en Dimensión:** `region_codigo_subdere`
- **Tasa de Coincidencia de Registros:** **100%** (No cruzados: 0)

| Campo Puente | Tipo | Descripción de la Homologación |
| :--- | :--- | :--- |
| `nombre_region` | `VARCHAR(80)` | Nombre textual tal como figura en los registros CNED. |
| `region_codigo_subdere` | `VARCHAR(2)` | Código canónico oficial de 2 dígitos asignado por SUBDERE. |
| `region_nombre_estandar` | `VARCHAR(100)` | Denominación protocolar completa y estandarizada. |
| `hoja_ine` | `VARCHAR(50)` | Identificador unívoco de la pestaña en el libro oficial del INE. |

#### Tabla Puente: `puente_institucion.csv`
- **Propósito:** Tabla puente institucional para enlace de nombres abreviados del CNED con el código oficial SIES.
- **Granularidad:** `nombre_institucion_cned (259 grafías)`
- **Llave en Base Primaria:** `nombre_institucion` | **Llave en Dimensión:** `codigo_ies`
- **Tasa de Coincidencia de Registros:** **98.39%** (No cruzados: undefined)
- **Cobertura Institucional:** 92.66% entidades con código oficial SIES (99% de matrícula 1er año)

| Campo Puente | Tipo | Descripción de la Homologación |
| :--- | :--- | :--- |
| `nombre_institucion_cned` | `VARCHAR(150)` | Grafía exacta registrada en la base de matrícula CNED. |
| `nombre_normalizado` | `VARCHAR(150)` | Expansión léxica de siglas (U. -> UNIVERSIDAD, IP -> INSTITUTO PROFESIONAL, CFT -> CENTRO DE FORMACION TECNICA). |
| `codigo_ies` | `INTEGER` | Código de institución oficial SIES (NULL para no coincidentes). |
| `nombre_institucion_sies` | `VARCHAR(150)` | Razón social homóloga en el catálogo del SIES. |
| `metodo_cruce` | `VARCHAR(30)` | Estrategia algorítmica: exacto_normalizado (168), manual (47), aproximado_>=0.92 (25), sin_coincidencia (19). |
| `similitud` | `DECIMAL(4,3)` | Coeficiente de similitud de cadenas difflib (1.000 para exactos/manuales, >=0.920 para aproximados). |

