# Diccionario de Datos Exhaustivo - Hito 1
## Proyecto Final de Business Intelligence - Ingeniería en Negocios

| Nombre Final | Nombre Orig. (12-22) | Nombre Orig. (23-26) | Tipo | Categoría | Regla de Transformación ETL | Tratamiento de Nulos y Justificación |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ano` | Año | Año | `INTEGER` | Dimensión Temporal | Conversión a entero estándar de 4 dígitos [2012-2026]. | 0% nulos. Clave temporal obligatoria. |
| `nombre_institucion` | Nombre Institución | Nombre Institución | `VARCHAR(150)` | Dimensión Institución | Normalización de espacios y estandarización a mayúsculas consistentes. | 0% nulos. Clave de entidad institucional. |
| `tipo_institucion` | Tipo Institución | Tipo Institución | `VARCHAR(50)` | Dimensión Institución | Limpieza de caracteres especiales y recorte de espacios. | 0% nulos. Clasificación estructural del sistema de educación superior. |
| `clasificacion2` | Clasificación2 | Clasificación2 | `VARCHAR(100)` | Dimensión Institución | Mapeo directo y limpieza de prefijos alfanuméricos. | Preservación de nulos si no aplica subclasificación. |
| `acreditacion` | Acreditación | Clasificación3 | `VARCHAR(50)` | Dimensión Institución | Mapeo de 'Clasificación3' del CNED 2023-2026 a 'acreditacion'. | Preservación del estado para modelar cambios en el tiempo (SCD Tipo 2). |
| `autonomia` | Autonomía | Clasificación4 | `VARCHAR(50)` | Dimensión Institución | Mapeo de 'Clasificación4' del CNED 2023-2026 a 'autonomia'. | Preservación del estado institucional. |
| `gratuidad` | Gratuidad | Clasificación5 | `VARCHAR(50)` | Dimensión Institución | Mapeo de 'Clasificación5' del CNED 2023-2026 a 'gratuidad'. | Nulos antes de 2016 reflejan inexistencia legal previa de la política. |
| `nombre_sede` | Nombre de la Sede | Nombre de la Sede | `VARCHAR(100)` | Dimensión Sede | Normalización de textos y remoción de espacios redundantes. | 0% nulos. |
| `nombre_region` | Nombre Region | Nombre Region | `VARCHAR(80)` | Dimensión Geográfica | Normalización ortográfica y compatibilización con estándares SUBDERE/INE. | 0% nulos. |
| `region_codigo_subdere` | (Calculado) | (Calculado) | `VARCHAR(2)` | Dimensión Geográfica | Mapeo determinista basado en nombre de región. | 0% nulos. Llave canónica para cruces externos (INE, Casen). |
| `flag_quiebre_nuble` | (Calculado) | (Calculado) | `INTEGER (0/1)` | Dimensión Geográfica | 1 si codigo='16' y ano < 2018; 0 en otro caso. | 0% nulos. |
| `carrera_generica` | Carrera Genérica | Carrera Genérica | `VARCHAR(120)` | Dimensión Carrera | Limpieza de tildes, caracteres especiales y mayúsculas. | 0% nulos. Llave para cruce con mifuturo.cl. |
| `nombre_programa` | Nombre Programa | Nombre Programa | `VARCHAR(200)` | Dimensión Programa | Limpieza de textos y normalización de mayúsculas. | 0% nulos. |
| `horario` | Horario | Horario | `VARCHAR(30)` | Dimensión Programa | Recorte de espacios y tipificación uniforme. | 0% nulos. |
| `tipo_programa` | Tipo Programa | Tipo Programa | `VARCHAR(50)` | Dimensión Programa | Normalización de texto. | 0% nulos. |
| `area_conocimiento` | Area Conocimiento | Area Conocimiento | `VARCHAR(80)` | Dimensión Programa | Limpieza de caracteres especiales. | 0% nulos. |
| `tipo_prueba_admision` | (Calculado) | (Calculado) | `VARCHAR(10)` | Atributo de Hecho | Mapeo condicional por año cronológico. | 0% nulos. Esencial para segmentar análisis psicométrico. |
| `puntaje_promedio_original` | Promedio Puntaje | Promedio Puntaje | `DECIMAL(6,2)` | Hecho / Medida | Casting numérico. Escala [150-850] en PSU/PDT y [100-1000] en PAES. | 80.5% nulos justificados (CFT/IP). Preservados como NULL. |
| `puntaje_promedio_norm_0_100` | (Calculado) | (Calculado) | `DECIMAL(5,2)` | Hecho / Medida | PSU/PDT: (Score-150)/700*100; PAES: (Score-100)/900*100. | Preservado como NULL para instituciones sin requisito de prueba. |
| `puntaje_promedio_equiv_paes` | (Calculado) | (Calculado) | `DECIMAL(6,2)` | Hecho / Medida | PSU/PDT: 100 + (Score-150)/700*900; PAES: Score nativo. | Preservado como NULL. |
| `puntaje_promedio_zscore_anual` | (Calculado) | (Calculado) | `DECIMAL(5,3)` | Hecho / Medida | (Score - Media_Anual) / Desv_Anual. | Preservado como NULL. |
| `flag_exige_prueba_admision` | (Calculado) | (Calculado) | `INTEGER (0/1)` | Atributo Dim. | 1 si puntaje no es nulo; 0 en caso contrario. | 0% nulos. Filtro indispensable para Power BI. |
| `vacantes` | Vacantes | Vacantes | `INTEGER` | Hecho / Medida | Casting numérico a entero. | 25.4% nulos en programas con admisión abierta. Preservados como NULL. |
| `flag_vacantes_declaradas` | (Calculado) | (Calculado) | `INTEGER (0/1)` | Atributo Dim. | 1 si vacantes > 0; 0 si es nulo o no informado. | 0% nulos. Asegura cálculo correcto de tasas de ocupación. |
| `matricula_primer_ano_total` | Matrícula 1er Año | Matrícula 1er Año | `INTEGER` | Hecho / Medida | Casting numérico entero. Imputación de nulos a 0. | 0% nulos (medida aditiva). |
| `matricula_total` | Matrícula Total | Matrícula Total | `INTEGER` | Hecho / Medida | Casting numérico entero. Imputación de nulos a 0. | 0% nulos (medida aditiva). |
| `tasa_ocupacion_primer_ano` | (Calculado) | (Calculado) | `DECIMAL(6,2)` | Métrica Analítica | (Matricula Primer Año / Vacantes) * 100. | Calculado solo cuando flag_vacantes_declaradas=1. |
