# Entregables Hito 2 — Modelo Dimensional y DataMart Relacional
## Proyecto Práctico Final de Business Intelligence (2012–2026)

Este directorio contiene la solución formal, reproducible y verificada para el **Hito 2** del proyecto, reorientado estratégicamente hacia la **Región Metropolitana de Santiago (RM)** según la retroalimentación del profesor.

---

## 📁 Estructura Modular de `Avance Hito 2/`

```text
Avance Hito 2/
├── 00_DOCUMENTOS_PARA_PRESENTAR_Y_DEFENDER/
│   ├── Informe_Hito2_Persona1_DataMart.pdf     # Informe técnico formal de Persona 1
│   ├── Informe_Hito2_Persona1_DataMart.tex     # Código fuente LaTeX del informe
│   └── RESUMEN_FEEDBACK_Y_REORIENTACION_HITO2.md # Síntesis ejecutiva de la reorientación a RM
│
├── 01_PROPUESTA_VALOR_Y_CANVAS_BI_RM/         # Enfoque estratégico acotado a la Región Metropolitana
│   └── (Insumos de Persona 2: Canvas BI RM y 3 Preguntas de Negocio)
│
├── 02_MODELO_DIMENSIONAL_Y_ARQUITECTURA/      # Arquitectura conceptual y lógica (Persona 3 y 5)
│   └── (Diagrama Estrella, Grano declarado, SCD Tipo 2 y Aditividad de Medidas)
│
├── 03_DATAMART_SCRIPTS_DDL_Y_CARGA/           # Entregables centrales de Persona 1 (Ingeniero de Datos)
│   ├── schema_datamart.sql                     # Script DDL formal (CREATE TABLE, PK, FK, Índices)
│   ├── 01_build_and_load_datamart.py           # Pipeline de carga masiva automatizada en Python
│   ├── datamart_indices_2012_2026.db           # Base de datos relacional SQLite (DataMart físico)
│   └── vistas_analiticas_rm.sql                # Vistas optimizadas para la Región Metropolitana
│
├── 04_CERTIFICACION_CUADRE_Y_AUDITORIA/       # Certificación de cuadre contra la fuente (4 Pts Pauta)
│   ├── 02_verify_cuadre_datamart.py            # Script automatizado de auditoría matemática
│   ├── reporte_cuadre_datamart.md              # Tabla de Control Totals y certificación formal
│   └── reporte_cuadre_datamart.json            # Reporte estructurado para evaluación automatizada
│
└── 05_CONEXION_POWERBI_Y_PRUEBAS/             # Conexión directa DataMart -> Power BI (Persona 4)
    └── guia_conexion_powerbi_datamart.md       # Guía paso a paso para cumplir "Conectado al DataMart, no a Excel"
```

---

## 🚀 Cómo Reproducir el DataMart y la Certificación de Cuadre

Todo el pipeline es 100% reproducible y automatizado:

1. **Construir y Poblar el DataMart Relacional:**
   ```bash
   python "Avance Hito 2/03_DATAMART_SCRIPTS_DDL_Y_CARGA/01_build_and_load_datamart.py"
   ```
2. **Auditar y Certificar el Cuadre Estricto:**
   ```bash
   python "Avance Hito 2/04_CERTIFICACION_CUADRE_Y_AUDITORIA/02_verify_cuadre_datamart.py"
   ```

---

## 📊 Resumen de Resultados Técnicos (Hito 2)

1. **Cuadre Perfecto contra la Fuente (0 Pérdidas, 0 Duplicados):**
   * Registros en fuente original consolidada: **158.211 filas**.
   * Registros en `fact_matricula_admision`: **158.211 filas**.
   * Diferencia neta: **0 registros**.
   * Integridad referencial: **100%** (0 registros huérfanos con claves foráneas nulas).

2. **Universo de la Región Metropolitana:**
   * La RM concentra **82.348 registros** de pregrado (más del 52% de la base nacional).
   * Cuenta con vistas dedicadas (`vw_rm_sobredemanda_y_capacidad`) para responder directamente a las 3 preguntas de negocio en Power BI.

3. **Arquitectura Dimensional Implementada:**
   * **Tabla de Hechos:** `fact_matricula_admision` (Grano: una fila por programa, sede, horario y año).
   * **Dimensiones:** `dim_tiempo`, `dim_sede_geografia`, `dim_institucion` (con historial SCD Tipo 2 por año), `dim_carrera_programa`.

