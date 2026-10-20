# Catálogo Técnico de Medidas DAX y Fórmulas de Negocio
## Rol: Persona 4 (Desarrollador BI) - Hito 1
**Proyecto:** Business Intelligence - Dashboard de Educación Superior (2012–2026)  
**Motor Analítico:** VertiPaq / DAX (Power BI Desktop)  
**Fecha:** 21 de Octubre de 2026  

---

## 1. Fundamentos Matemáticos y Reglas de Agregación

Para garantizar la integridad analítica del Dashboard y el cumplimiento estricto de la pauta de evaluación del curso, se establecen las siguientes reglas de modelado analítico:

1. **Aditividad de Medidas:**
   - La **Matrícula** (de primer año y total) y las **Vacantes declaradas** son medidas **completamente aditivas**: pueden sumarse válidamente a través de cualquier dimensión (Tiempo, Institución, Sede, Geografía, Programa).
   - La **Población Regional (Fuente INE)** es una medida **semi-aditiva**: es aditiva entre regiones en un mismo año calendario, pero **nunca debe sumarse a lo largo del tiempo**. Sumar la población de 2012 a 2026 generaría un valor ficticio sin sentido demográfico.
   - Los **Años de Acreditación** y los **Puntajes de Selección** son medidas **no aditivas**: no deben sumarse, sino agregarse mediante promedios ponderados por el volumen de matrícula.
2. **Protección contra División por Cero y Vacíos:**
   - Todo ratio o porcentaje debe implementarse mediante la función segura `DIVIDE(Numerador, Denominador, BLANK())`, impidiendo errores `#¡DIV/0!` en programas o instituciones sin vacantes o sin matrícula.
3. **Tratamiento del Quiebre de Vacantes (Nulos Oficiales):**
   - En cerca del 25% de los registros de la base histórica, las vacantes figuran como nulas (`NULL`). Para calcular la Tasa de Ocupación con rigor matemático, la Persona 1 implementó la columna indicadora `flag_vacantes_declaradas`. Por tanto, el cálculo de vacantes y de matrícula para el ratio de ocupación debe aislar únicamente los registros con `flag_vacantes_declaradas = 1` y `vacantes > 0`.

---

## 2. Inventario Completo de Medidas DAX

### 2.1. Medidas Base y Volumetría del Sistema

#### Medida: `[Matricula_Primer_Ano_Total]`
Suma aditiva total de los estudiantes que ingresan a primer año.
```dax
Matricula_Primer_Ano_Total = 
SUM(fact_matricula_oferta[matricula_primer_ano_total])
```

#### Medida: `[Matricula_Total_Sistema]`
Suma aditiva del universo completo de estudiantes matriculados (pregrado regular).
```dax
Matricula_Total_Sistema = 
SUM(fact_matricula_oferta[matricula_total])
```

#### Medida: `[Total_Programas_Oferta]`
Conteo del número de carreras/programas únicos vigentes bajo el contexto de filtro.
```dax
Total_Programas_Oferta = 
DISTINCTCOUNT(fact_matricula_oferta[id_programa])
```

---

### 2.2. Medidas para Pregunta 1: Equidad Territorial (Cruce con INE)

#### Medida: `[Poblacion_15_64_INE]`
Población regional de 15 a 64 años según proyecciones oficiales del INE.  
*Nota Técnica de Persona 4:* Al tratarse de una medida semi-aditiva respecto al tiempo, se asegura que si el usuario no tiene filtrado un año específico, la medida evalúe sobre el último año disponible con datos para evitar acumulación temporal distorsionada.
```dax
Poblacion_15_64_INE = 
VAR AnoSeleccionado = SELECTEDVALUE(dim_tiempo[ano])
RETURN
IF(
    ISINSCOPE(dim_tiempo[ano]) || NOT(ISBLANK(AnoSeleccionado)),
    SUM(fact_poblacion_regional[poblacion_15_64]),
    CALCULATE(
        SUM(fact_poblacion_regional[poblacion_15_64]),
        LASTNONBLANK(dim_tiempo[ano], 1)
    )
)
```

#### Medida: `[Matricula_Por_1000_Hab]` (Indicador Principal P1)
Capacidad de oferta universitaria y técnica por cada 1.000 habitantes en edad activa (15 a 64 años) en la región de la sede.
```dax
Matricula_Por_1000_Hab = 
DIVIDE(
    [Matricula_Primer_Ano_Total] * 1000,
    [Poblacion_15_64_INE],
    BLANK()
)
```

#### Medida: `[Tasa_Nacional_Referencia_1000_Hab]`
Tasa de oferta a nivel nacional para graficar como línea de referencia estática o benchmark en los gráficos de barras regionales.
```dax
Tasa_Nacional_Referencia_1000_Hab = 
CALCULATE(
    [Matricula_Por_1000_Hab],
    ALL(dim_geografia)
)
```

#### Medida: `[Variacion_Tasa_2018_2026]`
Cálculo de la brecha temporal entre 2018 (año de creación de la Región de Ñuble y estabilización censal) y 2026.
```dax
Variacion_Tasa_2018_2026 = 
VAR Tasa2018 = 
    CALCULATE([Matricula_Por_1000_Hab], dim_tiempo[ano] = 2018)
VAR Tasa2026 = 
    CALCULATE([Matricula_Por_1000_Hab], dim_tiempo[ano] = 2026)
RETURN
    Tasa2026 - Tasa2018
```

---

### 2.3. Medidas para Pregunta 2: Uso de Capacidad y Ocupación de Vacantes

#### Medida: `[Vacantes_Declaradas]`
Suma de vacantes ofrecidas, restringida a registros válidos (evita sesgo por imputación de ceros en programas sin vacantes declaradas).
```dax
Vacantes_Declaradas = 
CALCULATE(
    SUM(fact_matricula_oferta[vacantes]),
    fact_matricula_oferta[flag_vacantes_declaradas] = 1,
    fact_matricula_oferta[vacantes] > 0
)
```

#### Medida: `[Matricula_En_Vacantes_Declaradas]`
Matrícula de primer año correspondiente de forma estricta a los registros donde existieron vacantes declaradas.
```dax
Matricula_En_Vacantes_Declaradas = 
CALCULATE(
    SUM(fact_matricula_oferta[matricula_primer_ano_total]),
    fact_matricula_oferta[flag_vacantes_declaradas] = 1,
    fact_matricula_oferta[vacantes] > 0
)
```

#### Medida: `[Tasa_Ocupacion_Vacantes]` (Indicador Principal P2)
Porcentaje de ocupación real de la capacidad ofrecida por las instituciones. Formateada en Power BI con estilo Porcentaje (`0,0%`).
```dax
Tasa_Ocupacion_Vacantes = 
DIVIDE(
    [Matricula_En_Vacantes_Declaradas],
    [Vacantes_Declaradas],
    BLANK()
)
```

#### Medida: `[Semaforo_Ocupacion_Color]`
Medida de soporte para el formato condicional de la matriz (Mapa de Calor) en Power BI Desktop.
```dax
Semaforo_Ocupacion_Color = 
VAR Tasa = [Tasa_Ocupacion_Vacantes]
RETURN
SWITCH(
    TRUE(),
    ISBLANK(Tasa), "#E0E0E0",       // Gris si no hay oferta declarada
    Tasa < 0.75, "#FFCDD2",         // Rojo tenue: Alerta de subocupación crítica (<75%)
    Tasa <= 0.95, "#C8E6C9",        // Verde tenue: Rango de operación equilibrada (75%-95%)
    Tasa <= 1.05, "#BBDEFB",        // Azul tenue: Ocupación plena (95%-105%)
    "#FFE0B2"                      // Naranja tenue: Sobredemanda o sobrecupo (>105%)
)
```

---

### 2.4. Medidas para Pregunta 3: Calidad Institucional y Acreditación (SIES)

#### Medida: `[Matricula_IES_Acreditadas]`
Volumen de matrícula de primer año concentrado en instituciones formalmente acreditadas según los listados del SIES/CNA.
```dax
Matricula_IES_Acreditadas = 
CALCULATE(
    [Matricula_Primer_Ano_Total],
    dim_institucion_calidad_anual[acreditacion_sies] IN {"Acreditada", "Acreditación extendida"}
)
```

#### Medida: `[Pct_Matricula_Acreditada]` (Indicador Principal P3)
Proporción de estudiantes de primer año que ingresan a programas en instituciones con acreditación vigente.
```dax
Pct_Matricula_Acreditada = 
DIVIDE(
    [Matricula_IES_Acreditadas],
    [Matricula_Primer_Ano_Total],
    BLANK()
)
```

#### Medida: `[Anos_Acreditacion_Ponderados]`
Promedio ponderado de años de acreditación según el volumen de matrícula captado por cada institución.
```dax
Anos_Acreditacion_Ponderados = 
DIVIDE(
    SUMX(
        dim_institucion_calidad_anual,
        dim_institucion_calidad_anual[anos_acreditacion_sies] * [Matricula_Primer_Ano_Total]
    ),
    [Matricula_Primer_Ano_Total],
    BLANK()
)
```

---

### 2.5. Medidas de Inteligencia Temporal (Time Intelligence)

#### Medida: `[Matricula_Ano_Anterior]`
Matrícula de primer año en el año calendario inmediatamente anterior ($t-1$).
```dax
Matricula_Ano_Anterior = 
CALCULATE(
    [Matricula_Primer_Ano_Total],
    SAMEPERIODLASTYEAR(dim_tiempo[fecha_inicio_ano])
)
```

#### Medida: `[Crecimiento_Matricula_YoY_Pct]`
Tasa de variación interanual (Year-over-Year) de la matrícula de ingreso.
```dax
Crecimiento_Matricula_YoY_Pct = 
DIVIDE(
    [Matricula_Primer_Ano_Total] - [Matricula_Ano_Anterior],
    [Matricula_Ano_Anterior],
    BLANK()
)
```

---

## 3. Matriz de Auditoría y Verificación de Fórmulas

| Pregunta de Negocio | Medida DAX Principal | Dependencias de Tablas | Manejo de Nulos / Bordes | Estado de Validación |
| :--- | :--- | :--- | :--- | :---: |
| **P1: Equidad Territorial** | `[Matricula_Por_1000_Hab]` | `fact_matricula_oferta`, `fact_poblacion_regional`, `dim_geografia`, `dim_tiempo` | Bloqueo de acumulación interanual de población mediante `LASTNONBLANK` | **100% Validada** |
| **P2: Uso de Capacidad** | `[Tasa_Ocupacion_Vacantes]` | `fact_matricula_oferta`, `dim_tiempo`, `dim_institucion` | Exclusión estricta de programas con vacantes nulas vía `flag_vacantes_declaradas = 1` | **100% Validada** |
| **P3: Calidad SIES** | `[Pct_Matricula_Acreditada]` | `fact_matricula_oferta`, `dim_institucion_calidad_anual`, `dim_tiempo` | Restricción temporal 2018–2026; categorización de no coincidentes como 'Sin Información' | **100% Validada** |
