# Diccionario de fuentes externas y tablas puente (Persona 2, Hito 1)

Insumo para la Persona 5 (anexo del diccionario de datos). Todas las tablas se generan con
`P2_Hito1/scripts/06_build_external_bridges.py` y quedan en `P2_Hito1/data_processed/`.

## 1. Fuentes y trazabilidad

| Fuente | Archivo local | URL | Fecha descarga | Grano | Llave de cruce |
|---|---|---|---|---|---|
| INE: estimaciones y proyecciones de poblacion 2002-2035 (base Censo 2017) | `data_external/INE_proyecciones_2017_region_area.xlsx` | https://www.ine.gob.cl/docs/default-source/proyecciones-de-poblacion/cuadros-estadisticos/base-2017/ine_estimaciones-y-proyecciones-2002-2035_base-2017_region_area_tabulados.xlsx?sfvrsn=e9bd6edf_6 (pagina: https://www.ine.gob.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion) | 2026-10-15 | region x ano | `region_codigo_subdere` + `ano` |
| SIES/MINEDUC: listado de IES vigentes (9 cortes: dic. 2018 a dic. 2025 y sep. 2026) | `data_external/SIES_IES_vigentes_AAAA-MM.xlsx` | https://www.mifuturo.cl/instituciones-de-educacion-superior-en-chile/ (URL de cada archivo en `manifiesto_descargas.json`) | 2026-10-15 | institucion x corte anual | `nombre_institucion` -> `codigo_ies`; `codigo_ies` + `ano` |

Tamano y SHA-256 de cada archivo: `data_external/manifiesto_descargas.json`.

## 2. `ext_ine_poblacion_region_ano.csv`

| Columna | Tipo | Descripcion | Regla de transformacion |
|---|---|---|---|
| `region_codigo_subdere` | entero | Codigo SUBDERE de la region (1-16) | Asignado por hoja segun tabla `puente_region` |
| `hoja_ine` | texto | Nombre de la hoja en el libro INE | Literal |
| `ano` | entero | Ano calendario (2002-2035) | Encabezado de columna |
| `poblacion_total` | entero | Poblacion al 30 de junio, ambos sexos | Fila "Ambos sexos" bajo "Poblacion (al 30 de junio)" |
| `poblacion_hombres` / `poblacion_mujeres` | entero | Poblacion por sexo | Filas "Hombres" / "Mujeres" |
| `poblacion_0_14` / `poblacion_15_64` / `poblacion_65_mas` | entero | Poblacion por grandes grupos de edad | Filas homonimas |

## 3. `ext_sies_acreditacion_ies_ano.csv`

| Columna | Tipo | Descripcion | Regla de transformacion |
|---|---|---|---|
| `codigo_ies` | entero | Codigo de institucion SIES | Columna "Codigo de institucion" (el nombre varia por ano; se mapea por prefijo) |
| `tipo_institucion` | texto | Universidad, IP, CFT u otras | Literal |
| `nombre_institucion_sies` | texto | Nombre oficial en el corte | Literal |
| `autonomia` | texto | Estado de autonomia | Disponible desde el corte 2023-12; NULL antes |
| `acreditacion` | texto | Estado de acreditacion segun el listado | Literal |
| `acreditacion_norm` | texto | Acreditada / Acreditacion extendida / Bajo tutela / No acreditada | Armonizacion de variantes de mayusculas y asteriscos |
| `vigencia` | texto | Texto de vigencia de la acreditacion | Literal |
| `anos_acreditacion` | numerico | Anos de acreditacion | Conversion numerica; NULL si no aplica |
| `ano_corte` / `corte` | entero / texto | Ano y corte (AAAA-MM) | Del nombre del archivo; en 2026 solo existe el corte 2026-09 |
| `nombre_norm` | texto | Nombre en mayusculas sin tildes ni puntuacion | `norm()` del script |

## 4. `puente_region.csv`

| Columna | Descripcion |
|---|---|
| `nombre_region` | Nombre de region como viene en la base CNED (16 valores) |
| `region_codigo_subdere`, `region_nombre_estandar` | Campos de la Persona 1 |
| `hoja_ine` | Hoja equivalente en el libro INE |

Coincidencia: 100% de los 158.211 registros, 16/16 regiones.

## 5. `puente_institucion.csv`

| Columna | Descripcion |
|---|---|
| `nombre_institucion_cned` | Nombre tal como aparece en la base (cada grafia por separado) |
| `nombre_normalizado` | Nombre expandido (U. -> UNIVERSIDAD, IP -> INSTITUTO PROFESIONAL, C.F.T. -> CENTRO DE FORMACION TECNICA) |
| `codigo_ies` | Codigo SIES; NULL si no hay coincidencia |
| `nombre_institucion_sies` | Nombre SIES asociado |
| `metodo_cruce` | `exacto_normalizado`, `manual`, `aproximado_>=0.92` o `sin_coincidencia` |
| `similitud` | 1.0 en exacto/manual; razon de difflib en aproximado |

Coincidencia: 240 de 259 nombres (92,66%); 98,39% de los registros; 99,00% de la matricula de primer ano.
Metodos: 168 exactos, 47 manuales, 25 aproximados revisados, 19 sin coincidencia.

Registros sin coincidencia: se conservan con `codigo_ies = NULL` (miembro desconocido en la dimension).
15 de los 19 nombres desaparecen de la base CNED antes de 2018 (primer listado SIES). Cuatro siguen activos
(`C.F.T. ICCE`/`CFT ICCE`, `I.P. IPEGE`/`IP IPEGE`) y estan pendientes de verificacion manual.
Detalle en `cruce_no_coincidentes_institucion.csv`.

## 6. Reglas de uso

- Acreditacion 2012-2017: no existe listado comparable, queda NULL; no imputar con el valor de 2018.
- Cruce de acreditacion por ano: `codigo_ies` + `ano` contra `ano_corte`.
- `poblacion_*` es aditiva entre regiones pero no en el tiempo (stock al 30 de junio).
- Los indicadores regionales usan la region de la sede, no la del estudiante.
