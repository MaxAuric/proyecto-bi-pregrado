# Certificación Final DataMart Estrella RM + Tasas, KPIs y Buenas Prácticas DW
**Responsable:** Persona 1 (Ingeniero de Datos)  
**Alcance Oficial:** Región Metropolitana de Santiago (`region_codigo_subdere == '13'`)

## 1. Resumen de Tablas en `datamart_estrella_rm_final.db` y `DataMart_Estrella_RM_PowerBI.xlsx`
- **`fact_matricula_admision`**: `58,926` ofertas académicas de la Región Metropolitana (`100%` numérica, cero columnas `VARCHAR` según `Clase 4 - DW.pdf` Pág. 62; auditada contra las `158,211` filas nacionales).
- **`dim_tiempo_ine_rm`**: `15` años (`2012–2026`) integrados con proyecciones **INE RM** y tasas de absorción juvenil y cobertura bruta.
- **`dim_institucion_sies`**: `1,298` registros históricos institucionales SCD Tipo 2 en la RM (`69` IES activas en 2026: `35` Universidades, `19` IP, `11` CFT, `4` FF.AA.), sin abreviaturas ni prefijos `(a)/(b)`, integrados con **SIES Acreditación** y Market Share RM.
- **`dim_sede_geografia`**: `22` sedes en la RM con jerarquía geográfica completa y tasas históricas de ocupación y saturación.
- **`dim_carrera_programa`**: `5,184` programas en la RM con clasificación de presión de capacidad y tasa de presión de laboratorio (base 35 alumnos).
- **`agg_resumen_anual_institucion_rm`**: `1,298` filas agregadas anuales por institución en la RM (cumple `Clase 4 - DW.pdf` Pág. 63: tablas agregadas para rendimiento OLAP).
- **`puente_institucion_sies`**: `259` instituciones mapeadas con su tasa de coincidencia documentada (cumple `Pauta_Trabajo_Final_BI.pdf` Pág. 3).

## 2. Auditoría de Cruce de Fuentes Externas (Requisito Pauta Pág. 3)
1. **Fuente Externa 1 (Demografía INE RM):** `100,0%` de coincidencia exacta en los 15 años (`2012–2026`).
2. **Fuente Externa 2 (Acreditación SIES/CNA en RM):** `98.25%` de las ofertas históricas de la RM (`57,892` de `58,926` filas) cruzan directamente con un código oficial SIES vigente. El `1.75%` restante corresponde a instituciones cerradas antes de 2018 o escuelas de las FF.AA., las cuales se preservan sin pérdida de filas (`LEFT JOIN`) imputando su tramo según el atributo histórico `acreditacion_cned`.

## 3. Indicadores de Control y Capacidad en la RM (2012–2026)
- **Matrícula 1er Año Acumulada RM:** `2,488,186` estudiantes.
- **Matrícula Total Acumulada RM:** `8,536,191` estudiantes.
- **Vacantes Declaradas RM:** `2,907,448` cupos.
- **Ofertas con Sobredemanda Crítica (>100% cupos):** `13,995` programas.
- **Paralelos/Secciones Extra de Laboratorio (base 35 alumnos) exigidos por sobrecupo:** `7,529` secciones adicionales.
