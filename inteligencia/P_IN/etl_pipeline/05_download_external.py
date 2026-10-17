"""
05_download_external.py  -  Persona 2 (Hito 1)
Descarga las fuentes externas oficiales y registra URL, fecha y hash SHA-256 en un manifiesto.

Fuente 1 (nivel REGION)      : INE - Estimaciones y proyecciones de poblacion 2002-2035 (base Censo 2017)
Fuente 2 (nivel INSTITUCION) : SIES/MINEDUC - Listado de IES vigentes (codigo, autonomia, acreditacion)
"""
import hashlib, json, sys, datetime as dt
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data_external"
RAW.mkdir(exist_ok=True)

PAG_INE = "https://www.ine.gob.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion"
PAG_SIES = "https://www.mifuturo.cl/instituciones-de-educacion-superior-en-chile/"
SIES = "https://www.mifuturo.cl/wp-content/uploads/"

FUENTES = {
    "INE_proyecciones_2017_region_area.xlsx": {
        "fuente": "INE - Estimaciones y proyecciones de poblacion 2002-2035, base Censo 2017 (totales regionales)",
        "pagina": PAG_INE,
        "url": "https://www.ine.gob.cl/docs/default-source/proyecciones-de-poblacion/cuadros-estadisticos/base-2017/ine_estimaciones-y-proyecciones-2002-2035_base-2017_region_area_tabulados.xlsx?sfvrsn=e9bd6edf_6",
    },
}
# Listados anuales de IES vigentes (SIES): permiten reconstruir la historia de acreditacion/autonomia.
SIES_FILES = {
    "SIES_IES_vigentes_2018-12.xlsx": "2019/03/2_listado_instituciones_vigentes_31diciembre_2018-3.xlsx",
    "SIES_IES_vigentes_2019-12.xlsx": "2020/01/listado_instituciones_vigentes_31_diciembre_2019.xlsx",
    "SIES_IES_vigentes_2020-12.xlsx": "2020/12/listado_instituciones_vigentes_31_diciembre_2020.xlsx",
    "SIES_IES_vigentes_2021-12.xlsx": "2022/01/listado_instituciones_vigentes_31_diciembre_2021.xlsx",
    "SIES_IES_vigentes_2022-12.xlsx": "2023/01/Listado_IES_vigentes_31_diciembre_2022.xlsx",
    "SIES_IES_vigentes_2023-12.xlsx": "2024/01/Listado_IES_vigentes_al_31_de_diciembre_2023.xlsx",
    "SIES_IES_vigentes_2024-12.xlsx": "2025/01/Listado_IES_vigentes_31_diciembre_2024_SIES.xlsx",
    "SIES_IES_vigentes_2025-12.xlsx": "2026/01/Listado_IES_vigentes_31_diciembre_2025_SIES.xlsx",
    "SIES_IES_vigentes_2026-09.xlsx": "2026/10/Listado_IES_vigentes_30_septiembre_2026_SIES.xlsx",
}
for n, rel in SIES_FILES.items():
    FUENTES[n] = {"fuente": "SIES/MINEDUC - Listado de IES vigentes (" + n[-12:-5] + ")",
                  "pagina": PAG_SIES, "url": SIES + rel}


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def descargar(nombre, meta):
    dest = RAW / nombre
    r = requests.get(meta["url"], timeout=180, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    if r.content[:2] != b"PK":  # un .xlsx valido es un zip
        raise ValueError("el contenido descargado no es un xlsx valido")
    dest.write_bytes(r.content)
    return {**meta, "archivo": nombre, "bytes": dest.stat().st_size,
            "sha256": sha256(dest), "fecha_descarga": dt.date.today().isoformat()}


if __name__ == "__main__":
    mf = RAW / "manifiesto_descargas.json"
    previo = json.loads(mf.read_text(encoding="utf-8")) if mf.exists() else {}
    for n, m in FUENTES.items():
        try:
            previo[n] = descargar(n, m)
            print("OK ", n, previo[n]["bytes"])
        except Exception as e:
            print("ERR", n, e, file=sys.stderr)
    mf.write_text(json.dumps(previo, indent=2, ensure_ascii=False), encoding="utf-8")
