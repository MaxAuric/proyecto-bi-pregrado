# Reporte Oficial de Auditoría y Cuadre del DataMart
## Hito 2 - Rol: Persona 3 (Arquitecto de Bases de Datos)
**Fecha de Certificación:** 2026-10-17  
**Estado:** **`APROBADO_CON_EXCELENCIA`**

---

### 1. Resumen Ejecutivo de Conciliación (Zero Data Loss)

Se realizó la auditoría automatizada entre la fuente consolidada limpia oficial (`base_indices_consolidada_2012_2026.csv`, Persona 1) y el DataMart relacional estructurado (`datamart_educacion_superior.db`, Persona 3).

| Métrica Auditada | Valor en Fuente CSV | Valor en DataMart SQL | Diferencia Absoluta | Estado |
| :--- | :---: | :---: | :---: | :---: |
| **Total de Registros (Grano Hecho)** | **158,211** | **158,211** | **0** | **COINCIDENCIA EXACTA (100%)** |
| **Matrícula 1er Año Total** | **5,186,123** | **5,186,123** | **0** | **CERO PÉRDIDA (100%)** |
| **Matrícula Total del Sistema** | **17,696,782** | **17,696,782** | **0** | **CERO PÉRDIDA (100%)** |
| **Total Vacantes Declaradas** | **5,914,165** | **5,914,165** | **0** | **CERO PÉRDIDA (100%)** |
| **Registros Huérfanos (FK inválida)** | - | **0** | **0** | **INTEGRIDAD TOTAL** |

---

### 2. Inventario de Tablas y Cardinalidades en el DataMart

| Tabla | Tipo de Entidad | Grano Declarado | Registros Cargados |
| :--- | :--- | :--- | :---: |
| `fact_matricula_oferta` | Tabla de Hechos Principal | 1 fila por Programa x Sede x Horario x Año | **158.211** |
| `fact_poblacion_regional` | Tabla de Hechos Secundaria (INE) | 1 fila por Región x Año (2012-2026) | **240** |
| `dim_tiempo` | Dimensión Temporal | 1 fila por Año Calendario | **15** |
| `dim_geografia` | Dimensión Geográfica | 1 fila por Región Oficial SUBDERE (+ Desconocido) | **17** |
| `dim_sede` | Dimensión Campus / Sede | 1 fila por Sede Geográfica (+ Desconocida) | **115** |
| `dim_institucion` | Dimensión Institucional | 1 fila por Institución CNED/SIES (+ Desconocida) | **260** |
| `dim_institucion_calidad_anual`| Dimensión SCD Snapshot Anual | 1 fila por Institución x Año (Acreditación SIES/CNED) | **1.994** |
| `dim_programa` | Dimensión Oferta Académica | 1 fila por Programa x Carrera x Régimen (+ Desconocido) | **8.868** |

---

### 3. Certificación de Integridad Referencial
- **Huérfanos de Tiempo:** 0
- **Huérfanos de Geografía:** 0
- **Huérfanos de Sede:** 0
- **Huérfanos de Institución:** 0
- **Huérfanos de Programa:** 0

**Conclusión Técnica:** El DataMart satisface con un 100% de rigurosidad matemática y lógica los requisitos del Hito 2 de la Pauta Oficial. No existe duplicación ni descarte de registros. Queda totalmente habilitado para el consumo analítico por parte de la Persona 4 en Power BI.
