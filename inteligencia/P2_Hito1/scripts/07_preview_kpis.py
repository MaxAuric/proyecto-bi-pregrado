"""
07_preview_kpis.py  -  Persona 2 (Hito 1)
Valida que las dos fuentes externas permiten responder las 3 preguntas de negocio y entrega cifras
preliminares (no sustituyen al panel de Hito 3). Salida: data_processed/kpi_preview_*.csv
"""
from pathlib import Path
import warnings
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data_processed"
BASE = ROOT.parent / "P_IN" / "data_processed" / "base_indices_consolidada_2012_2026.csv"

b = pd.read_csv(BASE, low_memory=False, encoding="utf-8", usecols=[
    "ano", "nombre_institucion", "region_codigo_subdere", "region_nombre_estandar", "tipo_carrera",
    "vacantes", "matricula_primer_ano_total", "matricula_total", "flag_vacantes_declaradas"])
ine = pd.read_csv(OUT / "ext_ine_poblacion_region_ano.csv")
sies = pd.read_csv(OUT / "ext_sies_acreditacion_ies_ano.csv")
pin = pd.read_csv(OUT / "puente_institucion.csv")

# ---- P1 / P2: demanda y equidad territorial -> matricula 1er ano cada 1.000 habitantes de 15-64 anos
reg = (b.groupby(["ano", "region_codigo_subdere", "region_nombre_estandar"], as_index=False)
         ["matricula_primer_ano_total"].sum().merge(ine, on=["region_codigo_subdere", "ano"], how="left"))
reg["mat1_por_1000_hab_15_64"] = 1000 * reg["matricula_primer_ano_total"] / reg["poblacion_15_64"]
reg.to_csv(OUT / "kpi_preview_region_ano.csv", index=False, encoding="utf-8")

# ---- P3: calidad institucional -> % matricula 1er ano en IES acreditadas (2018-2026)
x = (b.merge(pin[["nombre_institucion_cned", "codigo_ies"]], left_on="nombre_institucion",
             right_on="nombre_institucion_cned", how="left")
       .merge(sies[["codigo_ies", "ano_corte", "acreditacion_norm", "anos_acreditacion"]],
              left_on=["codigo_ies", "ano"], right_on=["codigo_ies", "ano_corte"], how="left"))
x["estado"] = x["acreditacion_norm"].fillna("Sin dato de acreditacion")
acr = (x[x.ano >= 2018].groupby(["ano", "estado"])["matricula_primer_ano_total"].sum().unstack(fill_value=0))
acr_pct = acr.div(acr.sum(axis=1), axis=0).mul(100).round(2)
acr_pct.to_csv(OUT / "kpi_preview_acreditacion_ano.csv", encoding="utf-8")

# ---- P2: vacantes y ocupacion (solo registros con vacantes declaradas)
v = b[(b.flag_vacantes_declaradas == 1) & (b.vacantes > 0)]
oc = v.groupby("ano").apply(lambda d: 100 * d.matricula_primer_ano_total.sum() / d.vacantes.sum()).round(1)
oc.to_csv(OUT / "kpi_preview_ocupacion_ano.csv", header=["ocupacion_pct"], encoding="utf-8")

pd.set_option("display.width", 220, "display.max_rows", 100)
print("MATRICULA 1ER ANO NACIONAL"); print(b.groupby("ano").matricula_primer_ano_total.sum().to_string())
print("\nOCUPACION % (matricula 1er ano / vacantes declaradas)"); print(oc.to_string())
print("\nREGION 2026: matricula 1er ano por 1.000 hab 15-64")
print(reg[reg.ano == 2026][["region_nombre_estandar", "matricula_primer_ano_total", "poblacion_15_64",
                            "mat1_por_1000_hab_15_64"]].sort_values("mat1_por_1000_hab_15_64").round(1).to_string(index=False))
print("\nREGION 2018 vs 2026")
p = reg[reg.ano.isin([2018, 2026])].pivot(index="region_nombre_estandar", columns="ano", values="mat1_por_1000_hab_15_64").round(1)
print(p.to_string())
print("\nACREDITACION % matricula 1er ano"); print(acr_pct.to_string())
