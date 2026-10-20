import sys
import warnings
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# Configuracion de estilo visual corporativo BI
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#D0D7DE'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#E1E4E8'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

SCRIPT_DIR = Path(__file__).resolve().parent
P4_ROOT = SCRIPT_DIR.parent
INTELIGENCIA_ROOT = P4_ROOT.parent

BASE_CSV = INTELIGENCIA_ROOT / "P_IN" / "data_processed" / "base_indices_consolidada_2012_2026.csv"
DATA_P2 = INTELIGENCIA_ROOT / "P2_Hito1" / "data_processed"
INE_CSV = DATA_P2 / "ext_ine_poblacion_region_ano.csv"
SIES_CSV = DATA_P2 / "ext_sies_acreditacion_ies_ano.csv"
PUENTE_INST_CSV = DATA_P2 / "puente_institucion.csv"

PROTO_DIR = P4_ROOT / "data_validation" / "visual_prototypes"
PROTO_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("GENERACION DE PROTOTIPOS VISUALES POWER BI")
print("=" * 80)

# A) Carga de datos
print("\n[1/4] Cargando datasets...")
df_base = pd.read_csv(
    BASE_CSV,
    low_memory=False,
    encoding="utf-8",
    usecols=[
        "ano", "nombre_institucion", "tipo_institucion", "region_codigo_subdere",
        "region_nombre_estandar", "vacantes", "matricula_primer_ano_total",
        "matricula_total", "flag_vacantes_declaradas"
    ]
)
df_ine = pd.read_csv(INE_CSV, encoding="utf-8")
df_sies = pd.read_csv(SIES_CSV, encoding="utf-8")
df_puente = pd.read_csv(PUENTE_INST_CSV, encoding="utf-8")

# Paleta ejecutiva coincidente con los informes LaTeX
PRIMARY_BLUE = "#102C57"
SECONDARY_BLUE = "#35598F"
ACCENT_TEAL = "#146E78"
ALERT_RED = "#D32F2F"
OPTIMAL_GREEN = "#2E7D32"
LIGHT_BG = "#F8F9FA"


# Prototipo 1: P1(Equidad territorial)

print("\n[2/4] Generando Prototipo Visual P1 (Equidad Territorial)...")
p1_agg = df_base.groupby(["ano", "region_codigo_subdere", "region_nombre_estandar"], as_index=False)[
    "matricula_primer_ano_total"
].sum()
p1_merged = p1_agg.merge(df_ine, on=["region_codigo_subdere", "ano"], how="left")
p1_merged["tasa_1000"] = 1000.0 * p1_merged["matricula_primer_ano_total"] / p1_merged["poblacion_15_64"]

p1_comp = p1_merged[p1_merged["ano"].isin([2018, 2026])].pivot(
    index="region_nombre_estandar",
    columns="ano",
    values="tasa_1000"
).reset_index()
p1_comp = p1_comp.sort_values(by=2026, ascending=True)

fig, ax = plt.subplots(figsize=(10, 7), facecolor="white")
y_pos = np.arange(len(p1_comp))
height = 0.38

bars_2018 = ax.barh(y_pos - height/2, p1_comp[2018], height, label="Año 2018", color="#90A4AE", alpha=0.9)
bars_2026 = ax.barh(y_pos + height/2, p1_comp[2026], height, label="Año 2026", color=SECONDARY_BLUE, alpha=0.95)

# Linea de promedio nacional 2026
prom_2026 = (
    1000.0 * df_base[df_base["ano"] == 2026]["matricula_primer_ano_total"].sum() /
    df_ine[df_ine["ano"] == 2026]["poblacion_15_64"].sum()
)
ax.axvline(prom_2026, color=ALERT_RED, linestyle="--", linewidth=1.5, label=f"Promedio Nacional 2026 ({prom_2026:.1f} ‰)")

ax.set_yticks(y_pos)
ax.set_yticklabels(p1_comp["region_nombre_estandar"], fontsize=9.5, fontweight="medium")
ax.set_xlabel("Matricula de 1er Año por cada 1.000 habitantes (15 a 64 años)", fontsize=10, fontweight="bold", color=PRIMARY_BLUE)
ax.set_title("P1: Equidad Territorial - Capacidad de Oferta por 1.000 Habitantes (2018 vs. 2026)\n"
             "Validacion Visual para Grafico de Barras Ordenadas en Power BI", fontsize=12, fontweight="bold", color=PRIMARY_BLUE, pad=15)
ax.legend(loc="lower right", frameon=True, facecolor="white", edgecolor="#D0D7DE", fontsize=9.5)
ax.grid(axis="x", linestyle="--", alpha=0.6)
ax.set_xlim(0, p1_comp[2026].max() * 1.15)

# Etiquetas en las barras de 2026
for i, val in enumerate(p1_comp[2026]):
    ax.text(val + 0.5, i + height/2, f"{val:.1f}", va="center", ha="left", fontsize=8.5, color=PRIMARY_BLUE, fontweight="bold")

plt.tight_layout()
p1_img = PROTO_DIR / "p1_equidad_territorial.png"
plt.savefig(p1_img, dpi=300)
plt.close()
print(f" -> Guardado: {p1_img.name}")


# Prototipo 2: P2(Capacidad y ocupacion de vacantes)

print("\n[3/4] Generando prototipo visual P2...")
df_v = df_base[(df_base["flag_vacantes_declaradas"] == 1) & (df_base["vacantes"] > 0)]

# Panel A: Serie historica nacional 
p2_hist = df_v.groupby("ano").agg(
    vacantes=("vacantes", "sum"),
    matricula=("matricula_primer_ano_total", "sum")
).reset_index()
p2_hist["ocupacion_pct"] = (p2_hist["matricula"] / p2_hist["vacantes"]) * 100.0

# Panel B: Ocupacion por tipo de institucion
p2_tipo = df_v[df_v["ano"] == 2026].groupby("tipo_institucion").agg(
    vacantes=("vacantes", "sum"),
    matricula=("matricula_primer_ano_total", "sum")
).reset_index()
p2_tipo["ocupacion_pct"] = (p2_tipo["matricula"] / p2_tipo["vacantes"]) * 100.0

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), facecolor="white")

# Subplot 1: Serie temporal
ax1.plot(p2_hist["ano"], p2_hist["ocupacion_pct"], marker="o", linewidth=2.5, color=PRIMARY_BLUE, label="Tasa de Ocupacion Real")
ax1.axhline(100, color=ALERT_RED, linestyle=":", linewidth=1.2, label="Capacidad Teorica (100%)")
ax1.axhline(80, color=ACCENT_TEAL, linestyle="--", linewidth=1.2, label="Umbral Optimo (80%)")
ax1.fill_between(p2_hist["ano"], 80, 100, color=ACCENT_TEAL, alpha=0.1)

ax1.set_title("Evolucion historica de ocupacion", fontsize=11, fontweight="bold", color=PRIMARY_BLUE)
ax1.set_xlabel("Año de Proceso", fontsize=9.5, fontweight="bold")
ax1.set_ylabel("Tasa de Ocupacion (%)", fontsize=9.5, fontweight="bold")
ax1.set_ylim(70, 105)
ax1.set_xticks(p2_hist["ano"])
ax1.set_xticklabels(p2_hist["ano"], rotation=45, ha="right", fontsize=8.5)
ax1.grid(True)
ax1.legend(loc="lower left", fontsize=8.5)

for _, row in p2_hist.iterrows():
    ax1.annotate(f"{row['ocupacion_pct']:.1f}%", (row['ano'], row['ocupacion_pct'] + 1.0),
                 ha="center", fontsize=8, fontweight="bold", color=PRIMARY_BLUE)

# Subplot 2: Comparativa por tipo de institucion
colors = [SECONDARY_BLUE if x >= 80 else ALERT_RED for x in p2_tipo["ocupacion_pct"]]
bars = ax2.bar(p2_tipo["tipo_institucion"], p2_tipo["ocupacion_pct"], color=colors, width=0.55, alpha=0.9)
ax2.axhline(80, color=ACCENT_TEAL, linestyle="--", linewidth=1.2, label="Umbral Referencia 80%")
ax2.set_title("Tasa de Ocupacion por Tipo de IES (2026)", fontsize=11, fontweight="bold", color=PRIMARY_BLUE)
ax2.set_ylabel("Tasa de Ocupacion (%)", fontsize=9.5, fontweight="bold")
ax2.set_ylim(0, 110)
ax2.grid(axis="y")
ax2.legend(loc="lower right", fontsize=8.5)

for bar in bars:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f"{yval:.1f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")

plt.suptitle("P2: Uso de Capacidad",
             fontsize=12, fontweight="bold", color=PRIMARY_BLUE, y=0.98)
plt.tight_layout()
p2_img = PROTO_DIR / "p2_capacidad_ocupacion.png"
plt.savefig(p2_img, dpi=300)
plt.close()
print(f" -> Guardado: {p2_img.name}")


# Prototipo 3: P3(Calidad y acreditacion)

print("\n[4/4] Generando Prototipo Visual P3 (Calidad y Competencia)...")
df_b_inst = df_base.merge(
    df_puente[["nombre_institucion_cned", "codigo_ies"]],
    left_on="nombre_institucion",
    right_on="nombre_institucion_cned",
    how="left"
)
df_p3 = df_b_inst.merge(
    df_sies[["codigo_ies", "ano_corte", "acreditacion_norm", "anos_acreditacion"]],
    left_on=["codigo_ies", "ano"],
    right_on=["codigo_ies", "ano_corte"],
    how="left"
)
df_p3["estado_acreditacion"] = df_p3["acreditacion_norm"].fillna("Sin dato de acreditacion")

# Panel A: Matriz 100% apilada
p3_series = df_p3[df_p3["ano"] >= 2018].groupby(
    ["ano", "estado_acreditacion"]
)["matricula_primer_ano_total"].sum().unstack(fill_value=0)
p3_pct = p3_series.div(p3_series.sum(axis=1), axis=0).mul(100.0)

# Panel B: Dispersion Institucional 2026
p3_inst_2026 = df_p3[df_p3["ano"] == 2026].groupby(
    ["nombre_institucion", "tipo_institucion", "estado_acreditacion"], as_index=False
).agg(
    anos_acreditacion=("anos_acreditacion", "max"),
    matricula_1er_ano=("matricula_primer_ano_total", "sum")
)
p3_inst_2026["anos_acreditacion"] = p3_inst_2026["anos_acreditacion"].fillna(0)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), facecolor="white")

# Stacked bar chart
years = p3_pct.index
bottom = np.zeros(len(years))
color_map = {
    "Acreditada": "#2E7D32",
    "Acreditacion extendida": "#1565C0",
    "Bajo tutela": "#F57C00",
    "No acreditada": "#D32F2F",
    "Sin dato de acreditacion": "#757575"
}

for cat in ["Acreditada", "Acreditacion extendida", "Bajo tutela", "No acreditada", "Sin dato de acreditacion"]:
    if cat in p3_pct.columns:
        vals = p3_pct[cat].values
        ax1.bar(years, vals, bottom=bottom, label=cat, color=color_map.get(cat, "#B0BEC5"), width=0.65)
        bottom += vals

ax1.set_title("Evolucion % matricula por estado SIES (2018-2026)", fontsize=11, fontweight="bold", color=PRIMARY_BLUE)
ax1.set_ylabel("% de matricula de 1er año", fontsize=9.5, fontweight="bold")
ax1.set_xlabel("Año de admision", fontsize=9.5, fontweight="bold")
ax1.set_ylim(0, 100)
ax1.set_xticks(years)
ax1.set_xticklabels(years, rotation=45, ha="right", fontsize=8.5)
ax1.grid(axis="y", linestyle="--", alpha=0.6)
ax1.legend(loc="upper left", bbox_to_anchor=(0.0, -0.18), ncol=2, fontsize=8, frameon=True)

# Scatter plot
tipos = p3_inst_2026["tipo_institucion"].unique()
tipo_colors = {"UNIVERSIDAD": PRIMARY_BLUE, "INSTITUTO PROFESIONAL": "#F57C00", "CENTRO DE FORMACION TECNICA": ACCENT_TEAL}

for tipo in tipos:
    sub = p3_inst_2026[p3_inst_2026["tipo_institucion"] == tipo]
    ax2.scatter(
        sub["anos_acreditacion"],
        sub["matricula_1er_ano"],
        label=tipo,
        color=tipo_colors.get(tipo, "#757575"),
        alpha=0.75,
        s=45,
        edgecolors="none"
    )

ax2.set_title("Dispersion: Años acreditacion vs. Matricula 1er año", fontsize=11, fontweight="bold", color=PRIMARY_BLUE)
ax2.set_xlabel("Años de acreditacion institucional", fontsize=9.5, fontweight="bold")
ax2.set_ylabel("Matricula de 1er año", fontsize=9.5, fontweight="bold")
ax2.set_xlim(-0.5, 7.5)
ax2.set_xticks(range(0, 8))
ax2.grid(True, linestyle="--", alpha=0.6)
ax2.legend(loc="upper left", fontsize=8, frameon=True)

plt.suptitle("P3: Calidad y Acreditacion)",
             fontsize=12, fontweight="bold", color=PRIMARY_BLUE, y=0.98)
plt.tight_layout()
p3_img = PROTO_DIR / "p3_calidad_acreditacion.png"
plt.savefig(p3_img, dpi=300)
plt.close()
print(f" -> Guardado: {p3_img.name}")

# Prototipo 4: Arquitectura de navegacion y wireframe del dashboard

print("\n[5/5] Generando Wireframe Conceptual del Dashboard Power BI...")
fig, ax = plt.subplots(figsize=(12, 6.8), facecolor="#ECEFF1")
ax.axis("off")

# Banner Superior
ax.fill_between([0, 100], [90, 90], [100, 100], color=PRIMARY_BLUE)
ax.text(3, 95, "DASHBOARD ESTRATEGICO DE EDUCACION SUPERIOR (2012–2026)", fontsize=13, fontweight="bold", color="white", va="center")
ax.text(97, 95, "POWER BI | HITO 1 PROTOTYPE", fontsize=10, fontweight="bold", color="#80D8FF", va="center", ha="right")

# Barra lateral de navegacion y filtros 
ax.fill_between([0, 22], [0, 0], [90, 90], color="#263238")
ax.text(11, 85, "FILTROS GLOBALES", color="white", fontweight="bold", fontsize=10, ha="center")
ax.text(11, 78, "[ Slicer: Año (2012-2026) ]\n[ Slicer: Tipo Institucion ]\n[ Slicer: Macro-Zona / Region ]\n[ Slicer: Area Conocimiento ]",
        color="#B0BEC5", fontsize=8.5, ha="center", va="top")

ax.text(11, 48, "PAGINAS DEL PANEL", color="white", fontweight="bold", fontsize=10, ha="center")
pages = [
    "1. Resumen Ejecutivo (KPIs)",
    "2. P1: Equidad Territorial",
    "3. P2: Uso de Capacidad",
    "4. P3: Calidad y Acreditacion",
    "5. Matriz Detallada Oferta"
]
for idx, p in enumerate(pages):
    y_btn = 40 - idx * 7
    ax.fill_between([2, 20], [y_btn - 2.5, y_btn - 2.5], [y_btn + 2.5, y_btn + 2.5], color=SECONDARY_BLUE if idx == 0 else "#37474F")
    ax.text(11, y_btn, p, color="white", fontsize=8, ha="center", va="center", fontweight="bold" if idx == 0 else "normal")

# Tarjetas KPI superiores
kpis = [
    ("Matricula 1er Año Total", "399.015", "+19.7% vs 2022"),
    ("Vacantes Declaradas", "472.580", "158.211 programas"),
    ("Tasa Ocupacion Nacional", "84.4%", "Optimo (>80%)"),
    ("Tasa Promedio p/1000 hab", "27.6 ‰", "Brecha Max: 35.5 vs 14.1"),
    ("% Matricula Acreditada", "90.5%", "SIES Oficial 2026")
]
for i, (titulo, val, sub) in enumerate(kpis):
    x_start = 24 + i * 15
    ax.fill_between([x_start, x_start + 14], [75, 75], [88, 88], color="white", edgecolor="#CFD8DC")
    ax.text(x_start + 7, 84, titulo, fontsize=7.5, color="#546E7A", ha="center", fontweight="bold")
    ax.text(x_start + 7, 80, val, fontsize=12, color=PRIMARY_BLUE, ha="center", fontweight="bold")
    ax.text(x_start + 7, 76.5, sub, fontsize=6.8, color=ACCENT_TEAL, ha="center")

# Panel visual izquierdo 
ax.fill_between([24, 60], [5, 5], [72, 72], color="white", edgecolor="#CFD8DC")
ax.text(42, 68, "Visual 1: Equidad Territorial (P1)", fontsize=10, fontweight="bold", color=PRIMARY_BLUE, ha="center")
ax.text(42, 64, "Mapa Coropletico Regional / Barras Ordenadas vs Poblacion INE", fontsize=8, color="#78909C", ha="center")
ax.text(42, 38, "[ Prototipo de Grafico de Barras Ordenadas por Tasa 1.000 hab ]\n(Top: RM 35.5 ‰, Biobio 32.5 ‰ | Min: O'Higgins 14.1 ‰)",
        fontsize=8.5, color="#90A4AE", ha="center", va="center")

# Panel visual derecho
ax.fill_between([62, 98], [5, 5], [72, 72], color="white", edgecolor="#CFD8DC")
ax.text(80, 68, "Visual 2 & 3: Capacidad & Calidad (P2 / P3)", fontsize=10, fontweight="bold", color=PRIMARY_BLUE, ha="center")
ax.text(80, 64, "Matriz de Ocupacion y Dispersion Acreditacion SIES", fontsize=8, color="#78909C", ha="center")
ax.text(80, 38, "[ Prototipo Matriz Heatmap Tipo IES x Region ]\n+\n[ Dispersion Años Acreditacion vs Matricula ]",
        fontsize=8.5, color="#90A4AE", ha="center", va="center")

plt.tight_layout()
wire_img = PROTO_DIR / "dashboard_wireframe_arquitectura.png"
plt.savefig(wire_img, dpi=300)
plt.close()
print(f" -> Guardado: {wire_img.name}")

print("\n[OK] Todos los prototipos visuales fueron generados exitosamente.")
print("=" * 80)
