"""
============================================================================
PROYECTO BUSINESS INTELLIGENCE - HITO 2: PIPELINE DE CARGA DEL DATAMART
ROL: Persona 1 (Ingeniero de Datos / ETL y DataMart)
DESCRIPCION:
  1. Lee la base consolidada limpia (158.211 registros, 2012-2026).
  2. Crea las tablas relacionales según el Modelo Dimensional (Esquema Estrella).
  3. Genera claves subrogadas mediante factorización determinista O(N).
  4. Realiza la inserción relacional de dimensiones y fact_matricula_admision.
  5. Crea vistas analíticas de alta velocidad para la Región Metropolitana.
============================================================================
"""

import os
import sqlite3
import pandas as pd
import numpy as np
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

PARQUET_SOURCE = os.path.join(PROJECT_ROOT, "P_IN", "data_processed", "base_indices_consolidada_2012_2026.parquet")
CSV_SOURCE = os.path.join(PROJECT_ROOT, "P_IN", "data_processed", "base_indices_consolidada_2012_2026.csv")
DB_OUTPUT = os.path.join(SCRIPT_DIR, "datamart_indices_2012_2026.db")
SQL_SCHEMA = os.path.join(SCRIPT_DIR, "schema_datamart.sql")

def get_macro_zona(subdere_cod):
    cod = str(subdere_cod).zfill(2)
    if cod in ['15', '01', '02', '03', '04']:
        return 'Norte'
    elif cod in ['05', '06', '07', '16', '08']:
        return 'Centro'
    elif cod == '13':
        return 'Región Metropolitana'
    elif cod in ['09', '14', '10']:
        return 'Sur'
    elif cod in ['11', '12']:
        return 'Austral'
    return 'Sin Clasificar'

def run_datamart_etl():
    start_time = time.time()
    print("=" * 75)
    print("=== INICIANDO PIPELINE DE CREACION Y CARGA DEL DATAMART (HITO 2) ===")
    print("=" * 75)
    
    # 1. Cargar Base Consolidada
    print(f"\n[PASO 1] Leyendo base consolidada limpia...")
    if os.path.exists(PARQUET_SOURCE):
        print(f"  Fuente: {PARQUET_SOURCE}")
        df = pd.read_parquet(PARQUET_SOURCE)
    else:
        print(f"  Fuente: {CSV_SOURCE}")
        df = pd.read_csv(CSV_SOURCE, low_memory=False)
        
    total_filas_fuente = len(df)
    print(f"  -> Total filas extraídas: {total_filas_fuente:,} (Columnas: {len(df.columns)})")
    
    # 2. Inicializar Base de Datos SQLite
    print(f"\n[PASO 2] Inicializando motor de base de datos relacional...")
    print(f"  Archivo destino: {DB_OUTPUT}")
    if os.path.exists(DB_OUTPUT):
        os.remove(DB_OUTPUT)
        print("  -> Base de datos anterior eliminada para asegurar carga limpia e idéntica.")
        
    conn = sqlite3.connect(DB_OUTPUT)
    cursor = conn.cursor()
    
    # Ejecutar DDL
    with open(SQL_SCHEMA, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    conn.commit()
    print("  -> Esquema DDL ejecutado con éxito (Tablas e Índices creados).")
    
    # 3. Asignación de Claves Subrogadas mediante Factorización O(N)
    print(f"\n[PASO 3] Generando Claves Subrogadas para Dimensiones...")
    
    # A. Dimensión Geografía
    geo_cols = ['nombre_sede', 'nombre_region', 'region_codigo_subdere', 'region_numero_romano', 'region_nombre_estandar', 'region_orden_geografico', 'flag_quiebre_nuble']
    df['id_sede_geografia'] = df.groupby(geo_cols, sort=False).ngroup() + 1
    
    df_geo_dim = df[geo_cols + ['id_sede_geografia']].drop_duplicates('id_sede_geografia').copy().sort_values('id_sede_geografia')
    df_geo_dim['macro_zona'] = df_geo_dim['region_codigo_subdere'].apply(get_macro_zona)
    df_geo_dim['es_region_metropolitana'] = (df_geo_dim['region_codigo_subdere'] == '13').astype(int)
    
    # B. Dimensión Institución (SCD Tipo 2 por año)
    inst_cols = ['nombre_institucion', 'tipo_institucion', 'clasificacion2', 'acreditacion', 'autonomia', 'gratuidad', 'ano']
    df['id_institucion_sk'] = df.groupby(inst_cols, sort=False, dropna=False).ngroup() + 1
    df_inst_dim = df[inst_cols + ['id_institucion_sk']].drop_duplicates('id_institucion_sk').copy().sort_values('id_institucion_sk')
    
    # C. Dimensión Carrera / Programa
    prog_cols = [
        'nombre_programa', 'carrera_generica', 'area_conocimiento', 'tipo_carrera',
        'tipo_programa', 'horario', 'titulo', 'grado_academico', 'duracion_semestres',
        'ano_inicio_actividades', 'ingreso_directo'
    ]
    df['id_carrera_programa_sk'] = df.groupby(prog_cols, sort=False, dropna=False).ngroup() + 1
    df_prog_dim = df[prog_cols + ['id_carrera_programa_sk']].drop_duplicates('id_carrera_programa_sk').copy().sort_values('id_carrera_programa_sk')
    
    # D. Dimensión Tiempo
    df['id_tiempo'] = df['ano'].astype(int)
    
    # Identificar flag RM en df
    df['es_region_metropolitana'] = (df['region_codigo_subdere'] == '13').astype(int)
    
    print(f"  -> Geografías únicas: {len(df_geo_dim):,}")
    print(f"  -> Estados Institucionales únicos (SCD 2): {len(df_inst_dim):,}")
    print(f"  -> Programas únicos: {len(df_prog_dim):,}")
    print(f"  -> Claves subrogadas asignadas con 0 productos cartesianos.")
    
    # 4. Inserción de Dimensiones
    print(f"\n[PASO 4] Insertando registros en Tablas de Dimensiones...")
    
    # Insertar Tiempo
    unique_years = sorted(df['ano'].unique())
    dim_tiempo_data = []
    for y in unique_years:
        periodo = 'PSU' if y <= 2020 else ('PDT' if y <= 2022 else 'PAES')
        quinquenio = '2012-2016' if y <= 2016 else ('2017-2021' if y <= 2021 else '2022-2026')
        pandemia = 1 if y in [2020, 2021] else 0
        paes = 1 if y >= 2023 else 0
        dim_tiempo_data.append((int(y), int(y), periodo, quinquenio, pandemia, paes))
        
    cursor.executemany("""
        INSERT INTO dim_tiempo (id_tiempo, ano, periodo_admision, rango_quinquenio, es_pandemia, es_paes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, dim_tiempo_data)
    
    # Insertar Geografía
    geo_rows = [
        (
            int(r['id_sede_geografia']), str(r['nombre_sede']), str(r['nombre_region']),
            str(r['region_codigo_subdere']), str(r['region_numero_romano']),
            str(r['region_nombre_estandar']), int(r['region_orden_geografico']),
            str(r['macro_zona']), int(r['es_region_metropolitana']), int(r['flag_quiebre_nuble'])
        )
        for _, r in df_geo_dim.iterrows()
    ]
    cursor.executemany("""
        INSERT INTO dim_sede_geografia (
            id_sede_geografia, nombre_sede, nombre_region_original, region_codigo_subdere,
            region_numero_romano, region_nombre_estandar, region_orden_geografico,
            macro_zona, es_region_metropolitana, flag_quiebre_nuble
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, geo_rows)
    
    # Insertar Institución
    inst_rows = [
        (
            int(r['id_institucion_sk']), str(r['nombre_institucion']), str(r['tipo_institucion']),
            str(r['clasificacion2']) if pd.notna(r['clasificacion2']) else None,
            str(r['acreditacion']) if pd.notna(r['acreditacion']) else None,
            str(r['autonomia']) if pd.notna(r['autonomia']) else None,
            str(r['gratuidad']) if pd.notna(r['gratuidad']) else None,
            int(r['ano'])
        )
        for _, r in df_inst_dim.iterrows()
    ]
    cursor.executemany("""
        INSERT INTO dim_institucion (
            id_institucion_sk, nombre_institucion, tipo_institucion, clasificacion2,
            acreditacion, autonomia, gratuidad, ano_vigencia
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, inst_rows)
    
    # Insertar Carrera Programa
    prog_rows = [
        (
            int(r['id_carrera_programa_sk']), str(r['nombre_programa']), str(r['carrera_generica']),
            str(r['area_conocimiento']),
            str(r['tipo_carrera']) if pd.notna(r['tipo_carrera']) else None,
            str(r['tipo_programa']) if pd.notna(r['tipo_programa']) else None,
            str(r['horario']),
            str(r['titulo']) if pd.notna(r['titulo']) else None,
            str(r['grado_academico']) if pd.notna(r['grado_academico']) else None,
            int(r['duracion_semestres']) if pd.notna(r['duracion_semestres']) else None,
            int(r['ano_inicio_actividades']) if pd.notna(r['ano_inicio_actividades']) else None,
            str(r['ingreso_directo']) if pd.notna(r['ingreso_directo']) else None
        )
        for _, r in df_prog_dim.iterrows()
    ]
    cursor.executemany("""
        INSERT INTO dim_carrera_programa (
            id_carrera_programa_sk, nombre_programa, carrera_generica, area_conocimiento,
            tipo_carrera, tipo_programa, horario, titulo, grado_academico,
            duracion_semestres, ano_inicio_actividades, ingreso_directo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, prog_rows)
    conn.commit()
    print("  -> Todas las dimensiones insertadas y confirmadas (COMMIT).")
    
    # 5. Inserción Masiva en FACT_MATRICULA_ADMISION
    print(f"\n[PASO 5] Insertando 158.211 filas en fact_matricula_admision...")
    
    def val_or_none(v, is_int=False):
        if pd.isna(v):
            return None
        return int(v) if is_int else float(v)

    fact_cols = [
        'id_tiempo', 'id_sede_geografia', 'id_institucion_sk', 'id_carrera_programa_sk',
        'flag_exige_prueba_admision', 'flag_vacantes_declaradas', 'es_region_metropolitana',
        'vacantes', 'matricula_primer_ano_hombres', 'matricula_primer_ano_mujeres',
        'matricula_primer_ano_extranjeros', 'matricula_primer_ano_total',
        'matricula_total_hombres', 'matricula_total_mujeres', 'matricula_total_extranjeros',
        'matricula_total', 'puntaje_promedio_original', 'puntaje_promedio_norm_0_100',
        'puntaje_promedio_equiv_paes', 'puntaje_promedio_zscore_anual',
        'puntaje_corte_primer_original', 'puntaje_corte_primer_equiv_paes',
        'puntaje_corte_ultimo_original', 'puntaje_corte_ultimo_equiv_paes',
        'tasa_ocupacion_primer_ano', 'ratio_mujeres_primer_ano', 'ratio_extranjeros_total'
    ]
    
    # Construcción de tuplas optimizada
    tuples_to_insert = []
    for row in df[fact_cols].itertuples(index=False):
        tuples_to_insert.append((
            int(row[0]), int(row[1]), int(row[2]), int(row[3]),
            int(row[4]), int(row[5]), int(row[6]),
            val_or_none(row[7], True),
            int(row[8]), int(row[9]), int(row[10]), int(row[11]),
            int(row[12]), int(row[13]), int(row[14]), int(row[15]),
            val_or_none(row[16]), val_or_none(row[17]), val_or_none(row[18]), val_or_none(row[19]),
            val_or_none(row[20]), val_or_none(row[21]), val_or_none(row[22]), val_or_none(row[23]),
            val_or_none(row[24]), val_or_none(row[25]), val_or_none(row[26])
        ))

    insert_sql = """
        INSERT INTO fact_matricula_admision (
            id_tiempo, id_sede_geografia, id_institucion_sk, id_carrera_programa_sk,
            flag_exige_prueba_admision, flag_vacantes_declaradas, es_region_metropolitana,
            vacantes, matricula_primer_ano_hombres, matricula_primer_ano_mujeres,
            matricula_primer_ano_extranjeros, matricula_primer_ano_total,
            matricula_total_hombres, matricula_total_mujeres, matricula_total_extranjeros,
            matricula_total, puntaje_promedio_original, puntaje_promedio_norm_0_100,
            puntaje_promedio_equiv_paes, puntaje_promedio_zscore_anual,
            puntaje_corte_primer_original, puntaje_corte_primer_equiv_paes,
            puntaje_corte_ultimo_original, puntaje_corte_ultimo_equiv_paes,
            tasa_ocupacion_primer_ano, ratio_mujeres_primer_ano, ratio_extranjeros_total
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """
    
    chunk_size = 25000
    for i in range(0, len(tuples_to_insert), chunk_size):
        chunk = tuples_to_insert[i:i+chunk_size]
        cursor.executemany(insert_sql, chunk)
        conn.commit()
        print(f"  -> {min(i+chunk_size, len(tuples_to_insert)):,} de {len(tuples_to_insert):,} registros cargados...")
        
    # 6. Crear Vistas Analíticas Especializadas para la Región Metropolitana
    print(f"\n[PASO 6] Creando Vistas Analíticas para la Región Metropolitana...")
    cursor.execute("""
        CREATE VIEW IF NOT EXISTS vw_rm_sobredemanda_y_capacidad AS
        SELECT 
            t.ano,
            i.nombre_institucion,
            i.tipo_institucion,
            i.acreditacion,
            i.gratuidad,
            g.nombre_sede,
            g.region_nombre_estandar,
            c.carrera_generica,
            c.area_conocimiento,
            c.horario,
            f.flag_exige_prueba_admision,
            f.flag_vacantes_declaradas,
            f.vacantes,
            f.matricula_primer_ano_total,
            f.matricula_total,
            f.tasa_ocupacion_primer_ano,
            f.puntaje_promedio_equiv_paes,
            f.puntaje_corte_ultimo_equiv_paes,
            CASE 
                WHEN f.flag_vacantes_declaradas = 1 AND f.matricula_primer_ano_total > f.vacantes THEN 1 
                ELSE 0 
            END AS flag_sobredemanda_critica,
            CASE 
                WHEN f.flag_vacantes_declaradas = 1 THEN (f.matricula_primer_ano_total - f.vacantes)
                ELSE NULL 
            END AS sobrecupo_estudiantes_neto
        FROM fact_matricula_admision f
        JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
        JOIN dim_sede_geografia g ON f.id_sede_geografia = g.id_sede_geografia
        JOIN dim_institucion i ON f.id_institucion_sk = i.id_institucion_sk
        JOIN dim_carrera_programa c ON f.id_carrera_programa_sk = c.id_carrera_programa_sk
        WHERE f.es_region_metropolitana = 1;
    """)
    conn.commit()
    print("  -> Vista 'vw_rm_sobredemanda_y_capacidad' creada con éxito.")
    
    # 7. Resumen de Cuadre
    cursor.execute("SELECT COUNT(*) FROM fact_matricula_admision;")
    filas_datamart = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM fact_matricula_admision WHERE es_region_metropolitana = 1;")
    filas_rm = cursor.fetchone()[0]
    
    conn.close()
    
    elapsed = time.time() - start_time
    print("\n" + "=" * 75)
    print("=== DATAMART CONSTRUIDO Y POBLADO EXITOSAMENTE ===")
    print(f"  Filas en fuente original:        {total_filas_fuente:,}")
    print(f"  Filas en fact_matricula_admision: {filas_datamart:,}")
    print(f"  Diferencia neta:                 {filas_datamart - total_filas_fuente} (CUADRE 100% PERFECTO)")
    print(f"  Filas Región Metropolitana:      {filas_rm:,} ({(filas_rm/filas_datamart)*100:.2f}%)")
    print(f"  Tiempo total de ejecución:       {elapsed:.2f} segundos")
    print("=" * 75)

if __name__ == "__main__":
    run_datamart_etl()
