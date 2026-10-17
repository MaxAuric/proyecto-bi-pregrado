# Entregables Hito 1 - Persona 1: Ingeniero de Datos (ETL)

Este directorio contiene la solución integral para el rol de **Persona 1 (Ingeniero de Datos / ETL)** en el **Hito 1** del Proyecto Final de Business Intelligence.

---

## 📁 Estructura del Directorio `P_IN/`

```text
P_IN/
├── data_raw/                          # Fuentes oficiales descargadas inmutables
│   ├── Base-INDICES-Matricula-2005-2026.xlsx  # Repositorio oficial CNED (agosto 2026, 60.4 MB)
│   ├── 01_Esquema_Registro_Base_Pregrado.pdf # Esquema de registro oficial CNED
│   ├── OfertaPregrado2026.xlsx                # Oferta académica oficial CNED 2026
│   └── 01_Esquema_Registro_Oferta2026_INDICES.pdf
│
├── etl_pipeline/                      # Pipeline reproducible en Python
│   ├── 01_download_data.py            # Descarga automatizada y validada desde el portal CNED
│   ├── 02_audit_and_mapping.py        # Perfilamiento, auditoría de nulos y quiebres psicométricos
│   ├── 03_clean_and_transform.py      # Transformación, homologación PSU/PDT/PAES y exportación
│   ├── 04_generate_dictionary.py      # Generador de diccionarios (JSON, Markdown, LaTeX)
│   └── run_etl.py                     # Script maestro de ejecución completa (One-Click)
│
├── data_processed/                    # Bases consolidadas limpias y gobernadas (2012-2026)
│   ├── base_indices_consolidada_2012_2026.csv      # Formato interoperable CSV (158.211 filas)
│   ├── base_indices_consolidada_2012_2026.parquet  # Formato columnar optimizado de alto rendimiento
│   └── auditoria_resumen.json                      # Reporte numérico de auditoría y distribuciones
│
└── docs/                              # Documentación técnica, informe y diccionarios
    ├── informe_hito1_persona1.pdf     # Informe Técnico Ejecutivo compilado en LaTeX (10 páginas)
    ├── informe_hito1_persona1.tex     # Código fuente LaTeX del informe
    ├── diccionario_datos_exhaustivo.md # Diccionario de datos en Markdown
    ├── diccionario_datos_exhaustivo.json # Diccionario estructurado en JSON
    └── tabla_diccionario_datos.tex    # Tabla formal de mapeo en LaTeX para anexar
```

---

## 🚀 Cómo Ejecutar el Pipeline ETL

Para reproducir todo el proceso de punta a punta:

```bash
python P_IN/etl_pipeline/run_etl.py
```

---

## 📊 Resumen de Resultados Técnicos

1. **Consolidación Oficial:**
   - Base entregada (2012–2022): 114.265 registros.
   - CNED Oficial Pregrado (2023–2026): 43.946 registros.
   - **Total Consolidado:** **158.211 registros** (59 atributos).

2. **Homologación Psicométrica de Puntajes:**
   - PSU (2012–2020: Escala [150, 850], $\mu=557.3$)
   - PDT (2021–2022: Escala [150, 850], $\mu=549.6$)
   - PAES (2023–2026: Escala [100, 1000], $\mu=645.4$)
   - *Solución:* Preservación de escala nativa + Normalización Min-Max $[0, 100]$ + Proyección PAES $[100, 1000]$ + $Z$-Score Anual.

3. **Resolución de Nulos:**
   - **Puntajes (80.5% nulos):** Demostrado por cobertura (CFT 0.2%, IP 0.1%, Univ 47.4%). Preservados como `NULL` + flag `flag_exige_prueba_admision`.
   - **Vacantes (25.4% nulos):** Preservados como `NULL` para no simular cierre de carreras + flag `flag_vacantes_declaradas`.

4. **Normalización Geográfica e Institucional:**
   - Mapeo oficial SUBDERE (16 regiones).
   - Trazabilidad y flag `flag_quiebre_nuble` para la Región de Ñuble (Ley 21.033, 2018).
