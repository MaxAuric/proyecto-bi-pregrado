"""
Script 09: Validación de llaves de cruce para integración con el DataMart (Persona 1)
Persona 2 - Hito 2: Analista de Negocio y Fuentes Externas

Verifica que las tablas externas de la RM puedan cruzarse sin pérdidas
contra la base consolidada de Persona 1, y emite un reporte de cuadre
para que Persona 3 pueda declarar las FK en el DDL del DataMart.

Prerequisito: haber ejecutado 08_extract_rm_data.py
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd


class _NumpyEncoder(json.JSONEncoder):
    """Convierte tipos numpy a tipos Python nativos para json.dump."""
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

# ─── Rutas ───────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[3]
DATA_RM = Path(__file__).resolve().parents[1] / "data_rm"
P2H1_PROC = ROOT / "P2_Hito1" / "data_processed"

print("=" * 65)
print("PERSONA 2 - HITO 2: Validación de llaves de cruce DataMart")
print("=" * 65)

resultados = {}

# ─── 1. Carga datos base RM ──────────────────────────────────────────────────
rm_csv = DATA_RM / "rm_base_consolidada.csv"
if not rm_csv.exists():
    print("[ERROR] Ejecute primero 08_extract_rm_data.py")
    exit(1)

df_rm = pd.read_csv(rm_csv, low_memory=False)
print(f"[OK] Base RM: {len(df_rm):,} registros")

# ─── 2. Validar INE RM ───────────────────────────────────────────────────────
ine_rm = DATA_RM / "rm_ext_ine_poblacion.csv"
if ine_rm.exists():
    df_ine = pd.read_csv(ine_rm)
    anos_rm = set()
    for c in df_rm.columns:
        if c.lower() in ("ano", "año", "anio", "year"):
            anos_rm = set(df_rm[c].dropna().astype(int).unique())
            break
    anos_ine = set(df_ine["ano"].astype(int).unique())
    anos_sin_ine = anos_rm - anos_ine
    pct_cobertura = (len(anos_rm & anos_ine) / len(anos_rm) * 100) if anos_rm else 0

    resultados["INE"] = {
        "filas": len(df_ine),
        "anos_rm": sorted(anos_rm),
        "anos_ine_disponibles": sorted(anos_ine),
        "anos_sin_cobertura_ine": sorted(anos_sin_ine),
        "pct_cobertura_temporal": round(pct_cobertura, 1),
        "llave_union": "region_codigo_subdere=13 + ano",
        "estado": "OK" if not anos_sin_ine else f"AVISO: {len(anos_sin_ine)} años sin INE",
    }
    print(f"\n[INE] Cobertura temporal: {pct_cobertura:.1f}%")
    if anos_sin_ine:
        print(f"  Años sin dato INE: {sorted(anos_sin_ine)}")
    else:
        print("  Todos los años de la base RM tienen dato INE.")
else:
    print("[AVISO] No se encontró rm_ext_ine_poblacion.csv")

# ─── 3. Validar SIES RM ──────────────────────────────────────────────────────
sies_rm = DATA_RM / "rm_ext_sies_acreditacion.csv"
puente_inst = P2H1_PROC / "puente_institucion.csv"
if sies_rm.exists() and puente_inst.exists():
    df_sies = pd.read_csv(sies_rm, low_memory=False)
    df_puente = pd.read_csv(puente_inst)

    # Instituciones únicas RM (por nombre)
    col_inst_rm = None
    for c in df_rm.columns:
        if "institucion" in c.lower():
            col_inst_rm = c
            break

    if col_inst_rm:
        inst_rm_nombres = set(df_rm[col_inst_rm].dropna().unique())
        inst_con_codigo = set(df_puente[df_puente["codigo_ies"].notna()]["nombre_institucion_cned"].unique())
        inst_sin_codigo_rm = inst_rm_nombres - inst_con_codigo
        pct_inst_ok = (len(inst_rm_nombres & inst_con_codigo) / len(inst_rm_nombres) * 100) if inst_rm_nombres else 0

        resultados["SIES"] = {
            "instituciones_unicas_rm": len(inst_rm_nombres),
            "con_codigo_ies": len(inst_rm_nombres & inst_con_codigo),
            "sin_codigo_ies": len(inst_sin_codigo_rm),
            "pct_instituciones_ok": round(pct_inst_ok, 2),
            "llave_union": "codigo_ies + ano_corte",
            "estado": "OK" if pct_inst_ok >= 95 else f"REVISAR: {len(inst_sin_codigo_rm)} instituciones sin código",
        }
        print(f"\n[SIES] Instituciones RM con código IES: {pct_inst_ok:.1f}%")
        if inst_sin_codigo_rm:
            print(f"  Sin código: {sorted(list(inst_sin_codigo_rm))[:10]} ...")

    # Cobertura temporal SIES (solo 2018+)
    if "ano_corte" in df_sies.columns:
        anos_sies = set(df_sies["ano_corte"].astype(int).unique())
        resultados["SIES"]["anos_sies_disponibles"] = sorted(anos_sies)
        resultados["SIES"]["nota"] = "Acreditación NULL para 2012–2017 (sin listado SIES previo a 2018)"
else:
    print("[AVISO] No se pudo validar SIES RM")

# ─── 4. Verificar columnas clave para el DataMart ────────────────────────────
print("\n--- Columnas disponibles en base RM (para Persona 3 / DDL) ---")
print(f"Total columnas: {len(df_rm.columns)}")
print(df_rm.dtypes.to_string())

# Detectar columnas de puntaje para P2
puntaje_cols = [c for c in df_rm.columns if "puntaje" in c.lower() or "ptje" in c.lower()]
print(f"\n[Puntajes detectados]: {puntaje_cols}")
if puntaje_cols:
    print(df_rm[puntaje_cols].describe().round(1).to_string())

resultados["columnas_base_rm"] = {
    "total": len(df_rm.columns),
    "puntajes": puntaje_cols,
    "todas": list(df_rm.columns),
}

# ─── 5. Reporte final JSON ────────────────────────────────────────────────────
reporte = {
    "descripcion": "Validación de llaves de cruce - Persona 2 Hito 2",
    "total_registros_rm": int(len(df_rm)),
    "validaciones": resultados,
    "conclusion": (
        "Las fuentes externas INE y SIES están listas para integrarse como dimensiones "
        "complementarias en el DataMart. Ver rm_llaves_dimension_externa.json para el "
        "detalle de FK y tablas de dimensión recomendadas."
    ),
}

out_path = DATA_RM / "rm_validacion_llaves.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(reporte, f, ensure_ascii=False, indent=2, cls=_NumpyEncoder)
print(f"\n[GUARDADO] rm_validacion_llaves.json")
print("\n[LISTO] Validación de llaves completada.")
