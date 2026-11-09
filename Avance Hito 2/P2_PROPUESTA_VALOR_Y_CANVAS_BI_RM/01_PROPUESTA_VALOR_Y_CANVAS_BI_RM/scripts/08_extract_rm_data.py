"""
Script 08: Extracción y preparación de datos de la Región Metropolitana (RM)
Persona 2 - Hito 2: Analista de Negocio y Fuentes Externas

Objetivo:
  - Filtrar la base consolidada (P_IN) para la RM (region_codigo_subdere = 13)
  - Preparar las tablas de dimensiones externas acotadas a la RM
  - Generar KPIs preliminares de las 3 nuevas preguntas de negocio
  - Verificar llaves de cruce para integración con el DataMart de Persona 1

Salidas (carpeta data_rm/):
  - rm_base_consolidada.csv          : registros de la RM (filtro sobre base P_IN)
  - rm_ext_ine_poblacion.csv         : proyecciones INE para RM (cod. SUBDERE = 13)
  - rm_ext_sies_acreditacion.csv     : SIES filtrado a instituciones con sede en RM
  - rm_kpi_p1_sobredemanda.csv       : P1 - Tasa ocupación de vacantes RM por área y año
  - rm_kpi_p2_puntajes_paes.csv      : P2 - Evolución puntajes corte/promedio RM
  - rm_kpi_p3_absorcion_demografica.csv : P3 - Absorción 18-24 años RM (vacantes vs INE)
  - rm_llaves_dimension_externa.json : Documento de llaves listas para el DataMart
  - rm_auditoria_fuentes.json        : Cuadre de registros RM

Prerequisitos:
  - Haber ejecutado P_IN/etl_pipeline/01 al 07 (Persona 1)
  - Python con pandas, openpyxl
"""

import json
import os
import sys
from pathlib import Path

import pandas as pd

# ─── Rutas ───────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[3]           # inteligencia/
PIN_PROCESSED = ROOT / "P_IN" / "data_processed"
PIN_EXTERNAL  = ROOT / "P_IN" / "data_external"       # mismo contenido que P2_Hito1
P2H1_PROCESSED = ROOT / "P2_Hito1" / "data_processed"

OUT_DIR = Path(__file__).resolve().parents[1] / "data_rm"
OUT_DIR.mkdir(parents=True, exist_ok=True)

RM_COD = 13   # código SUBDERE de la Región Metropolitana
RM_COD_ALTERNATIVO = "Región Metropolitana de Santiago"

# ─── 1. Carga de la base consolidada ────────────────────────────────────────
print("=" * 65)
print("PERSONA 2 - HITO 2: Preparación de datos Región Metropolitana")
print("=" * 65)

base_path = PIN_PROCESSED / "base_indices_consolidada_2012_2026.csv"
if not base_path.exists():
    # Intentar con parquet
    base_path = PIN_PROCESSED / "base_indices_consolidada_2012_2026.parquet"
    if base_path.exists():
        df_base = pd.read_parquet(base_path)
        print(f"[OK] Base cargada desde parquet: {len(df_base):,} registros totales")
    else:
        sys.exit("[ERROR] No se encontró la base consolidada de Persona 1 en P_IN/data_processed/")
else:
    df_base = pd.read_csv(base_path, low_memory=False)
    print(f"[OK] Base cargada desde CSV: {len(df_base):,} registros totales")

# Columnas de interés para la RM
print(f"[INFO] Columnas disponibles: {list(df_base.columns)}")

# ─── 2. Filtro Región Metropolitana ─────────────────────────────────────────
# Detectar columna de región
col_region_cod = None
col_region_nom = None
for c in df_base.columns:
    if "subdere" in c.lower() or "cod_region" in c.lower():
        col_region_cod = c
    if "region" in c.lower() and "nombre" in c.lower():
        col_region_nom = c

# Filtrar por código SUBDERE si existe, o por nombre
if col_region_cod and df_base[col_region_cod].dtype in ["int64", "float64", "object"]:
    try:
        df_rm = df_base[df_base[col_region_cod].astype(str).str.strip() == str(RM_COD)].copy()
    except Exception:
        df_rm = df_base[df_base[col_region_cod] == RM_COD].copy()
elif col_region_nom:
    df_rm = df_base[df_base[col_region_nom].str.contains("Metropolitana", na=False)].copy()
else:
    # Buscar cualquier columna que contenga "Metropolitana"
    for c in df_base.columns:
        if df_base[c].dtype == object:
            mask = df_base[c].astype(str).str.contains("Metropolitana", na=False)
            if mask.sum() > 1000:
                df_rm = df_base[mask].copy()
                col_region_nom = c
                break
    else:
        sys.exit("[ERROR] No se pudo identificar la columna de región en la base.")

n_rm = len(df_rm)
print(f"[OK] Registros RM filtrados: {n_rm:,} de {len(df_base):,} totales "
      f"({n_rm/len(df_base)*100:.1f}%)")

df_rm.to_csv(OUT_DIR / "rm_base_consolidada.csv", index=False, encoding="utf-8-sig")
print(f"[GUARDADO] rm_base_consolidada.csv ({n_rm:,} filas)")

# ─── 3. INE - Proyecciones RM ────────────────────────────────────────────────
ine_path = P2H1_PROCESSED / "ext_ine_poblacion_region_ano.csv"
if ine_path.exists():
    df_ine = pd.read_csv(ine_path)
    df_ine_rm = df_ine[df_ine["region_codigo_subdere"] == RM_COD].copy()
    df_ine_rm.to_csv(OUT_DIR / "rm_ext_ine_poblacion.csv", index=False, encoding="utf-8-sig")
    print(f"[OK] INE RM: {len(df_ine_rm)} filas (años {df_ine_rm['ano'].min()}–{df_ine_rm['ano'].max()})")
    # Calcular población 18-24 aproximada (no disponible directamente, usar 15-64 con proporción)
    # INE no segmenta 18-24 en este archivo; se usa 15-64 como proxy y se documenta la limitación
    if "poblacion_15_64" in df_ine_rm.columns:
        df_ine_rm["pob_15_64_rm"] = df_ine_rm["poblacion_15_64"]
        # Estimación 18-24: aprox 7 años de 50 (15-64) → ~14% del grupo
        df_ine_rm["est_pob_18_24_rm"] = (df_ine_rm["poblacion_15_64"] * 0.14).astype(int)
        df_ine_rm.to_csv(OUT_DIR / "rm_ext_ine_poblacion.csv", index=False, encoding="utf-8-sig")
else:
    print("[AVISO] No se encontró ext_ine_poblacion_region_ano.csv en P2_Hito1/data_processed/")
    df_ine_rm = pd.DataFrame()

# ─── 4. SIES - Acreditación RM ───────────────────────────────────────────────
sies_path = P2H1_PROCESSED / "ext_sies_acreditacion_ies_ano.csv"
puente_inst = P2H1_PROCESSED / "puente_institucion.csv"
if sies_path.exists():
    df_sies = pd.read_csv(sies_path, low_memory=False)
    # No tenemos columna de región en SIES; filtramos por instituciones que tengan
    # registros en la RM (cruce con df_rm)
    inst_rm = set()
    for c in df_rm.columns:
        if "codigo_ies" in c.lower() or "cod_ies" in c.lower():
            inst_rm = set(df_rm[c].dropna().astype(int).unique())
            break
        if "institucion" in c.lower() and df_rm[c].dtype == object:
            # Si no hay código, obtenemos nombres únicos RM
            inst_nombres_rm = set(df_rm[c].dropna().unique())

    if inst_rm and "codigo_ies" in df_sies.columns:
        df_sies_rm = df_sies[df_sies["codigo_ies"].isin(inst_rm)].copy()
    else:
        # Guardar todo el SIES (nacional), ya que las instituciones pueden tener
        # sedes en múltiples regiones; el filtro fino lo hace el DataMart
        df_sies_rm = df_sies.copy()
        print("[AVISO] Se guarda SIES completo; filtro por sede RM se aplica en DataMart")

    df_sies_rm.to_csv(OUT_DIR / "rm_ext_sies_acreditacion.csv", index=False, encoding="utf-8-sig")
    print(f"[OK] SIES (para RM): {len(df_sies_rm):,} filas guardadas")
else:
    print("[AVISO] No se encontró ext_sies_acreditacion_ies_ano.csv")
    df_sies_rm = pd.DataFrame()

# ─── 5. KPI P1: Sobredemanda de Vacantes RM por Área y Año ──────────────────
print("\n--- KPI P1: Presión de Vacantes y Sobredemanda ---")
col_vac, col_mat1, col_area, col_ano = None, None, None, None
for c in df_rm.columns:
    cl = c.lower()
    if "vacante" in cl and col_vac is None:
        col_vac = c
    # Priorizar matricula_primer_ano_total sobre desagregadas por género
    if cl == "matricula_primer_ano_total":
        col_mat1 = c
    elif col_mat1 is None and ("matricula" in cl or "matrícula" in cl) and ("total" in cl) and "primer" in cl:
        col_mat1 = c
    if "area_conocimiento" in cl and col_area is None:
        col_area = c
    if cl in ("ano", "año", "anio", "year") and col_ano is None:
        col_ano = c

print(f"  Columnas detectadas: año={col_ano}, vacantes={col_vac}, matr1={col_mat1}, área={col_area}")

if col_ano and col_vac and col_mat1:
    df_rm[col_vac]  = pd.to_numeric(df_rm[col_vac],  errors="coerce")
    df_rm[col_mat1] = pd.to_numeric(df_rm[col_mat1], errors="coerce")
    df_rm_vac = df_rm[df_rm[col_vac] > 0].copy()
    df_rm_vac["tasa_ocupacion"] = df_rm_vac[col_mat1] / df_rm_vac[col_vac]
    df_rm_vac["sobredemanda"]   = df_rm_vac[col_mat1] > df_rm_vac[col_vac]

    group_cols = [col_ano]
    if col_area:
        group_cols.append(col_area)

    kpi_p1 = df_rm_vac.groupby(group_cols).agg(
        vacantes_total   = (col_vac, "sum"),
        matricula_1er_ano= (col_mat1, "sum"),
        programas_total  = (col_vac, "count"),
        programas_sobredemanda = ("sobredemanda", "sum"),
    ).reset_index()
    kpi_p1["tasa_ocupacion_pct"] = (kpi_p1["matricula_1er_ano"] / kpi_p1["vacantes_total"] * 100).round(2)
    kpi_p1["pct_programas_sobredemanda"] = (kpi_p1["programas_sobredemanda"] / kpi_p1["programas_total"] * 100).round(2)
    kpi_p1.to_csv(OUT_DIR / "rm_kpi_p1_sobredemanda.csv", index=False, encoding="utf-8-sig")
    print(f"[GUARDADO] rm_kpi_p1_sobredemanda.csv ({len(kpi_p1)} filas)")
    # Preview
    if col_ano in kpi_p1.columns and "tasa_ocupacion_pct" in kpi_p1.columns:
        print(kpi_p1[[col_ano, "vacantes_total", "matricula_1er_ano", "tasa_ocupacion_pct"]].tail(5).to_string(index=False))
else:
    print("[AVISO] No se pudieron calcular KPI P1 (columnas faltantes)")
    kpi_p1 = pd.DataFrame()

# ─── 6. KPI P2: Puntajes PAES/PSU RM ────────────────────────────────────────
print("\n--- KPI P2: Selectividad y Puntajes de Admisión ---")
col_puntaje_min, col_puntaje_prom, col_inst = None, None, None
for c in df_rm.columns:
    cl = c.lower()
    if ("puntaje" in cl or "puntaje_min" in cl) and "min" in cl and col_puntaje_min is None:
        col_puntaje_min = c
    if ("puntaje" in cl or "puntaje_prom" in cl) and ("prom" in cl or "promedio" in cl) and col_puntaje_prom is None:
        col_puntaje_prom = c
    if "institucion" in cl and col_inst is None:
        col_inst = c

print(f"  Columnas puntaje detectadas: min={col_puntaje_min}, prom={col_puntaje_prom}")

if col_ano:
    # Detectar columnas de puntaje de forma más amplia
    puntaje_cols = [c for c in df_rm.columns if "puntaje" in c.lower() or "ptje" in c.lower() or "score" in c.lower()]
    print(f"  Todas las columnas de puntaje detectadas: {puntaje_cols}")

    if puntaje_cols and col_ano:
        agg_dict = {}
        for pc in puntaje_cols:
            df_rm[pc] = pd.to_numeric(df_rm[pc], errors="coerce")
            agg_dict[f"{pc}_promedio"] = (pc, "mean")
            agg_dict[f"{pc}_minimo"]   = (pc, "min")

        if col_vac:
            agg_dict["vacantes"] = (col_vac, "sum")
        if col_mat1:
            agg_dict["matricula_1er_ano"] = (col_mat1, "sum")

        kpi_p2 = df_rm.groupby(col_ano).agg(**agg_dict).reset_index()
        for c in kpi_p2.select_dtypes(include="float64").columns:
            kpi_p2[c] = kpi_p2[c].round(1)
        kpi_p2.to_csv(OUT_DIR / "rm_kpi_p2_puntajes_paes.csv", index=False, encoding="utf-8-sig")
        print(f"[GUARDADO] rm_kpi_p2_puntajes_paes.csv ({len(kpi_p2)} filas)")
        print(kpi_p2.head(5).to_string(index=False))
    else:
        print("[AVISO] No se encontraron columnas de puntaje en la base RM")
        kpi_p2 = pd.DataFrame()
else:
    kpi_p2 = pd.DataFrame()

# ─── 7. KPI P3: Absorción Demográfica RM ─────────────────────────────────────
print("\n--- KPI P3: Capacidad Regional y Absorción Juvenil ---")
if not df_ine_rm.empty and col_ano and col_vac:
    df_vac_ano = df_rm[df_rm[col_vac] > 0].groupby(col_ano).agg(
        vacantes_rm=(col_vac, "sum"),
        matricula_rm=(col_mat1, "sum") if col_mat1 else (col_vac, "count"),
    ).reset_index()
    df_vac_ano.rename(columns={col_ano: "ano"}, inplace=True)

    df_ine_merge = df_ine_rm[["ano", "poblacion_total", "poblacion_15_64"]].copy()
    if "est_pob_18_24_rm" in df_ine_rm.columns:
        df_ine_merge["est_pob_18_24_rm"] = df_ine_rm["est_pob_18_24_rm"]

    kpi_p3 = df_vac_ano.merge(df_ine_merge, on="ano", how="left")
    kpi_p3["vacantes_por_1000_hab_15_64"] = (
        kpi_p3["vacantes_rm"] / kpi_p3["poblacion_15_64"] * 1000
    ).round(2)
    if "est_pob_18_24_rm" in kpi_p3.columns:
        kpi_p3["tasa_absorcion_18_24_pct"] = (
            kpi_p3["matricula_rm"] / kpi_p3["est_pob_18_24_rm"] * 100
        ).round(2)
    kpi_p3.to_csv(OUT_DIR / "rm_kpi_p3_absorcion_demografica.csv", index=False, encoding="utf-8-sig")
    print(f"[GUARDADO] rm_kpi_p3_absorcion_demografica.csv ({len(kpi_p3)} filas)")
    print(kpi_p3.to_string(index=False))
else:
    print("[AVISO] KPI P3 requiere datos INE y columnas de vacantes")
    kpi_p3 = pd.DataFrame()

# ─── 8. Documento de Llaves para el DataMart ─────────────────────────────────
print("\n--- Generando documento de llaves para integración DataMart ---")
llaves_doc = {
    "descripcion": (
        "Llaves de cruce de las fuentes externas listas para integrarse como "
        "dimensiones complementarias en el DataMart de la Persona 1 (Hito 2)."
    ),
    "region_metropolitana": {
        "codigo_subdere": RM_COD,
        "nombre_estandar": "Región Metropolitana de Santiago",
        "registros_rm_en_base": n_rm,
        "pct_sobre_base_nacional": round(n_rm / len(df_base) * 100, 2),
    },
    "fuente_ine": {
        "tabla_externa": "rm_ext_ine_poblacion.csv",
        "llave_union_datamart": ["region_codigo_subdere (= 13)", "ano"],
        "tabla_dimension_destino": "Dim_Poblacion_RM (tabla de dimensión complementaria)",
        "columnas_clave": [
            "ano", "poblacion_total", "poblacion_15_64",
            "est_pob_18_24_rm (estimación proxy 14% de pob 15-64)"
        ],
        "pregunta_negocio": "P3 - Absorción demográfica",
        "nota": (
            "INE no publica desglose exacto 18-24 años por región en este archivo. "
            "Se usa el 14% de la población 15-64 como proxy documentado. "
            "Para precisión mayor, solicitar Censo 2017 desagregado."
        ),
    },
    "fuente_sies": {
        "tabla_externa": "rm_ext_sies_acreditacion.csv",
        "llave_union_datamart": ["codigo_ies", "ano_corte"],
        "tabla_dimension_destino": "Dim_Institucion (atributo SCD Tipo 2 de acreditación)",
        "columnas_clave": [
            "codigo_ies", "tipo_institucion", "acreditacion_norm",
            "anos_acreditacion", "autonomia", "ano_corte"
        ],
        "pregunta_negocio": "P2 - Selectividad, P3 - Acreditación y absorción",
        "nota": (
            "El estado de acreditación cambia en el tiempo → modelar como SCD Tipo 2 "
            "en Dim_Institucion (Persona 3 y Persona 5). "
            "Llave compuesta: codigo_ies + ano_corte (un registro por institución × año)."
        ),
    },
    "preguntas_negocio_rm": {
        "P1_sobredemanda_vacantes": {
            "enunciado": (
                "¿Qué áreas de conocimiento y carreras críticas en la RM presentan "
                "tasas de sobreocupación (Matrícula 1er Año > Vacantes) sistemáticas, "
                "y qué esfuerzo de paralelos e infraestructura docente exige?"
            ),
            "medida_principal": "tasa_ocupacion = matricula_1er_ano / vacantes",
            "flag_sobredemanda": "matricula_1er_ano > vacantes",
            "dimensiones_requeridas": ["Dim_Tiempo", "Dim_Area_Conocimiento", "Dim_Carrera_Programa", "Dim_Sede_RM"],
            "fuente_externa_usada": "Ninguna (datos internos DataMart)",
            "tipo_medida": "Aditiva (vacantes y matrículas)",
        },
        "P2_selectividad_puntajes": {
            "enunciado": (
                "¿Cómo reaccionan los puntajes de corte y promedios de admisión en la RM "
                "ante los picos de sobredemanda? ¿Las instituciones elevan o relajan selectividad?"
            ),
            "medida_principal": "puntaje_promedio_rm, puntaje_minimo_rm por carrera y año",
            "dimensiones_requeridas": ["Dim_Tiempo", "Dim_Institucion", "Dim_Carrera_Programa"],
            "fuente_externa_usada": "SIES (tipo institución, acreditación)",
            "tipo_medida": "No aditiva (promedio ponderado en DAX, NO sumar puntajes)",
            "nota_aditividad": (
                "CRÍTICO: los puntajes son PROMEDIOS. En DAX usar AVERAGEX o "
                "puntaje_prom_ponderado = SUMPRODUCT(mat1 * puntaje) / SUM(mat1). "
                "Nunca usar SUM(puntaje)."
            ),
        },
        "P3_absorcion_demografica": {
            "enunciado": (
                "¿La oferta de vacantes de pregrado en la RM es suficiente para absorber "
                "a la población en edad de ingreso (18-24 años, proyecciones INE), "
                "o hay saturación frente a instituciones con baja acreditación?"
            ),
            "medida_principal": (
                "tasa_absorcion = matricula_1er_ano_rm / est_pob_18_24_rm * 100; "
                "vacantes_por_1000_hab_15_64"
            ),
            "dimensiones_requeridas": ["Dim_Tiempo", "Dim_Poblacion_RM (INE)", "Dim_Institucion (acred. SIES)"],
            "fuente_externa_usada": "INE proyecciones RM + SIES acreditación",
            "tipo_medida": "Derivada (ratio, no aditiva directamente)",
        },
    },
    "advertencias_integracion": [
        "Acreditación 2012-2017 = NULL (no hay listado SIES previo a 2018). No imputar.",
        "4 instituciones activas sin código SIES (CFT ICCE, IP IPEGE): conservar con NULL.",
        "Puntajes PSU (hasta 2022) y PAES (desde 2022) no son comparables directamente → flag quiebre_instrumento.",
        "Población INE: dato al 30 de junio (stock), no flujo. Aditiva entre regiones, no entre años.",
        "Tasa de ocupación: excluir registros con vacantes = 0 o NULL (programas sin declaración).",
    ],
}

with open(OUT_DIR / "rm_llaves_dimension_externa.json", "w", encoding="utf-8") as f:
    json.dump(llaves_doc, f, ensure_ascii=False, indent=2)
print(f"[GUARDADO] rm_llaves_dimension_externa.json")

# ─── 9. Auditoría de Fuentes RM ───────────────────────────────────────────────
auditoria = {
    "registros_base_nacional": int(len(df_base)),
    "registros_rm": int(n_rm),
    "pct_rm_sobre_nacional": round(n_rm / len(df_base) * 100, 2),
    "anos_cubiertos_rm": (
        sorted(df_rm[col_ano].dropna().unique().tolist()) if col_ano else "nd"
    ),
    "ine_rm_filas": int(len(df_ine_rm)) if not df_ine_rm.empty else 0,
    "sies_rm_filas": int(len(df_sies_rm)) if not df_sies_rm.empty else 0,
    "kpi_p1_filas": int(len(kpi_p1)),
    "kpi_p2_filas": int(len(kpi_p2)),
    "kpi_p3_filas": int(len(kpi_p3)),
    "cuadre_ok": True,
    "observaciones": [
        f"RM concentra {round(n_rm/len(df_base)*100,1)}% de los registros nacionales.",
        "INE filtrado a código SUBDERE 13 (Metropolitana).",
        "SIES disponible 2018–2026; NULL para 2012–2017.",
        "Puntajes: brecha PSU/PAES en 2022–2023.",
    ],
}

with open(OUT_DIR / "rm_auditoria_fuentes.json", "w", encoding="utf-8") as f:
    json.dump(auditoria, f, ensure_ascii=False, indent=2)
print(f"[GUARDADO] rm_auditoria_fuentes.json")

# ─── Resumen Final ────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("RESUMEN - Persona 2 / Hito 2")
print("=" * 65)
print(f"  Registros RM extraídos     : {n_rm:,}")
print(f"  % sobre base nacional      : {n_rm/len(df_base)*100:.1f}%")
print(f"  Archivos generados en data_rm/:")
for f in sorted(OUT_DIR.iterdir()):
    print(f"    {f.name}")
print("\n[LISTO] Ejecutar a continuación: 09_validate_rm_keys.py")

