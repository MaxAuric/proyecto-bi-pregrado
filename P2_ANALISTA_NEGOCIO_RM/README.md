# P2 — Analista de Negocio RM | Entrega Final Business Intelligence 2026

## Rol
**Persona 2: Analista de Negocio RM**
Responsable de la propuesta de valor, el Canvas BI de 10 bloques (100% foco Región Metropolitana), la traducción de cada KPI a decisiones de negocio concretas y la Sección 1 del Informe Ejecutivo Final.

---

## Archivos Entregados

| Archivo | Tipo | Descripción |
|:---|:---:|:---|
| `docs/informe_final_persona2_negocio_rm.tex` | LaTeX | **Informe principal** (~600 líneas). Sección 1 del Informe Ejecutivo Final. Contiene: Resumen ejecutivo, Canvas BI de 10 bloques, 3 preguntas de negocio con KPIs y fórmulas, mapa KPI→decisión, reglas de negocio críticas y tabla de coordinación por persona. |
| `docs/canvas_bi_rm_10_bloques.md` | Markdown | Canvas BI de 10 bloques en formato Markdown (complemento para PPT y referencia rápida del equipo). |
| `docs/analisis_kpis_negocio_rm.md` | Markdown | Mapa completo de KPIs: fórmula algebraica, umbral de decisión y acción concreta para cada tasa. Incluye tabla por área (RM 2026) y serie histórica de absorción/cobertura. |
| `docs/cifras_rm_2026.json` | JSON | Resumen de cifras oficiales auditadas, generado automáticamente por el script Python. |
| `scripts/analisis_negocio_rm.py` | Python | Script de reproducibilidad que extrae todas las cifras del DataMart y las valida contra el informe. |

---

## Cifras Clave RM 2026 (Auditadas)

| Indicador | Valor |
|:---|:---:|
| Registros históricos RM (2012–2026) | **58.926** |
| Vacantes declaradas RM 2026 | **253.018** |
| Matrícula 1er año RM 2026 | **208.311** |
| Tasa de ocupación de vacantes RM | **82,3%** |
| Secciones extra por sobrecupo 2026 | **674** |
| Programas con sobredemanda crítica 2026 | **1.232** |
| Tasa de absorción juvenil RM 2026 (INE) | **25,35%** |
| Tasa de cobertura bruta RM 2026 | **86,26%** |
| Puntaje PAES promedio ponderado RM 2026 | **703,6** |
| Retención aparente RM 2026 | **70,61%** |

---

## Cómo Compilar el Informe PDF

El archivo `.tex` requiere **LaTeX** (paquetes: `booktabs`, `tcolorbox`, `tabularx`, `longtable`, `amsmath`, `babel` español).

**Opción A — Overleaf (recomendada):**
1. Subir `docs/informe_final_persona2_negocio_rm.tex` a [Overleaf](https://www.overleaf.com)
2. Compilar con `pdflatex` → descarga el PDF

**Opción B — Local (si LaTeX está instalado):**
```powershell
cd "c:\Users\...\entregacasiulltimainteligencia\proyecto-bi-pregrado-main"
pdflatex -output-directory="Final\P2_ANALISTA_NEGOCIO_RM\docs" "Final\P2_ANALISTA_NEGOCIO_RM\docs\informe_final_persona2_negocio_rm.tex"
```

**Opción C — Entregar a Persona 5:**
Persona 5 (Gestor/Documentación) es quien integra todos los informes en el PDF final. Entregar el `.tex` sin compilar.

---

## Cómo Ejecutar el Script de Reproducibilidad

```powershell
cd "c:\Users\IIfie\OneDrive\Escritorio\entregacasiulltimainteligencia\proyecto-bi-pregrado-main"
python "Final\P2_ANALISTA_NEGOCIO_RM\scripts\analisis_negocio_rm.py"
```

El script lee directamente desde `Final/00_DATAMART_LISTO_PARA_POWERBI/tablas_estrella_csv/` y exporta un resumen JSON en `docs/cifras_rm_2026.json`.

---

## Dependencia con Otros Roles

| Persona | Qué recibe de P2 | Qué usa de P2 |
|:---|:---|:---|
| **P1 (Ing. Datos)** | — (P1 ya entregó el DataMart completo) | Columnas exactas del DataMart documentadas en este informe |
| **P3 (Arquitecto)** | Bloque 7 del Canvas BI (dimensiones y medidas) | Tipos de aditividad de cada medida (Sección 4 del .tex) |
| **P4 (Dev. BI)** | Medidas DAX en `lo nuevo/02_CATALOGO_NUEVAS_TASAS_KPIS_Y_DAX_RM.md` | Umbrales de colores para tarjetas KPI (Sección 4 del .tex) |
| **P5 (Gestor/Doc)** | Este informe completo (`.tex`) es la **Sección 1 del Informe Final** | Cifras y tabla P1 para las conclusiones del informe ejecutivo |

---

## Restricciones Críticas (para Defensa Oral)

1. **Puntajes PAES ≠ aditivos** → DAX: `DIVIDE(SUMX(..., puntaje × mat), SUMX(..., mat))`. Nunca `SUM(puntaje)`.
2. **Tasas ≠ promediables** → Recalcular siempre desde totales con `DIVIDE()`.
3. **Acreditación 2012–2017**: NULL estructural → no imputar; filtrar a 2018–2026.
4. **Vacantes nulas**: filtrar con `flag_vacantes_declaradas = 1` antes de calcular ocupación.
5. **Quiebre PSU→PAES (2022)**: usar siempre `puntaje_promedio_equiv_paes` para series continuas.
6. **Matrícula por sede RM**, no por domicilio del alumno.

---

*Entrega Final — Business Intelligence | 18 de Noviembre de 2026*
