-- ============================================================================
-- PROYECTO FINAL BUSINESS INTELLIGENCE - ENTREGA FINAL (18 NOVIEMBRE 2026)
-- MODELO DIMENSIONAL ESTRELLA ENRIQUECIDO CON TASAS, KPIS Y FUENTES EXTERNAS
-- ENFOQUE: REGION METROPOLITANA DE SANTIAGO (RM)
-- AUTOR: Persona 1 (Ingeniero de Datos / ETL y DataMart)
-- ============================================================================

-- 1. DIMENSION TIEMPO Y DEMOGRAFIA RM (Integra Fuente Externa 1: INE Proyecciones RM)
CREATE TABLE IF NOT EXISTS dim_tiempo_ine_rm (
    id_tiempo INTEGER PRIMARY KEY,                       -- Año cronológico (2012 a 2026)
    ano INTEGER NOT NULL,
    periodo_admision VARCHAR(20) NOT NULL,               -- 'PSU (2012-2020)', 'PDT (2021-2022)', 'PAES (2023-2026)'
    rango_quinquenio VARCHAR(20) NOT NULL,               -- '2012-2016', '2017-2021', '2022-2026'
    estado_sanitario VARCHAR(25) NOT NULL,               -- 'Pre-Pandemia', 'Pandemia COVID-19', 'Post-Pandemia'
    es_paes INTEGER NOT NULL,
    -- Variables Demográficas Oficiales INE (Región Metropolitana)
    poblacion_total_rm INTEGER NOT NULL,
    poblacion_15_64_rm INTEGER NOT NULL,
    poblacion_joven_18_24_rm INTEGER NOT NULL,
    -- TASAS Y KPIS MACRO ANUALES EN LA RM (Tributan a Pregunta 3 y Contexto Temporal)
    tasa_crecimiento_joven_rm_yoy_pct REAL,              -- % Variación anual población 18-24 años en RM
    tasa_absorcion_juvenil_rm_pct REAL NOT NULL,         -- (Matrícula 1er Año RM / Pob 18-24 RM) * 100
    tasa_oferta_vacantes_1000_jovenes_rm REAL NOT NULL,  -- (Vacantes RM / Pob 18-24 RM) * 1000
    tasa_ocupacion_anual_rm_pct REAL NOT NULL,           -- (Matrícula 1er Año RM / Vacantes RM) * 100
    tasa_crecimiento_matricula_rm_yoy_pct REAL,          -- % Variación anual Matrícula 1er Año en RM
    media_anual_paes_rm REAL                             -- Promedio anual homologado PAES en la RM
);

-- 2. DIMENSION SEDE Y GEOGRAFIA (Sin abreviaciones, enriquecida con tasas de sede)
CREATE TABLE IF NOT EXISTS dim_sede_geografia (
    id_sede_geografia INTEGER PRIMARY KEY,
    nombre_sede VARCHAR(120) NOT NULL,
    region_codigo_subdere VARCHAR(2) NOT NULL,           -- '13' para Región Metropolitana
    region_numero_romano VARCHAR(5) NOT NULL,
    region_nombre_estandar VARCHAR(100) NOT NULL,
    macro_zona VARCHAR(30) NOT NULL,
    es_region_metropolitana INTEGER NOT NULL,            -- 1 = Región Metropolitana de Santiago
    estado_territorial VARCHAR(40) NOT NULL,             -- 'Región Metropolitana (Foco Estudio)' vs 'Otras Regiones'
    -- TASAS Y KPIS DE SEDE (Tributan a Pregunta 1: Capacidad por Sede)
    tasa_ocupacion_historica_sede_pct REAL,              -- (Suma Matrícula 1er Año Sede / Suma Vacantes Sede) * 100
    tasa_sobredemanda_sede_pct REAL,                     -- % de ofertas en la sede con Matrícula > Vacantes
    participacion_matricula_rm_sede_pct REAL             -- % de peso de la sede sobre la matrícula total de la RM
);

-- 3. DIMENSION INSTITUCION Y CALIDAD SIES (SCD Tipo 2 + Fuente Externa 2: SIES Acreditación)
CREATE TABLE IF NOT EXISTS dim_institucion_sies (
    id_institucion_sk INTEGER PRIMARY KEY,
    codigo_ies_sies INTEGER,                             -- Código oficial MINEDUC/SIES (Fuente Externa 2)
    nombre_institucion VARCHAR(150) NOT NULL,
    tipo_institucion VARCHAR(60) NOT NULL,               -- Expandido: 'Universidad', 'Instituto Profesional', 'Centro de Formación Técnica'
    subtipo_institucion VARCHAR(100) NOT NULL,           -- Clasificación limpia (CRUCH, Privada, etc.)
    acreditacion_cned VARCHAR(50) NOT NULL,              -- Estado de acreditación en el año (SCD Tipo 2)
    anos_acreditacion_sies REAL,                         -- Años de acreditación CNA/SIES (0 a 7 años)
    tramo_acreditacion_sies VARCHAR(40) NOT NULL,        -- 'Excelencia (6-7 años)', 'Avanzada (4-5 años)', 'Básica (1-3 años)', 'No Acreditada'
    autonomia VARCHAR(50) NOT NULL,
    gratuidad VARCHAR(50) NOT NULL,                      -- Estado de Gratuidad en el año (SCD Tipo 2)
    ano_vigencia INTEGER NOT NULL,                       -- Año de la fotografía histórica (SCD Tipo 2)
    en_region_metropolitana INTEGER NOT NULL,            -- 1 si tuvo oferta activa en la RM ese año
    -- TASAS Y KPIS INSTITUCIONALES ANUALES (Tributan a Preguntas 1, 2 y 3)
    tasa_ocupacion_inst_anual_pct REAL,                  -- (Matrícula 1er Año Inst / Vacantes Inst) * 100 en ese año
    tasa_programas_sobredemanda_inst_pct REAL,           -- % de carreras de la institución con sobrecupo (>100%) ese año
    cuota_mercado_matricula_rm_pct REAL,                 -- % Market Share de la institución en la RM ese año
    tasa_permanencia_cohortes_sup_pct REAL,              -- ((Matrícula Total - Matrícula 1er Año) / Matrícula Total) * 100
    puntaje_paes_ponderado_inst REAL                     -- Puntaje PAES promedio ponderado por matrícula 1er año de la institución
);

-- 4. DIMENSION CARRERA Y PROGRAMA ACADEMICO (Enriquecida con tasas de presión académica)
CREATE TABLE IF NOT EXISTS dim_carrera_programa (
    id_carrera_programa_sk INTEGER PRIMARY KEY,
    nombre_programa VARCHAR(220) NOT NULL,
    carrera_generica VARCHAR(150) NOT NULL,
    area_conocimiento VARCHAR(100) NOT NULL,
    es_area_stem VARCHAR(20) NOT NULL,                   -- 'STEM (Tecnología y Ciencias)' vs 'Otras Áreas'
    tipo_carrera VARCHAR(80) NOT NULL,
    tipo_programa VARCHAR(60) NOT NULL,
    horario VARCHAR(30) NOT NULL,                        -- 'Diurno', 'Vespertino', 'A Distancia / Otro'
    titulo VARCHAR(220) NOT NULL,
    grado_academico VARCHAR(100) NOT NULL,
    duracion_semestres INTEGER,
    duracion_anos REAL,                                  -- Duración en años (semestres / 2)
    ingreso_directo VARCHAR(30) NOT NULL,                -- 'Ingreso Directo' vs 'Admisión Regular / Prueba'
    -- TASAS Y KPIS HISTORICOS DEL PROGRAMA (Tributan a Pregunta 1 y 2)
    tasa_ocupacion_historica_prog_pct REAL,              -- Ocupación acumulada histórica del programa
    tasa_frecuencia_sobredemanda_prog_pct REAL,          -- % de años en que el programa tuvo Matrícula > Vacantes
    promedio_historico_paes_prog REAL,                   -- Puntaje PAES promedio histórico del programa
    clasificacion_presion_capacidad VARCHAR(45) NOT NULL -- '1. Sobredemanda Crítica (>100%)', '2. Capacidad Óptima (80-100%)', '3. Subutilización (<80%)', '4. Admisión Abierta'
);

-- 5. TABLA DE HECHOS PRINCIPAL: FACT MATRICULA Y ADMISION
-- Grano: Una fila por oferta de programa académico, en una sede y horario específico, en un año cronológico.
CREATE TABLE IF NOT EXISTS fact_matricula_admision (
    id_fact INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Claves Foráneas del Esquema Estrella
    id_tiempo INTEGER NOT NULL,
    id_sede_geografia INTEGER NOT NULL,
    id_institucion_sk INTEGER NOT NULL,
    id_carrera_programa_sk INTEGER NOT NULL,
    
    -- Flags de Gobernabilidad y Filtrado Rápido
    es_region_metropolitana INTEGER NOT NULL,            -- 1 = Región Metropolitana de Santiago (58.926 filas)
    flag_exige_prueba_admision INTEGER NOT NULL,         -- 1 = Reporta puntaje PAES/PSU
    flag_vacantes_declaradas INTEGER NOT NULL,           -- 1 = Declara vacantes > 0
    flag_sobredemanda_critica INTEGER NOT NULL,          -- 1 = Matrícula 1er Año > Vacantes (Sobreocupación)
    estado_ocupacion_oferta VARCHAR(40) NOT NULL,        -- Semáforo de decisión operativa por oferta
    
    -- Medidas Aditivas Puras (Conteos de Personas y Cupos)
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
    
    -- Medidas No Aditivas (Puntajes Homologados en 4 Escalas)
    puntaje_promedio_original REAL,
    puntaje_promedio_norm_0_100 REAL,
    puntaje_promedio_equiv_paes REAL,
    puntaje_promedio_zscore_anual REAL,
    puntaje_corte_primer_equiv_paes REAL,
    puntaje_corte_ultimo_equiv_paes REAL,
    
    -- TASAS, BRECHAS Y KPIS DE NIVEL DE OFERTA (Tributan a las 3 Preguntas de la Propuesta de Valor)
    tasa_ocupacion_primer_ano REAL,                      -- (Matrícula 1er Año / Vacantes) * 100
    tasa_renovacion_primer_ano_pct REAL,                 -- (Matrícula 1er Año / Matrícula Total) * 100
    ratio_mujeres_primer_ano REAL,                       -- (Mujeres 1er Año / Total 1er Año) * 100
    ratio_mujeres_total_pct REAL,                        -- (Mujeres Total / Matrícula Total) * 100
    ratio_extranjeros_primer_ano_pct REAL,               -- (Extranjeros 1er Año / Total 1er Año) * 100
    ratio_extranjeros_total REAL,                        -- (Extranjeros Total / Matrícula Total) * 100
    brecha_dispersa_max_min_paes REAL,                   -- Puntaje Máx PAES - Puntaje Mín PAES (Heterogeneidad en aula)
    brecha_corte_vs_media_rm_paes REAL,                  -- Puntaje Corte Último PAES - Media RM del Año (Selectividad relativa)
    indice_presion_selectiva_kpi REAL,                   -- (Tasa Ocupación / 100) * (Puntaje PAES / 600) * 100
    
    FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo_ine_rm(id_tiempo),
    FOREIGN KEY (id_sede_geografia) REFERENCES dim_sede_geografia(id_sede_geografia),
    FOREIGN KEY (id_institucion_sk) REFERENCES dim_institucion_sies(id_institucion_sk),
    FOREIGN KEY (id_carrera_programa_sk) REFERENCES dim_carrera_programa(id_carrera_programa_sk)
);

CREATE INDEX IF NOT EXISTS idx_f_tiempo ON fact_matricula_admision(id_tiempo);
CREATE INDEX IF NOT EXISTS idx_f_sede ON fact_matricula_admision(id_sede_geografia);
CREATE INDEX IF NOT EXISTS idx_f_inst ON fact_matricula_admision(id_institucion_sk);
CREATE INDEX IF NOT EXISTS idx_f_carr ON fact_matricula_admision(id_carrera_programa_sk);
CREATE INDEX IF NOT EXISTS idx_f_rm ON fact_matricula_admision(es_region_metropolitana);
