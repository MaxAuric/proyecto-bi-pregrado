# Guia de Conexion Power BI al DataMart Estrella RM

## Resumen
Este documento describe el proceso paso a paso para conectar Power BI Desktop al archivo **DataMart_Estrella_RM_PowerBI.xlsx** ubicado en `Final/00_DATAMART_LISTO_PARA_POWERBI/`. La conexion es instantanea (2-3 segundos) y no requiere scripts Python dentro de Power Query.

---

## 1. Requisitos Previos

- Power BI Desktop (version actualizada Septiembre 2026 o superior)
- Archivo: `Final/00_DATAMART_LISTO_PARA_POWERBI/DataMart_Estrella_RM_PowerBI.xlsx`
- Acceso a la carpeta del proyecto

---

## 2. Pasos de Conexion

### Paso 1: Obtener Datos de Excel
1. Abrir Power BI Desktop
2. Cinta **Inicio** -> **Obtener datos** -> **Excel**
3. Navegar a: `Final/00_DATAMART_LISTO_PARA_POWERBI/DataMart_Estrella_RM_PowerBI.xlsx`
4. Click **Abrir**

### Paso 2: Seleccionar Hojas del Modelo Estrella
En el navegador, marcar **exactamente estas 6 hojas/ tablas**:

| Hoja Excel | Tabla en Power BI | Rol | Filas Esperadas |
|------------|-------------------|-----|-----------------|
| `dim_tiempo_ine_rm` | `dim_tiempo_ine_rm` | Dimension Tiempo + Demografia INE | 15 |
| `dim_sede_geografia` | `dim_sede_geografia` | Dimension Sede/Geografia RM | 22 |
| `dim_institucion_sies` | `dim_institucion_sies` | Dimension Institucion SCD2 + SIES | 1,298 |
| `dim_carrera_programa` | `dim_carrera_programa` | Dimension Carrera/Programa | 5,108 |
| `fact_matricula_admision` | `fact_matricula_admision` | Tabla de Hechos Central | 58,926 |
| `agg_resumen_institucion_rm` | `agg_resumen_institucion_rm` | Tabla Agregada Anual Institucion | 1,298 |

**NO marcar:** `puente_institucion_sies` (es tabla puente de auditoria, no parte del modelo analitico)

Click **Cargar** (no "Transformar datos" - los datos ya estan limpios y listos)

### Paso 3: Verificar Relaciones (Vista Modelo)
Power BI detectara automaticamente las relaciones 1:* basadas en las claves:

```
dim_tiempo_ine_rm (1) ----< fact_matricula_admision (> id_tiempo)
dim_sede_geografia (1) ----< fact_matricula_admision (> id_sede_geografia)
dim_institucion_sies (1) ----< fact_matricula_admision (> id_institucion_sk)
dim_carrera_programa (1) ----< fact_matricula_admision (> id_carrera_programa_sk)
```

**Verificar direccion de filtro:** Todas deben ser **Unidireccional (1 -> *)** desde dimension a hecho.

### Paso 4: Configurar Propiedades de Columnas Clave
Para cada tabla de dimension, marcar la columna clave como **"No resumir"** en Propiedades de columna:
- `dim_tiempo_ine_rm[id_tiempo]`
- `dim_sede_geografia[id_sede_geografia]`
- `dim_institucion_sies[id_institucion_sk]`
- `dim_carrera_programa[id_carrera_programa_sk]`

---

## 3. Crear Tabla de Medidas DAX

### Paso 1: Crear Tabla Vacia
1. Cinta **Modelado** -> **Nueva tabla** (o click derecho en panel Campos -> Nueva tabla)
2. Nombre: `Medidas DAX RM`
3. En la barra de formula escribir: `Medidas DAX RM = { BLANK() }` y Enter
4. Click derecho en la tabla -> **Ocultar en vista de informe** (opcional, solo para organizar)

### Paso 2: Pegar Medidas
1. Abrir archivo: `docs/medidas_dax_completas_rm.dax`
2. Copiar cada bloque de medida (desde el nombre hasta el cierre)
3. En Power BI: Click derecho en `Medidas DAX RM` -> **Nueva medida**
4. Pegar y Enter
5. Repetir para todas las medidas

### Paso 3: Organizar en Carpetas (Display Folders)
En el panel Propiedades de cada medida, asignar **Carpeta de visualizacion**:

| Medida | Carpeta |
|--------|---------|
| Matricula 1er Ano RM, Matricula Total RM, Vacantes Ofrecidas RM, Sobrecupo Neto Alumnos RM, Vacantes Ociosas Netas RM, Matricula 1er Ano Hombres RM, Matricula 1er Ano Mujeres RM, Matricula 1er Ano Extranjeros RM | `01 Conteos Base` |
| Tasa Ocupacion Vacantes RM (%), Tasa Sobredemanda RM (%), Tasa Ocupacion Solo Con Vacantes (%) | `02 Tasas Ocupacion` |
| Secciones Lab Planificadas Base 35, Secciones Lab Reales Requeridas Base 35, Secciones Lab Extra por Sobrecupo, Tasa Saturacion Laboratorios RM (%), Holgura Laboratorios 35 Puestos, Pct Ofertas Con Secciones Extra | `03 Laboratorios` |
| Tasa Renovacion Cohorte RM (%), Tasa Retencion Aparente RM (%), Tasa Renovacion Por Institucion (%) | `04 Renovacion Retencion` |
| Puntaje PAES Promedio Ponderado RM, Puntaje PAES Corte Ponderado RM, Tasa Heterogeneidad PAES Promedio (%), Brecha PAES Max Min Promedio, Brecha Corte Vs Media RM PAES, Indice Presion Selectiva KPI | `05 Selectividad PAES` |
| Cuota Mercado Matricula RM (%), Tasa Absorcion Juvenil INE RM (%), Tasa Cobertura Bruta INE RM (%), Tasa Oferta Vacantes 1000 Jovenes RM, Variacion Interanual Matricula 1er Ano (%) | `06 Demografia INE` |
| Ratio Mujeres 1er Ano (%), Ratio Mujeres Total (%), Ratio Extranjeros 1er Ano (%), Ratio Extranjeros Total (%) | `07 Genero Extranjeros` |
| Cantidad Ofertas Academicas, Cantidad Instituciones, Cantidad Sedes, Cantidad Carreras, Cantidad Anos | `08 Conteos Filtros` |
| Matricula 1er Ano Con Prueba, Matricula 1er Ano Acreditadas, Matricula 1er Ano Universidades, Matricula 1er Ano IP, Matricula 1er Ano CFT, Matricula 1er Ano FF.AA. | `09 Filtros Especificos` |
| Semaforo Ocupacion Vacantes, Semaforo Saturacion Laboratorios, Semaforo Posicionamiento Competitivo, Semaforo Nivel Saturacion Sede, Semaforo Presion Capacidad Programa | `10 Semaforos Decision` |
| Matricula 1er Ano Ano Anterior, Tasa Ocupacion Ano Anterior, Crecimiento Matricula Interanual | `11 Tendencias` |
| Ofertas Activas RM, Vacantes Totales RM Agregado, Matricula 1er Ano RM Agregado, Matricula Total RM Agregado, Tasa Ocupacion RM Agregado (%), Cuota Mercado RM Agregado (%), Puntaje PAES Ponderado RM Agregado, Secciones Lab Planificadas RM Agregado, Secciones Lab Reales RM Agregado, Secciones Extra Sobrecupo RM Agregado | `12 Tabla Agregada` |

---

## 4. Configurar Formato de Medidas

| Tipo de Medida | Formato | Decimales |
|----------------|---------|-----------|
| Conteos (Matricula, Vacantes, etc.) | Entero (#,##0) | 0 |
| Tasas y Porcentajes | Porcentaje (##0.0%) | 1 |
| Puntajes PAES | Decimal (#,##0.0) | 1 |
| Semaforos (texto) | Texto | - |

---

## 5. Crear Jerarquias para Drill-Down

### En `dim_sede_geografia`:
Click derecho -> **Nueva jerarquia** -> Nombre: `Jerarquia Geografica RM`
1. `macro_zona` (solo RM)
2. `region_nombre_estandar` (solo RM)
3. `nombre_sede` (comuna/campus en Santiago)

### En `dim_institucion_sies`:
Click derecho -> **Nueva jerarquia** -> Nombre: `Jerarquia Institucional`
1. `tipo_institucion` (Universidad, Instituto Profesional, Centro de Formacion Tecnica, Institucion de las FF.AA. y Orden)
2. `subtipo_institucion` (Universidades Estatales CRUCH, Privadas CRUCH, etc.)
3. `nombre_institucion`

### En `dim_carrera_programa`:
Click derecho -> **Nueva jerarquia** -> Nombre: `Jerarquia Academica`
1. `area_conocimiento` (11 areas oficiales)
2. `es_area_stem` (STEM vs Otras)
3. `carrera_generica` (284 carreras genericas)
4. `nombre_programa` (programa especifico)

### En `dim_tiempo_ine_rm`:
Click derecho -> **Nueva jerarquia** -> Nombre: `Jerarquia Temporal`
1. `rango_quinquenio` (2012-2016, 2017-2021, 2022-2026)
2. `periodo_admision` (PSU, PDT, PAES)
3. `ano` (2012 a 2026)
4. `estado_sanitario` (Pre-Pandemia, Pandemia COVID-19, Post-Pandemia)

---

## 6. Configurar Segmentadores Obligatorios (Pauta Oficial)

Crear **4 segmentadores** en la pagina de filtros principales:

| Segmentador | Campo | Tipo Control | Configuracion |
|-------------|-------|--------------|---------------|
| **Ano** | `dim_tiempo_ine_rm[ano]` | Lista desplegable / Lista horizontal | Seleccion multiple activada, orden ascendente |
| **Institucion** | `dim_institucion_sies[nombre_institucion]` | Busqueda predictiva / Lista | Orden alfabetico, 69 instituciones activas 2026 |
| **Sede/Comuna RM** | `dim_sede_geografia[nombre_sede]` | Botones / Lista | Solo 22 sedes en RM |
| **Tramo Acreditacion SIES** | `dim_institucion_sies[tramo_acreditacion_sies]` | Lista / Casillas | 4 valores: Excelencia, Avanzada, Basica, No Acreditada |

**Filtro de pagina predeterminado (nivel de pagina):**
- `dim_sede_geografia[es_region_metropolitana] = 1` (siempre activo, oculta al usuario)

---

## 7. Validacion de Cuadre (Sanity Check)

Despues de cargar, crear una tabla simple con:

| Medida | Valor Esperado (2026) |
|--------|----------------------|
| `Cantidad Ofertas Academicas` | ~4,500-5,000 (ofertas activas 2026) |
| `Matricula 1er Ano RM` | ~25,000-30,000 |
| `Vacantes Ofrecidas RM` | ~28,000-33,000 |
| `Tasa Ocupacion Vacantes RM (%)` | ~85-95% |
| `Cantidad Instituciones` | 69 (activas 2026) |
| `Cantidad Sedes` | 22 (comunas/campus RM) |
| `Puntaje PAES Promedio Ponderado RM` | ~650-750 |

Si los numeros coinciden -> **Conexion exitosa y cuadre validado**

---

## 8. Respaldo: Conexion a SQLite (Opcional)

Si se prefiere conexion directa a base de datos:

1. **Obtener datos** -> **Mas...** -> **SQLite database**
2. Archivo: `Final/00_DATAMART_LISTO_PARA_POWERBI/datamart_estrella_rm_final.db`
3. Seleccionar las mismas 6 tablas
4. Mismo proceso de relaciones y medidas

**Nota:** La conexion Excel es mas rapida y portable (sin drivers ODBC).

---

## 9. Archivos de Referencia

- `Final/00_DATAMART_LISTO_PARA_POWERBI/DataMart_Estrella_RM_PowerBI.xlsx` - Fuente principal
- `Final/00_DATAMART_LISTO_PARA_POWERBI/datamart_estrella_rm_final.db` - Respaldo SQLite
- `docs/medidas_dax_completas_rm.dax` - Todas las medidas DAX listas para copiar
- `docs/diseno_dashboard_3_vistas_rm.md` - Especificacion de las 3 paginas del dashboard
- `scripts/validar_modelo_powerbi.py` - Script de validacion automatica (ver abajo)

---

## 10. Script de Validacion Automatica

Ejecutar despues de crear el modelo en Power BI para certificar cuadre:

```python
# scripts/validar_modelo_powerbi.py
# Se ejecuta en Python local contra el .db para comparar con Power BI
import sqlite3
import pandas as pd

conn = sqlite3.connect(r"Final/00_DATAMART_LISTO_PARA_POWERBI/datamart_estrella_rm_final.db")

# Verificar conteos
tablas = ["dim_tiempo_ine_rm", "dim_sede_geografia", "dim_institucion_sies", 
          "dim_carrera_programa", "fact_matricula_admision", "agg_resumen_institucion_rm"]

for t in tablas:
    n = pd.read_sql(f"SELECT COUNT(*) as n FROM {t}", conn).iloc[0,0]
    print(f"{t}: {n} filas")

# Verificar cuadre hechos vs dimensiones
hechos = pd.read_sql("SELECT COUNT(*) as n FROM fact_matricula_admision", conn).iloc[0,0]
print(f"\nTotal hechos: {hechos}")

# Verificar integridad referencial
for dim, fk in [("dim_tiempo_ine_rm", "id_tiempo"), ("dim_sede_geografia", "id_sede_geografia"),
                ("dim_institucion_sies", "id_institucion_sk"), ("dim_carrera_programa", "id_carrera_programa_sk")]:
    huerfanos = pd.read_sql(f"""
        SELECT COUNT(*) as n FROM fact_matricula_admision f
        LEFT JOIN {dim} d ON f.{fk} = d.{fk}
        WHERE d.{fk} IS NULL
    """, conn).iloc[0,0]
    print(f"Huerfanos en {dim}: {huerfanos}")

conn.close()
print("\nValidacion completa. Todos los huerfanos deben ser 0.")
```

---

**Fin de la guia.** Con estos pasos, Persona 4 tiene el modelo cargado, medidas creadas, jerarquias configuradas y segmentadores listos para construir las 3 vistas ejecutivas.