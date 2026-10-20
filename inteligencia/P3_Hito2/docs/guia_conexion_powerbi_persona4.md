# Guía Rápida de Conexión a Power BI - Para Persona 4 (Desarrollador BI)
## De: Persona 3 (Arquitecto de Bases de Datos)
**¡Hola Persona 4!** Tu DataMart ya está completamente construido, cargado con los **158.211 registros oficiales** y verificado con 0 errores y 0 pérdidas de datos.

Aquí tienes todo lo que necesitas para conectar Power BI en 5 minutos y empezar a diseñar tu Dashboard y programar tus medidas DAX.

---

### 1. Dónde están tus datos

Tienes dos formas de conectarte (elige la que te sea más cómoda):

#### Opcion A (La mas rapida y recomendada - Cero configuracion):
En la carpeta:
`inteligencia/P3_Hito2/data/tablas_csv_powerbi/`
Tienes las 8 tablas relacionales del DataMart exportadas en formato CSV de alto rendimiento:
1. `fact_matricula_oferta.csv` (158.211 filas - Hecho principal)
2. `fact_poblacion_regional.csv` (240 filas - Fuente Externa 1: INE)
3. `dim_tiempo.csv` (15 filas: 2012–2026)
4. `dim_geografia.csv` (17 filas: 16 regiones oficiales + desconocido)
5. `dim_sede.csv` (115 filas)
6. `dim_institucion.csv` (260 filas: incluye código SIES)
7. `dim_institucion_calidad_anual.csv` (1.994 filas: acreditación y años SIES por institución y año)
8. `dim_programa.csv` (8.868 filas)

**Pasos en Power BI Desktop:**
1. Clic en **Obtener datos** $\rightarrow$ **Texto o CSV** (o **Obtener datos** $\rightarrow$ **Más...** $\rightarrow$ **Carpeta** y seleccionas la ruta `inteligencia/P3_Hito2/data/tablas_csv_powerbi/`).
2. Cargas las tablas en tu modelo.

#### Opcion B (Base de datos SQLite nativa):
El archivo de la base de datos relacional está en:
`inteligencia/P3_Hito2/data/datamart_educacion_superior.db`
Puedes conectarte usando el **Controlador ODBC de SQLite** o ejecutando un script de Python de 3 líneas en Power BI (**Obtener datos** $\rightarrow$ **Script de Python**):
```python
import sqlite3
import pandas as pd
conn = sqlite3.connect(r"A:\Descargassss\Entrega2InteligenciaNegocio\inteligencia\P3_Hito2\data\datamart_educacion_superior.db")
fact_matricula = pd.read_sql("SELECT * FROM fact_matricula_oferta", conn)
fact_poblacion = pd.read_sql("SELECT * FROM fact_poblacion_regional", conn)
dim_tiempo = pd.read_sql("SELECT * FROM dim_tiempo", conn)
dim_geografia = pd.read_sql("SELECT * FROM dim_geografia", conn)
dim_sede = pd.read_sql("SELECT * FROM dim_sede", conn)
dim_institucion = pd.read_sql("SELECT * FROM dim_institucion", conn)
dim_programa = pd.read_sql("SELECT * FROM dim_programa", conn)
dim_calidad = pd.read_sql("SELECT * FROM dim_institucion_calidad_anual", conn)
```

---

### 2. Cómo configurar las Relaciones en la "Vista de Modelo"

En la pestaña **Vista de Modelo** de Power BI, une las tablas mediante relaciones **Uno a Varios ($1 \rightarrow *)$**, con **dirección de filtro única** (desde las dimensiones hacia las tablas de hechos):

| Tabla Origen (1) | Campo Origen | Tabla Destino (*) | Campo Destino | Tipo Relación |
| :--- | :--- | :--- | :--- | :---: |
| `dim_tiempo` | `id_tiempo` | `fact_matricula_oferta` | `id_tiempo` | $1 \rightarrow *$ |
| `dim_geografia` | `id_geografia` | `fact_matricula_oferta` | `id_geografia` | $1 \rightarrow *$ |
| `dim_sede` | `id_sede` | `fact_matricula_oferta` | `id_sede` | $1 \rightarrow *$ |
| `dim_institucion` | `id_institucion` | `fact_matricula_oferta` | `id_institucion` | $1 \rightarrow *$ |
| `dim_programa` | `id_programa` | `fact_matricula_oferta` | `id_programa` | $1 \rightarrow *$ |
| `dim_geografia` | `id_geografia` | `dim_sede` | `id_geografia` | $1 \rightarrow *$ |
| `dim_tiempo` | `id_tiempo` | `fact_poblacion_regional`| `id_tiempo` | $1 \rightarrow *$ |
| `dim_geografia` | `id_geografia` | `fact_poblacion_regional`| `id_geografia` | $1 \rightarrow *$ |
| `dim_institucion` | `id_institucion` | `dim_institucion_calidad_anual`| `id_institucion` | $1 \rightarrow *$ |

---

### 3. Fórmulas DAX listas para tus 3 Preguntas de Negocio

Copia y pega estas medidas DAX para responder exactamente lo que pide la pauta:

#### Pregunta 1: Equidad Territorial (Matrícula vs Población INE)
```dax
Matricula_Primer_Ano_Total = SUM(fact_matricula_oferta[matricula_primer_ano_total])

Poblacion_15_64 = SUM(fact_poblacion_regional[poblacion_15_64])

Matricula_Por_1000_Hab = 
DIVIDE(
    [Matricula_Primer_Ano_Total] * 1000,
    [Poblacion_15_64]
)
```

#### Pregunta 2: Uso de Capacidad y Tasa de Ocupación de Vacantes
```dax
Vacantes_Declaradas = 
CALCULATE(
    SUM(fact_matricula_oferta[vacantes]),
    fact_matricula_oferta[flag_vacantes_declaradas] = 1
)

Matricula_En_Vacantes_Declaradas = 
CALCULATE(
    SUM(fact_matricula_oferta[matricula_primer_ano_total]),
    fact_matricula_oferta[flag_vacantes_declaradas] = 1
)

Tasa_Ocupacion_Vacantes = 
DIVIDE(
    [Matricula_En_Vacantes_Declaradas],
    [Vacantes_Declaradas]
)
```
*(Formatea esta medida como Porcentaje `%` en Power BI).*

#### Pregunta 3: Calidad y Acreditación (SIES)
```dax
Matricula_Total_Sistema = SUM(fact_matricula_oferta[matricula_total])

Matricula_Instituciones_Acreditadas = 
CALCULATE(
    SUM(fact_matricula_oferta[matricula_primer_ano_total]),
    dim_institucion_calidad_anual[acreditacion_sies] = "Acreditada"
)

Pct_Matricula_Acreditada = 
DIVIDE(
    [Matricula_Instituciones_Acreditadas],
    [Matricula_Primer_Ano_Total]
)
```

---

### 4. Jerarquías Sugeridas para tus Visualizaciones

Crea con clic derecho estas jerarquías para que los usuarios puedan hacer *Drill-down*:
1. **Jerarquía Geográfica:** `zona_geografica` $\rightarrow$ `region_nombre_estandar` $\rightarrow$ `nombre_sede`.
2. **Jerarquía Académica:** `area_conocimiento` $\rightarrow$ `carrera_generica` $\rightarrow$ `nombre_programa`.
3. **Jerarquía Institucional:** `tipo_institucion` $\rightarrow$ `clasificacion2` $\rightarrow$ `nombre_institucion`.

¡Cualquier duda me avisas! El DataMart está listo para que te luzcas con el Dashboard.
