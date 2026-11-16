"""
analisis_negocio_rm.py
======================
Script de reproducibilidad — Persona 2: Analista de Negocio RM
Entrega Final — Business Intelligence | Noviembre 2026

Extrae y valida todas las cifras reales del DataMart usadas en:
  - informe_final_persona2_negocio_rm.tex
  - analisis_kpis_negocio_rm.md
  - canvas_bi_rm_10_bloques.md

Uso:
    python Final/P2_ANALISTA_NEGOCIO_RM/scripts/analisis_negocio_rm.py

Fuente de datos:
    Final/00_DATAMART_LISTO_PARA_POWERBI/tablas_estrella_csv/

Restricción: 100% Región Metropolitana (region_codigo_subdere = '13')
             58.926 registros históricos 2012-2026.
"""

import os
import sys
import json
import warnings
import pandas as pd
import numpy as np

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# RUTAS
# ─────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
DATAMART_DIR = os.path.join(PROJECT_ROOT, "Final", "00_DATAMART_LISTO_PARA_POWERBI", "tablas_estrella_csv")
OUTPUT_DIR   = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))  # P2_ANALISTA_NEGOCIO_RM/


def ruta(nombre: str) -> str:
    return os.path.join(DATAMART_DIR, nombre)


# ─────────────────────────────────────────────────────────────────────────────
# CARGA DE TABLAS
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 70)
print("  ANÁLISIS DE NEGOCIO RM — Persona 2 | Entrega Final BI 2026")
print("=" * 70)
print(f"\nDataMart: {DATAMART_DIR}\n")

fact = pd.read_csv(ruta("fact_matricula_admision.csv"))
dc   = pd.read_csv(ruta("dim_carrera_programa.csv"))
dt   = pd.read_csv(ruta("dim_tiempo_ine_rm.csv"))
di   = pd.read_csv(ruta("dim_institucion_sies.csv"))
dsg  = pd.read_csv(ruta("dim_sede_geografia.csv"))

print(f"  fact_matricula_admision : {len(fact):>7,} filas x {fact.shape[1]} columnas")
print(f"  dim_carrera_programa    : {len(dc):>7,} filas x {dc.shape[1]} columnas")
print(f"  dim_tiempo_ine_rm       : {len(dt):>7,} filas x {dt.shape[1]} columnas")
print(f"  dim_institucion_sies    : {len(di):>7,} filas x {di.shape[1]} columnas")
print(f"  dim_sede_geografia      : {len(dsg):>7,} filas x {dsg.shape[1]} columnas")

# ─────────────────────────────────────────────────────────────────────────────
# FILTRO AÑO 2026
# ─────────────────────────────────────────────────────────────────────────────

f26  = fact[fact["id_tiempo"] == 2026].copy()
t26  = dt[dt["id_tiempo"] == 2026].iloc[0]
di26 = di[di["id_tiempo"] == 2026].copy() if "id_tiempo" in di.columns else di.copy()

print(f"\n  Registros año 2026: {len(f26):,}")

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 1: CIFRAS GLOBALES RM 2026 (Tabla de portada del informe)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "─" * 70)
print("  1. CIFRAS GLOBALES RM 2026")
print("─" * 70)

# Totales aditivos
total_vac_26  = f26["vacantes"].sum()
total_mat1_26 = f26["matricula_primer_ano_total"].sum()
total_mat_26  = f26["matricula_total"].sum()
total_sec_extra_26 = f26["secciones_extra_por_sobrecupo"].sum()
total_sobredemanda  = int(f26["flag_sobredemanda_critica"].sum()) if "flag_sobredemanda_critica" in f26.columns else "N/A"

# Tasas del DataMart (dim_tiempo)
absorcion_26  = float(t26["tasa_absorcion_juvenil_rm_pct"])
cobertura_26  = float(t26["tasa_cobertura_bruta_rm_pct"])
oferta1000_26 = float(t26["tasa_oferta_vacantes_1000_jovenes_rm"])
ocupacion_26  = float(t26["tasa_ocupacion_anual_rm_pct"])
paes_prom_26  = float(t26["media_anual_paes_rm"])
pob_joven_26  = int(t26["poblacion_joven_18_24_rm"])
yoy_mat_26    = float(t26["tasa_crecimiento_matricula_rm_yoy_pct"])

# Retención aparente RM 2026 (calculada aquí para validación)
retencion_26 = round((total_mat_26 - total_mat1_26) / total_mat_26 * 100, 2)

print(f"  Vacantes declaradas RM 2026          : {total_vac_26:>12,.0f}")
print(f"  Matrícula 1er año RM 2026            : {total_mat1_26:>12,.0f}")
print(f"  Matrícula total RM 2026              : {total_mat_26:>12,.0f}")
print(f"  Secciones extra por sobrecupo 2026   : {total_sec_extra_26:>12,.0f}")
print(f"  Programas sobredemanda crítica 2026  : {total_sobredemanda:>12}")
print(f"  Población joven 18-24 RM 2026 (INE)  : {pob_joven_26:>12,}")
print()
print(f"  Tasa de Ocupación de Vacantes RM     : {ocupacion_26:>11.2f}%")
print(f"  Tasa de Absorción Juvenil RM (INE)   : {absorcion_26:>11.2f}%")
print(f"  Tasa de Cobertura Bruta RM           : {cobertura_26:>11.2f}%")
print(f"  Oferta de Vacantes / 1.000 jóvenes   : {oferta1000_26:>11.1f}")
print(f"  Puntaje PAES Promedio RM (equiv.)    : {paes_prom_26:>11.1f}")
print(f"  Retención Aparente RM 2026           : {retencion_26:>11.2f}%")
print(f"  Crecimiento Matrícula RM YoY         : {yoy_mat_26:>11.2f}%")

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 2: CIFRAS POR ÁREA (Pregunta P1 del informe)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "─" * 70)
print("  2. P1 — SOBREDEMANDA POR ÁREA DE CONOCIMIENTO (RM 2026)")
print("─" * 70)

merged_area = f26.merge(
    dc[["id_carrera_programa_sk", "area_conocimiento"]],
    on="id_carrera_programa_sk",
    how="left"
)

area_grp = merged_area.groupby("area_conocimiento").agg(
    vacantes=("vacantes", "sum"),
    mat1=("matricula_primer_ano_total", "sum"),
    sec_extra=("secciones_extra_por_sobrecupo", "sum"),
    n_programas=("id_carrera_programa_sk", "count")
).reset_index()

area_grp["ocupacion_pct"] = (area_grp["mat1"] / area_grp["vacantes"].replace(0, pd.NA) * 100).round(1)
area_grp = area_grp.sort_values("ocupacion_pct", ascending=False)

print(f"\n  {'Área':45s} {'Vacantes':>10} {'Mat. 1er año':>13} {'Ocupación%':>11} {'Sec. Extra':>11}")
print("  " + "-" * 95)
for _, r in area_grp.iterrows():
    print(f"  {str(r['area_conocimiento'])[:44]:45s} {r['vacantes']:>10,.0f} {r['mat1']:>13,.0f} {r['ocupacion_pct']:>10.1f}% {r['sec_extra']:>11.0f}")

print(f"\n  {'TOTAL RM 2026':45s} {total_vac_26:>10,.0f} {total_mat1_26:>13,.0f} {ocupacion_26:>10.1f}% {total_sec_extra_26:>11.0f}")

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 3: EVOLUCIÓN PUNTAJES PAES (Pregunta P2 del informe)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "─" * 70)
print("  3. P2 — EVOLUCIÓN PUNTAJE PAES Y OCUPACIÓN RM (2012–2026)")
print("─" * 70)

# Puntaje PAES ponderado por matrícula (medida no aditiva — SUMX)
evol_paes = []
for anio in sorted(fact["id_tiempo"].unique()):
    fa = fact[fact["id_tiempo"] == anio].copy()
    ta = dt[dt["id_tiempo"] == anio]
    if ta.empty:
        continue
    ta = ta.iloc[0]

    # Filtrar solo registros con prueba de admisión y puntaje válido
    fa_valid = fa[
        (fa.get("flag_exige_prueba_admision", pd.Series(1, index=fa.index)) == 1) &
        fa["puntaje_promedio_equiv_paes"].notna() &
        (fa["matricula_primer_ano_total"] > 0)
    ] if "flag_exige_prueba_admision" in fa.columns else fa[
        fa["puntaje_promedio_equiv_paes"].notna() &
        (fa["matricula_primer_ano_total"] > 0)
    ]

    sum_pmat = (fa_valid["puntaje_promedio_equiv_paes"] * fa_valid["matricula_primer_ano_total"]).sum()
    sum_mat  = fa_valid["matricula_primer_ano_total"].sum()
    paes_pond = round(sum_pmat / sum_mat, 1) if sum_mat > 0 else None

    evol_paes.append({
        "ano": anio,
        "paes_ponderado": paes_pond,
        "ocupacion_pct": float(ta["tasa_ocupacion_anual_rm_pct"]),
        "es_paes": int(ta["es_paes"]) if "es_paes" in ta.index else None
    })

df_evol = pd.DataFrame(evol_paes)
print(f"\n  {'Año':6} {'PAES Pond.(equiv.)':>20} {'Ocupación RM(%)':>16} {'Instrumento':>12}")
print("  " + "-" * 60)
for _, r in df_evol.iterrows():
    inst = "PAES" if r["es_paes"] == 1 else "PSU (equiv.)"
    paes_str = f"{r['paes_ponderado']:.1f}" if r["paes_ponderado"] else "N/D"
    print(f"  {int(r['ano']):6} {paes_str:>20} {r['ocupacion_pct']:>15.1f}% {inst:>12}")

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 4: ABSORCIÓN Y COBERTURA (Pregunta P3 del informe)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "─" * 70)
print("  4. P3 — ABSORCIÓN JUVENIL Y COBERTURA BRUTA RM (2012–2026)")
print("─" * 70)

print(f"\n  {'Año':6} {'Absorción Juvenil(%)':>22} {'Cobertura Bruta(%)':>20} {'Oferta/1.000 jóv':>18}")
print("  " + "-" * 72)
for _, r in dt.sort_values("id_tiempo").iterrows():
    print(f"  {int(r['id_tiempo']):6} {float(r['tasa_absorcion_juvenil_rm_pct']):>21.2f}% "
          f"{float(r['tasa_cobertura_bruta_rm_pct']):>19.2f}% "
          f"{float(r['tasa_oferta_vacantes_1000_jovenes_rm']):>18.1f}")

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 5: POSICIONAMIENTO COMPETITIVO IES RM 2026
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "─" * 70)
print("  5. POSICIONAMIENTO COMPETITIVO IES RM 2026")
print("─" * 70)

if "posicionamiento_competitivo_rm" in di.columns:
    pos = di["posicionamiento_competitivo_rm"].value_counts()
    for cat, cnt in pos.items():
        print(f"  {cat:50s} : {cnt:>5}")
else:
    print("  Columna 'posicionamiento_competitivo_rm' no encontrada en dim_institucion_sies.")

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 6: VALIDACIÓN DEL CASO 120 → 140 ALUMNOS
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "─" * 70)
print("  6. VALIDACIÓN — CASO 120 → 140 ALUMNOS (módulo 35 puestos)")
print("─" * 70)

import math
for alumnos, label in [(120, "Situación inicial"), (140, "Sobredemanda (100%)"), (141, "Un alumno más")]:
    sec_plan = math.ceil(120 / 35)      # planificadas con 120 vacantes
    sec_real = math.ceil(alumnos / 35)  # reales con N matriculados
    sec_cap  = sec_plan * 35
    sat      = alumnos / sec_cap * 100
    extra    = max(0, sec_real - sec_plan)
    print(f"  {label:30s}: {alumnos:3d} mat → {sec_plan} sec plan → cap. {sec_cap} → sat {sat:.1f}% → extra={extra}")

# ─────────────────────────────────────────────────────────────────────────────
# EXPORTAR RESUMEN JSON
# ─────────────────────────────────────────────────────────────────────────────

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return super().default(obj)

resumen = {
    "fecha_extraccion": pd.Timestamp.now().isoformat()[:19],
    "cifras_globales_rm_2026": {
        "total_registros_rm": int(len(fact)),
        "registros_2026": int(len(f26)),
        "vacantes_rm_2026": float(total_vac_26),
        "matricula_1er_ano_rm_2026": float(total_mat1_26),
        "matricula_total_rm_2026": float(total_mat_26),
        "secciones_extra_sobrecupo_2026": float(total_sec_extra_26),
        "programas_sobredemanda_critica_2026": total_sobredemanda,
        "poblacion_joven_18_24_rm_2026_ine": pob_joven_26,
        "tasa_ocupacion_anual_rm_2026_pct": ocupacion_26,
        "tasa_absorcion_juvenil_rm_2026_pct": absorcion_26,
        "tasa_cobertura_bruta_rm_2026_pct": cobertura_26,
        "oferta_vacantes_1000_jovenes_2026": oferta1000_26,
        "paes_promedio_ponderado_rm_2026": paes_prom_26,
        "retencion_aparente_rm_2026_pct": retencion_26,
        "crecimiento_matricula_yoy_2026_pct": yoy_mat_26
    },
    "areas_conocimiento_rm_2026": area_grp[["area_conocimiento","vacantes","mat1","ocupacion_pct","sec_extra"]].to_dict(orient="records"),
    "evolucion_paes_ocupacion_rm": df_evol.to_dict(orient="records"),
    "tasas_demograficas_anuales_rm": dt[["id_tiempo","tasa_absorcion_juvenil_rm_pct","tasa_cobertura_bruta_rm_pct","tasa_oferta_vacantes_1000_jovenes_rm","tasa_ocupacion_anual_rm_pct"]].to_dict(orient="records")
}

json_path = os.path.join(OUTPUT_DIR, "docs", "cifras_rm_2026.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(resumen, f, ensure_ascii=False, indent=2, cls=NumpyEncoder)

print("\n" + "─" * 70)
print(f"  ✔  Resumen JSON exportado → {json_path}")
print("─" * 70)
print("\n  Validación completa. Todas las cifras provienen del DataMart oficial.")
print("  Usar estas cifras en el informe .tex y en el Dashboard Power BI.\n")
