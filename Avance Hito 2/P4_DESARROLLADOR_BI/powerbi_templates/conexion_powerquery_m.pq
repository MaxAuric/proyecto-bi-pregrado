let
    // Script de conexion maestro Power BI
    // Hito 2: Modelo dimensional, jerarquias y validacion de conexion
    // Ruta dinamica o configurable a la base de datos DataMart SQLite
    RutaBaseDatos = "C:\Users\repor\Downloads\Entrega N°3\proyecto-bi-pregrado\Avance Hito 2\P1\03_DATAMART_SCRIPTS_DDL_Y_CARGA\datamart_indices_2012_2026.db",
    
    // Metodo 1: Via Script Python embebido (Portabilidad total, sin instalar drivers)
    ScriptPythonCarga = "
import sqlite3
import pandas as pd

conn = sqlite3.connect(r'" & RutaBaseDatos & "')
dim_tiempo = pd.read_sql('SELECT * FROM dim_tiempo', conn)
dim_sede_geografia = pd.read_sql('SELECT * FROM dim_sede_geografia', conn)
dim_institucion = pd.read_sql('SELECT * FROM dim_institucion', conn)
dim_carrera_programa = pd.read_sql('SELECT * FROM dim_carrera_programa', conn)
dim_poblacion_rm = pd.read_sql('SELECT * FROM dim_poblacion_rm', conn)
fact_matricula_admision = pd.read_sql('SELECT * FROM fact_matricula_admision', conn)
vw_rm_sobredemanda = pd.read_sql('SELECT * FROM vw_rm_sobredemanda_y_capacidad', conn)
conn.close()
"
in
    ScriptPythonCarga

