-- ============================================================================
-- PROYECTO FINAL BUSINESS INTELLIGENCE (2012–2026) - HITO 2
-- MODELO DIMENSIONAL FORMAL (ESQUEMA ESTRELLA / STAR SCHEMA)
-- 
-- ROL: Persona 3 - Arquitecto de Datos y Modelador Dimensional
-- AUTOR: Angel Pino
-- FECHA: Noviembre 2026
-- ENTORNO DESTINO: SQLite / DuckDB / PostgreSQL / Azure Synapse
-- REQUISITOS PAUTA: Grano declarado, Esquema Estrella, Claves PK/FK,
--                   SCD Tipo 2, Aditividad de Medidas e Índices Analíticos
-- ============================================================================

-- ----------------------------------------------------------------------------
-- DECLARACION FORMAL DEL GRANO:
-- «Una fila por cada oferta de programa académico, sede física y régimen 
--  horario, reportada por una institución de educación superior en un año 
--  cronológico determinado en las bases oficiales INDICES del CNED».
-- Tupla identificadora: (id_tiempo, id_institucion_sk, id_sede_geografia, id_carrera_programa_sk)
-- Identificador unívoco del hecho: id_fact (INTEGER PRIMARY KEY)
-- ----------------------------------------------------------------------------

-- Habilitar soporte de claves foráneas en SQLite
PRAGMA foreign_keys = ON;

-- ============================================================================
-- 1. TABLAS DE DIMENSIONES (ESQUEMA ESTRELLA)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1.1. DIMENSION TIEMPO (dim_tiempo)
-- Grano: Un registro por cada año cronológico de la serie histórica (2012–2026).
-- Propósito: Gobernar el análisis temporal, segmentación por quinquenios y 
--            quiebres metodológicos de admisión (PSU -> PDT -> PAES).
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_tiempo (
    id_tiempo INTEGER PRIMARY KEY,                      -- Clave primaria natural: Año cronológico (2012 a 2026)
    ano INTEGER NOT NULL UNIQUE,                        -- Año calendario de referencia
    periodo_admision VARCHAR(10) NOT NULL,               -- 'PSU' (2012-2020), 'PDT' (2021-2022), 'PAES' (2023-2026)
    rango_quinquenio VARCHAR(20) NOT NULL,               -- Quinquenios de análisis: '2012-2016', '2017-2021', '2022-2026'
    es_pandemia INTEGER NOT NULL DEFAULT 0,              -- 1 si año in (2020, 2021); 0 en otro caso (quiebre operativo COVID-19)
    es_paes INTEGER NOT NULL DEFAULT 0,                  -- 1 si año >= 2023 (vigencia del sistema PAES de 100 a 1000 puntos)
    CONSTRAINT chk_periodo CHECK (periodo_admision IN ('PSU', 'PDT', 'PAES')),
    CONSTRAINT chk_pandemia CHECK (es_pandemia IN (0, 1)),
    CONSTRAINT chk_paes CHECK (es_paes IN (0, 1))
);

-- ----------------------------------------------------------------------------
-- 1.2. DIMENSION SEDE Y GEOGRAFIA (dim_sede_geografia)
-- Grano: Un registro por cada sede institucional y localización geográfica única.
-- Jerarquía Territorial: País -> Macro-zona -> Región (SUBDERE) -> Sede / Comuna.
-- Desnormalización: Cumple estándar Kimball en Estrella; absorbe códigos SUBDERE
--                   evitando tablas copo de nieve para agilizar el motor DAX.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_sede_geografia (
    id_sede_geografia INTEGER PRIMARY KEY AUTOINCREMENT, -- Clave subrogada geográfica
    nombre_sede VARCHAR(120) NOT NULL,                   -- Sede física reportada por la IES (ej. 'SANTIAGO', 'SAN JOAQUÍN')
    nombre_region_original VARCHAR(100) NOT NULL,        -- Denominación textual en base cruda CNED
    region_codigo_subdere VARCHAR(2) NOT NULL,           -- Código canónico SUBDERE ('01' a '16'; '13' = Región Metropolitana)
    region_numero_romano VARCHAR(5) NOT NULL,            -- Numeración tradicional ('RM', 'I', 'V', 'VIII', etc.)
    region_nombre_estandar VARCHAR(100) NOT NULL,        -- Nombre normalizado oficial (ej. 'Región Metropolitana de Santiago')
    region_orden_geografico INTEGER NOT NULL,            -- Orden geográfico de norte a sur para ordenamiento visual en Power BI
    macro_zona VARCHAR(20) NOT NULL,                     -- 'Norte', 'Centro', 'RM', 'Sur', 'Austral'
    es_region_metropolitana INTEGER NOT NULL DEFAULT 0,  -- 1 si región = 13 (RM); 0 en otras regiones (filtro núcleo Hito 2)
    flag_quiebre_nuble INTEGER NOT NULL DEFAULT 0,       -- 1 si registro es de Ñuble previo a 2018 (Ley 21.033)
    CONSTRAINT chk_es_rm CHECK (es_region_metropolitana IN (0, 1)),
    CONSTRAINT chk_nuble CHECK (flag_quiebre_nuble IN (0, 1))
);

-- ----------------------------------------------------------------------------
-- 1.3. DIMENSION INSTITUCION (dim_institucion - MODELADO SCD TIPO 2)
-- Grano: Un registro por cada institución de educación superior en cada año cronológico.
-- Justificación Técnica SCD Tipo 2: Atributos clave como la Acreditación Institucional 
--   (CNA/SIES), Autonomía y Gratuidad MUTAN en el tiempo.
--   - Un modelado SCD Tipo 1 destruiría la historia (atribuiría gratuidad en 2012 a una IES adscrita en 2016).
--   - Se implementa SCD Tipo 2 con clave subrogada anual (id_institucion_sk) y año de vigencia (ano_vigencia).
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_institucion (
    id_institucion_sk INTEGER PRIMARY KEY AUTOINCREMENT, -- Clave subrogada anual SCD Tipo 2
    nombre_institucion VARCHAR(150) NOT NULL,            -- Nombre oficial canónico de la institución
    tipo_institucion VARCHAR(60) NOT NULL,               -- 'Universidad', 'Instituto Profesional', 'Centro de Formación Técnica'
    clasificacion2 VARCHAR(100),                         -- Clasificación de origen: 'CRUCH', 'Privada', 'Estatal', etc.
    acreditacion VARCHAR(50),                            -- Estado de acreditación en dicho año: 'Acreditada', 'No Acreditada'
    autonomia VARCHAR(50),                               -- Condición jurídica: 'Autónoma', 'En Supervisión / Licenciamiento'
    gratuidad VARCHAR(50),                               -- Régimen de financiamiento: 'Adscrita', 'No Adscrita'
    ano_vigencia INTEGER NOT NULL,                       -- Año calendario de validez histórica de esta fotografía institucional
    CONSTRAINT chk_tipo_inst CHECK (tipo_institucion IN ('Universidad', 'Instituto Profesional', 'Centro de Formación Técnica'))
);

-- ----------------------------------------------------------------------------
-- 1.4. DIMENSION CARRERA Y PROGRAMA ACADEMICO (dim_carrera_programa)
-- Grano: Un registro por cada plan de estudios, carrera genérica, jornada y titulación.
-- Jerarquía Académica: Área de Conocimiento -> Carrera Genérica -> Programa Académico -> Horario.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_carrera_programa (
    id_carrera_programa_sk INTEGER PRIMARY KEY AUTOINCREMENT, -- Clave subrogada de programa académico
    nombre_programa VARCHAR(220) NOT NULL,                    -- Nombre específico del programa (ej. 'INGENIERÍA CIVIL INDUSTRIAL')
    carrera_generica VARCHAR(150) NOT NULL,                   -- Agrupador transversal nacional de carrera (284 genéricas únicas)
    area_conocimiento VARCHAR(100) NOT NULL,                  -- Área OCDE/CNED (11 áreas canónicas, ej. 'Tecnología', 'Salud')
    tipo_carrera VARCHAR(80),                                 -- 'Carreras Profesionales con Licenciatura', 'Técnicas', etc.
    tipo_programa VARCHAR(60),                                -- 'Programa Regular', 'Programa Especial / Trabajador', etc.
    horario VARCHAR(30) NOT NULL,                             -- Régimen horario: 'Diurno', 'Vespertino', 'A distancia / Semi-presencial'
    titulo VARCHAR(220),                                      -- Título profesional o técnico otorgado al egreso
    grado_academico VARCHAR(100),                             -- Grado académico: 'Licenciado', 'Bachiller', 'Magíster', o NULL
    duracion_semestres INTEGER,                               -- Duración formal teórica del plan en semestres
    ano_inicio_actividades INTEGER,                           -- Año formal de inicio de dictación del programa
    ingreso_directo VARCHAR(10)                               -- 'Ingreso Directo', 'No es Ingreso Directo' (exige prueba)
);

-- ----------------------------------------------------------------------------
-- 1.5. DIMENSION DEMOGRAFICA COMPLEMENTARIA (dim_poblacion_rm - FUENTE EXTERNA INE)
-- Grano: Un registro por cada año en la Región Metropolitana con estimaciones censales INE.
-- Propósito: Atender la Pregunta de Negocio 3 (Capacidad regional y absorción juvenil 18-24).
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_poblacion_rm (
    ano INTEGER PRIMARY KEY,                             -- Año cronológico (2002–2035)
    region_codigo_subdere VARCHAR(2) NOT NULL DEFAULT '13', -- Siempre '13' (Región Metropolitana)
    poblacion_total INTEGER NOT NULL,                    -- Población total proyectada RM al 30 de junio
    poblacion_hombres INTEGER NOT NULL,                  -- Población masculina proyectada
    poblacion_mujeres INTEGER NOT NULL,                  -- Población femenina proyectada
    poblacion_15_64 INTEGER NOT NULL,                    -- Población en edad de trabajar (15 a 64 años)
    est_pob_18_24_rm INTEGER NOT NULL,                   -- Proxy documentado de población en edad universitaria (14% de 15-64)
    fuente_origen VARCHAR(50) NOT NULL DEFAULT 'INE - Proyecciones Censo 2017'
);

-- ============================================================================
-- 2. TABLA DE HECHOS CENTRAL: FACT MATRICULA Y ADMISION (fact_matricula_admision)
-- ============================================================================
-- Grano Físico: 1 fila por oferta institucional de programa, sede, jornada y año.
-- Universo Completo: 158.211 filas (2012–2026 nacional).
-- Subconjunto RM: 58.926 filas (37,25% de la oferta académica nacional).
-- ============================================================================

CREATE TABLE IF NOT EXISTS fact_matricula_admision (
    id_fact INTEGER PRIMARY KEY AUTOINCREMENT,           -- Clave primaria subrogada del hecho atómico

    -- CLAVES FORANEAS (RELACIONES DIMENSIONALES 1:N)
    id_tiempo INTEGER NOT NULL,                          -- FK -> dim_tiempo.id_tiempo
    id_sede_geografia INTEGER NOT NULL,                  -- FK -> dim_sede_geografia.id_sede_geografia
    id_institucion_sk INTEGER NOT NULL,                  -- FK -> dim_institucion.id_institucion_sk (SCD Tipo 2)
    id_carrera_programa_sk INTEGER NOT NULL,             -- FK -> dim_carrera_programa.id_carrera_programa_sk

    -- DIMENSIONES DEGENERADAS Y FLAGS ANALITICOS (LINEA DE NEGOCIO RM)
    flag_exige_prueba_admision INTEGER NOT NULL,         -- 1 si carrera exige PSU/PDT/PAES (Universidades diurnas), 0 si es ingreso libre
    flag_vacantes_declaradas INTEGER NOT NULL,           -- 1 si declara vacantes formales > 0, 0 en otro caso
    es_region_metropolitana INTEGER NOT NULL,            -- 1 si pertenece a la RM (facilita particionamiento lógico)

    -- MEDIDAS COMPLETAMENTE ADITIVAS (VOLUMENES FISICOS DE ESTUDIANTES Y CUPOS)
    -- Justificación Kimball: Estas métricas son válidas y consistentes bajo el operador SUM() 
    -- a lo largo de cualquier corte dimensional (por año, por sede, por carrera o por institución).
    vacantes INTEGER,                                    -- Capacidad formal declarada por la institución
    matricula_primer_ano_hombres INTEGER NOT NULL DEFAULT 0,
    matricula_primer_ano_mujeres INTEGER NOT NULL DEFAULT 0,
    matricula_primer_ano_extranjeros INTEGER NOT NULL DEFAULT 0,
    matricula_primer_ano_total INTEGER NOT NULL DEFAULT 0, -- Medida núcleo para tasa de sobreocupación
    matricula_total_hombres INTEGER NOT NULL DEFAULT 0,
    matricula_total_mujeres INTEGER NOT NULL DEFAULT 0,
    matricula_total_extranjeros INTEGER NOT NULL DEFAULT 0,
    matricula_total INTEGER NOT NULL DEFAULT 0,          -- Matrícula total consolidada (todos los años de avance)

    -- MEDIDAS NO ADITIVAS (PUNTAJES PSICOMETRICOS Y CORTES DE SELECCION)
    -- Justificación Kimball: Los puntajes son intensivos / promedios. Sumarlos aritméticamente
    -- produce un disparate metodológico. DEBEN agregarse en Power BI / DAX mediante promedios ponderados:
    -- Promedio_Ponderado = SUMX(Fact, Fact[Puntaje] * Fact[Matricula_1er_Ano]) / SUM(Fact[Matricula_1er_Ano])
    puntaje_promedio_original REAL,                      -- Puntaje promedio en escala histórica del año (PSU / PDT / PAES)
    puntaje_promedio_norm_0_100 REAL,                    -- Puntaje estandarizado Min-Max a escala 0 a 100 puntos
    puntaje_promedio_equiv_paes REAL,                    -- Puntaje homologado hacia la escala PAES actual (100 a 1000 puntos)
    puntaje_promedio_zscore_anual REAL,                  -- Puntuación típica Z anual respecto a la cohorte nacional
    puntaje_corte_primer_original REAL,                  -- Puntaje del primer matriculado en escala histórica
    puntaje_corte_primer_equiv_paes REAL,                -- Primer matriculado en escala equivalente PAES
    puntaje_corte_ultimo_original REAL,                  -- Puntaje de corte del último matriculado seleccionado
    puntaje_corte_ultimo_equiv_paes REAL,                -- Último matriculado en escala equivalente PAES

    -- MEDIDAS SEMI-ADITIVAS / RATIOS DERIVADOS PRECALCULADOS A NIVEL ATOMICO
    -- Ojo DAX: A nivel agregado deben recalcularse dinámicamente como cociente de sumas aditivas.
    tasa_ocupacion_primer_ano REAL,                      -- (matricula_primer_ano_total / vacantes) * 100.0
    ratio_mujeres_primer_ano REAL,                       -- (matricula_primer_ano_mujeres / matricula_primer_ano_total) * 100.0
    ratio_extranjeros_total REAL,                        -- (matricula_total_extranjeros / matricula_total) * 100.0

    -- RESTRICCIONES DE INTEGRIDAD REFERENCIAL ESTRICTA
    FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo(id_tiempo)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_sede_geografia) REFERENCES dim_sede_geografia(id_sede_geografia)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_institucion_sk) REFERENCES dim_institucion(id_institucion_sk)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_carrera_programa_sk) REFERENCES dim_carrera_programa(id_carrera_programa_sk)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ============================================================================
-- 3. INDICES ANALITICOS OPTIMIZADOS PARA RENDIMIENTO EN POWER BI
-- ============================================================================
-- Diseñados específicamente para evitar cuellos de botella (Table Scans)
-- en las consultas enviadas por el conector ODBC / Python de Power BI.
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_fact_tiempo 
    ON fact_matricula_admision(id_tiempo);

CREATE INDEX IF NOT EXISTS idx_fact_geografia 
    ON fact_matricula_admision(id_sede_geografia);

CREATE INDEX IF NOT EXISTS idx_fact_institucion 
    ON fact_matricula_admision(id_institucion_sk);

CREATE INDEX IF NOT EXISTS idx_fact_carrera 
    ON fact_matricula_admision(id_carrera_programa_sk);

CREATE INDEX IF NOT EXISTS idx_fact_rm 
    ON fact_matricula_admision(es_region_metropolitana);

CREATE INDEX IF NOT EXISTS idx_fact_flags_negocio 
    ON fact_matricula_admision(flag_exige_prueba_admision, flag_vacantes_declaradas);

CREATE INDEX IF NOT EXISTS idx_fact_cubo_analitico 
    ON fact_matricula_admision(id_tiempo, es_region_metropolitana, id_carrera_programa_sk);

-- ============================================================================
-- 4. VISTAS ANALITICAS FOCALIZADAS EN LA REGION METROPOLITANA
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Vista 1: Analítica de Sobredemanda, Vacantes y Quiebre Operativo de Capacidad
-- Responde directamente a la Pregunta de Negocio 1 (El caso de los 20 alumnos)
-- ----------------------------------------------------------------------------
CREATE VIEW IF NOT EXISTS vw_rm_sobredemanda_y_capacidad AS
SELECT 
    t.ano,
    t.periodo_admision,
    t.rango_quinquenio,
    i.nombre_institucion,
    i.tipo_institucion,
    i.acreditacion,
    i.gratuidad,
    s.nombre_sede,
    s.macro_zona,
    c.carrera_generica,
    c.nombre_programa,
    c.area_conocimiento,
    c.horario,
    f.vacantes,
    f.matricula_primer_ano_total,
    f.matricula_total,
    -- Métricas de negocio calculadas
    (f.matricula_primer_ano_total - f.vacantes) AS sobrecupo_estudiantes,
    ROUND((CAST(f.matricula_primer_ano_total AS REAL) / NULLIF(f.vacantes, 0)) * 100.0, 2) AS tasa_ocupacion_pct,
    CASE 
        WHEN f.vacantes > 0 AND f.matricula_primer_ano_total > f.vacantes THEN 1 
        ELSE 0 
    END AS flag_sobredemanda_critica,
    -- Quiebre operativo: si sobrecupo supera 20 alumnos (caso práctico del profesor)
    CASE 
        WHEN (f.matricula_primer_ano_total - f.vacantes) >= 20 THEN 1 
        ELSE 0 
    END AS flag_quiebre_laboratorio_20plus
FROM fact_matricula_admision f
INNER JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
INNER JOIN dim_sede_geografia s ON f.id_sede_geografia = s.id_sede_geografia
INNER JOIN dim_institucion i ON f.id_institucion_sk = i.id_institucion_sk
INNER JOIN dim_carrera_programa c ON f.id_carrera_programa_sk = c.id_carrera_programa_sk
WHERE f.es_region_metropolitana = 1;

-- ----------------------------------------------------------------------------
-- Vista 2: Evolución de Puntajes de Admisión PAES/PSU y Selectividad
-- Responde directamente a la Pregunta de Negocio 2 (Comportamiento de cortes)
-- ----------------------------------------------------------------------------
CREATE VIEW IF NOT EXISTS vw_rm_evolucion_selectividad_paes AS
SELECT 
    t.ano,
    t.periodo_admision,
    i.nombre_institucion,
    i.tipo_institucion,
    c.carrera_generica,
    c.area_conocimiento,
    c.horario,
    f.vacantes,
    f.matricula_primer_ano_total,
    f.tasa_ocupacion_primer_ano,
    f.puntaje_promedio_equiv_paes,
    f.puntaje_corte_primer_equiv_paes,
    f.puntaje_corte_ultimo_equiv_paes,
    f.puntaje_promedio_zscore_anual
FROM fact_matricula_admision f
INNER JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
INNER JOIN dim_institucion i ON f.id_institucion_sk = i.id_institucion_sk
INNER JOIN dim_carrera_programa c ON f.id_carrera_programa_sk = c.id_carrera_programa_sk
WHERE f.es_region_metropolitana = 1 
  AND f.flag_exige_prueba_admision = 1
  AND f.puntaje_promedio_equiv_paes IS NOT NULL;

-- ----------------------------------------------------------------------------
-- Vista 3: Absorción Demográfica Externa (Cruce DataMart CNED con Demografía INE)
-- Responde directamente a la Pregunta de Negocio 3 (Capacidad regional RM vs jóvenes)
-- ----------------------------------------------------------------------------
CREATE VIEW IF NOT EXISTS vw_rm_absorcion_demografica_ine AS
SELECT 
    t.ano,
    p.poblacion_total AS pob_total_rm_ine,
    p.est_pob_18_24_rm AS pob_jovenes_18_24_rm_ine,
    SUM(f.vacantes) AS vacantes_totales_ofertadas_rm,
    SUM(f.matricula_primer_ano_total) AS matricula_1er_ano_efectiva_rm,
    ROUND((CAST(SUM(f.matricula_primer_ano_total) AS REAL) / p.est_pob_18_24_rm) * 100.0, 2) AS tasa_cobertura_demografica_pct,
    ROUND((CAST(SUM(f.vacantes) AS REAL) / p.est_pob_18_24_rm) * 100.0, 2) AS tasa_absorcion_potencial_vacantes_pct
FROM fact_matricula_admision f
INNER JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
LEFT JOIN dim_poblacion_rm p ON t.ano = p.ano
WHERE f.es_region_metropolitana = 1
GROUP BY t.ano, p.poblacion_total, p.est_pob_18_24_rm;

