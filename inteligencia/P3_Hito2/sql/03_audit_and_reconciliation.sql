-- ============================================================================
-- PROYECTO FINAL BUSINESS INTELLIGENCE - HITO 2
-- ROL: PERSONA 3 (ARQUITECTO DE BASES DE DATOS)
-- SCRIPT: 03_audit_and_reconciliation.sql
-- DESCRIPCIÓN: Consultas de auditoría, verificación y cuadre de integridad
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. CONTEO TOTAL DE REGISTROS DE HECHOS (Debe dar exactamente 158.211)
-- ----------------------------------------------------------------------------
SELECT 
    'fact_matricula_oferta' AS tabla,
    COUNT(*) AS total_registros,
    158211 AS valor_esperado,
    COUNT(*) - 158211 AS diferencia_filas
FROM fact_matricula_oferta;

-- ----------------------------------------------------------------------------
-- 2. AUDITORÍA DE MÉTRICAS ADITIVAS (Cuadre contra base fuente CSV)
-- ----------------------------------------------------------------------------
SELECT 
    SUM(matricula_primer_ano_total) AS total_matricula_primer_ano, -- Esperado: 5.186.123
    SUM(matricula_total) AS total_matricula_sistema,               -- Esperado: 17.696.782
    SUM(COALESCE(vacantes, 0)) AS total_vacantes_declaradas,       -- Esperado: 5.914.165
    COUNT(CASE WHEN vacantes IS NULL THEN 1 END) AS vacantes_nulas -- 25,4% esperado
FROM fact_matricula_oferta;

-- ----------------------------------------------------------------------------
-- 3. VERIFICACIÓN DE INTEGRIDAD REFERENCIAL (Cero Huérfanos)
-- ----------------------------------------------------------------------------
SELECT 
    'Huerfanos Tiempo' AS tipo_validacion,
    COUNT(*) AS registros_invalidos
FROM fact_matricula_oferta
WHERE id_tiempo NOT IN (SELECT id_tiempo FROM dim_tiempo)
UNION ALL
SELECT 
    'Huerfanos Geografia',
    COUNT(*)
FROM fact_matricula_oferta
WHERE id_geografia NOT IN (SELECT id_geografia FROM dim_geografia)
UNION ALL
SELECT 
    'Huerfanos Sede',
    COUNT(*)
FROM fact_matricula_oferta
WHERE id_sede NOT IN (SELECT id_sede FROM dim_sede)
UNION ALL
SELECT 
    'Huerfanos Institucion',
    COUNT(*)
FROM fact_matricula_oferta
WHERE id_institucion NOT IN (SELECT id_institucion FROM dim_institucion)
UNION ALL
SELECT 
    'Huerfanos Programa',
    COUNT(*)
FROM fact_matricula_oferta
WHERE id_programa NOT IN (SELECT id_programa FROM dim_programa);

-- ----------------------------------------------------------------------------
-- 4. VERIFICACIÓN DE CARDINALIDAD EN DIMENSIONES
-- ----------------------------------------------------------------------------
SELECT 'dim_tiempo' AS dimension, COUNT(*) AS filas FROM dim_tiempo
UNION ALL
SELECT 'dim_geografia (sin -1)', COUNT(*) FROM dim_geografia WHERE id_geografia != -1
UNION ALL
SELECT 'dim_sede (sin -1)', COUNT(*) FROM dim_sede WHERE id_sede != -1
UNION ALL
SELECT 'dim_institucion (sin -1)', COUNT(*) FROM dim_institucion WHERE id_institucion != -1
UNION ALL
SELECT 'dim_programa (sin -1)', COUNT(*) FROM dim_programa WHERE id_programa != -1
UNION ALL
SELECT 'dim_institucion_calidad_anual', COUNT(*) FROM dim_institucion_calidad_anual
UNION ALL
SELECT 'fact_poblacion_regional (INE)', COUNT(*) FROM fact_poblacion_regional;
