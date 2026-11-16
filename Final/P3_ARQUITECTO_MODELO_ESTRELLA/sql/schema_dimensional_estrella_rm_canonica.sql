-- ============================================================================
-- PROYECTO FINAL BUSINESS INTELLIGENCE (2012–2026) — ENTREGA FINAL (18 NOV 2026)
-- SCRIPT DDL CANÓNICO: ESQUEMA ESTRELLA FORMAL ENRIQUECIDO (REGIÓN METROPOLITANA)
-- ============================================================================
-- Integrante / Rol Evaluado: Persona 3 (Arquitecto Dimensional y Diccionario de Tasas/KPIs)
-- Autor: Angel Pino
-- Alcance Geográfico Oficial: 100% Región Metropolitana de Santiago (SUBDERE 13)
-- Universo Auditado: 58.926 ofertas académicas (2012–2026) | 69 IES activas en 2026
-- Cumplimiento Normativo: 
--   1. Clase 4 - DW (Pág. 62): Cero columnas VARCHAR en tabla de hechos.
--   2. Clase 4 - DW (Pág. 62): Cero abreviaturas en dimensiones ('Universidad', etc.).
--   3. Clase 4 - DW (Pág. 63): Incorporación de tabla agregada para optimización OLAP.
--   4. Kimball Dimensional Modeling: Grano atómico, SCD Tipo 2 e Integridad 1:N.
--   5. Pauta Oficial (Pág. 3): Integración de 2 fuentes externas (INE RM y SIES).
-- ============================================================================

-- Habilitar soporte de claves foráneas en SQLite
PRAGMA foreign_keys = ON;

-- ----------------------------------------------------------------------------
-- 1. DIMENSIÓN TIEMPO Y DEMOGRAFÍA JUVENIL RM (dim_tiempo_ine_rm)
-- ----------------------------------------------------------------------------
-- Propósito: Modela la línea temporal anual (2012-2026) e integra la Fuente Externa 1
-- (Proyecciones Demográficas del INE para la Región Metropolitana).
-- Permite calcular las tasas macro de absorción juvenil y cobertura bruta en Santiago.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_tiempo_ine_rm (
    id_tiempo INTEGER PRIMARY KEY,                          -- Clave primaria temporal (Año cronológico 2012-2026)
    ano INTEGER NOT NULL UNIQUE,                            -- Año calendario
    periodo_admision VARCHAR(30) NOT NULL,                  -- 'PSU (2012-2020)', 'PDT (2021-2022)', 'PAES (2023-2026)'
    rango_quinquenio VARCHAR(20) NOT NULL,                  -- '2012-2016', '2017-2021', '2022-2026'
    estado_sanitario VARCHAR(25) NOT NULL,                  -- 'Pre-Pandemia', 'Pandemia COVID-19', 'Post-Pandemia'
    es_paes INTEGER NOT NULL CHECK (es_paes IN (0, 1)),     -- 1 = Período PAES (2023-2026, escala 100-1000)
    
    -- Variables Demográficas Oficiales INE RM (Población Proyectada Santiago)
    poblacion_total_rm INTEGER NOT NULL,                    -- Población total proyectada RM (censo y proyecciones INE)
    poblacion_15_64_rm INTEGER NOT NULL,                    -- Población en edad activa laboral (15-64 años)
    poblacion_joven_18_24_rm INTEGER NOT NULL,              -- Target universitario oficial (18 a 24 años)
    
    -- Tasas y KPIs Demográficos Macro RM (Precalculados a nivel anual)
    tasa_crecimiento_joven_rm_yoy_pct REAL,                 -- % Crecimiento interanual cohorte juvenil 18-24
    tasa_absorcion_juvenil_rm_pct REAL NOT NULL,            -- (Matrícula 1er Año RM / Pob. Joven 18-24 RM) * 100
    tasa_cobertura_bruta_rm_pct REAL NOT NULL,              -- (Matrícula Total RM / Pob. Joven 18-24 RM) * 100
    tasa_oferta_vacantes_1000_jovenes_rm REAL NOT NULL,     -- (Vacantes RM / Pob. Joven 18-24 RM) * 1000
    tasa_ocupacion_anual_rm_pct REAL NOT NULL,              -- (Matrícula 1er Año RM / Vacantes RM) * 100
    tasa_crecimiento_matricula_rm_yoy_pct REAL,             -- % Variación anual de la matrícula de 1er año en RM
    media_anual_paes_rm REAL                                -- Promedio anual homologado PAES de corte en la RM
);

-- ----------------------------------------------------------------------------
-- 2. DIMENSIÓN SEDE Y GEOGRAFÍA RM (dim_sede_geografia)
-- ----------------------------------------------------------------------------
-- Propósito: Representa la infraestructura física territorial en Santiago.
-- Desnormaliza la jerarquía geográfica completa en una sola tabla (Clase 4 DW Pág. 62).
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_sede_geografia (
    id_sede_geografia INTEGER PRIMARY KEY,                  -- Surrogate Key (SK) geográfica
    nombre_sede VARCHAR(120) NOT NULL,                      -- Comuna o nombre de campus en Santiago (ej. 'SANTIAGO', 'LAS CONDES')
    region_codigo_subdere VARCHAR(2) NOT NULL DEFAULT '13', -- '13' = Región Metropolitana de Santiago
    region_numero_romano VARCHAR(5) NOT NULL DEFAULT 'RM',
    region_nombre_estandar VARCHAR(100) NOT NULL DEFAULT 'Región Metropolitana de Santiago',
    macro_zona VARCHAR(40) NOT NULL DEFAULT 'Región Metropolitana de Santiago',
    es_region_metropolitana INTEGER NOT NULL CHECK (es_region_metropolitana = 1), -- Siempre 1 (filtro estricto RM)
    estado_territorial VARCHAR(50) NOT NULL,                -- Descripción completa sin abreviaturas
    
    -- Tasas y KPIs Históricos de Capacidad por Sede en Santiago
    tasa_ocupacion_historica_sede_pct REAL,                 -- (Suma Matrícula 1er Año Sede / Suma Vacantes Sede) * 100
    tasa_sobredemanda_sede_pct REAL,                        -- % de ofertas de la sede con Matrícula 1er Año > Vacantes
    participacion_matricula_rm_sede_pct REAL,               -- % Cuota de matrícula de la sede sobre el total de la RM
    nivel_saturacion_sede VARCHAR(45) NOT NULL              -- Semáforo operativo ('1. Sede Saturada (>=95%)', etc.)
);

-- ----------------------------------------------------------------------------
-- 3. DIMENSIÓN INSTITUCIÓN Y CALIDAD SIES (dim_institucion_sies)
-- ----------------------------------------------------------------------------
-- Propósito: Modela el comportamiento institucional aplicando SCD Tipo 2
-- (Slowly Changing Dimensions) e integra la Fuente Externa 2 (Acreditación SIES/CNA).
-- Cumple estrictamente Clase 4 DW (Pág. 62): Cero abreviaturas ('Universidad', 'IP', 'CFT')
-- y cero prefijos regulatorios '(a)', '(b)', '(c)'.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_institucion_sies (
    id_institucion_sk INTEGER PRIMARY KEY,                  -- Surrogate Key (SK) para SCD Tipo 2 (fotografía anual)
    codigo_ies_sies INTEGER,                                -- Código identificador oficial MINEDUC / SIES
    nombre_institucion VARCHAR(150) NOT NULL,               -- Nombre oficial de la IES (ej. 'PONTIFICIA U. CATÓLICA DE CHILE')
    tipo_institucion VARCHAR(60) NOT NULL,                  -- 'Universidad', 'Instituto Profesional', 'Centro de Formación Técnica', 'Institución de las Fuerzas Armadas y de Orden'
    subtipo_institucion VARCHAR(100) NOT NULL,              -- Sin prefijos '(a)' ni abreviaturas 'Univ.'
    acreditacion_cned VARCHAR(50) NOT NULL,                 -- 'Institución Acreditada' / 'Institución No Acreditada'
    anos_acreditacion_sies REAL,                            -- Años certificados por CNA/SIES (0.0 a 7.0 años)
    score_calidad_sies_pct REAL NOT NULL,                   -- (anos_acreditacion_sies / 7.0) * 100 (0% a 100%)
    tramo_acreditacion_sies VARCHAR(45) NOT NULL,           -- '1. Excelencia (6 a 7 años)', '2. Avanzada (4 a 5 años)', '3. Básica (1 a 3 años)', '4. No Acreditada (0 años)'
    autonomia VARCHAR(50) NOT NULL,                         -- 'Autónoma' / 'No Autónoma' (sin prefijos)
    gratuidad VARCHAR(50) NOT NULL,                         -- 'Adscrita a Gratuidad', 'No Adscrita a Gratuidad', 'No Aplica'
    ano_vigencia INTEGER NOT NULL,                          -- Año de vigencia de la fotografía institucional (SCD Tipo 2)
    en_region_metropolitana INTEGER NOT NULL CHECK (en_region_metropolitana = 1),
    
    -- Tasas y KPIs Competitivos Anuales de la Institución en Santiago
    tasa_ocupacion_inst_anual_pct REAL,                     -- Eficiencia anual de llenado de vacantes de la institución
    tasa_programas_sobredemanda_inst_pct REAL,              -- % de carreras de la IES con sobrecupo crítico (>100%) ese año
    cuota_mercado_matricula_rm_pct REAL,                    -- Market Share anual de la institución en la RM (%)
    tasa_permanencia_cohortes_sup_pct REAL,                 -- ((Matrícula Total - Matrícula 1er Año) / Matrícula Total) * 100
    puntaje_paes_ponderado_inst REAL,                       -- Puntaje PAES promedio ponderado por matrícula nueva
    posicionamiento_competitivo_rm VARCHAR(60) NOT NULL     -- Clasificación en 4 cuadrantes (Calidad SIES vs. Ocupación)
);

-- ----------------------------------------------------------------------------
-- 4. DIMENSIÓN PROGRAMA ACADÉMICO Y CARRERA (dim_carrera_programa)
-- ----------------------------------------------------------------------------
-- Propósito: Jerarquía académica formal de títulos, grados y áreas de conocimiento.
-- Incluye métricas de presión sobre laboratorios base 35 puestos (Caso 120->140).
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_carrera_programa (
    id_carrera_programa_sk INTEGER PRIMARY KEY,             -- Surrogate Key (SK) de la oferta curricular
    nombre_programa VARCHAR(220) NOT NULL,                  -- Denominación formal del plan curricular
    carrera_generica VARCHAR(150) NOT NULL,                 -- Agrupador genérico oficial CNED
    area_conocimiento VARCHAR(100) NOT NULL,                -- 11 áreas oficiales sin abreviaturas
    es_area_stem VARCHAR(35) NOT NULL,                      -- 'STEM (Tecnología y Ciencias)' vs 'Otras Áreas del Conocimiento'
    tipo_carrera VARCHAR(80) NOT NULL,                      -- 'Profesional con Licenciatura', 'Técnica de Nivel Superior', etc.
    tipo_programa VARCHAR(60) NOT NULL,                     -- 'Programa Regular', 'Programa para Trabajadores', etc.
    horario VARCHAR(35) NOT NULL,                           -- 'Diurno', 'Vespertino', 'A Distancia / Otro Horario'
    titulo VARCHAR(220) NOT NULL,                           -- Título profesional o técnico otorgado
    grado_academico VARCHAR(180) NOT NULL,                  -- Sin abreviatura 'M/' -> 'con Mención en'
    duracion_semestres INTEGER,                             -- Duración formal en semestres
    duracion_anos REAL,                                     -- Duración formal en años (semestres / 2.0)
    ingreso_directo VARCHAR(40) NOT NULL,                   -- 'Ingreso Directo (Sin Prueba)' vs 'Admisión Regular con Prueba'
    
    -- Tasas Históricas y de Capacidad Operativa del Programa
    tasa_ocupacion_historica_prog_pct REAL,                 -- Ocupación acumulada histórica de vacantes del programa
    tasa_frecuencia_sobredemanda_prog_pct REAL,             -- % de años con sobrecupo de vacantes (>100%)
    tasa_presion_lab_base35_prog_pct REAL,                  -- (Matrícula 1er Año Promedio / 35 puestos) * 100
    promedio_historico_paes_prog REAL,                      -- Puntaje PAES medio histórico del programa
    clasificacion_presion_capacidad VARCHAR(45) NOT NULL    -- '1. Sobredemanda Crítica (>100%)', '2. Capacidad Óptima', etc.
);

-- ----------------------------------------------------------------------------
-- 5. TABLA DE HECHOS CENTRAL: FACT MATRICULA Y ADMISIÓN RM (fact_matricula_admision)
-- ----------------------------------------------------------------------------
-- Grano Declarado: Una fila por cada oferta académica específica de una institución,
-- en una sede de la Región Metropolitana, bajo un régimen horario, en un año cronológico (2012-2026).
-- Regla de Oro Clase 4 DW (Pág. 62): Cero columnas VARCHAR (100% numérica).
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fact_matricula_admision (
    id_fact INTEGER PRIMARY KEY AUTOINCREMENT,              -- Clave subrogada atómica de la tabla de hechos
    
    -- Claves Foráneas (Relaciones 1 a N del Esquema Estrella)
    id_tiempo INTEGER NOT NULL,                             -- FK -> dim_tiempo_ine_rm(id_tiempo)
    id_sede_geografia INTEGER NOT NULL,                     -- FK -> dim_sede_geografia(id_sede_geografia)
    id_institucion_sk INTEGER NOT NULL,                     -- FK -> dim_institucion_sies(id_institucion_sk)
    id_carrera_programa_sk INTEGER NOT NULL,                -- FK -> dim_carrera_programa(id_carrera_programa_sk)
    
    -- Flags Numéricos Degenerados de Filtrado Rápido (0/1 o Códigos Enteros)
    es_region_metropolitana INTEGER NOT NULL CHECK (es_region_metropolitana = 1),
    flag_exige_prueba_admision INTEGER NOT NULL CHECK (flag_exige_prueba_admision IN (0, 1)),
    flag_vacantes_declaradas INTEGER NOT NULL CHECK (flag_vacantes_declaradas IN (0, 1)),
    flag_sobredemanda_critica INTEGER NOT NULL CHECK (flag_sobredemanda_critica IN (0, 1)),
    codigo_estado_ocupacion INTEGER NOT NULL CHECK (codigo_estado_ocupacion IN (1, 2, 3, 4)),
    
    -- Medidas Numéricas Aditivas Puras (Clase 4 DW Pág. 29: Agregables con SUM y COUNT)
    vacantes INTEGER,                                       -- Capacidad formal declarada
    matricula_primer_ano_hombres INTEGER NOT NULL DEFAULT 0,
    matricula_primer_ano_mujeres INTEGER NOT NULL DEFAULT 0,
    matricula_primer_ano_extranjeros INTEGER NOT NULL DEFAULT 0,
    matricula_primer_ano_total INTEGER NOT NULL DEFAULT 0,  -- Total matriculados nuevos de 1er año
    matricula_total_hombres INTEGER NOT NULL DEFAULT 0,
    matricula_total_mujeres INTEGER NOT NULL DEFAULT 0,
    matricula_total_extranjeros INTEGER NOT NULL DEFAULT 0,
    matricula_total INTEGER NOT NULL DEFAULT 0,             -- Matrícula total vigente de la carrera
    
    -- Medidas Físicas de Infraestructura y Capacidad de Laboratorios (Caso 120->140 Alumnos, Módulo 35)
    sobrecupo_neto_alumnos INTEGER,                         -- MAX(0, matricula_primer_ano_total - vacantes)
    vacantes_ociosas_netas INTEGER,                         -- MAX(0, vacantes - matricula_primer_ano_total)
    secciones_lab_planificadas_35 INTEGER,                  -- CEIL(vacantes / 35.0)
    secciones_lab_reales_35 INTEGER NOT NULL,               -- CEIL(matricula_primer_ano_total / 35.0)
    secciones_extra_por_sobrecupo INTEGER,                  -- MAX(0, secciones_lab_reales - secciones_lab_planificadas)
    tasa_saturacion_lab_35_pct REAL,                        -- (matricula_primer_ano_total / (secciones_planificadas * 35)) * 100
    
    -- Medidas Continuas de Selectividad Homologada (No Aditivas Puras: Promediables Ponderadas en DAX)
    puntaje_promedio_original REAL,                         -- Escala histórica PSU (150-850) o PAES (100-1000)
    puntaje_promedio_norm_0_100 REAL,                       -- Normalización porcentual continua (0.0 a 100.0)
    puntaje_promedio_equiv_paes REAL,                       -- Homologación psicométrica oficial a escala PAES (100-1000)
    puntaje_promedio_zscore_anual REAL,                     -- Puntuación típica Z estandarizada por año
    puntaje_corte_primer_equiv_paes REAL,                   -- Puntaje del primer seleccionado (escala PAES)
    puntaje_corte_ultimo_equiv_paes REAL,                   -- Puntaje de corte del último matriculado (escala PAES)
    
    -- Tasas y Ratios Precalculados a Nivel de Oferta (No Aditivas: Recalcular con DIVIDE() al agregar)
    tasa_ocupacion_primer_ano REAL,                         -- (matricula_primer_ano_total / vacantes) * 100
    tasa_sobredemanda_oferta_pct REAL,                      -- MAX(0, tasa_ocupacion_primer_ano - 100.0)
    tasa_renovacion_primer_ano_pct REAL,                    -- (matricula_primer_ano_total / matricula_total) * 100
    tasa_retencion_aparente_pct REAL,                       -- ((matricula_total - matricula_primer_ano_total) / matricula_total) * 100
    ratio_mujeres_primer_ano REAL,                          -- (mujeres_primer_ano / total_primer_ano) * 100
    ratio_mujeres_total_pct REAL,                           -- (mujeres_total / total_matricula) * 100
    ratio_extranjeros_primer_ano_pct REAL,                  -- (extranjeros_primer_ano / total_primer_ano) * 100
    ratio_extranjeros_total REAL,                           -- (extranjeros_total / total_matricula) * 100
    brecha_dispersa_max_min_paes REAL,                      -- Amplitud PAES (Máximo - Mínimo) en la oferta
    tasa_heterogeneidad_paes_pct REAL,                      -- (brecha_dispersa / puntaje_promedio_paes) * 100
    brecha_corte_vs_media_rm_paes REAL,                     -- Corte de la carrera - Media RM del año
    indice_presion_selectiva_kpi REAL,                      -- (Tasa Ocupación / 100) * (Puntaje PAES / 600) * 100
    
    -- Restricciones de Integridad Referencial Formales (1 a N)
    CONSTRAINT fk_fact_tiempo FOREIGN KEY (id_tiempo) 
        REFERENCES dim_tiempo_ine_rm(id_tiempo) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_fact_sede FOREIGN KEY (id_sede_geografia) 
        REFERENCES dim_sede_geografia(id_sede_geografia) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_fact_institucion FOREIGN KEY (id_institucion_sk) 
        REFERENCES dim_institucion_sies(id_institucion_sk) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_fact_carrera FOREIGN KEY (id_carrera_programa_sk) 
        REFERENCES dim_carrera_programa(id_carrera_programa_sk) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ----------------------------------------------------------------------------
-- 6. TABLA AGREGADA ANUAL POR INSTITUCIÓN (agg_resumen_anual_institucion_rm)
-- ----------------------------------------------------------------------------
-- Propósito: Optimización de rendimiento OLAP para Power BI y consultas gerenciales.
-- Cumple Clase 4 DW (Pág. 63) y Clase 5 ETL (Slide 10: Estrategia de Resumen).
-- ----------------------------------------------------------------------------
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

-- ----------------------------------------------------------------------------
-- 7. TABLA PUENTE DE HOMOLOGACIÓN SIES (puente_institucion_sies)
-- ----------------------------------------------------------------------------
-- Propósito: Tabla puente de gobernanza de datos para auditar el cruce entre
-- la base CNED INDICES y los códigos oficiales SIES de acreditación CNA.
-- Cumple requisito explícito de Pauta Oficial (Pág. 3).
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS puente_institucion_sies (
    nombre_institucion_cned VARCHAR(150) PRIMARY KEY,
    codigo_ies_sies INTEGER,
    nombre_institucion_sies VARCHAR(150),
    metodo_cruce VARCHAR(60),
    estado_cruce VARCHAR(60)
);

-- ----------------------------------------------------------------------------
-- 8. ÍNDICES DE RENDIMIENTO MULTIDIMENSIONAL (Optimización B-Tree para Power BI)
-- ----------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_fact_tiempo ON fact_matricula_admision(id_tiempo);
CREATE INDEX IF NOT EXISTS idx_fact_sede ON fact_matricula_admision(id_sede_geografia);
CREATE INDEX IF NOT EXISTS idx_fact_inst ON fact_matricula_admision(id_institucion_sk);
CREATE INDEX IF NOT EXISTS idx_fact_carr ON fact_matricula_admision(id_carrera_programa_sk);
CREATE INDEX IF NOT EXISTS idx_fact_rm ON fact_matricula_admision(es_region_metropolitana);
CREATE INDEX IF NOT EXISTS idx_fact_vacantes_declaradas ON fact_matricula_admision(flag_vacantes_declaradas);
CREATE INDEX IF NOT EXISTS idx_fact_sobredemanda ON fact_matricula_admision(flag_sobredemanda_critica);
CREATE INDEX IF NOT EXISTS idx_fact_prueba ON fact_matricula_admision(flag_exige_prueba_admision);

-- ----------------------------------------------------------------------------
-- 9. VISTA ANALÍTICA GERENCIAL OLAP (v_vista_maestra_olap_rm)
-- ----------------------------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_vista_maestra_olap_rm AS
SELECT 
    t.ano,
    t.periodo_admision,
    t.estado_sanitario,
    t.poblacion_joven_18_24_rm,
    t.tasa_absorcion_juvenil_rm_pct,
    s.nombre_sede,
    s.nivel_saturacion_sede,
    i.nombre_institucion,
    i.tipo_institucion,
    i.tramo_acreditacion_sies,
    i.score_calidad_sies_pct,
    i.posicionamiento_competitivo_rm,
    c.nombre_programa,
    c.carrera_generica,
    c.area_conocimiento,
    c.es_area_stem,
    c.horario,
    c.clasificacion_presion_capacidad,
    f.vacantes,
    f.matricula_primer_ano_total,
    f.matricula_total,
    f.sobrecupo_neto_alumnos,
    f.secciones_lab_planificadas_35,
    f.secciones_lab_reales_35,
    f.secciones_extra_por_sobrecupo,
    f.tasa_saturacion_lab_35_pct,
    f.tasa_ocupacion_primer_ano,
    f.tasa_sobredemanda_oferta_pct,
    f.tasa_retencion_aparente_pct,
    f.puntaje_promedio_equiv_paes,
    f.puntaje_corte_ultimo_equiv_paes
FROM fact_matricula_admision f
INNER JOIN dim_tiempo_ine_rm t ON f.id_tiempo = t.id_tiempo
INNER JOIN dim_sede_geografia s ON f.id_sede_geografia = s.id_sede_geografia
INNER JOIN dim_institucion_sies i ON f.id_institucion_sk = i.id_institucion_sk
INNER JOIN dim_carrera_programa c ON f.id_carrera_programa_sk = c.id_carrera_programa_sk;

