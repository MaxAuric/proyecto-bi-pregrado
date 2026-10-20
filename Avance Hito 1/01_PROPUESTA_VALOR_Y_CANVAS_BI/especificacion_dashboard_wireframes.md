# Especificación de Usabilidad, Wireframes y Arquitectura de Visualización
## Rol: Persona 4 (Desarrollador BI) - Hito 1
**Proyecto:** Business Intelligence - Análisis Estratégico de Oferta, Capacidad y Calidad en la Educación Superior Chilena (2012–2026)  
**Herramienta Objetivo:** Power BI Desktop  
**Fecha:** 21 de Octubre de 2026  

---

## 1. Enfoque de Experiencia de Usuario (UX/UI) y Usabilidad

El panel de control en Power BI está diseñado para responder con inmediatez y claridad a la **Dirección de Admisión y Planificación Estratégica** de instituciones de educación superior, así como a analistas de política pública y comisiones evaluadoras.

### 1.1. Principios de Diseño
1. **Jerarquía Visual y Carga Cognitiva:**
   - La información macro (KPIs y totales agregados) se ubica en el tercio superior de cada página.
   - Las comparativas y segmentaciones dimensionales ocupan el cuerpo principal.
   - Las tablas detalladas con granularidad institucional o de programa quedan en vistas de drill-down o tooltips para no saturar al tomador de decisiones.
2. **Consistencia Cromática Semántica:**
   - **Azul Corporativo Primario (`#102C57`):** Totales, tendencias históricas y valores de referencia.
   - **Azul Secundario (`#35598F`):** Universidades y año de corte 2026.
   - **Verde Acreditación / Éxito (`#2E7D32`):** Instituciones acreditadas, tasas de ocupación óptimas (80%–100%).
   - **Rojo de Alerta (`#D32F2F`):** Zonas de déficit territorial, instituciones no acreditadas o tasas de ocupación críticas (< 75%).
   - **Naranja / Ámbar (`#F57C00`):** Instituciones bajo tutela o Institutos Profesionales.
3. **Interactividad y Cross-Filtering:**
   - Todos los gráficos actúan como filtros cruzados bidireccionales.
   - Se habilitan **Tooltips de Página (Report Page Tooltips)** que muestran la composición de matrícula por sexo y tipo de jornada al pasar el cursor sobre cualquier región o institución.

---

## 2. Mapa del Dashboard y Estructura por Páginas

El panel se compone de 4 páginas principales más 1 página oculta de tooltip interactivo:

```text
Dashboard Power BI (.pbix)
├── Página 1: Resumen Ejecutivo y Macrotendencias Nacionales (2012–2026)
├── Página 2: P1 - Equidad Territorial y Capacidad Regional (INE)
├── Página 3: P2 - Uso de la Capacidad y Ocupación de Vacantes (CNED)
├── Página 4: P3 - Calidad, Acreditación y Competencia (SIES)
└── Tooltip Page (Oculta): Perfil Académico y Demográfico por Institución/Región
```

---

## 3. Especificación Detallada por Página y Wireframes

### Página 1: Resumen Ejecutivo y Macrotendencias Nacionales
* **Objetivo:** Brindar a la rectoría y directivos una visión general de la evolución de la educación superior en los últimos 15 años.
* **Componentes:**
  - **Filtros Laterales:** Año (Segmentador entre 2012 y 2026), Tipo de Institución (Univ, IP, CFT), Macro-Zona.
  - **Tarjetas KPI (KPI Cards):**
    1. *Matrícula Primer Año Nacional:* 399.015 (Año 2026).
    2. *Vacantes Declaradas:* 472.580 vacantes oficiales.
    3. *Tasa Ocupación Global:* 84,4%.
    4. *Tasa Oferta p/ 1.000 hab. (15-64):* 27,6 ‰.
    5. *% Matrícula en IES Acreditadas:* 90,5%.
  - **Gráfico Principal:** Evolución de Matrícula Total vs. Primer Año (Área apilada / Líneas 2012–2026).
  - **Gráfico Secundario:** Distribución de Matrícula por Tipo de Institución (Donut chart).

```text
+----------------------------------------------------------------------------------------------------+
|  [LOGO]  DASHBOARD ESTRATÉGICO: EDUCACIÓN SUPERIOR CHILENA (2012-2026)             Página 1: Resumen |
+------------------+---------------------------------------------------------------------------------+
| FILTROS GLOBALES | [ KPI: Matrícula 1er Año ] [ KPI: Vacantes ] [ KPI: % Ocupación ] [ KPI: Acred ] |
| - Año: [ 2026  ] |           399.015               472.580             84,4%              90,5%   |
| - Tipo IES: [Todas] +-------------------------------------------------------------------------------+
| - Zona: [Todas ] |  VISUAL: Evolución Histórica de Matrícula (2012-2026)                            |
|                  |  [ Línea Matrícula Total vs. Matrícula 1er Año ]                                |
| NAVEGACIÓN       |                                                                                 |
| > Resumen        +----------------------------------------+----------------------------------------+
|   P1: Territorio |  VISUAL: Matrícula por Tipo de IES     |  VISUAL: Top 10 Instituciones          |
|   P2: Capacidad  |  [ Gráfico Donut: Univ / IP / CFT ]    |  [ Barras Horizontales con Matrícula ] |
|   P3: Calidad    |                                        |                                        |
+------------------+----------------------------------------+----------------------------------------+
```

---

### Página 2: P1 - Equidad Territorial y Capacidad de Oferta (INE)
* **Objetivo:** Identificar en qué regiones la capacidad instalada de vacantes y matrícula es insuficiente respecto de su población joven y adulta (15 a 64 años), analizando el cambio entre 2018 y 2026.
* **Componentes:**
  - **Segmentadores:** Año único (por defecto 2026), Zona Geográfica (Norte, Centro, RM, Sur, Austral).
  - **Visual 1 (Izquierda): Mapa Coroplético de Chile (Shape Map o Azure Maps):**
    - Saturación de color según `[Matricula_Por_1000_Hab]`.
    - Alertas visuales en regiones de baja oferta (O'Higgins con 14,1 ‰, Aysén con 15,2 ‰).
  - **Visual 2 (Derecha Superior): Gráfico de Barras Horizontales Ordenadas:**
    - Eje Y: Las 16 regiones oficiales ordenadas de mayor a menor tasa.
    - Eje X: Tasa de Matrícula por 1.000 hab.
    - Serie comparativa: Barras dobles (2018 en gris claro vs. 2026 en azul institucional).
    - Línea de referencia: Promedio Nacional (27,6 ‰).
  - **Visual 3 (Derecha Inferior): Matriz de Variación 2018–2026:**
    - Columnas: Región, Población 15-64 (2026), Matrícula 1er Año (2026), Tasa 2018, Tasa 2026, Delta Absoluto, Crecimiento %.

```text
+----------------------------------------------------------------------------------------------------+
|  P1: EQUIDAD TERRITORIAL Y OFERTA POR HABITANTE (CRUCE CON INE)                    Página 2: P1    |
+------------------+-----------------------------------+---------------------------------------------+
| FILTROS          | [ KPI: Tasa Promedio Nacional ]   | [ KPI: Región Más Alta ] [ KPI: Región Más  |
| - Año: [ 2026  ] |             27,6 ‰                |      RM (35,5 ‰)         Baja ] O'Higgins   |
| - Zona: [Todas ] +-----------------------------------+---------------------------------------------+
|                  | VISUAL: Mapa Coroplético de Chile | VISUAL: Ranking de Regiones (2018 vs. 2026) |
| LEYENDA TASA     | [ Regiones coloreadas por tasa ]  | RM         ====================== [35.5]   |
| [ ] < 20 ‰ (Baja)| - Norte: Media                    | Biobío     ====================   [32.5]   |
| [ ] 20-30 ‰ (Med)| - Centro: Muy baja                | Valparaíso ===================    [31.2]   |
| [ ] > 30 ‰ (Alta)| - RM: Concentración máxima        | ...                                        |
|                  | - Sur: Media-Alta                 | O'Higgins  ========               [14.1]   |
|                  | - Austral: Variable               | --- Línea Roja: Promedio Nacional (27.6) --|
+------------------+-----------------------------------+---------------------------------------------+
| NOTA METODOLÓGICA: La matrícula corresponde a la región de la SEDE institucional (capacidad de      |
| oferta territorial), no al domicilio residencial del estudiante (Pauta BI Hito 1).                 |
+----------------------------------------------------------------------------------------------------+
```

---

### Página 3: P2 - Uso de Capacidad y Ocupación de Vacantes (CNED)
* **Objetivo:** Detectar ineficiencias de oferta (carreras o tipos de institución con sobreocupación o con capacidad ociosa/subocupación).
* **Componentes:**
  - **Segmentadores:** Año (2012–2026), Tipo de Institución, Área de Conocimiento, Región.
  - **Visual 1 (Superior Izquierda): Tarjetas de Control de Capacidad:**
    - `[Vacantes_Declaradas]` | `[Matricula_Primer_Ano_Oferta]` | `[Tasa_Ocupacion_Vacantes]`
  - **Visual 2 (Superior Derecha): Gráfico de Líneas Temporal (2012–2026):**
    - Serie de Tasa de Ocupación con bandas sombreadas: Zona de Subocupación (< 75%), Zona de Equilibrio (75%–95%), Zona de Sobredemanda (> 100%).
  - **Visual 3 (Inferior Completo): Matriz / Heatmap Institución $\times$ Región:**
    - Filas: Tipo de Institución e Institución (Jerarquía activada).
    - Columnas: Regiones geográficas.
    - Valores: `% Tasa Ocupación` con escala de color semafórica automática en Power BI.

```text
+----------------------------------------------------------------------------------------------------+
|  P2: USO DE LA CAPACIDAD Y OCUPACIÓN DE VACANTES                                   Página 3: P2    |
+------------------+---------------------------------------------------------------------------------+
| FILTROS          | [ KPI: Vacantes Declaradas ] [ KPI: Matrícula Real ] [ KPI: Tasa Ocupación ]    |
| - Año: [ 2026  ] |            472.580                    399.015                  84,4%               |
| - Tipo: [Todos ] +----------------------------------------+----------------------------------------+
| - Área: [Todas ] | VISUAL: Evolución Histórica Ocupación  | VISUAL: Ocupación por Tipo de IES      |
|                  | [ Línea 2012-2026 con banda 80-100% ]  | Universidades: 86,2%                   |
| FILTRO DE DATOS  | Mínimo: 2022 (80,2%) | 2026: 84,4%     | Inst. Profesionales: 83,1%             |
| Vacantes > 0     |                                        | CFT: 81,9%                             |
| (Excluye nulos)  +---------------------------------------------------------------------------------+
|                  | VISUAL: Matriz Institución x Región (Mapa de Calor de Ocupación %)              |
|                  | Inst / Región     |   RM   | Valparaíso | Biobío | Maule | O'Higgins | ...     |
|                  | Univ. CRUCH       |  94%   |    91%     |  93%   |  89%  |    84%    |         |
|                  | Univ. Privadas    |  85%   |    82%     |  84%   |  80%  |    76%    |         |
|                  | IP / CFT          |  82%   |    80%     |  81%   |  77%  |    71%    |         |
+------------------+---------------------------------------------------------------------------------+
```

---

### Página 4: P3 - Calidad, Acreditación y Competencia (SIES)
* **Objetivo:** Monitorear la concentración del mercado estudiantil en instituciones acreditadas y analizar la correlación entre reputación de calidad (años de acreditación) y volumen de matrícula.
* **Componentes:**
  - **Filtro Automático de Página:** `Año >= 2018` (con aviso visible de inicio de serie SIES homogénea).
  - **Segmentadores:** Año, Tipo de Institución, Tramo de Acreditación (No Acreditada, 1-3 años, 4-5 años, 6-7 años).
  - **Visual 1 (Izquierda): Barras 100% Apiladas (100% Stacked Bar Chart):**
    - Eje X: Años (2018 a 2026).
    - Eje Y: Porcentaje de Matrícula de 1er Año.
    - Leyenda: `Acreditada` (Verde), `Acreditación extendida` (Azul), `Bajo tutela` (Naranja), `No acreditada` (Rojo), `Sin dato` (Gris).
  - **Visual 2 (Derecha): Gráfico de Dispersión (Scatter Plot - Burbujas):**
    - Eje X: `Años de Acreditación` (0 a 7 años).
    - Eje Y: `Matrícula de Primer Año` (Alumnos).
    - Tamaño de Burbuja: `Matrícula Total`.
    - Color de Burbuja: `Tipo de Institución` (Univ, IP, CFT).
    - Interactividad: Permite identificar cuadrantes estratégicos de instituciones consolidadas vs. vulnerables.

```text
+----------------------------------------------------------------------------------------------------+
|  P3: CALIDAD INSTITUCIONAL Y ACREDITACIÓN SIES (2018–2026)                         Página 4: P3    |
+------------------+-----------------------------------+---------------------------------------------+
| FILTROS          | [ KPI: % Matrícula Acreditada ]   | [ KPI: Promedio Años Acreditación Ponderado]|
| - Año: [ 2026  ] |              90,5%                |                 5,2 Años                    |
| - Tipo: [Todos ] +-----------------------------------+---------------------------------------------+
| - Tramo:[Todos ] | VISUAL: Barras 100% Apiladas      | VISUAL: Dispersión Matrícula vs. Calidad    |
|                  | (% Matrícula por Estado 2018-2026)| (Burbujas por Institución - Año 2026)       |
| LEYENDA SIES     | 100% [Verde: Acreditada]          | Matrícula ^                                 |
| [ ] Acreditada   |      [Azul: Extensión]            |  50k |          (U. de Chile - 7 años)      |
| [ ] Extensión    |      [Naranja: Tutela]            |      |          (PUC - 7 años)              |
| [ ] Tutela       |      [Rojo: No Acreditada]        |  20k |     (IP INACAP - 6 años)             |
| [ ] No Acred.    |   0% +--------------------------+ |      | (CFTs)                               |
|                  |      2018 2020 2022 2024 2026     |   0k +---+---+---+---+---+---+---+--->      |
|                  |                                   |      0   1   2   3   4   5   6   7 (Años)    |
+------------------+-----------------------------------+---------------------------------------------+
| AVISO: La serie de acreditación SIES comienza en 2018. Los años 2012-2017 no poseen registro oficial |
| comparable y se excluyen de este análisis para evitar imputaciones ficticias (Pauta BI Hito 1).     |
+----------------------------------------------------------------------------------------------------+
```

---

## 4. Matriz de Controles e Interacción (Cross-Filtering)

| Elemento Seleccionado | Efecto en Visual 1 (P1) | Efecto en Visual 2 (P2) | Efecto en Visual 3 (P3) |
| :--- | :--- | :--- | :--- |
| **Clic en una Región (ej. Biobío)** | Filtra el mapa y destaca la barra de Biobío. | Filtra la matriz de ocupación a las sedes de Biobío. | Filtra las instituciones con presencia física en Biobío. |
| **Clic en Tipo IES (ej. CFT)** | Recalcula la tasa territorial solo para oferta técnica. | Muestra la ocupación exclusiva de Centros de Formación Técnica. | Resalta las burbujas de CFTs en la dispersión. |
| **Segmentador de Año (ej. 2022)** | Actualiza población INE a 2022 y compara contra 2018. | Refleja el mínimo histórico post-pandemia (80,2%). | Muestra la distribución de acreditación del corte 2022. |

---

## 5. Validación de Accesibilidad y Directrices de Entrega
- **Contraste de Color:** La relación de contraste texto-fondo cumple con la norma WCAG AA ($\geq 4.5:1$).
- **Lectura Intuitiva:** Se evita el uso de abreviaciones técnicas no estándar; los nombres de regiones e instituciones corresponden a los campos estandarizados generados por la Persona 1 y Persona 2.
- **Rendimiento:** Las medidas DAX han sido optimizadas para evaluar en milisegundos sin loops iterativos innecesarios (`SUMX` solo en promedios ponderados).
