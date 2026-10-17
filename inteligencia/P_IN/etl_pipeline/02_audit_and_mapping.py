import os
import pandas as pd
import numpy as np
import unicodedata
import json

DATA_RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data_raw")
INFO_PROY_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "info_proy")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data_processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

def clean_col_name(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ASCII', 'ignore').decode('utf-8')
    s = s.lower().strip()
    s = s.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_').replace('.', '').replace('-', '_')
    while '__' in s:
        s = s.replace('__', '_')
    return s.strip('_')

def run_audit():
    print("=== INICIANDO AUDITORIA Y PERFILAMIENTO DE DATOS ===")
    
    # 1. Cargar Base Entregada (2012-2022)
    path_old = os.path.join(INFO_PROY_DIR, "01_BaseINDICES_Pregrado24.xlsx")
    print(f"[AUDIT] Leyendo base entregada: {path_old}...")
    df_old = pd.read_excel(path_old, engine='calamine')
    orig_cols_old = list(df_old.columns)
    df_old.columns = [clean_col_name(c) for c in df_old.columns]
    print(f"  Registros en base entregada: {len(df_old):,} | Columnas: {len(df_old.columns)}")
    
    # 2. Cargar Base CNED Oficial (2005-2026)
    path_new = os.path.join(DATA_RAW_DIR, "Base-INDICES-Matricula-2005-2026.xlsx")
    print(f"[AUDIT] Leyendo base CNED oficial: {path_new}...")
    df_new = pd.read_excel(path_new, engine='calamine')
    orig_cols_new = list(df_new.columns)
    df_new.columns = [clean_col_name(c) for c in df_new.columns]
    print(f"  Registros totales en CNED: {len(df_new):,} | Columnas: {len(df_new.columns)}")
    
    # Filtrar CNED para Pregrado y anos 2023 a 2026
    level_col = [c for c in df_new.columns if 'pregrado' in c or 'posgrado' in c][0]
    df_new_pre = df_new[df_new[level_col] == 'Pregrado'].copy()
    
    year_col_new = 'ano'
    year_col_old = 'ano'
    
    df_new_recent = df_new_pre[(df_new_pre[year_col_new] >= 2023) & (df_new_pre[year_col_new] <= 2026)].copy()
    print(f"  Registros Pregrado 2023-2026 en CNED: {len(df_new_recent):,}")
    
    # 3. Analisis de Quiebre de Puntajes por Periodo de Admision
    # PSU: 2012-2020 (Escala 150 - 850)
    # PDT: 2021-2022 (Escala 150 - 850)
    # PAES: 2023-2026 (Escala 100 - 1000)
    print("\n--- ANALISIS DE QUIEBRE ESTRUCTURAL DE PUNTAJES ---")
    score_col_old = [c for c in df_old.columns if 'promedio_puntaje_promedio' in c][0]
    score_col_new = [c for c in df_new.columns if 'promedio_puntaje_promedio' in c][0]
    
    stats_psu = pd.to_numeric(df_old[df_old[year_col_old] <= 2020][score_col_old], errors='coerce').dropna()
    stats_pdt = pd.to_numeric(df_old[(df_old[year_col_old] >= 2021) & (df_old[year_col_old] <= 2022)][score_col_old], errors='coerce').dropna()
    stats_paes = pd.to_numeric(df_new_recent[score_col_new], errors='coerce').dropna()
    
    print(f"  PSU  (2012-2020) -> N: {len(stats_psu):,} | Min: {stats_psu.min():.1f} | Max: {stats_psu.max():.1f} | Media: {stats_psu.mean():.1f} | Desv: {stats_psu.std():.1f} | Mediana: {stats_psu.median():.1f}")
    print(f"  PDT  (2021-2022) -> N: {len(stats_pdt):,} | Min: {stats_pdt.min():.1f} | Max: {stats_pdt.max():.1f} | Media: {stats_pdt.mean():.1f} | Desv: {stats_pdt.std():.1f} | Mediana: {stats_pdt.median():.1f}")
    print(f"  PAES (2023-2026) -> N: {len(stats_paes):,} | Min: {stats_paes.min():.1f} | Max: {stats_paes.max():.1f} | Media: {stats_paes.mean():.1f} | Desv: {stats_paes.std():.1f} | Mediana: {stats_paes.median():.1f}")
    
    # 4. Analisis de Nulos en Variables Clave
    print("\n--- ANALISIS DE DATOS NULOS (BASE ENTREGADA 2012-2022) ---")
    total_old = len(df_old)
    null_report = {}
    for orig, clean in zip(orig_cols_old, df_old.columns):
        null_count = int(df_old[clean].isna().sum())
        pct = (null_count / total_old) * 100
        null_report[orig] = {
            "clean_name": clean,
            "null_count": null_count,
            "null_pct": round(pct, 2),
            "dtype": str(df_old[clean].dtype)
        }
        if pct > 20 or "puntaje" in clean or "vacantes" in clean:
            print(f"  {orig:55}: {null_count:,} nulos ({pct:.2f}%)")
            
    # 5. Analisis de Instituciones y Cobertura de Prueba de Admision
    tipo_inst_col = [c for c in df_old.columns if 'tipo_institucion' in c][0]
    print("\n--- COBERTURA DE PUNTAJES POR TIPO DE INSTITUCION ---")
    for t_inst, grp in df_old.groupby(tipo_inst_col):
        n_inst = len(grp)
        n_scores = grp[score_col_old].notna().sum()
        pct_scores = (n_scores / n_inst) * 100
        print(f"  {t_inst:35}: {n_scores:,} / {n_inst:,} registros con puntaje ({pct_scores:.1f}%)")
        
    # Guardar resultados en JSON
    audit_results = {
        "resumen_filas": {
            "base_entregada_2012_2022": len(df_old),
            "cned_pregrado_2023_2026": len(df_new_recent),
            "total_integrado_esperado": len(df_old) + len(df_new_recent)
        },
        "quiebre_puntajes": {
            "PSU_2012_2020": {"n": int(len(stats_psu)), "min": float(stats_psu.min()), "max": float(stats_psu.max()), "mean": float(stats_psu.mean()), "std": float(stats_psu.std()), "median": float(stats_psu.median())},
            "PDT_2021_2022": {"n": int(len(stats_pdt)), "min": float(stats_pdt.min()), "max": float(stats_pdt.max()), "mean": float(stats_pdt.mean()), "std": float(stats_pdt.std()), "median": float(stats_pdt.median())},
            "PAES_2023_2026": {"n": int(len(stats_paes)), "min": float(stats_paes.min()), "max": float(stats_paes.max()), "mean": float(stats_paes.mean()), "std": float(stats_paes.std()), "median": float(stats_paes.median())}
        },
        "reporte_nulos_base_entregada": null_report
    }
    
    audit_json_path = os.path.join(PROCESSED_DIR, "auditoria_resumen.json")
    with open(audit_json_path, "w", encoding="utf-8") as f:
        json.dump(audit_results, f, indent=2, ensure_ascii=False)
        
    print(f"\n[AUDIT] Resumen de auditoria guardado exitosamente en: {audit_json_path}")
    return audit_results

if __name__ == "__main__":
    run_audit()
