-- ============================================================================
-- PROYECTO FINAL BUSINESS INTELLIGENCE - HITO 2
-- ROL: PERSONA 3 (ARQUITECTO DE BASES DE DATOS)
-- SCRIPT: 02_views_powerbi.sql
-- DESCRIPCIÓN: Vistas semánticas analíticas pre-construidas para Power BI
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Vista 1: Modelo Completo Desnormalizado (Opción directa para Power BI)
-- ----------------------------------------------------------------------------
DROP VIEW IF EXISTS vw_datamart_matricula_completo;
CREATE VIEW vw_datamart_matricula_completo AS
SELECT 
    f.id_fact,
    t.ano,
    t.periodo_quinquenal,
    t.tipo_prueba_admision,
    t.flag_gratuidad_vigente,
    t.flag_reforma_nuble,
    
    g.region_codigo_subdere,
    g.region_nombre_estandar AS region_nombre,
    g.region_numero_romano AS region_romano,
    g.zona_geografica,
    
    s.nombre_sede,
    
    i.id_institucion,
    i.nombre_institucion,
    i.tipo_institucion,
    i.clasificacion2,
    i.codigo_ies,
    i.nombre_sies,
    
    c.acreditacion_cned,
    c.gratuidad_cned,
    c.autonomia_cned,
    c.acreditacion_sies,
    c.anos_acreditacion_sies,
    
    p.nombre_programa,
    p.carrera_generica,
    p.area_conocimiento,
    p.horario,
    p.tipo_programa,
    p.tipo_carrera,
    p.duracion_semestres,
    
    f.vacantes,
    f.matricula_primer_ano_total,
    f.matricula_primer_ano_hombres,
    f.matricula_primer_ano_mujeres,
    f.matricula_primer_ano_extranjeros,
    f.matricula_total,
    f.matricula_total_hombres,
    f.matricula_total_mujeres,
    f.matricula_total_extranjeros,
    
    f.puntaje_promedio_original,
    f.puntaje_promedio_norm_0_100,
    f.puntaje_promedio_equiv_paes,
    f.puntaje_promedio_zscore_anual,
    
    f.tasa_ocupacion_primer_ano,
    f.ratio_mujeres_primer_ano,
    f.ratio_extranjeros_total,
    f.flag_exige_prueba_admision,
    f.flag_vacantes_declaradas,
    f.flag_quiebre_nuble
FROM fact_matricula_oferta f
JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
JOIN dim_geografia g ON f.id_geografia = g.id_geografia
JOIN dim_sede s ON f.id_sede = s.id_sede
JOIN dim_institucion i ON f.id_institucion = i.id_institucion
JOIN dim_programa p ON f.id_programa = p.id_programa
LEFT JOIN dim_institucion_calidad_anual c ON f.id_institucion = c.id_institucion AND f.id_tiempo = c.id_tiempo;

-- ----------------------------------------------------------------------------
-- Vista 2: KPI Pregunta 1 - Equidad Territorial (Cruce Matrícula vs Población INE)
-- Matrícula 1er año por cada 1.000 habitantes de 15-64 años
-- ----------------------------------------------------------------------------
DROP VIEW IF EXISTS vw_kpi_p1_equidad_territorial;
CREATE VIEW vw_kpi_p1_equidad_territorial AS
WITH mat_regional AS (
    SELECT 
        f.id_tiempo,
        f.id_geografia,
        SUM(f.matricula_primer_ano_total) AS total_matricula_1er_ano,
        SUM(f.matricula_total) AS total_matricula
    FROM fact_matricula_oferta f
    GROUP BY f.id_tiempo, f.id_geografia
)
SELECT 
    t.ano,
    g.region_codigo_subdere,
    g.region_nombre_estandar AS region_nombre,
    g.zona_geografica,
    m.total_matricula_1er_ano,
    p.poblacion_total,
    p.poblacion_15_64,
    ROUND((m.total_matricula_1er_ano * 1000.0) / p.poblacion_15_64, 2) AS matricula_por_1000_hab_15_64
FROM mat_regional m
JOIN dim_tiempo t ON m.id_tiempo = t.id_tiempo
JOIN dim_geografia g ON m.id_geografia = g.id_geografia
JOIN fact_poblacion_regional p ON m.id_geografia = p.id_geografia AND m.id_tiempo = p.id_tiempo;

-- ----------------------------------------------------------------------------
-- Vista 3: KPI Pregunta 2 - Uso de Capacidad y Tasa de Ocupación
-- ----------------------------------------------------------------------------
DROP VIEW IF EXISTS vw_kpi_p2_capacidad_ocupacion;
CREATE VIEW vw_kpi_p2_capacidad_ocupacion AS
SELECT 
    t.ano,
    i.tipo_institucion,
    g.region_nombre_estandar AS region_nombre,
    SUM(CASE WHEN f.flag_vacantes_declaradas = 1 THEN f.vacantes ELSE 0 END) AS total_vacantes_declaradas,
    SUM(CASE WHEN f.flag_vacantes_declaradas = 1 THEN f.matricula_primer_ano_total ELSE 0 END) AS matricula_en_vacantes_declaradas,
    ROUND(
        (SUM(CASE WHEN f.flag_vacantes_declaradas = 1 THEN f.matricula_primer_ano_total ELSE 0 END) * 100.0) / 
        NULLIF(SUM(CASE WHEN f.flag_vacantes_declaradas = 1 THEN f.vacantes ELSE 0 END), 0), 
        2
    ) AS tasa_ocupacion_pct
FROM fact_matricula_oferta f
JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
JOIN dim_institucion i ON f.id_institucion = i.id_institucion
JOIN dim_geografia g ON f.id_geografia = g.id_geografia
GROUP BY t.ano, i.tipo_institucion, g.region_nombre_estandar;

-- ----------------------------------------------------------------------------
-- Vista 4: KPI Pregunta 3 - Calidad y Cobertura de Acreditación (SIES)
-- ----------------------------------------------------------------------------
DROP VIEW IF EXISTS vw_kpi_p3_calidad_acreditacion;
CREATE VIEW vw_kpi_p3_calidad_acreditacion AS
SELECT 
    t.ano,
    COALESCE(c.acreditacion_sies, 'Sin Información') AS estado_acreditacion,
    SUM(f.matricula_primer_ano_total) AS matricula_1er_ano,
    SUM(f.matricula_total) AS matricula_total,
    ROUND(AVG(c.anos_acreditacion_sies), 2) AS promedio_anos_acreditacion
FROM fact_matricula_oferta f
JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
JOIN dim_institucion i ON f.id_institucion = i.id_institucion
LEFT JOIN dim_institucion_calidad_anual c ON f.id_institucion = c.id_institucion AND f.id_tiempo = c.id_tiempo
GROUP BY t.ano, COALESCE(c.acreditacion_sies, 'Sin Información');
