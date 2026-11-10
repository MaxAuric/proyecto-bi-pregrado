# Modulo de Persona 4: Joaquin Aguilera — Hito 2
## Proyecto practico de Inteligencia de Negocios

Este directorio contiene la solucion formal, reproducible y verificada para las tareas asignadas a la **Persona 4 (Joaquin Aguilera)** en el **Hito 2 (Modelo Dimensional y DataMart Relacional)**:

---

## Estructura del modulo `P4_DESARROLLADOR_BI/`

```text
P4_DESARROLLADOR_BI/
├── README.md                                          # Este documento de presentacion del modulo
├── docs/                                              # Documentacion formal e informes tecnicos
│   ├── informe_hito2_persona4_desarrollador_bi.md     # Informe formal de Persona 4 para Hito 2
│   ├── modelado_jerarquias_y_filtros_p4.md            # Especificacion exhaustiva de las 4 jerarquias analiticas
│   ├── protocolo_pruebas_conexion_datamart_p4.md      # Certificacion de conexion directa Power BI -> DataMart
│   └── certificacion_conexion_jerarquias_p4.json      # Metricas y benchmarks de latencia estructurados
├── powerbi_templates/                                 # Conectores y templates de Power Query M y DAX
│   └── conexion_powerquery_m.pq                       # Script M / Python para ingesta directa en Power BI
└── scripts/                                           # Scripts reproducibles de prueba y auditoria
    └── audit_and_test_connections_p4.py               # Suite automatizada de pruebas de conexion y latencia
```

---

##  Como reproducir las pruebas de la Persona 4

Para ejecutar la suite de pruebas de conexion y validar el rendimiento de las jerarquias en el DataMart:

```bash
python "Avance Hito 2/P4_DESARROLLADOR_BI/scripts/audit_and_test_connections_p4.py"
```

---

##  Resumen de resultados certificados

1. **Conexion exitosa al DataMart:** Probada y certificada contra SQLite (`datamart_indices_2012_2026.db`, 158.211 filas). Cumple con el mandato de la pauta: *"Conectado al DataMart, no a Excel"*.
2. **4 Jerarquias implementadas:**
   * **Geografica:** Macro-Zona $\rightarrow$ Region $\rightarrow$ Sede (permite filtrar por RM, Quinta Region y resto del pais).
   * **Institucional:** Tipo de IES $\rightarrow$ Institucion $\rightarrow$ Año SCD Tipo 2.
   * **Academica:** Area de conocimiento $\rightarrow$ Carrera generica $\rightarrow$ Programa especifico.
   * **Temporal:** Quinquenio $\rightarrow$ Periodo de admision (PSU/PDT/PAES) $\rightarrow$ Año cronologico.
3. **Latencia optima:** Resolucion relacional promedio de **205 ms**, garantizando interactividad instantanea en Power BI Desktop.

