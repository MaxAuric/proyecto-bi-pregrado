# Entregables Hito 1 - Persona 2: Analista de Negocios y Datos Externos

Propuesta de Valor, Canvas BI y dos fuentes externas con llave de cruce hacia la base
consolidada de la Persona 1 (`P_IN/data_processed/base_indices_consolidada_2012_2026.csv`).

```text
P2_Hito1/
├── scripts/
│   ├── 05_download_external.py        # Descarga INE y SIES; manifiesto con URL, fecha y SHA-256
│   ├── 06_build_external_bridges.py   # Tablas externas, puentes region/institucion y tasas de cruce
│   └── 07_preview_kpis.py             # Cifras preliminares de las 3 preguntas de negocio
├── data_external/                     # Archivos oficiales descargados (inmutables)
├── data_processed/                    # Tablas externas, puentes, resumen de cruce y KPIs
└── docs/
    ├── informe_hito1_persona2.tex     # Propuesta de Valor + Canvas BI + fuentes (LaTeX)
    └── diccionario_fuentes_externas.md # Insumo para el diccionario de la Persona 5
```

## Ejecucion

```bash
python P2_Hito1/scripts/05_download_external.py
python P2_Hito1/scripts/06_build_external_bridges.py
python P2_Hito1/scripts/07_preview_kpis.py
# Informe (requiere LaTeX, dos pasadas por el indice):
pdflatex -output-directory=P2_Hito1/docs P2_Hito1/docs/informe_hito1_persona2.tex
```

## Resultados

| Fuente | Nivel de cruce | Coincidencia |
|---|---|---|
| INE (poblacion regional) | Region (codigo SUBDERE) | 100% de registros |
| SIES (IES vigentes, acreditacion) | Institucion (codigo IES) | 98,39% de registros, 99,00% de matricula 1er ano |

Pendiente: verificar a mano 4 nombres activos sin codigo (`ICCE`, `IPEGE`).
Requiere Python con `pandas`, `openpyxl` y `requests`.
