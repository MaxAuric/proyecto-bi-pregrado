-- ============================================================================
-- PROYECTO FINAL BUSINESS INTELLIGENCE - HITO 2
-- ROL: PERSONA 3 (ARQUITECTO DE BASES DE DATOS)
-- SCRIPT: 01_ddl_datamart.sql
-- DESCRIPCIÓN: Definición formal del esquema dimensional (DataMart)
-- MOTOR: SQLite 3 / Compatible ANSI SQL
-- MODELO: Constelación de Hechos (Fact Constellation) con Dimensiones Conformadas
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ----------------------------------------------------------------------------
-- 1. DIMENSIÓN TEMPORAL (dim_tiempo)
-- Grano: Un registro por año calendario (2012 - 2026)
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS fact_matricula_oferta;
DROP TABLE IF EXISTS fact_poblacion_regional;
DROP TABLE IF EXISTS dim_institucion_calidad_anual;
DROP TABLE IF EXISTS dim_programa;
DROP TABLE IF EXISTS dim_institucion;
DROP TABLE IF EXISTS dim_sede;
DROP TABLE IF EXISTS dim_geografia;
DROP TABLE IF EXISTS dim_tiempo;

CREATE TABLE dim_tiempo (
    id_tiempo               INTEGER PRIMARY KEY, -- Año calendario como clave natural/sustituta (ej: 2024)
    ano                     INTEGER NOT NULL UNIQUE,
    periodo_quinquenal      VARCHAR(30) NOT NULL,
    tipo_prueba_admision    VARCHAR(10) NOT NULL, -- PSU (2012-2020), PDT (2021-2022), PAES (2023-2026)
    flag_gratuidad_vigente  INTEGER NOT NULL CHECK(flag_gratuidad_vigente IN (0, 1)), -- 1 desde 2016
    flag_reforma_nuble      INTEGER NOT NULL CHECK(flag_reforma_nuble IN (0, 1)),     -- 1 desde 2018 (Ley 21.033)
    flag_pandemia           INTEGER NOT NULL CHECK(flag_pandemia IN (0, 1))           -- 1 en 2020-2021
);

-- ----------------------------------------------------------------------------
-- 2. DIMENSIÓN GEOGRÁFICA REGIONAL (dim_geografia)
-- Grano: 16 regiones oficiales de Chile (estándar SUBDERE / INE) + Miembro Desconocido
-- ----------------------------------------------------------------------------
CREATE TABLE dim_geografia (
    id_geografia            INTEGER PRIMARY KEY,
    region_codigo_subdere   VARCHAR(2) NOT NULL UNIQUE, -- '01' a '16' o '-1'
    region_nombre_estandar  VARCHAR(100) NOT NULL,
    region_numero_romano    VARCHAR(10) NOT NULL,
    zona_geografica         VARCHAR(50) NOT NULL,       -- Norte Grande, Norte Chico, Centro, Sur, Austral
    orden_geografico        INTEGER NOT NULL
);

-- ----------------------------------------------------------------------------
-- 3. DIMENSIÓN SEDE (dim_sede)
-- Grano: Sedes geográficas de impartición (114 sedes únicas)
-- ----------------------------------------------------------------------------
CREATE TABLE dim_sede (
    id_sede                 INTEGER PRIMARY KEY,
    nombre_sede             VARCHAR(100) NOT NULL UNIQUE,
    id_geografia            INTEGER NOT NULL,
    region_codigo_subdere   VARCHAR(2) NOT NULL,
    region_nombre           VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_geografia) REFERENCES dim_geografia(id_geografia)
);

-- ----------------------------------------------------------------------------
-- 4. DIMENSIÓN INSTITUCIÓN (dim_institucion)
-- Grano: Entidades de educación superior (259 instituciones CNED) + Desconocido
-- Cruce con SIES mediante codigo_ies (puente_institucion)
-- ----------------------------------------------------------------------------
CREATE TABLE dim_institucion (
    id_institucion          INTEGER PRIMARY KEY,
    nombre_institucion      VARCHAR(150) NOT NULL UNIQUE, -- Nombre canónico CNED
    nombre_normalizado      VARCHAR(150),                 -- Nombre expandido sin abreviaciones
    codigo_ies              INTEGER,                      -- Código oficial SIES (NULL si no cruza)
    nombre_sies             VARCHAR(150),                 -- Nombre oficial en SIES
    tipo_institucion        VARCHAR(50) NOT NULL,         -- Universidad, Instituto Profesional, CFT
    clasificacion2          VARCHAR(100),                 -- CRUCH, Privadas, etc.
    metodo_cruce_sies       VARCHAR(50)                   -- exacto_normalizado, manual, aproximado, sin_coincidencia
);

-- ----------------------------------------------------------------------------
-- 5. DIMENSIÓN INSTITUCIÓN - CALIDAD Y ESTADO ANUAL (dim_institucion_calidad_anual)
-- Modelado del cambio en el tiempo (SCD Snapshot Anual de Calidad y Acreditación)
-- Grano: Institución x Año (Permite responder Pregunta de Negocio 3 y cambios anuales)
-- ----------------------------------------------------------------------------
CREATE TABLE dim_institucion_calidad_anual (
    id_institucion_calidad  INTEGER PRIMARY KEY AUTOINCREMENT,
    id_institucion          INTEGER NOT NULL,
    id_tiempo               INTEGER NOT NULL,
    codigo_ies              INTEGER,
    acreditacion_cned       VARCHAR(50),                  -- Estado según base CNED
    autonomia_cned          VARCHAR(50),
    gratuidad_cned          VARCHAR(50),
    acreditacion_sies       VARCHAR(50),                  -- Acreditada, No Acreditada, Bajo Tutela, Acreditación Extendida
    anos_acreditacion_sies  REAL,                         -- Años de acreditación numérico (NULL si no aplica)
    vigencia_sies           VARCHAR(100),
    autonomia_sies          VARCHAR(50),
    fuente_calidad          VARCHAR(30) NOT NULL,         -- 'CNED' (2012-2017) o 'SIES_OFICIAL' (2018-2026)
    FOREIGN KEY (id_institucion) REFERENCES dim_institucion(id_institucion),
    FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo(id_tiempo),
    UNIQUE(id_institucion, id_tiempo)
);

-- ----------------------------------------------------------------------------
-- 6. DIMENSIÓN PROGRAMA / CARRERA (dim_programa)
-- Grano: Oferta académica tipificada (carrera, área de conocimiento, régimen y grado)
-- ----------------------------------------------------------------------------
CREATE TABLE dim_programa (
    id_programa             INTEGER PRIMARY KEY,
    nombre_programa         VARCHAR(200) NOT NULL,
    carrera_generica        VARCHAR(120) NOT NULL,
    area_conocimiento       VARCHAR(80) NOT NULL,
    tipo_programa           VARCHAR(50),
    tipo_carrera            VARCHAR(50),
    horario                 VARCHAR(30) NOT NULL,         -- Diurno, Vespertino, A Distancia, etc.
    duracion_semestres      INTEGER,
    titulo                  VARCHAR(200),
    grado_academico         VARCHAR(100)
);

-- ----------------------------------------------------------------------------
-- 7. TABLA DE HECHOS PRINCIPAL: MATRÍCULA Y OFERTA (fact_matricula_oferta)
-- Grano: Un registro por Institución, Sede, Programa, Horario y Año (158.211 registros)
-- ----------------------------------------------------------------------------
CREATE TABLE fact_matricula_oferta (
    id_fact                         INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tiempo                       INTEGER NOT NULL,
    id_geografia                    INTEGER NOT NULL,
    id_sede                         INTEGER NOT NULL,
    id_institucion                  INTEGER NOT NULL,
    id_programa                     INTEGER NOT NULL,
    
    -- Medidas Totalmente Aditivas (Enteros)
    vacantes                        INTEGER, -- Preservado como NULL si no declara para evitar sesgos
    matricula_primer_ano_total      INTEGER NOT NULL,
    matricula_primer_ano_hombres    INTEGER NOT NULL,
    matricula_primer_ano_mujeres    INTEGER NOT NULL,
    matricula_primer_ano_extranjeros INTEGER NOT NULL,
    matricula_total                 INTEGER NOT NULL,
    matricula_total_hombres         INTEGER NOT NULL,
    matricula_total_mujeres         INTEGER NOT NULL,
    matricula_total_extranjeros     INTEGER NOT NULL,
    
    -- Medidas No Aditivas / Puntajes Psicométricos Normalizados
    puntaje_promedio_original       REAL,    -- Escala nativa [150-850] o [100-1000]
    puntaje_promedio_norm_0_100     REAL,    -- Normalización min-max [0-100]
    puntaje_promedio_equiv_paes     REAL,    -- Proyección estándar escala PAES [100-1000]
    puntaje_promedio_zscore_anual   REAL,    -- Z-score anual
    
    -- Métricas Derivadas y Flags de Gobernanza
    tasa_ocupacion_primer_ano       REAL,    -- (matricula 1er ano / vacantes) * 100 si vacantes > 0
    ratio_mujeres_primer_ano        REAL,
    ratio_extranjeros_total         REAL,
    flag_exige_prueba_admision      INTEGER NOT NULL CHECK(flag_exige_prueba_admision IN (0, 1)),
    flag_vacantes_declaradas        INTEGER NOT NULL CHECK(flag_vacantes_declaradas IN (0, 1)),
    flag_quiebre_nuble              INTEGER NOT NULL CHECK(flag_quiebre_nuble IN (0, 1)),
    
    -- Restricciones de Integridad Referencial
    FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo(id_tiempo),
    FOREIGN KEY (id_geografia) REFERENCES dim_geografia(id_geografia),
    FOREIGN KEY (id_sede) REFERENCES dim_sede(id_sede),
    FOREIGN KEY (id_institucion) REFERENCES dim_institucion(id_institucion),
    FOREIGN KEY (id_programa) REFERENCES dim_programa(id_programa)
);

-- ----------------------------------------------------------------------------
-- 8. TABLA DE HECHOS SECUNDARIA: POBLACIÓN REGIONAL (fact_poblacion_regional)
-- Fuente Externa 1: INE Proyecciones de Población (Base Censo 2017)
-- Grano: Un registro por Región x Año (544 registros)
-- Medidas Semi-aditivas: Aditivas entre regiones para un año, NO a través del tiempo
-- ----------------------------------------------------------------------------
CREATE TABLE fact_poblacion_regional (
    id_poblacion            INTEGER PRIMARY KEY AUTOINCREMENT,
    id_geografia            INTEGER NOT NULL,
    id_tiempo               INTEGER NOT NULL,
    poblacion_total         INTEGER NOT NULL,
    poblacion_hombres       INTEGER NOT NULL,
    poblacion_mujeres       INTEGER NOT NULL,
    poblacion_0_14          INTEGER NOT NULL,
    poblacion_15_64         INTEGER NOT NULL, -- Población objetivo en edad de estudiar/trabajar (P1)
    poblacion_65_mas        INTEGER NOT NULL,
    FOREIGN KEY (id_geografia) REFERENCES dim_geografia(id_geografia),
    FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo(id_tiempo),
    UNIQUE(id_geografia, id_tiempo)
);

-- ============================================================================
-- ÍNDICES DE ALTO RENDIMIENTO (Optimizados para consultas de Power BI)
-- ============================================================================
CREATE INDEX idx_fact_tiempo ON fact_matricula_oferta(id_tiempo);
CREATE INDEX idx_fact_geografia ON fact_matricula_oferta(id_geografia);
CREATE INDEX idx_fact_sede ON fact_matricula_oferta(id_sede);
CREATE INDEX idx_fact_institucion ON fact_matricula_oferta(id_institucion);
CREATE INDEX idx_fact_programa ON fact_matricula_oferta(id_programa);
CREATE INDEX idx_fact_flags ON fact_matricula_oferta(flag_vacantes_declaradas, flag_exige_prueba_admision);

CREATE INDEX idx_pob_geo_tiempo ON fact_poblacion_regional(id_geografia, id_tiempo);
CREATE INDEX idx_calidad_inst_tiempo ON dim_institucion_calidad_anual(id_institucion, id_tiempo);
