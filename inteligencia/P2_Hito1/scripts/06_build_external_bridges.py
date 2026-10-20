"""
06_build_external_bridges.py  -  Persona 2 (Hito 1)

Construye:
  - ext_ine_poblacion_region_ano.csv      (Fuente 1, grano: region x ano)
  - ext_sies_acreditacion_ies_ano.csv     (Fuente 2, grano: institucion x corte anual)
  - puente_region.csv                     (SUBDERE <-> hoja INE <-> nombres de la base CNED)
  - puente_institucion.csv                (nombre_institucion CNED -> codigo IES SIES)
  - cruce_resumen.json / cruce_no_coincidentes_institucion.csv  (tasas de coincidencia)

Reproducible: python P2_Hito1/scripts/06_build_external_bridges.py
"""
import re, json, glob, unicodedata, warnings, difflib
from pathlib import Path
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent / "P_IN" / "data_processed" / "base_indices_consolidada_2012_2026.csv"
EXT = ROOT / "data_external"
OUT = ROOT / "data_processed"
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------- utilidades
def norm(s):
    """Mayusculas, sin tildes, sin puntuacion, espacios colapsados."""
    if pd.isna(s):
        return ""
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = s.upper().replace("`", "'")
    s = re.sub(r"[^A-Z0-9' ]", " ", s.replace("-", " "))
    return re.sub(r"\s+", " ", s).strip()


def expandir_institucion(n):
    """Convierte la nomenclatura abreviada de la base CNED a la denominacion SIES."""
    n = norm(n)
    n = re.sub(r"^PONTIFICIA U\b", "PONTIFICIA UNIVERSIDAD", n)
    n = re.sub(r"^U\b", "UNIVERSIDAD", n)
    n = re.sub(r"^(I P|IP)\b", "INSTITUTO PROFESIONAL", n)
    n = re.sub(r"^(C F T|CFT)\b", "CENTRO DE FORMACION TECNICA", n)
    n = n.replace("'", "")
    return re.sub(r"\s+", " ", n).strip()


def sin_conectores(n):
    return re.sub(r"\b(DE|DEL|LA|LAS|LOS|Y|E)\b", " ", n).replace("  ", " ").strip()


# ---------------------------------------------------------------- Fuente 1: INE
REGIONES = [  # codigo SUBDERE, hoja INE, nombre estandar (P1)
    (15, "Arica y Parinacota"), (1, "Tarapacá"), (2, "Antofagasta"), (3, "Atacama"),
    (4, "Coquimbo"), (5, "Valparaíso"), (13, "Metropolitana"), (6, "O'Higgins"),
    (7, "Maule"), (16, "Ñuble"), (8, "Biobío"), (9, "La Araucanía"),
    (14, "Los Ríos"), (10, "Los Lagos"), (11, "Aysén"), (12, "Magallanes"),
]


def parse_ine():
    x = pd.ExcelFile(EXT / "INE_proyecciones_2017_region_area.xlsx")
    filas = []
    for cod, hoja in REGIONES:
        d = x.parse(hoja, header=None)
        r_year = d.index[d.iloc[:, 1:].apply(lambda r: (r == 2002).any(), axis=1)][0]
        years = d.iloc[r_year, 1:].tolist()
        lab = d.iloc[:, 0].astype(str).str.strip()
        i0 = lab[lab == "Población (al 30 de junio)"].index[0]

        def fila(etq, desde=i0):
            idx = lab[(lab == etq) & (lab.index > desde)].index[0]
            return d.iloc[idx, 1:].tolist()

        tot, hom, muj = fila("Ambos sexos"), fila("Hombres"), fila("Mujeres")
        g0, g1, g2 = fila("0-14 años"), fila("15-64 años"), fila("65 y más años")
        for k, y in enumerate(years):
            filas.append(dict(region_codigo_subdere=cod, hoja_ine=hoja, ano=int(y),
                              poblacion_total=tot[k], poblacion_hombres=hom[k],
                              poblacion_mujeres=muj[k], poblacion_0_14=g0[k],
                              poblacion_15_64=g1[k], poblacion_65_mas=g2[k]))
    df = pd.DataFrame(filas).sort_values(["region_codigo_subdere", "ano"])
    df.to_csv(OUT / "ext_ine_poblacion_region_ano.csv", index=False, encoding="utf-8")
    return df


# ---------------------------------------------------------------- Fuente 2: SIES
def pick(cols, *prefijos):
    for p in prefijos:
        for c in cols:
            if str(c).lower().startswith(p.lower()):
                return c
    return None


def parse_sies():
    out = []
    for f in sorted(glob.glob(str(EXT / "SIES_IES_vigentes_*.xlsx"))):
        corte = Path(f).stem.split("_")[-1]            # 2025-12
        ano = int(corte[:4])
        x = pd.ExcelFile(f)
        d = x.parse(x.sheet_names[0])
        c = list(d.columns)
        m = {
            "codigo_ies": pick(c, "código de inst", "código inst", "codigo de inst", "codigo inst"),
            "tipo_institucion": pick(c, "tipo de institución"),
            "nombre_institucion_sies": pick(c, "nombre inst"),
            "autonomia": pick(c, "autonom"),
            "acreditacion": pick(c, "acreditación", "acreditacion"),
            "vigencia": pick(c, "vigencia"),
            "anos_acreditacion": pick(c, "años acred", "anos acred"),
        }
        t = pd.DataFrame({k: (d[v] if v else None) for k, v in m.items()})
        t["ano_corte"] = ano
        t["corte"] = corte
        out.append(t)
    s = pd.concat(out, ignore_index=True)
    s = s[pd.to_numeric(s["codigo_ies"], errors="coerce").notna()].copy()
    s["codigo_ies"] = s["codigo_ies"].astype(int)
    s["anos_acreditacion"] = pd.to_numeric(s["anos_acreditacion"], errors="coerce")
    a = s["acreditacion"].astype(str).str.lower()
    s["acreditacion_norm"] = (
        pd.Series("Otro", index=s.index)
        .mask(a.str.contains("no acreditada"), "No acreditada")
        .mask(a.str.contains("extendida"), "Acreditacion extendida")
        .mask(a.str.contains("bajo tutela"), "Bajo tutela")
        .mask(a.str.match(r"^acreditada"), "Acreditada"))
    s["nombre_norm"] = s["nombre_institucion_sies"].map(norm).str.replace("'", "", regex=False)
    # el listado de 2025-12 y 2026-09 conviven con el ano 2026: se conserva el corte mas reciente por ano
    s = s.sort_values(["codigo_ies", "ano_corte", "corte"]).drop_duplicates(["codigo_ies", "ano_corte"], keep="last")
    s.to_csv(OUT / "ext_sies_acreditacion_ies_ano.csv", index=False, encoding="utf-8")
    return s


# ---------------------------------------------------------------- Puentes
# Correcciones manuales documentadas (nombre base normalizado -> codigo IES); se completa tras revisar no coincidentes
# Correcciones manuales documentadas, clave = nombre normalizado/expandido de la base CNED -> codigo IES (SIES).
# Cada una fue verificada contra el catalogo SIES (misma institucion con distinta grafia o sigla).
_CFT_ESTATALES = {"ANTOFAGASTA": 908, "ARICA Y PARINACOTA": 902, "ATACAMA": 909, "AYSEN": 919,
                  "COQUIMBO": 910, "LA ARAUCANIA": 916, "LOS LAGOS": 918, "LOS RIOS": 917,
                  "MAGALLANES": 920, "TARAPACA": 906, "VALPARAISO": 911, "O HIGGINS": 913,
                  "DEL BIO BIO": 915, "DEL MAULE": 914, "METROPOLITANO": 912}
OVERRIDES_INST = {}
for _r, _c in _CFT_ESTATALES.items():
    _p = "DE " if not _r.startswith(("DEL ", "METROPOLITANO")) else ""
    OVERRIDES_INST["CENTRO DE FORMACION TECNICA ESTATAL " + _p + _r] = _c
    OVERRIDES_INST["CFTE " + _p + _r] = _c
OVERRIDES_INST.update({
    "ACADEMIA NAC EST POLITICOS Y ESTRATEGICOS ANEPE": 674,
    "CENTRO DE FORMACION TECNICA ESANE DEL NORTE": 305,
    "CENTRO DE FORMACION TECNICA DE EST SUP Y CAPACITACION PROFESIONAL LAPLACE": 427,
    "CENTRO DE FORMACION TECNICA DE LA INDUSTRIA GRAFICA O C F T INGRAF": 591,
    "CENTRO DE FORMACION TECNICA SAN AGUSTIN DE TALCA": 367,
    "CENTRO DE FORMACION TECNICA U VALPO": 550,
    "CENTRO DE FORMACION TECNICA INSALCO": 241,
    "INSTITUTO PROFESIONAL CHILENO BRITANICO": 108,
    "INSTITUTO PROFESIONAL GUILLERMO SUBERCASEAUX": 103,
    "INSTITUTO PROFESIONAL HELEN KELLER": 140,
    "ESC DE ESPECIALIDADES SGTO 1O ADOLFO MENADIER ROJAS": 671,
    "ESCUELA MILITAR DEL GENERAL BERNARDO OHIGGINS": 728,
    "ESCUELA TECNICA AERONAUTICA": 675,
    "ESCUELA DE AVIACION": 741,
})
# Coincidencias aproximadas (difflib >= 0.92) revisadas a mano y RECHAZADAS por ser instituciones distintas.
RECHAZADOS_APROX = {
    "CENTRO DE FORMACION TECNICA CEPONAL", "CENTRO DE FORMACION TECNICA CRECIC",
    "CENTRO DE FORMACION TECNICA ICCE", "CENTRO DE FORMACION TECNICA INSEC",
    "CENTRO DE FORMACION TECNICA LA ARAUCANA", "CENTRO DE FORMACION TECNICA LOS LEONES",
    "INSTITUTO PROFESIONAL IPEGE",
}



def puente_region(base):
    reg = base[["nombre_region", "region_codigo_subdere", "region_nombre_estandar"]].drop_duplicates()
    hoja = {c: h for c, h in REGIONES}
    reg["hoja_ine"] = reg["region_codigo_subdere"].map(hoja)
    reg = reg.sort_values("region_codigo_subdere")
    reg.to_csv(OUT / "puente_region.csv", index=False, encoding="utf-8")
    return reg


def puente_institucion(base, sies):
    # Catalogo de nombres SIES (todos los cortes): un codigo puede tener varios nombres historicos
    cat = sies[["codigo_ies", "nombre_institucion_sies", "nombre_norm"]].drop_duplicates()
    cat["clave2"] = cat["nombre_norm"].map(sin_conectores)
    exacto = cat.drop_duplicates("nombre_norm").set_index("nombre_norm")
    exacto2 = cat.drop_duplicates("clave2").set_index("clave2")

    inst = base["nombre_institucion"].dropna().drop_duplicates().to_frame()
    inst["nombre_expandido"] = inst["nombre_institucion"].map(expandir_institucion)
    filas = []
    for _, r in inst.iterrows():
        e = r["nombre_expandido"]
        cod, nom, met, sc = None, None, "sin_coincidencia", 0.0
        ov = OVERRIDES_INST.get(e)
        if ov is not None:
            cod, met, sc = ov, "manual", 1.0
            nom = cat[cat.codigo_ies == ov]["nombre_institucion_sies"].iloc[-1]
        elif e in exacto.index:
            cod, nom, met, sc = int(exacto.loc[e, "codigo_ies"]), exacto.loc[e, "nombre_institucion_sies"], "exacto_normalizado", 1.0
        elif sin_conectores(e) in exacto2.index:
            k = sin_conectores(e)
            cod, nom, met, sc = int(exacto2.loc[k, "codigo_ies"]), exacto2.loc[k, "nombre_institucion_sies"], "exacto_sin_conectores", 1.0
        else:
            cand = [] if e in RECHAZADOS_APROX else difflib.get_close_matches(
                e, cat["nombre_norm"].tolist(), n=1, cutoff=0.92)
            if cand:
                fila = cat[cat.nombre_norm == cand[0]].iloc[0]
                cod, nom, met = int(fila.codigo_ies), fila.nombre_institucion_sies, "aproximado_>=0.92"
                sc = difflib.SequenceMatcher(None, e, cand[0]).ratio()
        filas.append(dict(nombre_institucion_cned=r["nombre_institucion"], nombre_normalizado=e,
                          codigo_ies=cod, nombre_institucion_sies=nom, metodo_cruce=met, similitud=round(sc, 3)))
    p = pd.DataFrame(filas).sort_values("nombre_institucion_cned")
    p.to_csv(OUT / "puente_institucion.csv", index=False, encoding="utf-8")
    return p


# ---------------------------------------------------------------- Cruces y metricas
def main():
    base = pd.read_csv(BASE, low_memory=False, encoding="utf-8",
                       usecols=["ano", "nombre_institucion", "nombre_region", "region_codigo_subdere",
                                "region_nombre_estandar", "matricula_primer_ano_total", "vacantes"])
    ine, sies = parse_ine(), parse_sies()
    preg = puente_region(base)
    pins = puente_institucion(base, sies)

    # --- cruce regional
    j = base.merge(ine[["region_codigo_subdere", "ano", "poblacion_total"]],
                   on=["region_codigo_subdere", "ano"], how="left")
    reg_ok = j["poblacion_total"].notna()

    # --- cruce institucional (nivel registro y por ano)
    b2 = base.merge(pins[["nombre_institucion_cned", "codigo_ies"]],
                    left_on="nombre_institucion", right_on="nombre_institucion_cned", how="left")
    b2["tiene_codigo"] = b2["codigo_ies"].notna()
    b3 = b2.merge(sies[["codigo_ies", "ano_corte", "acreditacion", "anos_acreditacion"]],
                  left_on=["codigo_ies", "ano"], right_on=["codigo_ies", "ano_corte"], how="left")
    b3["con_acreditacion_historica"] = b3["ano_corte"].notna()

    m1 = b2["matricula_primer_ano_total"].fillna(0)
    res = {
        "registros_base": int(len(base)),
        "region": {
            "regiones_distintas_base": int(preg.shape[0]),
            "tasa_registros_cruzados_pct": round(100 * reg_ok.mean(), 3),
            "no_cruzados": int((~reg_ok).sum()),
        },
        "institucion": {
            "instituciones_distintas_base": int(pins.shape[0]),
            "instituciones_con_codigo": int(pins["codigo_ies"].notna().sum()),
            "tasa_instituciones_con_codigo_pct": round(100 * pins["codigo_ies"].notna().mean(), 2),
            "tasa_registros_con_codigo_pct": round(100 * b2["tiene_codigo"].mean(), 2),
            "tasa_matricula_1er_ano_con_codigo_pct": round(100 * m1[b2["tiene_codigo"]].sum() / m1.sum(), 2),
            "metodos": pins["metodo_cruce"].value_counts().to_dict(),
        },
        "institucion_por_ano_acreditacion_disponible_pct": (
            b3.groupby("ano")["con_acreditacion_historica"].mean().mul(100).round(2).to_dict()),
    }
    (OUT / "cruce_resumen.json").write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    pins[pins["codigo_ies"].isna()].to_csv(OUT / "cruce_no_coincidentes_institucion.csv", index=False, encoding="utf-8")
    print(json.dumps(res, indent=2, ensure_ascii=False))
    print("\nSIN CODIGO:")
    print(pins[pins["codigo_ies"].isna()][["nombre_institucion_cned", "nombre_normalizado"]].to_string())


if __name__ == "__main__":
    main()
