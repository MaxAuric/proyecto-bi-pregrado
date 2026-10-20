# Informe Técnico de Auditoría de Viabilidad y Graficabilidad en Power BI
## Rol: Persona 4 (Desarrollador BI) - Hito 1
**Proyecto:** Business Intelligence - Análisis Estratégico de Oferta, Capacidad y Calidad en la Educación Superior Chilena (2012–2026)  
**Fecha de Entrega:** 21 de Octubre de 2026  
**Equipo de Trabajo:**
- Persona 1: Ingeniero de Datos (ETL)
- Persona 2: Analista de Negocios y Datos Externos
- Persona 3: Arquitecto de Bases de Datos
- **Persona 4: Desarrollador BI (Autor del Informe)**
- Persona 5: Gestor de Proyecto y Documentador

---

## 1. Resumen Ejecutivo

En el marco del **Hito 1** del proyecto práctico final de Business Intelligence, el documento oficial de planificación (*Planificación y Asignación de Roles*, 10 de octubre de 2026) estipula como responsabilidad exclusiva de la **Persona 4 (Desarrollador BI)**:

> **«Revisa la Propuesta de Valor para asegurar que las 3 preguntas de negocio propuestas puedan ser graficadas a futuro en el panel».**

El presente informe documenta la auditoría exhaustiva llevada a cabo sobre la base consolidada 2012–2026 (158.211 registros, preparada por Persona 1) y las fuentes externas normalizadas por Persona 2 (INE Proyecciones de Población y SIES Catálogo de Acreditación Institucional), certificando una **factibilidad técnica del 100%** para la construcción del Dashboard en Power BI Desktop.

### Cuadro Resumen de la Auditoría

| Pregunta de Negocio | Indicador Clave | Fuentes de Datos Requeridas | Factibilidad Visual | Regla Analítica / DAX Crítica |
| :--- | :--- | :--- | :---: | :--- |
| **P1: Equidad Territorial** | Matrícula 1er año por 1.000 hab. (15 a 64 años) | CNED Pregrado + INE Proyecciones Población | **100% Viable** (Shape Map + Barras Ordenadas) | Población regional es **semi-aditiva**. Se bloquea suma multianual mediante `LASTNONBLANK`. |
| **P2: Uso de Capacidad** | Tasa de Ocupación = Matrícula 1er año / Vacantes | CNED Pregrado (Vacantes declaradas) | **100% Viable** (Serie temporal + Heatmap IES $\times$ Región) | Exclusión estricta de vacantes nulas vía `flag_vacantes_declaradas = 1` y uso de `DIVIDE`. |
| **P3: Calidad Institucional** | % Matrícula en IES Acreditadas y Años Ponderados | CNED Pregrado + SIES Listados Vigentes | **100% Viable** (Barras 100% apiladas + Dispersión) | Filtro predeterminado a nivel de página en $A\tilde{n}o \geq 2018$ por cobertura SIES. |

---

## 2. Auditoría Técnica de Graficabilidad por Pregunta de Negocio

### 2.1. Pregunta 1: Equidad Territorial y Capacidad Regional
* **Pregunta:** *«¿En qué regiones la oferta de ingreso es baja respecto de su población, y cómo ha cambiado desde 2018?»*
* **Granularidad requerida:** Región geográfica $\times$ Año.
* **Cruce con INE:** Cruce 100% exitoso mediante el código oficial SUBDERE (`region_codigo_subdere`) presente en ambas fuentes para las 16 regiones del país.
* **Objetos Visuales en Power BI:**
  1. **Mapa Coroplético Regional:** Empleo del objeto nativo *Shape Map* con mapa TopoJSON de Chile o Azure Maps, coloreado según la tasa por 1.000 habitantes.
  2. **Gráfico de Barras Horizontales Ordenadas:** Ranking descendente de regiones para el año seleccionado, con doble barra (2018 vs. 2026) y línea de referencia con el promedio nacional (27,6 ‰).
* **Hallazgos con datos reales:**
  - En 2026, la Región Metropolitana (35,5 ‰) y Biobío (32,5 ‰) presentan la mayor capacidad instalada relativa.
  - Las regiones con mayor déficit de oferta son O'Higgins (14,1 ‰), Aysén (15,2 ‰) y Atacama (17,2 ‰).
  - La brecha entre la región líder y la más rezagada es de $2,52\times$.
* **Medida DAX Principal:**
```dax
Matricula_Por_1000_Hab = 
DIVIDE(
    [Matricula_Primer_Ano_Total] * 1000,
    [Poblacion_15_64_INE],
    BLANK()
)
```

---

### 2.2. Pregunta 2: Uso de la Capacidad y Ocupación de Vacantes
* **Pregunta:** *«¿Cuánto de la oferta de vacantes se ocupa realmente y en qué tipos de institución y región se concentra la sobre u subocupación?»*
* **Granularidad requerida:** Tipo de Institución $\times$ Región $\times$ Año.
* **Tratamiento del Quiebre de Vacantes Nulas:**
  - En la base histórica, el 25,6% de los registros no declara vacantes.
  - Para evitar dividir por cero o distorsionar la capacidad del sistema, se utiliza de forma estricta el filtro lógico `flag_vacantes_declaradas = 1` y `vacantes > 0`.
* **Objetos Visuales en Power BI:**
  1. **Serie Temporal Continua (2012–2026):** Gráfico de líneas con zonas de control sombreadas (Subocupación crítica $<75\%$, equilibrio $75\%$--$95\%$, sobredemanda $>100\%$).
  2. **Matriz Heatmap (Tipo IES $\times$ Región):** Tabla dinámica con escala de color condicional automática que resalta focos de capacidad ociosa o saturación.
* **Hallazgos con datos reales:**
  - La ocupación nacional fluctúa entre un mínimo histórico de 80,2% (2022) y un máximo de 91,1% (2014), situándose en **84,4%** en 2026.
  - En 2026, las Universidades lideran en ocupación con 86,2%, seguidas por los Institutos Profesionales (83,1%) y Centros de Formación Técnica (81,9%).
* **Medida DAX Principal:**
```dax
Tasa_Ocupacion_Vacantes = 
DIVIDE(
    CALCULATE(SUM(fact_matricula_oferta[matricula_primer_ano_total]), fact_matricula_oferta[flag_vacantes_declaradas] = 1, fact_matricula_oferta[vacantes] > 0),
    CALCULATE(SUM(fact_matricula_oferta[vacantes]), fact_matricula_oferta[flag_vacantes_declaradas] = 1, fact_matricula_oferta[vacantes] > 0),
    BLANK()
)
```

---

### 2.3. Pregunta 3: Calidad Institucional y Acreditación (SIES)
* **Pregunta:** *«¿Qué proporción de la matrícula de primer año se concentra en instituciones acreditadas, y cómo se relaciona con los años de acreditación?»*
* **Granularidad requerida:** Institución $\times$ Nivel de Acreditación $\times$ Año.
* **Cruce Institucional:** Tasa de coincidencia del 98,39% de los registros y 99,00% de la matrícula mediante el puente homologado (`puente_institucion.csv`).
* **Objetos Visuales en Power BI:**
  1. **Barras 100% Apiladas (100% Stacked Bar Chart):** Evolución 2018–2026 de la proporción de matrícula por estado SIES (Acreditada, Extensión, Tutela, No Acreditada).
  2. **Gráfico de Dispersión (Scatter Plot):**
     - Eje X: Años de acreditación (0 a 7 años).
     - Eje Y: Matrícula de 1er año.
     - Tamaño de burbuja: Matrícula total institucional.
     - Color: Tipo de institución.
* **Hallazgos con datos reales:**
  - La proporción de matrícula en instituciones no acreditadas se redujo drásticamente de 9,52% en 2018 a solo **0,16%** en 2026.
  - En 2026, el 81,0% de la matrícula está en instituciones con acreditación regular, 6,9% con acreditación extendida y 2,4% bajo tutela.
* **Medida DAX Principal:**
```dax
Pct_Matricula_Acreditada = 
DIVIDE(
    CALCULATE([Matricula_Primer_Ano_Total], dim_institucion_calidad_anual[acreditacion_sies] IN {"Acreditada", "Acreditación extendida"}),
    [Matricula_Primer_Ano_Total],
    BLANK()
)
```

---

## 3. Arquitectura del Panel y UX/UI (Power BI Desktop)

El Dashboard está estructurado en 4 páginas de alta densidad ejecutiva:
1. **Página 1 - Resumen Ejecutivo:** Tarjetas KPI globales, evolución histórica agregada y filtros principales.
2. **Página 2 - Equidad Territorial (P1):** Mapa coroplético regional, gráfico de barras ordenadas y tabla de variación 2018–2026.
3. **Página 3 - Uso de Capacidad (P2):** Evolución histórica de ocupación, matriz heatmap cruzada institucional $\times$ territorial y distribución de vacantes.
4. **Página 4 - Calidad y Competencia (P3):** Barras 100% apiladas por año y gráfico de burbujas de calidad vs. matrícula.

### Jerarquías de Drill-Down Validadas:
- **Geográfica:** `Macro-Zona` $\rightarrow$ `Región` $\rightarrow$ `Sede`.
- **Institucional:** `Tipo Institución` $\rightarrow$ `Clasificación` $\rightarrow$ `Institución`.
- **Curricular:** `Área Conocimiento` $\rightarrow$ `Carrera Genérica` $\rightarrow$ `Programa` $\rightarrow$ `Horario`.

---

## 4. Scripts y Reproducibilidad Computacional

En la carpeta `inteligencia/P4_Hito1/scripts/` se crearon dos herramientas de validación:
1. `08_validar_viabilidad_visual_p4.py`: Procesa la base consolidada y las fuentes externas, verifica la completitud de las llaves, calcula los KPIs exactos y genera los archivos de auditoría en `data_validation/`.
2. `09_generar_visualizaciones_prototipo.py`: Renderiza los prototipos gráficos de alta resolución que demuestran la viabilidad de representación de cada gráfico antes de la fase de construcción en Power BI.

---

## 5. Próximos Pasos para Persona 4 en el Hito 2 y Final

1. **Hito 2 (4 de Noviembre):**
   - Configurar y probar la conexión de Power BI al DataMart SQLite / archivos CSV provistos por Persona 3.
   - Definir formalmente las relaciones $1 \rightarrow *$ con dirección de filtro unidireccional en la Vista de Modelo.
   - Implementar las jerarquías de navegación en el modelo semántico.
2. **Entrega Final (18 de Noviembre):**
   - Desarrollar el archivo interactivo `.pbix` con diseño visual final, tooltips avanzados y marcadores de navegación (bookmarks).
   - Ensayo de la defensa individual sobre consultas DAX y diseño del panel.
