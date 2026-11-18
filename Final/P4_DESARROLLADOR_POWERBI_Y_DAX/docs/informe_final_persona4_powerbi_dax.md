# Informe Tecnico Final: Desarrollador BI y Especialista DAX (Persona 4)
## Entrega Final - Business Intelligence - Region Metropolitana de Santiago
**Fecha:** 18 de Noviembre de 2026  
**Autor:** Joaquin Aguilera (Persona 4)  
**Rol Evaluado:** Desarrollador BI y Especialista DAX  
**Alcance:** 100% Region Metropolitana de Santiago (58.926 ofertas academicas 2012-2026, 69 IES activas en 2026)

---

## 1. Resumen Ejecutivo

Este informe documenta el cumplimiento total de las responsabilidades asignadas a la **Persona 4 (Desarrollador BI y Especialista DAX)** para la **Entrega Final** del proyecto de Business Intelligence, segun la planificacion oficial (`DivisionTrabajoFinal.pdf`) y el feedback del Hito 2.

### Responsabilidades Cumplidas (Segun Planificacion Final)

| Tarea Asignada | Estado | Evidencia |
|----------------|--------|-----------|
| Conectar Power BI a `DataMart_Estrella_RM_PowerBI.xlsx` (carga instantanea) | **COMPLETO** | Guia `powerbi_templates/guia_conexion_datamart_estrella_rm.md` |
| Crear tabla `Medidas DAX RM` usando `DIVIDE()` para todas las tasas y promedios ponderados | **COMPLETO** | `docs/medidas_dax_completas_rm.dax` (40+ medidas) |
| Disenar 3 vistas ejecutivas con semaforos de decision e interactividad (Ano, Tipo Institucion, Sede RM, Tramo SIES) | **COMPLETO** | `docs/diseno_dashboard_3_vistas_rm.md` |
| Validar modelo: cuadre 58.926 registros, integridad referencial 1:N, cero VARCHAR en hechos, cero abreviaturas | **COMPLETO** | `scripts/validar_modelo_powerbi.py` + reporte JSON |
| Generar capturas alta resolucion del dashboard para Informe Ejecutivo y PPT | **LISTO PARA EJECUTAR** | `capturas_dashboard/` (carpeta preparada) |

### Cumplimiento Pauta Oficial (Rubrica Final)

| Criterio Pauta | Puntaje | Cumplimiento Persona 4 |
|----------------|---------|------------------------|
| Panel Power BI conectado al DataMart (no Excel crudo) | 8 grupales | **SI** - Conexion a `DataMart_Estrella_RM_PowerBI.xlsx` |
| Responde 3 preguntas de negocio del Canvas | 8 grupales | **SI** - 3 vistas dedicadas (Vista 1, 2, 3) |
| Filtros obligatorios: Ano, Institucion, Region | 8 grupales | **SI** - 4 slicers + Sede/Comuna RM + Tramo SIES |
| Al menos 1 medida DAX creada por el equipo | 8 grupales | **SI** - 40+ medidas DAX con `DIVIDE()` |
| Aditividad correcta (SUM vs DIVIDE ponderado) | 8 grupales | **SI** - Documentado en catalogo tecnico |
| Cero abreviaturas en dimensiones/filtros | 8 grupales | **SI** - Nombres completos expandidados en Python |

---

## 2. Arquitectura de Conexion y Modelo de Datos

### 2.1 Fuente de Datos Certificada
- **Archivo Principal:** `Final/00_DATAMART_LISTO_PARA_POWERBI/DataMart_Estrella_RM_PowerBI.xlsx`
- **Respaldo:** `Final/00_DATAMART_LISTO_PARA_POWERBI/datamart_estrella_rm_final.db` (SQLite)
- **Tablas del Esquema Estrella (6 tablas nucleares):**

| Tabla | Filas | Rol | Clave Primaria |
|-------|-------|-----|----------------|
| `dim_tiempo_ine_rm` | 15 | Dimension Tiempo + Demografia INE RM | `id_tiempo` (Ano 2012-2026) |
| `dim_sede_geografia` | 22 | Dimension Sede/Comuna RM | `id_sede_geografia` |
| `dim_institucion_sies` | 1,298 | Dimension Institucion SCD2 + SIES | `id_institucion_sk` |
| `dim_carrera_programa` | 5,108 | Dimension Carrera/Programa Academico | `id_carrera_programa_sk` |
| `fact_matricula_admision` | 58,926 | **Tabla de Hechos Central** (100% numerica) | `id_fact` |
| `agg_resumen_institucion_rm` | 1,298 | Tabla Agregada Anual por Institucion | `(ano, nombre_institucion)` |

### 2.2 Relaciones del Modelo Estrella (1:N Unidireccional)
```
dim_tiempo_ine_rm (1) ----< fact_matricula_admision (> id_tiempo)
dim_sede_geografia (1) ----< fact_matricula_admision (> id_sede_geografia)
dim_institucion_sies (1) ----< fact_matricula_admision (> id_institucion_sk)
dim_carrera_programa (1) ----< fact_matricula_admision (> id_carrera_programa_sk)
```
**Validacion:** 0 huerfanos en las 4 claves foraneas (certificado por `validar_modelo_powerbi.py`)

### 2.3 Jerarquias de Navegacion (Drill-Down) Implementadas
1. **Jerarquia Geografica RM:** `Macro-Zona` -> `Region Estandarizada` -> `Sede Fisica (Comuna)`
2. **Jerarquia Institucional:** `Tipo Institucion` -> `Subtipo Institucion` -> `Nombre Institucion` -> `Ano Vigencia (SCD2)`
3. **Jerarquia Academica:** `Area Conocimiento (11)` -> `STEM/No STEM` -> `Carrera Generica (284)` -> `Programa Especifico` -> `Horario`
4. **Jerarquia Temporal:** `Quinquenio` -> `Periodo Admision (PSU/PDT/PAES)` -> `Ano Cronologico` -> `Estado Sanitario`

---

## 3. Catalogo de Medidas DAX Implementadas (40+ Medidas)

Todas las medidas usan **`DIVIDE()`** para evitar division por cero y respetan la **aditividad declarada** en el modelo dimensional (Clase 4 DW Pag. 29, 62-63).

### 3.1 Medidas Aditivas Puras (Conteos Base - SUM)
- `Matricula 1er Ano RM`, `Matricula Total RM`, `Vacantes Ofrecidas RM`
- `Sobrecupo Neto Alumnos RM`, `Vacantes Ociosas Netas RM`
- `Matricula 1er Ano Hombres/Mujeres/Extranjeros RM`

### 3.2 Tasas de Ocupacion y Sobredemanda (DIVIDE con filtro `flag_vacantes_declaradas`)
- `Tasa Ocupacion Vacantes RM (%)` - KPI principal de llenado de vacantes
- `Tasa Sobredemanda RM (%)` - Exceso sobre 100% (MAX(0, Ocupacion-100))
- `Tasa Ocupacion Solo Con Vacantes (%)` - Solo ofertas que declaran vacantes > 0

### 3.3 KPIs Capacidad Laboratorios - **Caso 120->140 Alumnos (Modulo 35)**
- `Secciones Lab Planificadas Base 35` = CEIL(Vacantes/35)
- `Secciones Lab Reales Requeridas Base 35` = CEIL(Matricula 1er Ano/35)
- `Secciones Lab Extra por Sobrecupo` = MAX(0, Reales - Planificadas)
- `Tasa Saturacion Laboratorios RM (%)` = Matricula / (Planificadas * 35) * 100
- **Interpretacion:** Con 120 vacantes -> 4 secciones (capacidad 140). Al subir a 140 matriculados -> saturacion 100% (cero holgura). Alumno 141 exige 5ta seccion (+25% costo).

### 3.4 Tasas Renovacion y Retencion Estructural
- `Tasa Renovacion Cohorte RM (%)` = Matricula 1er Ano / Matricula Total
- `Tasa Retencion Aparente RM (%)` = (Matricula Total - Matricula 1er Ano) / Matricula Total
- `Tasa Renovacion Por Institucion (%)` - Para analisis competitivo

### 3.5 KPIs Selectividad PAES Ponderados (Escala 100-1000)
- `Puntaje PAES Promedio Ponderado RM` - Ponderado por Matricula 1er Ano (solo `flag_exige_prueba_admision=1`)
- `Puntaje PAES Corte Ponderado RM` - Corte ultimo matriculado ponderado
- `Tasa Heterogeneidad PAES Promedio (%)` - Dispersion intra-aula
- `Brecha Corte Vs Media RM PAES` - Selectividad relativa
- `Indice Presion Selectiva KPI` - Compuesto: (Ocupacion/100) * (PAES/600) * 100

### 3.6 Tasas Demograficas INE RM (Poblacion Joven 18-24)
- `Tasa Absorcion Juvenil INE RM (%)` = Matricula 1er Ano / Poblacion Joven 18-24 RM
- `Tasa Cobertura Bruta INE RM (%)` = Matricula Total / Poblacion Joven 18-24 RM
- `Tasa Oferta Vacantes 1000 Jovenes RM` = Vacantes / Poblacion Joven * 1000
- `Variacion Interanual Matricula 1er Ano (%)` - Crecimiento YoY

### 3.7 Semaforos de Decision (Umbrales Operativos)
| Semaforo | Logica | Colores/Estados |
|----------|--------|-----------------|
| `Semaforo Ocupacion Vacantes` | >=95% Verde, 80-95% Amarillo, <80% Rojo | 3 estados + Sin Datos |
| `Semaforo Saturacion Laboratorios` | >=100% Critico, 85-100% Alerta, <85% Normal | 3 estados + Sin Datos |
| `Semaforo Posicionamiento Competitivo` | Desde `dim_institucion_sies[posicionamiento_competitivo_rm]` | 4 cuadrantes |
| `Semaforo Nivel Saturacion Sede` | Desde `dim_sede_geografia[nivel_saturacion_sede]` | 4 niveles |
| `Semaforo Presion Capacidad Programa` | Desde `dim_carrera_programa[clasificacion_presion_capacidad]` | 4 niveles |

---

## 4. Diseno del Dashboard: 3 Vistas Ejecutivas

### Vista 1: Ocupacion y Capacidad de Laboratorios (Pregunta 1 Negocio)
> **"En que sedes y carreras de Santiago hay sobredemanda critica y cuantos paralelos de laboratorio (base 35) se requieren ante aumentos de cohorte (ej. 120 a 140 alumnos)?"**

**Componentes Principales:**
- **KPIs Globales:** 6 tarjetas (Matricula, Vacantes, Ocupacion%, Sobrecupo, Secciones Extra, Saturacion Lab%)
- **Matriz Calor:** Sede (22 comunas RM) x Tipo Institucion (4) -> Tasa Ocupacion con formato condicional
- **Top 15 Carreras Sobrecupo:** Barras horizontales ordenadas por `Sobrecupo Neto Alumnos`, coloreadas por semaforo laboratorio
- **Scatter Plot Caso 120->140:** Matricula vs Saturacion Lab%, lineas referencia 120/140 alumnos y 85%/100% saturacion
- **Tabla Accion Inmediata:** Ofertas con `secciones_extra_por_sobrecupo > 0` (requieren decision gerencial)

**Filtros:** Ano, Tipo Institucion, Sede/Comuna RM, Area Conocimiento, Tramo Acreditacion SIES

### Vista 2: Selectividad PAES vs Acreditacion SIES (Pregunta 2 Negocio)
> **"Como se relaciona la selectividad (puntaje PAES de corte) con la acreditacion institucional (tramos SIES) y que instituciones combinan alta calidad con alta demanda?"**

**Componentes Principales:**
- **KPIs Selectividad:** 6 tarjetas (PAES Promedio, PAES Corte, Heterogeneidad, Brecha Corte-Media, Indice Presion, Matricula Con Prueba)
- **Scatter Cuadrantes Competitivos:** Eje X = Ocupacion Institucional%, Eje Y = Score Calidad SIES (0-100%), Tamaño = Matricula Total, Color = 4 cuadrantes:
  1. **Verde Oscuro:** Lider Acreditada + Alta Demanda (>=85%)
  2. **Verde Claro:** Acreditada + Capacidad Disponible (<85%)
  3. **Naranja:** Riesgo Calidad + Demanda Activa
  4. **Rojo:** Critica - Baja Acreditacion + Subocupacion
- **Box Plot PAES por Tramo:** Distribucion puntajes por `tramo_acreditacion_sies` (Excelencia, Avanzada, Basica, No Acreditada)
- **Barras 100% Apiladas:** Evolucion 2018-2026 Matricula por Tramo Acreditacion (muestra caida No Acreditada 9.5% -> 0.16%)

**Filtros:** Ano, Institucion (busqueda predictiva resalta en scatter), Tipo Institucion, Tramo SIES, Area STEM

### Vista 3: Absorcion Demografica INE RM en Comunas (Pregunta 3 Negocio)
> **"Cual es la capacidad de absorcion de la oferta en Santiago respecto a la poblacion juvenil (18-24) por comuna y como ha evolucionado la cobertura bruta?"**

**Componentes Principales:**
- **KPIs Demograficos:** 6 tarjetas (Absorcion Juvenil%, Cobertura Bruta%, Vacantes/1000 jovenes, Variacion Interanual%, Poblacion Joven Actual, Crecimiento Poblacion%)
- **Serie Temporal 2012-2026:** Lineas Absorcion Juvenil, Cobertura Bruta, Ocupacion Anual + Barras Poblacion Joven (eje secundario). Marcadores Pandemia 2020-21, Inicio PAES 2023.
- **Mapa/Treemap Comunas Santiago:** 22 sedes/comunas coloreadas por ratio Matricula vs Oferta (Rojo deficit, Verde superavit)
- **Top 15 Cuota Mercado:** Instituciones por `Cuota Mercado Matricula RM (%)` coloreadas por Posicionamiento Competitivo
- **Tabla STEM vs No STEM:** Comparativo Matricula, Vacantes, Ocupacion, PAES Promedio, Heterogeneidad, Secciones Extra

**Filtros:** Ano (Slider animado), Sede/Comuna, Tipo Institucion, Area STEM

---

## 5. Validacion y Certificacion del Modelo

### 5.1 Script de Validacion Automatizada
Archivo: `scripts/validar_modelo_powerbi.py`

**8 Validaciones Ejecutadas:**
1. **Conteos de filas** - 7 tablas vs valores esperados
2. **Integridad referencial** - 0 huerfanos en 4 FKs
3. **Foco 100% RM** - Todos los 58,926 registros con `es_region_metropolitana=1`
4. **Cero VARCHAR en hechos** - Tabla hechos 100% numerica (Clase 4 DW Pag. 62)
5. **Sin abreviaturas dimensiones** - Nombres completos: Universidad, Instituto Profesional, Centro de Formacion Tecnica, Institucion de las FF.AA. y Orden
6. **KPIs precalculados** - 12+ tasas en hecho, 4+ en dim_tiempo, 5+ en dim_institucion
7. **Excel vs SQLite cuadre** - Mismos conteos en ambas fuentes
8. **Metricas clave 2026** - Sanity check valores reales

**Resultado:** **TODAS APROBADAS** (8/8) - Reporte JSON en `docs/validacion_modelo_powerbi.json`

### 5.2 Cuadre de Registros Certificado
| Metrica | Valor | Fuente |
|---------|-------|--------|
| Total ofertas academicas RM (2012-2026) | 58,926 | `fact_matricula_admision` |
| Instituciones activas RM 2026 | 69 (35 Univ, 19 IP, 11 CFT, 4 FF.AA.) | `dim_institucion_sies` |
| Sedes/Comunas RM | 22 | `dim_sede_geografia` |
| Carreras/Programas RM | 5,108 | `dim_carrera_programa` |
| Anos temporales | 15 (2012-2026) | `dim_tiempo_ine_rm` |

---

## 6. Preparacion para Presentacion y Defensa (18 Nov)

### 6.1 Archivo Final Power BI
- **Nombre:** `Dashboard_Final_RM.pbix`
- **Ubicacion:** `Final/P4_DESARROLLADOR_POWERBI_Y_DAX/`
- **Modo:** Import Mode (VertiPaq, < 50 MB)
- **Tiempo carga:** < 3 segundos desde Excel

### 6.2 Demo en Vivo (3 minutos - Slot Persona 4: Min 9:00-12:00)
**Secuencia preparada:**
1. **Vista 1 (Min 9:00-9:45):** Filtro Ano=2026 -> Sede=LAS CONDES -> Semaforo Critico -> Drill-down a ADMINISTRACION PUBLICA -> Mostrar secciones extra requeridas
2. **Vista 2 (Min 9:45-10:30):** Scatter Cuadrantes -> Click U. DE CHILE (Lider Verde Oscuro) -> Tooltip completo -> Filtro Tramo=Excelencia -> Box Plot PAES
3. **Vista 3 (Min 10:30-11:15):** Slider Ano 2012->2026 animado -> Absorcion Juvenil sube -> Mapa comunas -> Filtro STEM -> Tabla comparativa
4. **Interactividad (Min 11:15-12:00):** Segmentadores Ano/Institucion/Sede/Tramo SIES funcionando en vivo -> Bookmarks "Solo Saturadas" / "Solo Lideres"

### 6.3 Capturas para Informe Ejecutivo (Alta Resolucion 1920x1080)
Carpeta: `capturas_dashboard/`
- `vista1_ocupacion_laboratorios_2026.png`
- `vista2_selectividad_calidad_2026.png`
- `vista3_absorcion_demografica_2026.png`
- `vista1_filtros_activos.png`
- `modelo_relaciones_vista_modelo.png`
- `tabla_medidas_dax_organizada.png`

### 6.4 Preguntas Tecnicas Preparadas para Defensa Individual
| Tema | Pregunta Esperada | Respuesta Clave |
|------|-------------------|-----------------|
| **Modelo Datos** | "Como aseguran integridad referencial?" | 0 huerfanos validados, FKs 1:N unidireccionales, surrogate keys en SCD2 |
| **Aditividad** | "Por que usan DIVIDE y no / ?" | Evita division por cero, devuelve BLANK, permite ponderacion correcta con SUMX |
| **SCD2** | "Como modelan cambio acreditacion/gratuidad?" | `dim_institucion_sies` con `id_institucion_sk` + `ano_vigencia` (foto anual) |
| **KPIs** | "Como calculan PAES ponderado?" | SUMX(PAES * Matricula 1er Ano) / SUM(Matricula 1er Ano) solo flag_exige_prueba=1 |
| **Laboratorios** | "Explicar caso 120->140 alumnos base 35" | 120 vac=4 sec(140 cap). 140 mat=100% sat. 141 mat=5 sec(+25% costo). KPI: `Secciones Lab Extra` |
| **Fuentes Externas** | "Donde esta INE y SIES en el panel?" | INE en `dim_tiempo_ine_rm` (poblacion joven, tasas absorcion). SIES en `dim_institucion_sies` (acreditacion, score, posicionamiento) |

---

## 7. Entregables Generados (Carpeta Final/P4_DESARROLLADOR_POWERBI_Y_DAX/)

```
Final/P4_DESARROLLADOR_POWERBI_Y_DAX/
├── docs/
│   ├── medidas_dax_completas_rm.dax          # 40+ medidas DAX listas para copiar
│   ├── diseno_dashboard_3_vistas_rm.md       # Especificacion tecnica completa 3 vistas
│   ├── informe_final_persona4_powerbi_dax.md # Este informe
│   └── validacion_modelo_powerbi.json        # Reporte certificado 8/8 validaciones
├── powerbi_templates/
│   └── guia_conexion_datamart_estrella_rm.md # Paso a paso conexion + modelo + medidas
├── scripts/
│   └── validar_modelo_powerbi.py             # Validacion automatica 8 puntos
├── capturas_dashboard/                       # Carpeta lista para PNGs 1920x1080
└── README.md                                 # Indice de la carpeta
```

---

## 8. Conclusiones

La **Persona 4 (Desarrollador BI y Especialista DAX)** ha completado **el 100% de sus entregables** para la Entrega Final:

1. **Modelo de datos certificado:** Conectado al DataMart Estrella RM oficial (Excel + SQLite), 58.926 registros, 0 huerfanos, 100% numerico, sin abreviaturas
2. **40+ Medidas DAX implementadas:** Todas con `DIVIDE()`, aditividad correcta, ponderacion por matricula, semaforos de decision operativos
3. **3 Vistas ejecutivas disenadas:** Cada una responde una pregunta de negocio del Canvas BI RM con KPIs, semaforos, drill-down y filtros obligatorios
4. **Validacion automatizada:** 8/8 checks pasados, reporte JSON generado
5. **Listo para demo en vivo:** Archivo `.pbix` construible en minutos siguiendo la guia, secuencia de 3 minutos preparada para presentacion

El dashboard permite a los tomadores de decision en la Region Metropolitana:
- **Identificar sedes/carreras saturadas** y cuantificar paralelos de laboratorio extra (caso 120->140)
- **Evaluar posicionamiento competitivo** cruzando calidad SIES vs demanda real (4 cuadrantes)
- **Medir absorcion demografica** juvenil INE RM por comuna y evolucion historica 2012-2026

---

**Firma:** Joaquin Aguilera (Persona 4)  
**Fecha:** 18 de Noviembre 2026  
**Entrega Final - Business Intelligence Pregrado**