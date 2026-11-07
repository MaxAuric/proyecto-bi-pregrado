# 🔌 Guía de Conexión: Power BI Desktop al DataMart Relacional
## Proyecto Business Intelligence — Hito 2 y Entrega Final
**Para:** Persona 4 (Desarrollador BI)  
**Elaborado por:** Persona 1 (Ingeniero de Datos / ETL y DataMart)

---

### ⚠️ Regla Estricta de la Pauta Docente:
> *«El panel debe estar conectado al DataMart, no al Excel»* (Página 2 y 5 de la pauta).

Para cumplir con este requisito al 100%, Persona 1 implementó el DataMart en una base de datos relacional estándar:
📁 **Ruta del DataMart:** `Avance Hito 2/03_DATAMART_SCRIPTS_DDL_Y_CARGA/datamart_indices_2012_2026.db`

---

### Método 1: Conexión Nativa mediante Conector ODBC (Recomendado para Producción)

1. **Instalar el Driver SQLite ODBC (si no lo tienes en Windows):**
   * Descargar el driver oficial gratuito: [SQLite ODBC Driver for Windows](http://www.ch-werner.de/sqliteodbc/) (`sqliteodbc_w64.exe`).
   * Instalar el ejecutable (tarda 10 segundos).
2. **Abrir Power BI Desktop:**
   * Ir a **Obtener Datos (Get Data)** $\rightarrow$ Más... $\rightarrow$ **ODBC**.
   * En la cadena de conexión o DSN:
     * Si creas un DSN de usuario en el *Administrador de orígenes de datos ODBC (64 bits)* de Windows: seleccionar el DSN que apunte a `datamart_indices_2012_2026.db`.
     * O ingresar directamente en cadena de conexión:
       ```text
       Driver={SQLite3 ODBC Driver};Database=C:\Users\Shila\Documents\Otros\Proy IN\Avance Hito 2\03_DATAMART_SCRIPTS_DDL_Y_CARGA\datamart_indices_2012_2026.db;
       ```
3. **Seleccionar las Tablas en el Navegador:**
   * `fact_matricula_admision`
   * `dim_tiempo`
   * `dim_institucion`
   * `dim_sede_geografia`
   * `dim_carrera_programa`
   * O directamente la vista: `vw_rm_sobredemanda_y_capacidad`.

---

### Método 2: Conexión Directa en Power BI con Script Python (Cero Instalación de Drivers)

Si no quieres instalar drivers ODBC en tu máquina, Power BI incluye soporte nativo para scripts en Python:

1. En Power BI Desktop, ir a **Obtener Datos** $\rightarrow$ **Script de Python**.
2. Pegar el siguiente código que consulta directamente el DataMart:
```python
import sqlite3
import pandas as pd

# Conexión directa al DataMart
db_path = r"C:\Users\Shila\Documents\Otros\Proy IN\Avance Hito 2\03_DATAMART_SCRIPTS_DDL_Y_CARGA\datamart_indices_2012_2026.db"
conn = sqlite3.connect(db_path)

# Cargar dimensiones y hechos
dim_tiempo = pd.read_sql("SELECT * FROM dim_tiempo", conn)
dim_sede_geografia = pd.read_sql("SELECT * FROM dim_sede_geografia", conn)
dim_institucion = pd.read_sql("SELECT * FROM dim_institucion", conn)
dim_carrera_programa = pd.read_sql("SELECT * FROM dim_carrera_programa", conn)
fact_matricula_admision = pd.read_sql("SELECT * FROM fact_matricula_admision", conn)

# Vista especializada de la Región Metropolitana
vw_rm_sobredemanda = pd.read_sql("SELECT * FROM vw_rm_sobredemanda_y_capacidad", conn)

conn.close()
```
3. Dar clic en **Aceptar**: Power BI cargará las tablas directamente desde el motor SQLite, certificando ante el profesor que la fuente es el DataMart relacional.

---

### Relaciones a configurar en la Vista de Modelo de Power BI (Esquema Estrella):

* `fact_matricula_admision[id_tiempo]` $\rightarrow$ `dim_tiempo[id_tiempo]` (Muchos a Uno `*:1`, Dirección única).
* `fact_matricula_admision[id_sede_geografia]` $\rightarrow$ `dim_sede_geografia[id_sede_geografia]` (Muchos a Uno `*:1`).
* `fact_matricula_admision[id_institucion_sk]` $\rightarrow$ `dim_institucion[id_institucion_sk]` (Muchos a Uno `*:1`).
* `fact_matricula_admision[id_carrera_programa_sk]` $\rightarrow$ `dim_carrera_programa[id_carrera_programa_sk]` (Muchos a Uno `*:1`).

---

### Filtro Maestro sugerido para el Panel de la RM:
En el panel de Power BI, para cumplir con el feedback docente de enfocarse en la Región Metropolitana:
* Agregar un filtro a nivel de página o informe: `dim_sede_geografia[es_region_metropolitana] = 1`.
* O utilizar la tabla pre-filtrada `vw_rm_sobredemanda_y_capacidad`.

