# Entregables Hito 2 - Persona 3: Arquitecto de Bases de Datos
## Tarea Asignada: Diseno Conceptual y Logico del Modelo Dimensional y Construccion del DataMart

Este directorio contiene la solucion integral del rol de **Persona 3** para el **Hito 2** del Proyecto de Business Intelligence (Entrega: 4 de Noviembre de 2026).

---

## 1. Estructura del Directorio `P3_Hito2/`

```text
P3_Hito2/
├── README.md                      # Este archivo de descripcion
├── data/
│   ├── datamart_educacion_superior.db  # DataMart compilado en SQLite (23 MB, 158.211 registros)
│   └── tablas_csv_powerbi/             # 8 tablas relacionales exportadas en CSV para Power BI
├── diagrams/
│   └── modelo_dimensional.md          # Diagrama ER dimensional en Mermaid y jerarquias
├── docs/
│   ├── informe_hito2_persona3.md      # Informe tecnico formal (grano, aditividad, SCD y cuadre)
│   ├── reporte_cuadre_registros.md    # Certificado de cuadre exacto contra la fuente
│   ├── reporte_cuadre.json            # Metadatos de auditoria en JSON
│   └── guia_conexion_powerbi_persona4.md # Instructivo de conexion y formulas DAX para Persona 4
├── scripts/
│   ├── load_datamart.py               # Pipeline Python de carga automatizada y surrogate keys
│   └── verify_cuadre.py               # Script de auditoria matematica fuente vs DataMart
└── sql/
    ├── 01_ddl_datamart.sql            # Script DDL formal (tablas, PK, FK, indices)
    ├── 02_views_powerbi.sql           # Vistas semanticas para las preguntas P1, P2 y P3
    └── 03_audit_and_reconciliation.sql # Consultas SQL de auditoria de integridad
```

---

## 2. Como Reproducir la Carga y Auditoria

1. **Cargar el DataMart desde cero:**
   ```bash
   python P3_Hito2/scripts/load_datamart.py
   ```
2. **Ejecutar la verificacion de cuadre (Zero Data Loss):**
   ```bash
   python P3_Hito2/scripts/verify_cuadre.py
   ```

---

## 3. Resumen de Cuadre Certificado

| Metrica Auditada | Fuente Original (P1) | DataMart (P3) | Diferencia | Estado |
| :--- | :---: | :---: | :---: | :---: |
| Total de Registros (Hechos) | 158.211 | 158.211 | 0 | Coincidencia Exacta |
| Matricula 1er Ano Total | 5.186.123 | 5.186.123 | 0 | Cero Perdida |
| Matricula Total Sistema | 17.696.782 | 17.696.782 | 0 | Cero Perdida |
| Total Vacantes Declaradas | 5.914.165 | 5.914.165 | 0 | Cero Perdida |
| Registros Huerfanos | -- | 0 | 0 | Integridad Absoluta |
