# Diseno del Dashboard Power BI - 3 Vistas Ejecutivas Region Metropolitana

## Resumen General

**Objetivo:** Responder las 3 preguntas de negocio del Canvas BI RM mediante 3 paginas interactivas con semaforos de decision y filtros obligatorios (Ano, Institucion, Sede/Comuna RM, Tramo Acreditacion SIES).

**Fuente de datos:** `DataMart_Estrella_RM_PowerBI.xlsx` (carga instantanea, 58.926 registros historicos 2012-2026, 69 IES activas en 2026)

**Medidas DAX:** Ver `docs/medidas_dax_completas_rm.dax` (todas con DIVIDE, aditividad correcta)

---

## Vista 1: Ocupacion y Capacidad de Laboratorios (Pregunta 1 Negocio)

### Pregunta de Negocio
> "En que sedes y carreras de Santiago hay sobredemanda critica de vacantes y cuantos paralelos de laboratorio (base 35 puestos) se requieren ante aumentos de cohorte (ej. 120 a 140 alumnos)?"

### Objetivos Visuales
- Identificar sedes saturadas vs con capacidad ociosa
- Cuantificar sobrecupo neto de alumnos y secciones extra requeridas
- Visualizar el caso 120->140 alumnos en modulos de 35 puestos
- Permitir decision: abrir/cerrar secciones, ajustar vacantes 2027

### Layout de Pagina (16:9)

#### Fila Superior - KPIs Globales (Tarjetas)
| Posicion | Medida | Formato | Alerta Visual |
|----------|--------|---------|---------------|
| 1 | `Matricula 1er Ano RM` | Entero | - |
| 2 | `Vacantes Ofrecidas RM` | Entero | - |
| 3 | `Tasa Ocupacion Vacantes RM (%)` | % (1 dec) | Verde >=95%, Amarillo 80-95%, Rojo <80% |
| 4 | `Sobrecupo Neto Alumnos RM` | Entero | Rojo si > 0 |
| 5 | `Secciones Lab Extra por Sobrecupo` | Entero | Rojo si > 0 |
| 6 | `Tasa Saturacion Laboratorios RM (%)` | % (1 dec) | Rojo >=100%, Amarillo 85-100%, Verde <85% |

#### Fila Media - Graficos Principales

**Izquierda (60% ancho): Mapa de Calor - Sede x Tipo Institucion**
- Tipo: **Matriz** (Matrix visual)
- Filas: `dim_sede_geografia[nombre_sede]` (22 sedes RM)
- Columnas: `dim_institucion_sies[tipo_institucion]` (4 tipos)
- Valores: `Tasa Ocupacion Vacantes RM (%)` + formato condicional (rojo-amarillo-verde)
- Tooltip: `Matricula 1er Ano RM`, `Vacantes Ofrecidas RM`, `Sobrecupo Neto Alumnos RM`, `Secciones Lab Extra por Sobrecupo`
- Permite drill-down: Sede -> Institucion especifica

**Derecha (40% ancho): Barras Horizontales - Top 15 Carreras con Sobrecupo**
- Tipo: **Grafico de barras horizontales**
- Eje Y: `dim_carrera_programa[nombre_programa]` (Top 15 por `Sobrecupo Neto Alumnos RM`)
- Eje X: `Sobrecupo Neto Alumnos RM`
- Color: `Semaforo Saturacion Laboratorios` (Critico=Rojo, Alerta=Naranja, Normal=Verde)
- Tooltip: `area_conocimiento`, `tipo_institucion`, `nombre_sede`, `Tasa Saturacion Laboratorios RM (%)`, `secciones_extra_por_sobrecupo`

#### Fila Inferior - Analisis de Caso 120->140 Alumnos

**Izquierda: Scatter Plot - Presion Laboratorios vs Matricula**
- Eje X: `Matricula 1er Ano RM` (por oferta)
- Eje Y: `Tasa Saturacion Laboratorios RM (%)`
- Tamaño: `Sobrecupo Neto Alumnos RM`
- Color: `tipo_institucion`
- Linea de referencia horizontal: 100% (cero holgura), 85% (alerta)
- Linea de referencia vertical: 120, 140 alumnos (umbrales caso real)
- Quadrant labels: "Zona Critica (>=140, >=100%)", "Zona Alerta (120-140, 85-100%)", "Zona Normal"

**Derecha: Tabla Detalle - Ofertas que Requieren Accion Inmediata**
- Tipo: **Tabla** con formato condicional
- Columnas: `nombre_institucion`, `nombre_sede`, `nombre_programa`, `area_conocimiento`, `vacantes`, `matricula_primer_ano_total`, `sobrecupo_neto_alumnos`, `secciones_lab_planificadas_35`, `secciones_lab_reales_35`, `secciones_extra_por_sobrecupo`, `tasa_saturacion_lab_35_pct`, `Semaforo Saturacion Laboratorios`
- Filtro: `secciones_extra_por_sobrecupo > 0` (solo ofertas con accion requerida)
- Orden: `sobrecupo_neto_alumnos` descendente

### Filtros de Pagina (Slicers Visibles)
- **Ano** (`dim_tiempo_ine_rm[ano]`) - Lista horizontal, multi-seleccion
- **Tipo Institucion** (`dim_institucion_sies[tipo_institucion]`) - Botones
- **Sede/Comuna RM** (`dim_sede_geografia[nombre_sede]`) - Lista con busqueda
- **Area Conocimiento** (`dim_carrera_programa[area_conocimiento]`) - Lista
- **Tramo Acreditacion SIES** (`dim_institucion_sies[tramo_acreditacion_sies]`) - Casillas

### Bookmarks / Navegacion
- Bookmark "Vista General" (todos los filtros limpios)
- Bookmark "Solo Saturadas" (filtro `Semaforo Saturacion Laboratorios = "1. Critico"`)
- Bookmark "Solo Con Sobrecupo" (filtro `secciones_extra_por_sobrecupo > 0`)

---

## Vista 2: Selectividad PAES vs Acreditacion SIES (Pregunta 2 Negocio)

### Pregunta de Negocio
> "Como se relaciona la selectividad (puntaje PAES de corte) con la acreditacion institucional (tramos SIES) y que instituciones de Santiago combinan alta calidad con alta demanda?"

### Objetivos Visuales
- Visualizar posicionamiento competitivo: 4 cuadrantes (Calidad SIES x Ocupacion)
- Identificar lideres acreditados con alta demanda vs instituciones en riesgo
- Analizar dispersion de puntajes PAES por carrera/institucion
- Permitir decision: ajuste puntajes minimos, estrategia de retencion, marketing

### Layout de Pagina (16:9)

#### Fila Superior - KPIs Selectividad
| Posicion | Medida | Formato |
|----------|--------|---------|
| 1 | `Puntaje PAES Promedio Ponderado RM` | Decimal (1) |
| 2 | `Puntaje PAES Corte Ponderado RM` | Decimal (1) |
| 3 | `Tasa Heterogeneidad PAES Promedio (%)` | % (1 dec) |
| 4 | `Brecha Corte Vs Media RM PAES` | Decimal (1) |
| 5 | `Indice Presion Selectiva KPI` | Decimal (1) |
| 6 | `Matricula 1er Ano Con Prueba` | Entero |

#### Fila Media - Grafico Principal: Cuadrantes Competitivos

**Scatter Plot Institucional - Posicionamiento Competitivo RM**
- Eje X: `tasa_ocupacion_inst_anual_pct` (de `dim_institucion_sies`) - Ocupacion anual
- Eje Y: `score_calidad_sies_pct` (de `dim_institucion_sies`) - Calidad SIES 0-100%
- Tamaño: `Matricula Total RM` (burbuja = mercado)
- Color: `posicionamiento_competitivo_rm` (4 colores fijos):
  - **Verde Oscuro**: "1. Lider Acreditada con Alta Demanda (>=85%)"
  - **Verde Claro**: "2. Acreditada con Capacidad Disponible (<85%)"
  - **Naranja**: "3. En Riesgo de Calidad con Demanda Activa"
  - **Rojo**: "4. Critica: Baja Acreditacion y Subocupacion"
- Etiquetas de datos: `nombre_institucion` (solo top 10 por matricula)
- Lineas de referencia: X=85% (umbral alta demanda), Y=57% (4 anos acreditacion = basico)
- Tooltip: `tipo_institucion`, `anos_acreditacion_sies`, `cuota_mercado_matricula_rm_pct`, `tasa_permanencia_cohortes_sup_pct`, `puntaje_paes_ponderado_inst`

#### Fila Inferior - Analisis Detallado

**Izquierda (50%): Box Plot / Violin - Distribucion PAES por Tramo Acreditacion**
- Tipo: **Box and Whisker** (custom visual) o **Distribucion apilada**
- Eje X: `tramo_acreditacion_sies` (4 categorias ordenadas)
- Eje Y: `puntaje_promedio_equiv_paes` (o `puntaje_corte_ultimo_equiv_paes`)
- Grupo: `tipo_institucion` (colores)
- Muestra: dispersion real de puntajes en cada tramo
- Linea de referencia: Media RM (`Puntaje PAES Promedio Ponderado RM`)

**Derecha (50%): Barras Apiladas 100% - Matricula por Tramo Acreditacion x Ano**
- Tipo: **Columna apilada 100%**
- Eje X: `dim_tiempo_ine_rm[ano]` (2018-2026, desde cobertura SIES)
- Leyenda: `tramo_acreditacion_sies` (4 colores fijos)
- Valor: `Matricula 1er Ano RM` (proporcion)
- Muestra evolucion: reduccion drastica "No Acreditada" (9.5% -> 0.16% en 2026)

### Filtros de Pagina (Slicers Visibles)
- **Ano** (`dim_tiempo_ine_rm[ano]`) - Lista horizontal
- **Institucion** (`dim_institucion_sies[nombre_institucion]`) - Busqueda predictiva (resalta en scatter)
- **Tipo Institucion** (`dim_institucion_sies[tipo_institucion]`) - Botones
- **Tramo Acreditacion SIES** (`dim_institucion_sies[tramo_acreditacion_sies]`) - Casillas (filtra scatter y box plot)
- **Area STEM** (`dim_carrera_programa[es_area_stem]`) - Casilla (STEM vs No STEM)

### Bookmarks
- "Cuadrantes Completos" (vista general)
- "Solo Lideres" (filtro posicionamiento = Lider)
- "Solo Criticas" (filtro posicionamiento = Critica)
- "Solo STEM" / "Solo No STEM"

---

## Vista 3: Absorcion Demografica INE RM en Comunas de Santiago (Pregunta 3 Negocio)

### Pregunta de Negocio
> "Cual es la capacidad de absorcion de la oferta de educacion superior en Santiago respecto a la poblacion juvenil (18-24 anos) por comuna y como ha evolucionado la cobertura bruta?"

### Objetivos Visuales
- Conectar datos demograficos INE RM (poblacion joven 18-24) con matricula real
- Identificar comunas con deficit/superavit de oferta
- Visualizar tasa de absorcion juvenil y cobertura bruta historica
- Permitir decision: expansion de sedes, nueva oferta en comunas desatendidas

### Layout de Pagina (16:9)

#### Fila Superior - KPIs Demograficos
| Posicion | Medida | Formato | Contexto |
|----------|--------|---------|----------|
| 1 | `Tasa Absorcion Juvenil INE RM (%)` | % (1 dec) | Matricula 1er ano / Poblacion joven 18-24 RM |
| 2 | `Tasa Cobertura Bruta INE RM (%)` | % (1 dec) | Matricula total / Poblacion joven 18-24 RM |
| 3 | `Tasa Oferta Vacantes 1000 Jovenes RM` | Decimal (1) | Vacantes por 1000 jovenes |
| 4 | `Variacion Interanual Matricula 1er Ano (%)` | % (1 dec) | Crecimiento interanual |
| 5 | `Poblacion Joven 18-24 RM (Actual)` | Entero | Desde `dim_tiempo_ine_rm` ano seleccionado |
| 6 | `Crecimiento Poblacion Joven RM (%)` | % (1 dec) | `tasa_crecimiento_joven_rm_yoy_pct` |

#### Fila Media - Evolucion Temporal + Mapa Comunal

**Izquierda (55%): Serie Temporal - Tasas Demograficas Anuales**
- Tipo: **Grafico de lineas combinado**
- Eje X: `dim_tiempo_ine_rm[ano]` (2012-2026)
- Linea 1 (eje Y izquierdo): `tasa_absorcion_juvenil_rm_pct` (desde `dim_tiempo_ine_rm`) - Azul
- Linea 2 (eje Y izquierdo): `tasa_cobertura_bruta_rm_pct` - Verde
- Linea 3 (eje Y izquierdo): `tasa_ocupacion_anual_rm_pct` - Naranja
- Barras (eje Y derecho): `poblacion_joven_18_24_rm` - Gris transparente
- Marcadores: 2020-2021 (Pandemia), 2023 (Inicio PAES)
- Tooltip: Todas las tasas + `media_anual_paes_rm`

**Derecha (45%): Mapa de Comunas de Santiago - Capacidad vs Demanda**
- Tipo: **Mapa de forma (Shape Map) / Azure Maps** con TopoJSON comunas RM
- Alternativa si no hay mapa: **Treemap** por `nombre_sede` (comuna)
- Color: `participacion_matricula_rm_sede_pct` vs `tasa_oferta_vacantes_1000_jovenes_rm` (ratio)
- Esquema: Rojo (deficit oferta), Amarillo (equilibrio), Verde (superavit)
- Tooltip: `nombre_sede`, `participacion_matricula_rm_sede_pct`, `tasa_ocupacion_historica_sede_pct`, `nivel_saturacion_sede`, `Matricula 1er Ano RM`, `Vacantes Ofrecidas RM`
- Nota: 22 sedes/comunas en RM, usar `dim_sede_geografia` como dimension geografica

#### Fila Inferior - Analisis por Institucion y Carrera

**Izquierda: Barras - Cuota de Mercado RM por Institucion (Top 15)**
- Tipo: **Barras horizontales ordenadas**
- Eje Y: `nombre_institucion` (Top 15 por `cuota_mercado_matricula_rm_pct`)
- Eje X: `Cuota Mercado Matricula RM (%)`
- Color: `posicionamiento_competitivo_rm` (4 colores)
- Tooltip: `tipo_institucion`, `tramo_acreditacion_sies`, `Matricula Total RM`, `Tasa Ocupacion Vacantes RM (%)`, `Puntaje PAES Promedio Ponderado RM`

**Derecha: Tabla - Carreras STEM vs No STEM en Santiago**
- Tipo: **Tabla resumen**
- Filas: `es_area_stem` (2 filas: STEM, Otras Areas)
- Columnas: `Matricula 1er Ano RM`, `Vacantes Ofrecidas RM`, `Tasa Ocupacion Vacantes RM (%)`, `Puntaje PAES Promedio Ponderado RM`, `Tasa Heterogeneidad PAES Promedio (%)`, `Secciones Lab Extra por Sobrecupo`
- Formato condicional en tasa ocupacion y secciones extra

### Filtros de Pagina (Slicers Visibles)
- **Ano** (`dim_tiempo_ine_rm[ano]`) - Slider / Lista horizontal (clave para ver evolucion)
- **Sede/Comuna RM** (`dim_sede_geografia[nombre_sede]`) - Lista (filtra mapa y treemap)
- **Tipo Institucion** (`dim_institucion_sies[tipo_institucion]`) - Botones
- **Area STEM** (`dim_carrera_programa[es_area_stem]`) - Casilla

### Bookmarks
- "Evolucion 2012-2026" (todos los anos)
- "Solo 2026" (foto actual)
- "Pre-Pandemia" (2012-2019)
- "Pandemia" (2020-2021)
- "Post-Pandemia PAES" (2022-2026)

---

## Navegacion Global y UX

### Pestañas de Navegacion (Tabs)
1. **1. Ocupacion y Laboratorios** (Vista 1)
2. **2. Selectividad y Calidad** (Vista 2)
3. **3. Absorcion Demografica** (Vista 3)

### Barra de Navegacion Superior (Botones/Iconos)
- Boton "Resetear Filtros" (limpia todos los slicers)
- Boton "Pantalla Completa" (F11)
- Selector de Tema: Claro / Oscuro (Power BI nativo)

### Tooltips Personalizados
- **Tooltip Institucion**: `nombre_institucion`, `tipo_institucion`, `tramo_acreditacion_sies`, `anos_acreditacion_sies`, `cuota_mercado_matricula_rm_pct`, `posicionamiento_competitivo_rm`, `tasa_permanencia_cohortes_sup_pct`, `puntaje_paes_ponderado_inst`
- **Tooltip Programa**: `nombre_programa`, `carrera_generica`, `area_conocimiento`, `horario`, `tasa_ocupacion_historica_prog_pct`, `clasificacion_presion_capacidad`, `tasa_presion_lab_base35_prog_pct`
- **Tooltip Sede**: `nombre_sede`, `participacion_matricula_rm_sede_pct`, `tasa_ocupacion_historica_sede_pct`, `nivel_saturacion_sede`

### Accesibilidad
- Contraste alto en semaforos (no solo color, tambien iconos/texto)
- Orden de tabulacion logico
- Textos alternativos en graficos

---

## Publicacion y Demo en Vivo (18 Nov)

### Archivo Final
- **Nombre**: `Dashboard_Final_RM.pbix`
- **Ubicacion**: `Final/P4_DESARROLLADOR_POWERBI_Y_DAX/`
- **Tamaño estimado**: < 50 MB (Import Mode, datos comprimidos VertiPaq)

### Preparacion Demo (3 minutos en presentacion)
1. Abrir `.pbix` en Power BI Desktop
2. Vista 1: Mostrar filtro Ano=2026, Sede=LAS CONDES -> Semaforo Critico, drill-down a carrera ADMINISTRACION PUBLICA
3. Vista 2: Scatter cuadrantes, click en "U. DE CHILE" -> tooltip completo, filtro Tramo=Excelencia
4. Vista 3: Slider Ano 2012->2026 animado, mostrar absorcion juvenil subiendo, mapa comunas
5. Mostrar segmentadores funcionando en vivo (Ano, Institucion, Sede, Tramo SIES)

### Capturas para Informe (Alta Resolucion)
Exportar cada vista como PNG 1920x1080:
- `capturas_dashboard/vista1_ocupacion_laboratorios_2026.png`
- `capturas_dashboard/vista2_selectividad_calidad_2026.png`
- `capturas_dashboard/vista3_absorcion_demografica_2026.png`
- `capturas_dashboard/vista1_filtros_activos.png`
- `capturas_dashboard/modelo_relaciones_vista_modelo.png`
- `capturas_dashboard/tabla_medidas_dax_organizada.png`

---

## Checklist de Cumplimiento Pauta Oficial

| Requisito Pauta | Cumplimiento | Donde |
|-----------------|--------------|-------|
| Conectado al DataMart (no Excel crudo) | Si | `DataMart_Estrella_RM_PowerBI.xlsx` |
| Responde 3 preguntas de negocio | Si | 3 vistas dedicadas |
| Filtros: Ano, Institucion, Region | Si | 4 slicers obligatorios + Sede/Comuna RM |
| Al menos 1 medida DAX creada | Si | 40+ medidas DAX con DIVIDE |
| Medidas aditivas vs no aditivas correctas | Si | SUM para conteos, DIVIDE ponderado para tasas |
| Cero abreviaturas en filtros/visuales | Si | Nombres completos en dimensiones |
| Interactividad (drill-down, slicers) | Si | Jerarquias + slicers + bookmarks |
| Semaforos/umbrales de decision | Si | 5 semaforos DAX implementados |

---

**Fin del diseno.** Este documento sirve como especificacion tecnica para construir el `.pbix` y como evidencia para el Informe Ejecutivo Final y la PPT de defensa.