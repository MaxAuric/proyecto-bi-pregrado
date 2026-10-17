import os
import sys
import sqlite3
import pandas as pd
import numpy as np

# Rutas base
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
P1_DATA = os.path.join(BASE_DIR, "P_IN", "data_processed", "base_indices_consolidada_2012_2026.csv")
P2_INE = os.path.join(BASE_DIR, "P2_Hito1", "data_processed", "ext_ine_poblacion_region_ano.csv")
P2_SIES = os.path.join(BASE_DIR, "P2_Hito1", "data_processed", "ext_sies_acreditacion_ies_ano.csv")
P2_PUENTE_INST = os.path.join(BASE_DIR, "P2_Hito1", "data_processed", "puente_institucion.csv")
P2_PUENTE_REG = os.path.join(BASE_DIR, "P2_Hito1", "data_processed", "puente_region.csv")

SQL_DDL_PATH = os.path.join(BASE_DIR, "P3_Hito2", "sql", "01_ddl_datamart.sql")
SQL_VIEWS_PATH = os.path.join(BASE_DIR, "P3_Hito2", "sql", "02_views_powerbi.sql")
DB_PATH = os.path.join(BASE_DIR, "P3_Hito2", "data", "datamart_educacion_superior.db")
EXPORT_CSV_DIR = os.path.join(BASE_DIR, "P3_Hito2", "data", "tablas_csv_powerbi")
os.makedirs(EXPORT_CSV_DIR, exist_ok=True)

def asignar_zona(cod):
    cod = str(cod).zfill(2)
    if cod in ['15', '01', '02']:
        return 'Norte Grande'
    elif cod in ['03', '04']:
        return 'Norte Chico'
    elif cod in ['05', '13', '06', '07', '16', '08']:
        return 'Centro'
    elif cod in ['09', '14', '10']:
        return 'Sur'
    elif cod in ['11', '12']:
        return 'Austral'
    return 'Sin Dato'

def run():
    print("==================================================================")
    print("=== PIPELINE DE CARGA DEL DATAMART - PERSONA 3 (HITO 2) ===")
    print("==================================================================")
    
    # 1. Crear base de datos y esquema DDL
    print(f"\n[PASO 1] Inicializando DataMart SQLite en:\n  {DB_PATH}")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    with open(SQL_DDL_PATH, "r", encoding="utf-8") as f:
        ddl_script = f.read()
    cursor.executescript(ddl_script)
    conn.commit()
    print("  -> Tablas e indices creados exitosamente segun 01_ddl_datamart.sql")

    # 2. Cargar datos base de Persona 1
    print(f"\n[PASO 2] Cargando base oficial consolidada (Persona 1)...")
    df_base = pd.read_csv(P1_DATA, low_memory=False)
    print(f"  -> Total filas leidas: {len(df_base):,} (Esperado: 158.211)")
    assert len(df_base) == 158211, f"Error: Se esperaban 158.211 registros, hay {len(df_base)}"

    # 3. Poblar Dim_Tiempo
    print("\n[PASO 3] Poblando dim_tiempo...")
    anos = sorted(df_base['ano'].unique())
    tiempo_rows = []
    for a in anos:
        a = int(a)
        if a <= 2015:
            quinq = "2012-2015 (Pre-Gratuidad)"
        elif a <= 2020:
            quinq = "2016-2020 (Implementacion Gratuidad)"
        else:
            quinq = "2021-2026 (Era Post-Pandemia y PAES)"
            
        prueba = "PSU" if a <= 2020 else ("PDT" if a <= 2022 else "PAES")
        gratuidad_vig = 1 if a >= 2016 else 0
        nuble_vig = 1 if a >= 2018 else 0
        pandemia_vig = 1 if a in [2020, 2021] else 0
        
        tiempo_rows.append((a, a, quinq, prueba, gratuidad_vig, nuble_vig, pandemia_vig))
        
    cursor.executemany("""
        INSERT INTO dim_tiempo (id_tiempo, ano, periodo_quinquenal, tipo_prueba_admision, flag_gratuidad_vigente, flag_reforma_nuble, flag_pandemia)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, tiempo_rows)
    conn.commit()
    print(f"  -> {len(tiempo_rows)} anos cargados en dim_tiempo (2012-2026)")

    # 4. Poblar Dim_Geografia
    print("\n[PASO 4] Poblando dim_geografia...")
    # Registro Desconocido (-1)
    cursor.execute("""
        INSERT INTO dim_geografia (id_geografia, region_codigo_subdere, region_nombre_estandar, region_numero_romano, zona_geografica, orden_geografico)
        VALUES (-1, '-1', 'Sin Dato / Desconocido', 'N/A', 'Sin Dato', 99)
    """)
    
    geo_df = df_base[['region_codigo_subdere', 'region_nombre_estandar', 'region_numero_romano', 'region_orden_geografico']].drop_duplicates().sort_values('region_orden_geografico')
    geo_map = {} # codigo -> id_geografia
    geo_rows = []
    for idx, row in enumerate(geo_df.itertuples(), start=1):
        cod_str = str(int(row.region_codigo_subdere)).zfill(2)
        geo_map[cod_str] = idx
        geo_map[int(row.region_codigo_subdere)] = idx
        zona = asignar_zona(cod_str)
        geo_rows.append((idx, cod_str, row.region_nombre_estandar, row.region_numero_romano, zona, int(row.region_orden_geografico)))
        
    cursor.executemany("""
        INSERT INTO dim_geografia (id_geografia, region_codigo_subdere, region_nombre_estandar, region_numero_romano, zona_geografica, orden_geografico)
        VALUES (?, ?, ?, ?, ?, ?)
    """, geo_rows)
    conn.commit()
    print(f"  -> {len(geo_rows)} regiones cargadas en dim_geografia + 1 registro desconocido (-1)")

    # 5. Poblar Dim_Sede
    print("\n[PASO 5] Poblando dim_sede...")
    cursor.execute("""
        INSERT INTO dim_sede (id_sede, nombre_sede, id_geografia, region_codigo_subdere, region_nombre)
        VALUES (-1, 'Sin Dato / Desconocida', -1, '-1', 'Sin Dato')
    """)
    
    sede_df = df_base[['nombre_sede', 'region_codigo_subdere', 'region_nombre_estandar']].drop_duplicates().sort_values('nombre_sede')
    sede_map = {} # nombre_sede -> id_sede
    sede_rows = []
    for idx, row in enumerate(sede_df.itertuples(), start=1):
        cod_str = str(int(row.region_codigo_subdere)).zfill(2)
        id_geo = geo_map.get(cod_str, -1)
        sede_map[row.nombre_sede] = idx
        sede_rows.append((idx, row.nombre_sede, id_geo, cod_str, row.region_nombre_estandar))
        
    cursor.executemany("""
        INSERT INTO dim_sede (id_sede, nombre_sede, id_geografia, region_codigo_subdere, region_nombre)
        VALUES (?, ?, ?, ?, ?)
    """, sede_rows)
    conn.commit()
    print(f"  -> {len(sede_rows)} sedes cargadas en dim_sede + 1 registro desconocido (-1)")

    # 6. Poblar Dim_Institucion
    print("\n[PASO 6] Poblando dim_institucion (con cruce SIES)...")
    df_puente_inst = pd.read_csv(P2_PUENTE_INST)
    
    cursor.execute("""
        INSERT INTO dim_institucion (id_institucion, nombre_institucion, nombre_normalizado, codigo_ies, nombre_sies, tipo_institucion, clasificacion2, metodo_cruce_sies)
        VALUES (-1, 'No Informado / Desconocido', 'No Informado', NULL, 'Sin Dato SIES', 'Sin Clasificar', 'Sin Dato', 'sin_coincidencia')
    """)
    
    inst_df = df_base[['nombre_institucion', 'tipo_institucion', 'clasificacion2']].drop_duplicates(subset=['nombre_institucion'])
    inst_merged = inst_df.merge(df_puente_inst, left_on='nombre_institucion', right_on='nombre_institucion_cned', how='left')
    
    inst_map = {} # nombre_institucion -> id_institucion
    inst_rows = []
    for idx, row in enumerate(inst_merged.itertuples(), start=1):
        inst_map[row.nombre_institucion] = idx
        cod_ies = int(row.codigo_ies) if pd.notna(row.codigo_ies) else None
        nombre_norm = row.nombre_normalizado if pd.notna(row.nombre_normalizado) else row.nombre_institucion
        nombre_sies = row.nombre_institucion_sies if pd.notna(row.nombre_institucion_sies) else None
        metodo = row.metodo_cruce if pd.notna(row.metodo_cruce) else 'sin_coincidencia'
        clasif2 = row.clasificacion2 if pd.notna(row.clasificacion2) else None
        
        inst_rows.append((idx, row.nombre_institucion, nombre_norm, cod_ies, nombre_sies, row.tipo_institucion, clasif2, metodo))
        
    cursor.executemany("""
        INSERT INTO dim_institucion (id_institucion, nombre_institucion, nombre_normalizado, codigo_ies, nombre_sies, tipo_institucion, clasificacion2, metodo_cruce_sies)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, inst_rows)
    conn.commit()
    print(f"  -> {len(inst_rows)} instituciones cargadas en dim_institucion + 1 desconocido (-1)")

    # 7. Poblar Dim_Institucion_Calidad_Anual (SCD Snapshot Anual)
    print("\n[PASO 7] Poblando dim_institucion_calidad_anual (SCD Snapshot Anual)...")
    df_sies = pd.read_csv(P2_SIES)
    sies_dict = {}
    for r in df_sies.itertuples():
        # llave: (codigo_ies, ano_corte)
        sies_dict[(int(r.codigo_ies), int(r.ano_corte))] = r
        
    inst_calidad_df = df_base[['nombre_institucion', 'ano', 'acreditacion', 'autonomia', 'gratuidad']].drop_duplicates()
    calidad_rows = []
    for r in inst_calidad_df.itertuples():
        id_inst = inst_map.get(r.nombre_institucion, -1)
        ano = int(r.ano)
        
        # Obtener codigo_ies
        row_puente = df_puente_inst[df_puente_inst['nombre_institucion_cned'] == r.nombre_institucion]
        cod_ies = None
        if len(row_puente) > 0 and pd.notna(row_puente.iloc[0]['codigo_ies']):
            cod_ies = int(row_puente.iloc[0]['codigo_ies'])
            
        acred_cned = r.acreditacion if pd.notna(r.acreditacion) else None
        auto_cned = r.autonomia if pd.notna(r.autonomia) else None
        grat_cned = r.gratuidad if pd.notna(r.gratuidad) else None
        
        acred_sies = None
        anos_acred_sies = None
        vigencia_sies = None
        auto_sies = None
        fuente = 'CNED'
        
        if cod_ies is not None and (cod_ies, ano) in sies_dict:
            s_row = sies_dict[(cod_ies, ano)]
            acred_sies = s_row.acreditacion_norm if pd.notna(s_row.acreditacion_norm) else None
            anos_acred_sies = float(s_row.anos_acreditacion) if pd.notna(s_row.anos_acreditacion) else None
            vigencia_sies = s_row.vigencia if pd.notna(s_row.vigencia) else None
            auto_sies = s_row.autonomia if pd.notna(s_row.autonomia) else None
            fuente = 'SIES_OFICIAL'
            
        calidad_rows.append((id_inst, ano, cod_ies, acred_cned, auto_cned, grat_cned, acred_sies, anos_acred_sies, vigencia_sies, auto_sies, fuente))
        
    cursor.executemany("""
        INSERT INTO dim_institucion_calidad_anual (id_institucion, id_tiempo, codigo_ies, acreditacion_cned, autonomia_cned, gratuidad_cned, acreditacion_sies, anos_acreditacion_sies, vigencia_sies, autonomia_sies, fuente_calidad)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, calidad_rows)
    conn.commit()
    print(f"  -> {len(calidad_rows)} registros de calidad institucional anual cargados")

    # 8. Poblar Dim_Programa
    print("\n[PASO 8] Poblando dim_programa...")
    cursor.execute("""
        INSERT INTO dim_programa (id_programa, nombre_programa, carrera_generica, area_conocimiento, tipo_programa, tipo_carrera, horario, duracion_semestres, titulo, grado_academico)
        VALUES (-1, 'Programa No Informado', 'Sin Carrera', 'Sin Area', 'N/A', 'N/A', 'Sin Horario', 0, 'Sin Titulo', 'Sin Grado')
    """)
    
    prog_cols = ['nombre_programa', 'carrera_generica', 'area_conocimiento', 'tipo_programa', 'tipo_carrera', 'horario', 'duracion_semestres', 'titulo', 'grado_academico']
    prog_df = df_base[prog_cols].drop_duplicates().copy()
    prog_df = prog_df.fillna({'duracion_semestres': 0, 'tipo_programa': 'No Declarado', 'tipo_carrera': 'No Declarada', 'titulo': 'No Informado', 'grado_academico': 'No Informado'})
    
    prog_map = {}
    prog_rows = []
    for idx, r in enumerate(prog_df.itertuples(), start=1):
        key = (r.nombre_programa, r.carrera_generica, r.area_conocimiento, r.horario)
        if key not in prog_map:
            prog_map[key] = idx
        duracion = int(r.duracion_semestres) if pd.notna(r.duracion_semestres) else 0
        prog_rows.append((idx, r.nombre_programa, r.carrera_generica, r.area_conocimiento, str(r.tipo_programa), str(r.tipo_carrera), r.horario, duracion, str(r.titulo), str(r.grado_academico)))
        
    cursor.executemany("""
        INSERT INTO dim_programa (id_programa, nombre_programa, carrera_generica, area_conocimiento, tipo_programa, tipo_carrera, horario, duracion_semestres, titulo, grado_academico)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, prog_rows)
    conn.commit()
    print(f"  -> {len(prog_rows)} programas unicos cargados en dim_programa + 1 desconocido (-1)")

    # 9. Poblar Fact_Matricula_Oferta (158.211 registros)
    print("\n[PASO 9] Insertando 158.211 registros en fact_matricula_oferta...")
    fact_rows = []
    for r in df_base.itertuples():
        id_t = int(r.ano)
        
        cod_geo_str = str(int(r.region_codigo_subdere)).zfill(2)
        id_g = geo_map.get(cod_geo_str, -1)
        id_s = sede_map.get(r.nombre_sede, -1)
        id_i = inst_map.get(r.nombre_institucion, -1)
        
        prog_key = (r.nombre_programa, r.carrera_generica, r.area_conocimiento, r.horario)
        id_p = prog_map.get(prog_key, -1)
        
        vac = int(r.vacantes) if pd.notna(r.vacantes) else None
        m_1_tot = int(r.matricula_primer_ano_total)
        m_1_h = int(r.matricula_primer_ano_hombres)
        m_1_m = int(r.matricula_primer_ano_mujeres)
        m_1_ext = int(r.matricula_primer_ano_extranjeros)
        
        m_tot = int(r.matricula_total)
        m_h = int(r.matricula_total_hombres)
        m_m = int(r.matricula_total_mujeres)
        m_ext = int(r.matricula_total_extranjeros)
        
        p_orig = float(r.puntaje_promedio_original) if pd.notna(r.puntaje_promedio_original) else None
        p_norm = float(r.puntaje_promedio_norm_0_100) if pd.notna(r.puntaje_promedio_norm_0_100) else None
        p_paes = float(r.puntaje_promedio_equiv_paes) if pd.notna(r.puntaje_promedio_equiv_paes) else None
        p_z = float(r.puntaje_promedio_zscore_anual) if pd.notna(r.puntaje_promedio_zscore_anual) else None
        
        tasa_ocup = float(r.tasa_ocupacion_primer_ano) if pd.notna(r.tasa_ocupacion_primer_ano) else None
        rat_muj = float(r.ratio_mujeres_primer_ano) if pd.notna(r.ratio_mujeres_primer_ano) else None
        rat_ext = float(r.ratio_extranjeros_total) if pd.notna(r.ratio_extranjeros_total) else None
        
        flag_p = int(r.flag_exige_prueba_admision)
        flag_v = int(r.flag_vacantes_declaradas)
        flag_n = int(r.flag_quiebre_nuble)
        
        fact_rows.append((
            id_t, id_g, id_s, id_i, id_p,
            vac, m_1_tot, m_1_h, m_1_m, m_1_ext,
            m_tot, m_h, m_m, m_ext,
            p_orig, p_norm, p_paes, p_z,
            tasa_ocup, rat_muj, rat_ext,
            flag_p, flag_v, flag_n
        ))
        
    cursor.executemany("""
        INSERT INTO fact_matricula_oferta (
            id_tiempo, id_geografia, id_sede, id_institucion, id_programa,
            vacantes, matricula_primer_ano_total, matricula_primer_ano_hombres, matricula_primer_ano_mujeres, matricula_primer_ano_extranjeros,
            matricula_total, matricula_total_hombres, matricula_total_mujeres, matricula_total_extranjeros,
            puntaje_promedio_original, puntaje_promedio_norm_0_100, puntaje_promedio_equiv_paes, puntaje_promedio_zscore_anual,
            tasa_ocupacion_primer_ano, ratio_mujeres_primer_ano, ratio_extranjeros_total,
            flag_exige_prueba_admision, flag_vacantes_declaradas, flag_quiebre_nuble
        ) VALUES (
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?
        )
    """, fact_rows)
    conn.commit()
    print(f"  -> Filas insertadas en fact_matricula_oferta: {len(fact_rows):,} registros")

    # 10. Poblar Fact_Poblacion_Regional (INE)
    print("\n[PASO 10] Insertando datos demograficos en fact_poblacion_regional (INE)...")
    df_ine = pd.read_csv(P2_INE)
    ine_rows = []
    for r in df_ine.itertuples():
        ano = int(r.ano)
        if ano in anos: # Filtrar los años correspondientes al DataMart
            cod_geo_str = str(int(r.region_codigo_subdere)).zfill(2)
            id_g = geo_map.get(cod_geo_str, -1)
            ine_rows.append((
                id_g, ano,
                int(r.poblacion_total), int(r.poblacion_hombres), int(r.poblacion_mujeres),
                int(r.poblacion_0_14), int(r.poblacion_15_64), int(r.poblacion_65_mas)
            ))
            
    cursor.executemany("""
        INSERT INTO fact_poblacion_regional (
            id_geografia, id_tiempo,
            poblacion_total, poblacion_hombres, poblacion_mujeres,
            poblacion_0_14, poblacion_15_64, poblacion_65_mas
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ine_rows)
    conn.commit()
    print(f"  -> Filas insertadas en fact_poblacion_regional: {len(ine_rows):,} registros (16 regiones x 15 anos = 240)")

    # 11. Crear Vistas Semanticas para Power BI
    print("\n[PASO 11] Creando vistas analiticas para Power BI...")
    with open(SQL_VIEWS_PATH, "r", encoding="utf-8") as f:
        views_script = f.read()
    cursor.executescript(views_script)
    conn.commit()
    print("  -> Vistas vw_datamart_matricula_completo y vistas KPI creadas exitosamente")

    # 12. Exportar tablas en formato CSV interoperable para Persona 4
    print(f"\n[PASO 12] Exportando tablas del DataMart a CSV interoperables en:\n  {EXPORT_CSV_DIR}")
    tablas = [
        "dim_tiempo", "dim_geografia", "dim_sede", "dim_institucion",
        "dim_institucion_calidad_anual", "dim_programa",
        "fact_matricula_oferta", "fact_poblacion_regional"
    ]
    for t in tablas:
        df_export = pd.read_sql_query(f"SELECT * FROM {t}", conn)
        csv_out = os.path.join(EXPORT_CSV_DIR, f"{t}.csv")
        df_export.to_csv(csv_out, index=False)
        print(f"  -> Exportado {t}.csv ({len(df_export):,} filas)")

    conn.close()
    print("\n==================================================================")
    print("=== CARGA DEL DATAMART COMPLETADA CON EXITO (ZERO DATA LOSS) ===")
    print("==================================================================")

if __name__ == "__main__":
    run()
