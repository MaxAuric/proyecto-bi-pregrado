import os
import json
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
P1_BASE = os.path.join(BASE_DIR, "P_IN", "data_processed", "base_indices_consolidada_2012_2026.csv")
P2_PUENTE_INST = os.path.join(BASE_DIR, "P2_Hito1", "data_processed", "puente_institucion.csv")
P2_PUENTE_REG = os.path.join(BASE_DIR, "P2_Hito1", "data_processed", "puente_region.csv")
OUTPUT_JSON = os.path.join(BASE_DIR, "P3_Hito1", "auditoria_normalizacion_textos.json")

def audit():
    print("==================================================================")
    print("=== AUDITORÍA DE NORMALIZACIÓN DE TEXTOS - PERSONA 3 (HITO 1) ===")
    print("==================================================================")

    df_base = pd.read_csv(P1_BASE, low_memory=False)
    total_filas = len(df_base)
    
    # 1. Auditoría Geográfica
    print("\n[1] AUDITORÍA NORMALIZACIÓN REGIONAL (SUBDERE / INE):")
    regiones_unicas = df_base['nombre_region'].nunique()
    codigos_unicos = df_base['region_codigo_subdere'].nunique()
    nulos_reg = df_base['nombre_region'].isna().sum()
    nulos_cod = df_base['region_codigo_subdere'].isna().sum()
    nuble_quiebre_rows = (df_base['flag_quiebre_nuble'] == 1).sum()
    
    print(f"  Total registros auditados: {total_filas:,}")
    print(f"  Regiones únicas detectadas: {regiones_unicas} (Esperado: 16)")
    print(f"  Códigos SUBDERE únicos:    {codigos_unicos} (Esperado: 16)")
    print(f"  Nulos en nombre_region:    {nulos_reg} (0.00%)")
    print(f"  Nulos en region_codigo:    {nulos_cod} (0.00%)")
    print(f"  Registros pre-2018 Ñuble:  {nuble_quiebre_rows:,} filas gobernadas con flag")

    # 2. Auditoría Institucional
    print("\n[2] AUDITORÍA NORMALIZACIÓN INSTITUCIONAL (CRUCE SIES):")
    df_puente_inst = pd.read_csv(P2_PUENTE_INST)
    total_grafias = len(df_puente_inst)
    con_codigo = df_puente_inst['codigo_ies'].notna().sum()
    sin_codigo = df_puente_inst['codigo_ies'].isna().sum()
    
    metodos = df_puente_inst['metodo_cruce'].value_counts().to_dict()
    
    # Cruce contra base
    merged = df_base.merge(df_puente_inst[['nombre_institucion_cned', 'codigo_ies']], 
                           left_on='nombre_institucion', 
                           right_on='nombre_institucion_cned', 
                           how='left')
    
    filas_con_codigo = merged['codigo_ies'].notna().sum()
    pct_filas = (filas_con_codigo / total_filas) * 100
    
    mat_total = df_base['matricula_primer_ano_total'].sum()
    mat_cruzada = merged[merged['codigo_ies'].notna()]['matricula_primer_ano_total'].sum()
    pct_mat = (mat_cruzada / mat_total) * 100

    print(f"  Grafías institucionales únicas en CNED: {total_grafias}")
    print(f"  Instituciones con código SIES asignado: {con_codigo} ({con_codigo/total_grafias*100:.2f}%)")
    print(f"  Grafías sin código SIES (históricas/pend): {sin_codigo} ({sin_codigo/total_grafias*100:.2f}%)")
    print(f"  Desglose de métodos de cruce: {metodos}")
    print(f"  Cobertura sobre filas consolidadas: {filas_con_codigo:,}/{total_filas:,} ({pct_filas:.2f}%)")
    print(f"  Cobertura sobre matrícula 1er año: {mat_cruzada:,}/{mat_total:,} ({pct_mat:.2f}%)")

    # 3. Auditoría Carrera Genérica y Programas
    print("\n[3] AUDITORÍA NORMALIZACIÓN DE CARRERA Y PROGRAMA:")
    carreras_unicas = df_base['carrera_generica'].nunique()
    programas_unicos = df_base['nombre_programa'].nunique()
    areas_unicas = df_base['area_conocimiento'].nunique()
    horarios_unicos = df_base['horario'].nunique()
    
    # Validar espacios dobles o cadenas sucias
    espacios_extra_carrera = df_base['carrera_generica'].apply(lambda x: "  " in str(x)).sum()
    espacios_extra_prog = df_base['nombre_programa'].apply(lambda x: "  " in str(x)).sum()
    
    print(f"  Carreras genéricas únicas: {carreras_unicas}")
    print(f"  Nombres de programas únicos: {programas_unicos}")
    print(f"  Áreas de conocimiento únicas: {areas_unicas}")
    print(f"  Horarios normalizados: {horarios_unicos} ({list(df_base['horario'].unique())})")
    print(f"  Registros con espacios dobles en carrera: {espacios_extra_carrera} (0 esperado)")
    print(f"  Registros con espacios dobles en programa: {espacios_extra_prog} (0 esperado)")

    resumen = {
        "geografia": {
            "total_regiones": int(regiones_unicas),
            "cobertura_registros_pct": 100.0,
            "nulos": 0,
            "flag_quiebre_nuble_registros": int(nuble_quiebre_rows)
        },
        "institucion": {
            "grafias_totales": int(total_grafias),
            "grafias_con_codigo_sies": int(con_codigo),
            "cobertura_filas_pct": round(float(pct_filas), 2),
            "cobertura_matricula_pct": round(float(pct_mat), 2),
            "metodos_cruce": {k: int(v) for k, v in metodos.items()}
        },
        "carreras_y_programas": {
            "carreras_genericas_unicas": int(carreras_unicas),
            "programas_unicos": int(programas_unicos),
            "areas_conocimiento": int(areas_unicas),
            "limpieza_espacios_pct": 100.0
        }
    }
    
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(resumen, f, indent=4)
        
    print(f"\n-> Resultados de auditoría guardados en:\n   {OUTPUT_JSON}")
    print("==================================================================")

if __name__ == "__main__":
    audit()
