# Diccionario de Fuentes Externas RM — Hito 2 (Persona 2)

Insumo para la **Persona 5** (Gestor y Documentador). Tablas externas reacotadas a la Región Metropolitana, listas para integrarse como dimensiones en el DataMart de Hito 2.

---

## 1. Contexto del reajuste

En el Hito 1 las fuentes externas cubrían las 16 regiones. Para el Hito 2 se acota el análisis a la **Región Metropolitana (código SUBDERE = 13)**, en respuesta al feedback docente de focalizar en un problema real de negocio (planificación de capacidad instalada ante sobredemanda de vacantes).

---

## 2. `rm_ext_ine_poblacion.csv`

Generado por `scripts/08_extract_rm_data.py`. Filtro de `ext_ine_poblacion_region_ano.csv` (Hito 1) al código SUBDERE 13.

| Columna | Tipo | Descripción | Regla |
|---|---|---|---|
| `region_codigo_subdere` | entero | Siempre = 13 (RM) | Filtro del archivo nacional |
| `hoja_ine` | texto | `"Metropolitana"` | Nombre de hoja en el libro INE |
| `ano` | entero | Año calendario (2002–2035) | Encabezado de columna en libro INE |
| `poblacion_total` | entero | Población al 30 de junio, ambos sexos | Fila "Ambos sexos" |
| `poblacion_hombres` | entero | Población hombres | Fila "Hombres" |
| `poblacion_mujeres` | entero | Población mujeres | Fila "Mujeres" |
| `poblacion_0_14` | entero | Población 0–14 años | Fila homónima |
| `poblacion_15_64` | entero | Población 15–64 años | Fila homónima |
| `poblacion_65_mas` | entero | Población 65+ años | Fila homónima |
| `est_pob_18_24_rm` | entero | **Estimación proxy** 18–24 años RM | `= round(poblacion_15_64 × 0.14)` |

> **Limitación**: el archivo INE regional no desglosa el tramo 18–24 exacto. El proxy 14% (7 de cada 50 años del grupo 15–64) es una estimación documentada. Para mayor precisión usar el Censo 2017 desagregado por edad simple.

**Uso en DataMart**: tabla `Dim_Poblacion_RM` con PK = `ano`. FK en `Fact_Matricula_Admision.ano`.

---

## 3. `rm_ext_sies_acreditacion.csv`

Generado por `scripts/08_extract_rm_data.py`. Derivado de `ext_sies_acreditacion_ies_ano.csv` (Hito 1).

| Columna | Tipo | Descripción | Regla |
|---|---|---|---|
| `codigo_ies` | entero | Código SIES de la institución | Columna "Código de institución" |
| `tipo_institucion` | texto | Universidad, IP, CFT | Literal |
| `nombre_institucion_sies` | texto | Nombre oficial en el corte | Literal |
| `autonomia` | texto | Estado de autonomía | Disponible desde corte 2023-12; NULL antes |
| `acreditacion` | texto | Estado de acreditación (texto original) | Literal |
| `acreditacion_norm` | texto | Categoría normalizada | `{Acreditada, Acreditación extendida, Bajo tutela, No acreditada}` |
| `vigencia` | texto | Texto de vigencia de la acreditación | Literal |
| `anos_acreditacion` | numerico | Años de acreditación vigente | Conversión numérica; NULL si no aplica |
| `ano_corte` | entero | Año del corte SIES | Del nombre del archivo |
| `corte` | texto | Corte en formato `AAAA-MM` | Del nombre del archivo |
| `nombre_norm` | texto | Nombre normalizado (mayúsculas, sin tildes) | Para cruce textual |

**Uso en DataMart**: atributo SCD Tipo 2 de `Dim_Institucion`. Llave compuesta de cruce = `codigo_ies + ano_corte`. Un registro por institución × año.

> **CRÍTICO**: acreditación 2012–2017 = NULL (sin listado SIES previo a 2018). **No imputar** con valor de 2018.

---

## 4. `rm_kpi_p1_sobredemanda.csv`

| Columna | Descripción |
|---|---|
| `ano` | Año calendario |
| `area_conocimiento` | Área (si disponible en base) |
| `vacantes_total` | Suma de vacantes RM con vacantes > 0 |
| `matricula_1er_ano` | Suma de matrícula primer año RM |
| `programas_total` | N° programas con vacantes declaradas |
| `programas_sobredemanda` | N° programas con matrícula > vacantes |
| `tasa_ocupacion_pct` | `matricula_1er_ano / vacantes_total × 100` |
| `pct_programas_sobredemanda` | `programas_sobredemanda / programas_total × 100` |

**Aditividad**: `vacantes_total` y `matricula_1er_ano` son **aditivas**. `tasa_ocupacion_pct` es un ratio derivado; recalcular con los totales, no promediar tasas.

---

## 5. `rm_kpi_p2_puntajes_paes.csv`

| Columna | Descripción |
|---|---|
| `ano` | Año calendario |
| `{puntaje_col}_promedio` | Promedio del puntaje en la RM ese año |
| `{puntaje_col}_minimo` | Mínimo del puntaje en la RM ese año |
| `vacantes` | Total vacantes RM |
| `matricula_1er_ano` | Total matrícula primer año RM |

> **IMPORTANTE (Persona 4 / DAX)**: los promedios de puntaje **NO son aditivos**. No sumar entre años ni entre instituciones. Usar `AVERAGEX` ponderado por matrícula. Incluir filtro por `instrumento_admision` (PSU / PDT / PAES) para evitar comparación de escalas distintas.

---

## 6. `rm_kpi_p3_absorcion_demografica.csv`

| Columna | Descripción |
|---|---|
| `ano` | Año calendario |
| `vacantes_rm` | Suma de vacantes RM |
| `matricula_rm` | Matrícula primer año RM |
| `poblacion_total` | Población total RM (INE) |
| `poblacion_15_64` | Población 15–64 años RM (INE) |
| `est_pob_18_24_rm` | Estimación proxy 18–24 años RM |
| `vacantes_por_1000_hab_15_64` | `vacantes_rm / poblacion_15_64 × 1000` |
| `tasa_absorcion_18_24_pct` | `matricula_rm / est_pob_18_24_rm × 100` |

**Aditividad**: `tasa_absorcion_18_24_pct` y `vacantes_por_1000_hab_15_64` son **ratios derivados**. Calcular primero los totales (aditivos), luego dividir.

---

## 7. Reglas de Uso para Persona 5

| Riesgo | Regla |
|---|---|
| Puntajes | Son promedios, NO aditivos. Nunca `SUM(puntaje)` en DAX |
| Acreditación 2012–2017 | NULL estructural. No imputar |
| Quiebre PSU/PAES (2022) | Flag `instrumento_admision` en tabla de hechos |
| Población INE | Stock al 30-jun. Aditiva entre regiones, no entre años |
| Tasa de ocupación | Excluir vacantes = 0 o NULL |
| Matrícula | Por región de sede, no domicilio del estudiante |
| Proxy 18–24 | Estimación documentada; declarar en informe |

