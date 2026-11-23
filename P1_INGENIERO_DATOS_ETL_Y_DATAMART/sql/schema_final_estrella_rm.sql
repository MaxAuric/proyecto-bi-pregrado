-- ============================================================================
-- PROYECTO FINAL BUSINESS INTELLIGENCE - ENTREGA FINAL (18 NOVIEMBRE 2026)
-- MODELO DIMENSIONAL ESTRELLA ENRIQUECIDO CON TASAS, KPIS Y FUENTES EXTERNAS
-- ENFOQUE: REGION METROPOLITANA DE SANTIAGO (RM)
-- AUTOR: Persona 1 (Ingeniero de Datos / ETL y DataMart)
-- CUMPLIMIENTO: Pauta Oficial + Clase 3 (Arq. BI), Clase 4 (DW), Clase 5 (ETL)
-- ============================================================================

-- 1. DIMENSION TIEMPO Y DEMOGRAFIA RM (Integra Fuente Externa 1: INE Proyecciones RM)
CREATE TABLE IF NOT EXISTS dim_tiempo_ine_rm (
    id_tiempo INTEGER PRIMARY KEY,                       -- Clave primaria temporal (2012 a 2026)
    ano INTEGER NOT NULL,
    periodo_admision VARCHAR(30) NOT NULL,               -- 'PSU (2012-2020)', 'PDT (2021-2022)', 'PAES (2023-2026)'
    rango_quinquenio VARCHAR(20) NOT NULL,               -- '2012-2016', '2017-2021', '2022-2026'
    estado_sanitario VARCHAR(25) NOT NULL,               -- 'Pre-Pandemia', 'Pandemia COVID-19', 'Post-Pandemia'
    es_paes INTEGER NOT NULL,
    -- Variables Demográficas Oficiales INE (Región Metropolitana de Santiago)
    poblacion_total_rm INTEGER NOT NULL,
    poblacion_15_64_rm INTEGER NOT NULL,
    poblacion_joven_18_24_rm INTEGER NOT NULL,
    -- TASAS Y KPIS MACRO ANUALES EN LA RM (Tributan a Pregunta 3 y Contexto Temporal)
    tasa_crecimiento_joven_rm_yoy_pct REAL,              -- % Variación anual población 18-24 años en RM
    tasa_absorcion_juvenil_rm_pct REAL NOT NULL,         -- (Matrícula 1er Año RM / Pob 18-24 RM) * 100
    tasa_cobertura_bruta_rm_pct REAL NOT NULL,           -- (Matrícula Total RM / Pob 18-24 RM) * 100
    tasa_oferta_vacantes_1000_jovenes_rm REAL NOT NULL,  -- (Vacantes RM / Pob 18-24 RM) * 1000
    tasa_ocupacion_anual_rm_pct REAL NOT NULL,           -- (Matrícula 1er Año RM / Vacantes RM) * 100
    tasa_crecimiento_matricula_rm_yoy_pct REAL,          -- % Variación anual Matrícula 1er Año en RM
    media_anual_paes_rm REAL                             -- Promedio anual homologado PAES en la RM
);

-- 2. DIMENSION SEDE Y GEOGRAFIA (Jerarquía completa en 1 tabla según Clase 4 DW Pág. 62)
CREATE TABLE IF NOT EXISTS dim_sede_geografia (
    id_sede_geografia INTEGER PRIMARY KEY,               -- Surrogate Key (SK)
    nombre_sede VARCHAR(120) NOT NULL,
    region_codigo_subdere VARCHAR(2) NOT NULL,           -- '13' para Región Metropolitana de Santiago
    region_numero_romano VARCHAR(5) NOT NULL,
    region_nombre_estandar VARCHAR(100) NOT NULL,
    macro_zona VARCHAR(40) NOT NULL,
    es_region_metropolitana INTEGER NOT NULL,            -- 1 = Región Metropolitana de Santiago
    estado_territorial VARCHAR(50) NOT NULL,             -- Descripción completa sin abreviaturas
    -- TASAS Y KPIS DE SEDE (Tributan a Pregunta 1: Capacidad e Infraestructura por Sede)
    tasa_ocupacion_historica_sede_pct REAL,              -- (Suma Matrícula 1er Año Sede / Suma Vacantes Sede) * 100
    tasa_sobredemanda_sede_pct REAL,                     -- % de ofertas en la sede con Matrícula > Vacantes
    participacion_matricula_rm_sede_pct REAL,            -- % de peso de la sede sobre la matrícula total de la RM
    nivel_saturacion_sede VARCHAR(45) NOT NULL           -- Clasificación de presión de capacidad en la sede
);

-- 3. DIMENSION INSTITUCION Y CALIDAD SIES (SCD Tipo 2 + Fuente Externa 2: SIES Acreditación)
-- Cero abreviaturas y cero prefijos '(a)/(b)' según Clase 4 DW Pág. 62
CREATE TABLE IF NOT EXISTS dim_institucion_sies (
    id_institucion_sk INTEGER PRIMARY KEY,               -- Surrogate Key (SK) para SCD Tipo 2
    codigo_ies_sies INTEGER,                             -- Código oficial MINEDUC/SIES (Fuente Externa 2)
    nombre_institucion VARCHAR(150) NOT NULL,
    tipo_institucion VARCHAR(60) NOT NULL,               -- 'Universidad', 'Instituto Profesional', 'Centro de Formación Técnica', 'Institución de las Fuerzas Armadas y de Orden'
    subtipo_institucion VARCHAR(100) NOT NULL,           -- Sin prefijos '(a)' ni abreviaturas 'Univ.'/'F.F.A.A.'
    acreditacion_cned VARCHAR(50) NOT NULL,              -- 'Institución Acreditada' / 'Institución No Acreditada'
    anos_acreditacion_sies REAL,                         -- Años de acreditación CNA/SIES (0 a 7 años)
    score_calidad_sies_pct REAL NOT NULL,                -- (anos_acreditacion_sies / 7.0) * 100
    tramo_acreditacion_sies VARCHAR(45) NOT NULL,        -- '1. Excelencia (6 a 7 años)', '2. Avanzada (4 a 5 años)', '3. Básica (1 a 3 años)', '4. No Acreditada (0 años)'
    autonomia VARCHAR(50) NOT NULL,                      -- Sin prefijos '(a)'..'(e)'
    gratuidad VARCHAR(50) NOT NULL,                      -- 'Adscrita a Gratuidad', 'No Adscrita a Gratuidad', 'No Aplica (Pre-Ley de Gratuidad 2016)'
    ano_vigencia INTEGER NOT NULL,                       -- Año de la fotografía histórica (SCD Tipo 2)
    en_region_metropolitana INTEGER NOT NULL,            -- 1 si tuvo oferta activa en la RM ese año
    -- TASAS Y KPIS INSTITUCIONALES ANUALES (Tributan a Preguntas 1, 2 y 3)
    tasa_ocupacion_inst_anual_pct REAL,                  -- (Matrícula 1er Año Inst / Vacantes Inst) * 100 en ese año
    tasa_programas_sobredemanda_inst_pct REAL,           -- % de carreras de la institución con sobrecupo (>100%) ese año
    cuota_mercado_matricula_rm_pct REAL,                 -- % Market Share de la institución en la RM ese año
    tasa_permanencia_cohortes_sup_pct REAL,              -- ((Matrícula Total - Matrícula 1er Año) / Matrícula Total) * 100
    puntaje_paes_ponderado_inst REAL,                    -- Puntaje PAES promedio ponderado por matrícula 1er año de la institución
    posicionamiento_competitivo_rm VARCHAR(60) NOT NULL  -- Segmentación estratégica (Calidad SIES x Ocupación Vacantes)
);

-- 4. DIMENSION CARRERA Y PROGRAMA ACADEMICO (Jerarquía académica completa + tasas de presión)
CREATE TABLE IF NOT EXISTS dim_carrera_programa (
    id_carrera_programa_sk INTEGER PRIMARY KEY,          -- Surrogate Key (SK)
    nombre_programa VARCHAR(220) NOT NULL,
    carrera_generica VARCHAR(150) NOT NULL,
    area_conocimiento VARCHAR(100) NOT NULL,             -- Sin abreviaturas ('Fuerzas Armadas, Orden y Seguridad')
    es_area_stem VARCHAR(35) NOT NULL,                   -- 'STEM (Tecnología y Ciencias)' vs 'Otras Áreas del Conocimiento'
    tipo_carrera VARCHAR(80) NOT NULL,
    tipo_programa VARCHAR(60) NOT NULL,
    horario VARCHAR(35) NOT NULL,                        -- 'Diurno', 'Vespertino', 'A Distancia / Otro Horario'
    titulo VARCHAR(220) NOT NULL,
    grado_academico VARCHAR(180) NOT NULL,               -- Sin abreviatura 'M/' -> 'con Mención en'
    duracion_semestres INTEGER,
    duracion_anos REAL,                                  -- Duración en años (semestres / 2)
    ingreso_directo VARCHAR(40) NOT NULL,                -- 'Ingreso Directo (Sin Prueba)' vs 'Admisión Regular con Prueba'
    -- TASAS Y KPIS HISTORICOS DEL PROGRAMA (Tributan a Pregunta 1 y 2)
    tasa_ocupacion_historica_prog_pct REAL,              -- Ocupación acumulada histórica del programa
    tasa_frecuencia_sobredemanda_prog_pct REAL,          -- % de años en que el programa tuvo Matrícula > Vacantes
    tasa_presion_lab_base35_prog_pct REAL,               -- (Matrícula 1er Año Promedio / 35) * 100
    promedio_historico_paes_prog REAL,                   -- Puntaje PAES promedio histórico del programa
    clasificacion_presion_capacidad VARCHAR(45) NOT NULL -- '1. Sobredemanda Crítica (>100%)', '2. Capacidad Óptima (80-100%)', '3. Subutilización (<80%)', '4. Admisión Abierta'
);

-- 5. TABLA DE HECHOS PRINCIPAL: FACT MATRICULA Y ADMISION
-- REGLA CLASE 4 DW (Pág. 62): Cero columnas de texto VARCHAR en la tabla de hechos.
-- Solo claves foráneas (INTEGER), flags binarios/numéricos (INTEGER) y medidas/tasas numéricas (INTEGER/REAL).
-- Grano: Una fila por oferta de programa académico, en una sede y horario específico, en un año cronológico.
CREATE TABLE IF NOT EXISTS fact_matricula_admision (
    id_fact INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Claves Foráneas del Esquema Estrella
    id_tiempo INTEGER NOT NULL,
    id_sede_geografia INTEGER NOT NULL,
    id_institucion_sk INTEGER NOT NULL,
    id_carrera_programa_sk INTEGER NOT NULL,
    
    -- Flags Numéricos de Gobernabilidad y Filtrado Rápido (Cero VARCHAR en tabla de hechos)
    es_region_metropolitana INTEGER NOT NULL,            -- 1 = Región Metropolitana de Santiago (58.926 filas)
    flag_exige_prueba_admision INTEGER NOT NULL,         -- 1 = Reporta puntaje PAES/PSU válido
    flag_vacantes_declaradas INTEGER NOT NULL,           -- 1 = Declara vacantes > 0
    flag_sobredemanda_critica INTEGER NOT NULL,          -- 1 = Matrícula 1er Año > Vacantes (Sobreocupación)
    codigo_estado_ocupacion INTEGER NOT NULL,            -- 1=Sobredemanda (>100%), 2=Óptima (80-100%), 3=Subocupación (<80%), 4=Sin Vacantes Fijas
    
    -- Medidas Aditivas Puras / Distributivas (Clase 4 DW Pág. 29: SUM, COUNT)
    vacantes INTEGER,
    matricula_primer_ano_hombres INTEGER NOT NULL DEFAULT 0,
    matricula_primer_ano_mujeres INTEGER NOT NULL DEFAULT 0,
    matricula_primer_ano_extranjeros INTEGER NOT NULL DEFAULT 0,
    matricula_primer_ano_total INTEGER NOT NULL DEFAULT 0,
    matricula_total_hombres INTEGER NOT NULL DEFAULT 0,
    matricula_total_mujeres INTEGER NOT NULL DEFAULT 0,
    matricula_total_extranjeros INTEGER NOT NULL DEFAULT 0,
    matricula_total INTEGER NOT NULL DEFAULT 0,
    
    -- Medidas de Impacto Físico en Infraestructura (Caso 120 -> 140 alumnos, base 35 puestos/laboratorio)
    sobrecupo_neto_alumnos INTEGER,                      -- Alumnos por encima de las vacantes (0 si no hay sobrecupo)
    vacantes_ociosas_netas INTEGER,                      -- Cupos vacantes no llenados (0 si se llenó)
    secciones_lab_planificadas_35 INTEGER,               -- CEIL(Vacantes / 35)
    secciones_lab_reales_35 INTEGER NOT NULL,            -- CEIL(Matrícula 1er Año / 35)
    secciones_extra_por_sobrecupo INTEGER,               -- Paralelos adicionales forzados por sobredemanda
    tasa_saturacion_lab_35_pct REAL,                     -- (Matrícula 1er Año / (secciones_lab_planificadas_35 * 35)) * 100
    
    -- Medidas No Aditivas / Algebraicas (Clase 4 DW Pág. 29: Puntajes Homologados en 4 Escalas)
    puntaje_promedio_original REAL,
    puntaje_promedio_norm_0_100 REAL,
    puntaje_promedio_equiv_paes REAL,
    puntaje_promedio_zscore_anual REAL,
    puntaje_corte_primer_equiv_paes REAL,
    puntaje_corte_ultimo_equiv_paes REAL,
    
    -- TASAS, BRECHAS Y KPIS DE NIVEL DE OFERTA (Tributan a las 3 Preguntas de la Propuesta de Valor)
    tasa_ocupacion_primer_ano REAL,                      -- (Matrícula 1er Año / Vacantes) * 100
    tasa_sobredemanda_oferta_pct REAL,                   -- MAX(0, ((Matrícula 1er Año - Vacantes) / Vacantes) * 100)
    tasa_renovacion_primer_ano_pct REAL,                 -- (Matrícula 1er Año / Matrícula Total) * 100
    tasa_retencion_aparente_pct REAL,                    -- ((Matrícula Total - Matrícula 1er Año) / Matrícula Total) * 100
    ratio_mujeres_primer_ano REAL,                       -- (Mujeres 1er Año / Total 1er Año) * 100
    ratio_mujeres_total_pct REAL,                        -- (Mujeres Total / Matrícula Total) * 100
    ratio_extranjeros_primer_ano_pct REAL,               -- (Extranjeros 1er Año / Total 1er Año) * 100
    ratio_extranjeros_total REAL,                        -- (Extranjeros Total / Matrícula Total) * 100
    brecha_dispersa_max_min_paes REAL,                   -- Puntaje Máx PAES - Puntaje Mín PAES (Heterogeneidad en aula)
    tasa_heterogeneidad_paes_pct REAL,                   -- (brecha_dispersa_max_min_paes / puntaje_promedio_equiv_paes) * 100
    brecha_corte_vs_media_rm_paes REAL,                  -- Puntaje Corte Último PAES - Media RM del Año (Selectividad relativa)
    indice_presion_selectiva_kpi REAL,                   -- (Tasa Ocupación / 100) * (Puntaje PAES / 600) * 100
    
    FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo_ine_rm(id_tiempo),
    FOREIGN KEY (id_sede_geografia) REFERENCES dim_sede_geografia(id_sede_geografia),
    FOREIGN KEY (id_institucion_sk) REFERENCES dim_institucion_sies(id_institucion_sk),
    FOREIGN KEY (id_carrera_programa_sk) REFERENCES dim_carrera_programa(id_carrera_programa_sk)
);

-- 6. TABLA AGREGADA DE RENDIMIENTO OLAP (Cumple Clase 4 DW Pág. 63 y Clase 5 ETL Slide 10 'Resumen')
CREATE TABLE IF NOT EXISTS agg_resumen_anual_institucion_rm (
    ano INTEGER NOT NULL,
    codigo_ies_sies INTEGER,
    nombre_institucion VARCHAR(150) NOT NULL,
    tipo_institucion VARCHAR(60) NOT NULL,
    tramo_acreditacion_sies VARCHAR(45) NOT NULL,
    gratuidad VARCHAR(50) NOT NULL,
    ofertas_activas_rm INTEGER NOT NULL,
    vacantes_totales_rm INTEGER NOT NULL,
    matricula_primer_ano_rm INTEGER NOT NULL,
    matricula_total_rm INTEGER NOT NULL,
    secciones_lab_planificadas_rm INTEGER NOT NULL,
    secciones_lab_reales_rm INTEGER NOT NULL,
    secciones_extra_sobrecupo_rm INTEGER NOT NULL,
    tasa_ocupacion_rm_pct REAL,
    cuota_mercado_rm_pct REAL,
    puntaje_paes_ponderado_rm REAL,
    PRIMARY KEY (ano, nombre_institucion)
);

-- 7. TABLA PUENTE DE GOBERNANZA FUENTE EXTERNA SIES (Cumple Pauta Oficial Pág. 3)
CREATE TABLE IF NOT EXISTS puente_institucion_sies (
    nombre_institucion_cned VARCHAR(150) PRIMARY KEY,
    codigo_ies_sies INTEGER,
    nombre_institucion_sies VARCHAR(150),
    metodo_cruce VARCHAR(60),
    estado_cruce VARCHAR(60)
);

CREATE INDEX IF NOT EXISTS idx_f_tiempo ON fact_matricula_admision(id_tiempo);
CREATE INDEX IF NOT EXISTS idx_f_sede ON fact_matricula_admision(id_sede_geografia);
CREATE INDEX IF NOT EXISTS idx_f_inst ON fact_matricula_admision(id_institucion_sk);
CREATE INDEX IF NOT EXISTS idx_f_carr ON fact_matricula_admision(id_carrera_programa_sk);
CREATE INDEX IF NOT EXISTS idx_f_rm ON fact_matricula_admision(es_region_metropolitana);
