import os
import pandas as pd
import numpy as np
import unicodedata
import json

DATA_RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data_raw")
INFO_PROY_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "info_proy")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data_processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

# ---------------------------------------------------------
# TABLA DE NORMALIZACION REGIONAL OFICIAL (SUBDERE / INE)
# ---------------------------------------------------------
REGION_MAPPING = {
    "arica y parinacota": {"codigo": "15", "romano": "XV", "nombre_std": "Región de Arica y Parinacota", "orden": 1},
    "tarapaca":           {"codigo": "01", "romano": "I",  "nombre_std": "Región de Tarapacá", "orden": 2},
    "antofagasta":        {"codigo": "02", "romano": "II", "nombre_std": "Región de Antofagasta", "orden": 3},
    "atacama":            {"codigo": "03", "romano": "III","nombre_std": "Región de Atacama", "orden": 4},
    "coquimbo":           {"codigo": "04", "romano": "IV", "nombre_std": "Región de Coquimbo", "orden": 5},
    "valparaiso":         {"codigo": "05", "romano": "V",  "nombre_std": "Región de Valparaíso", "orden": 6},
    "metropolitana":      {"codigo": "13", "romano": "RM", "nombre_std": "Región Metropolitana de Santiago", "orden": 7},
    "o`higgins":          {"codigo": "06", "romano": "VI", "nombre_std": "Región del Libertador Gral. Bernardo O'Higgins", "orden": 8},
    "o'higgins":          {"codigo": "06", "romano": "VI", "nombre_std": "Región del Libertador Gral. Bernardo O'Higgins", "orden": 8},
    "ohiggins":           {"codigo": "06", "romano": "VI", "nombre_std": "Región del Libertador Gral. Bernardo O'Higgins", "orden": 8},
    "maule":              {"codigo": "07", "romano": "VII","nombre_std": "Región del Maule", "orden": 9},
    "nuble":              {"codigo": "16", "romano": "XVI","nombre_std": "Región de Ñuble", "orden": 10},
    "bio-bio":            {"codigo": "08", "romano": "VIII","nombre_std": "Región del Biobío", "orden": 11},
    "biobio":             {"codigo": "08", "romano": "VIII","nombre_std": "Región del Biobío", "orden": 11},
    "araucania":          {"codigo": "09", "romano": "IX", "nombre_std": "Región de La Araucanía", "orden": 12},
    "rios":               {"codigo": "14", "romano": "XIV","nombre_std": "Región de Los Ríos", "orden": 13},
    "lagos":              {"codigo": "10", "romano": "X",  "nombre_std": "Región de Los Lagos", "orden": 14},
    "aysen":              {"codigo": "11", "romano": "XI", "nombre_std": "Región de Aysén del Gral. Carlos Ibáñez del Campo", "orden": 15},
    "magallanes":         {"codigo": "12", "romano": "XII","nombre_std": "Región de Magallanes y de la Antártica Chilena", "orden": 16}
}

def clean_text_basic(val):
    if pd.isna(val):
        return None
    s = str(val).strip()
    s = " ".join(s.split()) # Quitar dobles espacios
    return s if s else None

def clean_text_upper(val):
    s = clean_text_basic(val)
    return s.upper() if s else None

def get_region_info(region_str):
    if pd.isna(region_str):
        return None, None, None, None
    
    # Normalizar string
    r_norm = unicodedata.normalize('NFKD', str(region_str)).encode('ASCII', 'ignore').decode('utf-8').lower()
    for key, info in REGION_MAPPING.items():
        if key in r_norm:
            return info["codigo"], info["romano"], info["nombre_std"], info["orden"]
    return None, None, str(region_str).strip(), 99

def run_etl():
    print("================================================================")
    print("=== PIPELINE ETL: CONSOLIDACION Y CALIDAD DE DATOS (2012-2026) ===")
    print("================================================================")

    # 1. EXTRACT: Cargar Base Entregada (2012-2022) y CNED Oficial (2023-2026)
    path_old = os.path.join(INFO_PROY_DIR, "01_BaseINDICES_Pregrado24.xlsx")
    path_new = os.path.join(DATA_RAW_DIR, "Base-INDICES-Matricula-2005-2026.xlsx")
    
    print(f"\n[PASO 1: EXTRACT]")
    print(f"  Leyendo base entregada (2012-2022): {path_old}")
    df_old = pd.read_excel(path_old, engine='calamine')
    print(f"  -> {len(df_old):,} registros cargados.")

    print(f"  Leyendo repositorio oficial CNED: {path_new}")
    df_new = pd.read_excel(path_new, engine='calamine')
    print(f"  -> {len(df_new):,} registros brutos cargados.")

    # 2. TRANSFORM & CONFORM: Mapear esquema y armonizar nombres de columnas
    print(f"\n[PASO 2: SCHEMA CONFORMATION & MAPPING]")
    
    # Filtrar solo Pregrado en la nueva base y años 2023-2026
    level_col = [c for c in df_new.columns if 'pregrado' in c.lower() or 'posgrado' in c.lower()][0]
    year_col_new = df_new.columns[0]
    df_new_recent = df_new[(df_new[level_col] == 'Pregrado') & (df_new[year_col_new] >= 2023) & (df_new[year_col_new] <= 2026)].copy()
    print(f"  -> Registros Pregrado 2023-2026 extraidos del CNED: {len(df_new_recent):,}")

    # Estandarizacion de columnas para las 35 variables originales requeridas en la pauta
    # Mapeo de columnas de Base CNED 62-cols hacia el estándar de 35 columnas
    COLUMN_MAPPING_NEW_TO_STD = {
        'Año': 'ano',
        'Nombre Institución': 'nombre_institucion',
        'Tipo Institución': 'tipo_institucion',
        'Clasificación2': 'clasificacion2',
        'Clasificación3': 'acreditacion',          # En la base entregada Clasificacion3 = Acreditacion
        'Clasificación4': 'autonomia',             # En la base entregada Clasificacion4 = Autonomia
        'Clasificación5': 'gratuidad',             # En la base entregada Clasificacion5 = Gratuidad
        'Nombre de la Sede': 'nombre_sede',
        'Nombre Region': 'nombre_region',
        'Carrera Genérica': 'carrera_generica',
        'Nombre Programa': 'nombre_programa',
        'Horario': 'horario',
        'Tipo Programa': 'tipo_programa',
        'Area Conocimiento': 'area_conocimiento',
        'Tipo Carrera': 'tipo_carrera',
        'IngresoDirecto': 'ingreso_directo',
        'Año Inicio Actividades': 'ano_inicio_actividades',
        'Duración (en semestres)': 'duracion_semestres',
        'Título': 'titulo',
        'Grado Académico': 'grado_academico',
        'Máximo Puntaje (promedio matemáticas y lenguaje)': 'puntaje_maximo_original',
        'Promedio Puntaje (promedio matemáticas y lenguaje)': 'puntaje_promedio_original',
        'Mínimo Puntaje (promedio matemáticas y lenguaje)': 'puntaje_minimo_original',
        'Puntaje de corte (primer seleccionado)': 'puntaje_corte_primer_original',
        'Puntaje de corte (promedio de la carrera)': 'puntaje_corte_promedio_original',
        'Puntaje de corte (último seleccionado)': 'puntaje_corte_ultimo_original',
        'Vacantes': 'vacantes',
        'Matrícula primer año hombres': 'matricula_primer_ano_hombres',
        'Matrícula primer año mujeres': 'matricula_primer_ano_mujeres',
        'Matrícula primer año extranjeros': 'matricula_primer_ano_extranjeros',
        'Matrícula Primer Año': 'matricula_primer_ano_total',
        'Matrícula total hombres': 'matricula_total_hombres',
        'Matrícula total mujeres': 'matricula_total_mujeres',
        'Matrícula total extranjeros': 'matricula_total_extranjeros',
        'Matrícula Total': 'matricula_total'
    }

    # Limpiar columnas de df_old mapeándolas al mismo estándar
    old_col_to_std = {}
    for c in df_old.columns:
        c_norm = unicodedata.normalize('NFKD', str(c)).encode('ASCII', 'ignore').decode('utf-8').lower().strip()
        if 'ano' in c_norm and 'inicio' not in c_norm and 'primer' not in c_norm:
            old_col_to_std[c] = 'ano'
        elif 'nombre' in c_norm and 'institucion' in c_norm:
            old_col_to_std[c] = 'nombre_institucion'
        elif 'tipo' in c_norm and 'institucion' in c_norm:
            old_col_to_std[c] = 'tipo_institucion'
        elif 'clasificacion2' in c_norm:
            old_col_to_std[c] = 'clasificacion2'
        elif 'acreditacion' in c_norm:
            old_col_to_std[c] = 'acreditacion'
        elif 'autonomia' in c_norm:
            old_col_to_std[c] = 'autonomia'
        elif 'gratuidad' in c_norm:
            old_col_to_std[c] = 'gratuidad'
        elif 'sede' in c_norm:
            old_col_to_std[c] = 'nombre_sede'
        elif 'region' in c_norm:
            old_col_to_std[c] = 'nombre_region'
        elif 'generica' in c_norm:
            old_col_to_std[c] = 'carrera_generica'
        elif 'nombre' in c_norm and 'programa' in c_norm:
            old_col_to_std[c] = 'nombre_programa'
        elif 'horario' in c_norm:
            old_col_to_std[c] = 'horario'
        elif 'tipo' in c_norm and 'programa' in c_norm:
            old_col_to_std[c] = 'tipo_programa'
        elif 'area' in c_norm:
            old_col_to_std[c] = 'area_conocimiento'
        elif 'tipo' in c_norm and 'carrera' in c_norm:
            old_col_to_std[c] = 'tipo_carrera'
        elif 'ingreso' in c_norm and 'directo' in c_norm:
            old_col_to_std[c] = 'ingreso_directo'
        elif 'inicio' in c_norm:
            old_col_to_std[c] = 'ano_inicio_actividades'
        elif 'duracion' in c_norm:
            old_col_to_std[c] = 'duracion_semestres'
        elif 'titulo' in c_norm:
            old_col_to_std[c] = 'titulo'
        elif 'grado' in c_norm:
            old_col_to_std[c] = 'grado_academico'
        elif 'maximo puntaje' in c_norm:
            old_col_to_std[c] = 'puntaje_maximo_original'
        elif 'promedio puntaje' in c_norm:
            old_col_to_std[c] = 'puntaje_promedio_original'
        elif 'minimo puntaje' in c_norm:
            old_col_to_std[c] = 'puntaje_minimo_original'
        elif 'corte' in c_norm and 'primer' in c_norm:
            old_col_to_std[c] = 'puntaje_corte_primer_original'
        elif 'corte' in c_norm and 'promedio' in c_norm:
            old_col_to_std[c] = 'puntaje_corte_promedio_original'
        elif 'corte' in c_norm and 'ultimo' in c_norm:
            old_col_to_std[c] = 'puntaje_corte_ultimo_original'
        elif 'vacantes' in c_norm:
            old_col_to_std[c] = 'vacantes'
        elif 'primer' in c_norm and 'hombres' in c_norm:
            old_col_to_std[c] = 'matricula_primer_ano_hombres'
        elif 'primer' in c_norm and 'mujeres' in c_norm:
            old_col_to_std[c] = 'matricula_primer_ano_mujeres'
        elif 'primer' in c_norm and 'extranjeros' in c_norm:
            old_col_to_std[c] = 'matricula_primer_ano_extranjeros'
        elif 'matricula primer ano' in c_norm or 'matricula primer a\ufffdo' in c_norm:
            old_col_to_std[c] = 'matricula_primer_ano_total'
        elif 'total' in c_norm and 'hombres' in c_norm:
            old_col_to_std[c] = 'matricula_total_hombres'
        elif 'total' in c_norm and 'mujeres' in c_norm:
            old_col_to_std[c] = 'matricula_total_mujeres'
        elif 'total' in c_norm and 'extranjeros' in c_norm:
            old_col_to_std[c] = 'matricula_total_extranjeros'
        elif 'matricula total' in c_norm:
            old_col_to_std[c] = 'matricula_total'

    # Renombrar dataframes
    df_old_std = df_old.rename(columns=old_col_to_std)[list(old_col_to_std.values())].copy()
    
    # Preparar df_new_recent con las mismas 35 columnas
    # Identificar nombres reales en df_new_recent
    new_cols_dict = {}
    for target_name, std_name in COLUMN_MAPPING_NEW_TO_STD.items():
        # Buscar en df_new_recent
        matches = [c for c in df_new_recent.columns if unicodedata.normalize('NFKD', str(c)).encode('ASCII', 'ignore').decode('utf-8').lower().strip() == unicodedata.normalize('NFKD', str(target_name)).encode('ASCII', 'ignore').decode('utf-8').lower().strip()]
        if matches:
            new_cols_dict[matches[0]] = std_name
        else:
            # Match por aproximacion
            for c in df_new_recent.columns:
                c_clean = unicodedata.normalize('NFKD', str(c)).encode('ASCII', 'ignore').decode('utf-8').lower().strip()
                t_clean = unicodedata.normalize('NFKD', str(target_name)).encode('ASCII', 'ignore').decode('utf-8').lower().strip()
                if t_clean in c_clean or c_clean in t_clean:
                    new_cols_dict[c] = std_name
                    break

    df_new_std = df_new_recent.rename(columns=new_cols_dict)
    # Conservar exactamente las 35 columnas
    cols_order = list(COLUMN_MAPPING_NEW_TO_STD.values())
    
    # Asegurar que todas las columnas existan
    for c in cols_order:
        if c not in df_old_std.columns:
            df_old_std[c] = np.nan
        if c not in df_new_std.columns:
            df_new_std[c] = np.nan
            
    df_old_std = df_old_std[cols_order].copy()
    df_new_std = df_new_std[cols_order].copy()

    # Concatenar ambas fuentes
    print(f"\n[PASO 3: DATA CONSOLIDATION (2012-2026)]")
    df_consolidated = pd.concat([df_old_std, df_new_std], ignore_index=True)
    print(f"  -> Total filas consolidadas: {len(df_consolidated):,} (2012-2022: {len(df_old_std):,} + 2023-2026: {len(df_new_std):,})")

    # 3. TRATAMIENTO DE QUIEBRE ESTRUCTURAL DE PUNTAJES (PSU / PDT / PAES)
    print(f"\n[PASO 4: HOMOLOGACION DEL QUIEBRE PSU / PDT / PAES]")
    # Asignar Tipo de Instrumento de Admision
    df_consolidated['ano'] = pd.to_numeric(df_consolidated['ano'], errors='coerce').astype(int)
    
    conditions = [
        df_consolidated['ano'] <= 2020,
        (df_consolidated['ano'] >= 2021) & (df_consolidated['ano'] <= 2022),
        df_consolidated['ano'] >= 2023
    ]
    choices = ['PSU', 'PDT', 'PAES']
    df_consolidated['tipo_prueba_admision'] = np.select(conditions, choices, default='DESCONOCIDO')
    
    # Escalas teoricas:
    # PSU: [150, 850] -> Rango = 700
    # PDT: [150, 850] -> Rango = 700
    # PAES: [100, 1000] -> Rango = 900
    
    score_cols = [
        'puntaje_maximo_original',
        'puntaje_promedio_original',
        'puntaje_minimo_original',
        'puntaje_corte_primer_original',
        'puntaje_corte_promedio_original',
        'puntaje_corte_ultimo_original'
    ]
    
    for sc in score_cols:
        df_consolidated[sc] = pd.to_numeric(df_consolidated[sc], errors='coerce')
        
        # 1. Normalizacion Min-Max a Escala [0, 100]
        # Formula PSU/PDT: (Score - 150) / (850 - 150) * 100
        # Formula PAES: (Score - 100) / (1000 - 100) * 100
        norm_0_100_col = sc.replace('_original', '_norm_0_100')
        
        is_psu_pdt = df_consolidated['tipo_prueba_admision'].isin(['PSU', 'PDT'])
        is_paes = df_consolidated['tipo_prueba_admision'] == 'PAES'
        
        df_consolidated[norm_0_100_col] = np.nan
        df_consolidated.loc[is_psu_pdt & df_consolidated[sc].notna(), norm_0_100_col] = (
            (df_consolidated.loc[is_psu_pdt, sc] - 150.0) / 700.0 * 100.0
        )
        df_consolidated.loc[is_paes & df_consolidated[sc].notna(), norm_0_100_col] = (
            (df_consolidated.loc[is_paes, sc] - 100.0) / 900.0 * 100.0
        )
        
        # Clip [0, 100] para evitar posibles anomalias de borde
        df_consolidated[norm_0_100_col] = df_consolidated[norm_0_100_col].clip(0.0, 100.0)

        # 2. Homologacion proyectada a Escala PAES (100 - 1000)
        # Permite visualizar toda la serie historica 2012-2026 en escala moderna
        paes_equiv_col = sc.replace('_original', '_equiv_paes')
        df_consolidated[paes_equiv_col] = np.nan
        df_consolidated.loc[is_psu_pdt & df_consolidated[sc].notna(), paes_equiv_col] = (
            100.0 + (df_consolidated.loc[is_psu_pdt, sc] - 150.0) / 700.0 * 900.0
        )
        df_consolidated.loc[is_paes & df_consolidated[sc].notna(), paes_equiv_col] = (
            df_consolidated.loc[is_paes, sc]
        )

    # 3. Z-Score Anual Estandarizado (sobre puntaje_promedio)
    df_consolidated['puntaje_promedio_zscore_anual'] = np.nan
    for y, grp in df_consolidated.groupby('ano'):
        valid_scores = grp['puntaje_promedio_original'].dropna()
        if len(valid_scores) > 10:
            mean_y = valid_scores.mean()
            std_y = valid_scores.std()
            if std_y > 0:
                idx = grp[grp['puntaje_promedio_original'].notna()].index
                df_consolidated.loc[idx, 'puntaje_promedio_zscore_anual'] = (
                    (df_consolidated.loc[idx, 'puntaje_promedio_original'] - mean_y) / std_y
                )

    print(f"  -> Homologacion completada exitosamente.")
    print(f"     * Columna original preservada (escala nativa)")
    print(f"     * Columna normalizada [0 - 100]")
    print(f"     * Columna proyectada a escala equivalente PAES [100 - 1000]")
    print(f"     * Z-score anual estandarizado")

    # 4. TRATAMIENTO LOGICO Y MATEMATICO DE DATOS NULOS
    print(f"\n[PASO 5: TRATAMIENTO DE DATOS NULOS Y FLAGS DE NEGOCIO]")
    
    # Flag 1: Exigencia de Prueba de Admision
    # Se marca 1 si la carrera reporta puntaje o pertenece al subsistema universitario con admision centralizada
    df_consolidated['flag_exige_prueba_admision'] = np.where(
        df_consolidated['puntaje_promedio_original'].notna(), 1, 0
    )
    
    # Flag 2: Vacantes Declaradas
    df_consolidated['vacantes'] = pd.to_numeric(df_consolidated['vacantes'], errors='coerce')
    df_consolidated['flag_vacantes_declaradas'] = np.where(
        df_consolidated['vacantes'].notna() & (df_consolidated['vacantes'] > 0), 1, 0
    )
    
    # Normalizar columnas numericas de matricula
    matricula_cols = [
        'matricula_primer_ano_hombres',
        'matricula_primer_ano_mujeres',
        'matricula_primer_ano_extranjeros',
        'matricula_primer_ano_total',
        'matricula_total_hombres',
        'matricula_total_mujeres',
        'matricula_total_extranjeros',
        'matricula_total'
    ]
    for mc in matricula_cols:
        df_consolidated[mc] = pd.to_numeric(df_consolidated[mc], errors='coerce').fillna(0).astype(int)

    # 5. NORMALIZACION GEOGRAFICA E INSTITUCIONAL
    print(f"\n[PASO 6: NORMALIZACION GEOGRAFICA Y DE TEXTOS]")
    
    # Normalizacion de Regiones con codificacion oficial SUBDERE
    reg_tuples = df_consolidated['nombre_region'].apply(get_region_info)
    df_consolidated['region_codigo_subdere'] = [t[0] for t in reg_tuples]
    df_consolidated['region_numero_romano'] = [t[1] for t in reg_tuples]
    df_consolidated['region_nombre_estandar'] = [t[2] for t in reg_tuples]
    df_consolidated['region_orden_geografico'] = [t[3] for t in reg_tuples]
    
    # Flag especifico para trazabilidad de la Región de Ñuble (Ley 21.033, vigente sept 2018)
    # Permite identificar registros anteriores a 2018 que correspondian a la antigua provincia de Ñuble
    df_consolidated['flag_quiebre_nuble'] = np.where(
        (df_consolidated['region_codigo_subdere'] == '16') & (df_consolidated['ano'] < 2018), 1, 0
    )

    # Normalizacion de Textos Categoriales
    text_cols_upper = ['nombre_institucion', 'nombre_sede', 'carrera_generica', 'nombre_programa', 'titulo']
    for tc in text_cols_upper:
        df_consolidated[tc] = df_consolidated[tc].apply(clean_text_upper)
        
    text_cols_basic = ['tipo_institucion', 'clasificacion2', 'acreditacion', 'autonomia', 'gratuidad', 'horario', 'tipo_programa', 'area_conocimiento', 'tipo_carrera', 'grado_academico']
    for tc in text_cols_basic:
        df_consolidated[tc] = df_consolidated[tc].apply(clean_text_basic)

    # 6. METRICAS DERIVADAS Y KPIS ANALITICOS (PARA FACILITAR HITO 2 Y POWER BI)
    print(f"\n[PASO 7: COMPUTO DE METRICAS Y RATIOS ANALITICOS]")
    # Tasa de ocupacion de vacantes en primer ano
    df_consolidated['tasa_ocupacion_primer_ano'] = np.where(
        df_consolidated['flag_vacantes_declaradas'] == 1,
        (df_consolidated['matricula_primer_ano_total'] / df_consolidated['vacantes']) * 100.0,
        np.nan
    )
    
    # Proporcion de genero
    df_consolidated['ratio_mujeres_primer_ano'] = np.where(
        df_consolidated['matricula_primer_ano_total'] > 0,
        (df_consolidated['matricula_primer_ano_mujeres'] / df_consolidated['matricula_primer_ano_total']) * 100.0,
        np.nan
    )
    
    # Proporcion extranjeros
    df_consolidated['ratio_extranjeros_total'] = np.where(
        df_consolidated['matricula_total'] > 0,
        (df_consolidated['matricula_total_extranjeros'] / df_consolidated['matricula_total']) * 100.0,
        np.nan
    )

    # 7. EXPORT: Generar Archivos Limpios y Documentados
    print(f"\n[PASO 8: EXPORTACION DE ENTREGABLES PROCESADOS]")
    
    csv_output_path = os.path.join(PROCESSED_DIR, "base_indices_consolidada_2012_2026.csv")
    parquet_output_path = os.path.join(PROCESSED_DIR, "base_indices_consolidada_2012_2026.parquet")
    
    print(f"  Exportando CSV: {csv_output_path}...")
    df_consolidated.to_csv(csv_output_path, index=False, encoding='utf-8')
    
    print(f"  Exportando Parquet: {parquet_output_path}...")
    df_consolidated.to_parquet(parquet_output_path, index=False)
    
    print(f"\n================================================================")
    print(f"=== ETL FINALIZADO CON EXITO ===")
    print(f"  Registros Totales: {len(df_consolidated):,}")
    print(f"  Columnas Totales:  {len(df_consolidated.columns)}")
    print(f"  Periodo Temporal:  {df_consolidated['ano'].min()} - {df_consolidated['ano'].max()}")
    print(f"================================================================")
    
    return df_consolidated

if __name__ == "__main__":
    run_etl()
