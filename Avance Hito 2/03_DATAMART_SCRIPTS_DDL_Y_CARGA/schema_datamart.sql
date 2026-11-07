-- ============================================================================
-- PROYECTO FINAL BUSINESS INTELLIGENCE - HITO 2: DATAMART DE EDUCACION SUPERIOR
-- MODELO DIMENSIONAL (ESQUEMA ESTRELLA)
-- AUTOR: Persona 1 (Ingeniero de Datos / ETL y DataMart)
-- MOTOR DESTINO: SQLite / DuckDB / PostgreSQL
-- ============================================================================

-- 1. DIMENSION TIEMPO
CREATE TABLE IF NOT EXISTS dim_tiempo (
    id_tiempo INTEGER PRIMARY KEY,           -- Año cronológico (2012 a 2026)
    ano INTEGER NOT NULL,
    periodo_admision VARCHAR(10) NOT NULL,    -- 'PSU' (2012-2020), 'PDT' (2021-2022), 'PAES' (2023-2026)
    rango_quinquenio VARCHAR(20) NOT NULL,    -- '2012-2016', '2017-2021', '2022-2026'
    es_pandemia INTEGER NOT NULL,             -- 1 si año in (2020, 2021), 0 en otro caso
    es_paes INTEGER NOT NULL                  -- 1 si año >= 2023, 0 en otro caso
);

-- 2. DIMENSION SEDE Y GEOGRAFIA
CREATE TABLE IF NOT EXISTS dim_sede_geografia (
    id_sede_geografia INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_sede VARCHAR(120) NOT NULL,
    nombre_region_original VARCHAR(100) NOT NULL,
    region_codigo_subdere VARCHAR(2) NOT NULL, -- '13' para Región Metropolitana
    region_numero_romano VARCHAR(5) NOT NULL,  -- 'RM', 'V', etc.
    region_nombre_estandar VARCHAR(100) NOT NULL,
    region_orden_geografico INTEGER NOT NULL,
    macro_zona VARCHAR(20) NOT NULL,           -- 'Norte', 'Centro', 'RM', 'Sur', 'Austral'
    es_region_metropolitana INTEGER NOT NULL,  -- 1 si codigo SUBDERE = '13', 0 en otro caso
    flag_quiebre_nuble INTEGER NOT NULL        -- 1 si es registro previo a 2018 asignado a Ñuble
);

-- 3. DIMENSION INSTITUCION (CON TRATAMIENTO SCD TIPO 2)
CREATE TABLE IF NOT EXISTS dim_institucion (
    id_institucion_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_institucion VARCHAR(150) NOT NULL,
    tipo_institucion VARCHAR(60) NOT NULL,     -- 'Universidad', 'Instituto Profesional', 'Centro de Formación Técnica'
    clasificacion2 VARCHAR(100),               -- Subclasificación institucional (ej. 'CRUCH', 'Privada')
    acreditacion VARCHAR(50),                  -- 'Acreditada', 'No Acreditada' (Atributo mutable SCD Tipo 2)
    autonomia VARCHAR(50),                     -- 'Autónoma', etc. (Atributo mutable SCD Tipo 2)
    gratuidad VARCHAR(50),                     -- 'Adscrita', 'No Adscrita' (Atributo mutable SCD Tipo 2)
    ano_vigencia INTEGER NOT NULL              -- Año de vigencia de este estado institucional
);

-- 4. DIMENSION CARRERA Y PROGRAMA ACADEMICO
CREATE TABLE IF NOT EXISTS dim_carrera_programa (
    id_carrera_programa_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_programa VARCHAR(220) NOT NULL,
    carrera_generica VARCHAR(150) NOT NULL,
    area_conocimiento VARCHAR(100) NOT NULL,
    tipo_carrera VARCHAR(80),                  -- 'Carreras Profesionales con Licenciatura', 'Técnicas', etc.
    tipo_programa VARCHAR(60),                 -- 'Plan Regular', 'Plan Trabajador', etc.
    horario VARCHAR(30) NOT NULL,              -- 'Diurno', 'Vespertino', 'A distancia'
    titulo VARCHAR(220),
    grado_academico VARCHAR(100),
    duracion_semestres INTEGER,
    ano_inicio_actividades INTEGER,
    ingreso_directo VARCHAR(10)                -- 'SI', 'NO'
);

-- 5. TABLA DE HECHOS: FACT MATRICULA Y ADMISION
-- Grano: Una fila por programa académico, en una sede y horario específico, reportado en un año cronológico determinado.
CREATE TABLE IF NOT EXISTS fact_matricula_admision (
    id_fact INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Claves Foráneas (Dimensiones)
    id_tiempo INTEGER NOT NULL,
    id_sede_geografia INTEGER NOT NULL,
    id_institucion_sk INTEGER NOT NULL,
    id_carrera_programa_sk INTEGER NOT NULL,
    
    -- Dimensiones Degeneradas / Flags de Negocio
    flag_exige_prueba_admision INTEGER NOT NULL, -- 1 si exige prueba (Universidades diurnas), 0 en otro caso
    flag_vacantes_declaradas INTEGER NOT NULL,   -- 1 si declara vacantes fijas > 0, 0 en otro caso
    es_region_metropolitana INTEGER NOT NULL,    -- 1 si la carrera pertenece a la RM (facilita filtrado)
    
    -- Medidas Totalmente Aditivas (Volúmenes)
    vacantes INTEGER,
    matricula_primer_ano_hombres INTEGER NOT NULL DEFAULT 0,
    matricula_primer_ano_mujeres INTEGER NOT NULL DEFAULT 0,
    matricula_primer_ano_extranjeros INTEGER NOT NULL DEFAULT 0,
    matricula_primer_ano_total INTEGER NOT NULL DEFAULT 0,
    matricula_total_hombres INTEGER NOT NULL DEFAULT 0,
    matricula_total_mujeres INTEGER NOT NULL DEFAULT 0,
    matricula_total_extranjeros INTEGER NOT NULL DEFAULT 0,
    matricula_total INTEGER NOT NULL DEFAULT 0,
    
    -- Medidas No Aditivas (Puntajes - Deben agregarse con promedios ponderados en DAX)
    puntaje_promedio_original REAL,
    puntaje_promedio_norm_0_100 REAL,
    puntaje_promedio_equiv_paes REAL,
    puntaje_promedio_zscore_anual REAL,
    puntaje_corte_primer_original REAL,
    puntaje_corte_primer_equiv_paes REAL,
    puntaje_corte_ultimo_original REAL,
    puntaje_corte_ultimo_equiv_paes REAL,
    
    -- Ratios Analíticos Precalculados
    tasa_ocupacion_primer_ano REAL,              -- (Matricula 1er Año / Vacantes) * 100
    ratio_mujeres_primer_ano REAL,               -- (Matricula Mujeres 1er Año / Total 1er Año) * 100
    ratio_extranjeros_total REAL,                -- (Matricula Extranjeros / Matricula Total) * 100
    
    -- Restricciones de Integridad Referencial
    FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo(id_tiempo),
    FOREIGN KEY (id_sede_geografia) REFERENCES dim_sede_geografia(id_sede_geografia),
    FOREIGN KEY (id_institucion_sk) REFERENCES dim_institucion(id_institucion_sk),
    FOREIGN KEY (id_carrera_programa_sk) REFERENCES dim_carrera_programa(id_carrera_programa_sk)
);

-- INDICES DE RENDIMIENTO PARA CONSULTAS RAPIDAS Y POWER BI
CREATE INDEX IF NOT EXISTS idx_fact_tiempo ON fact_matricula_admision(id_tiempo);
CREATE INDEX IF NOT EXISTS idx_fact_geografia ON fact_matricula_admision(id_sede_geografia);
CREATE INDEX IF NOT EXISTS idx_fact_institucion ON fact_matricula_admision(id_institucion_sk);
CREATE INDEX IF NOT EXISTS idx_fact_carrera ON fact_matricula_admision(id_carrera_programa_sk);
CREATE INDEX IF NOT EXISTS idx_fact_rm ON fact_matricula_admision(es_region_metropolitana);
CREATE INDEX IF NOT EXISTS idx_fact_flags ON fact_matricula_admision(flag_exige_prueba_admision, flag_vacantes_declaradas);

