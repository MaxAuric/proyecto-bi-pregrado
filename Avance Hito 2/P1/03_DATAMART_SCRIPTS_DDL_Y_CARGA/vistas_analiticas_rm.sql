-- ============================================================================
-- VISTAS ANALITICAS PARA POWER BI Y ANALISIS REGION METROPOLITANA
-- ROL: Persona 1 (Ingeniero de Datos / ETL y DataMart)
-- ============================================================================

-- VISTA 1: Analisis de Capacidad y Sobredemanda en la RM (Pregunta 1)
-- Identifica carreras con sobredemanda de matricula sobre vacantes y calculo de paralelos requeridos
CREATE VIEW IF NOT EXISTS vw_rm_sobredemanda_y_capacidad AS
SELECT 
    t.ano,
    i.nombre_institucion,
    i.tipo_institucion,
    i.clasificacion2,
    i.acreditacion,
    i.gratuidad,
    g.nombre_sede,
    c.carrera_generica,
    c.area_conocimiento,
    c.tipo_carrera,
    c.horario,
    f.flag_exige_prueba_admision,
    f.flag_vacantes_declaradas,
    f.vacantes,
    f.matricula_primer_ano_total,
    f.matricula_total,
    f.tasa_ocupacion_primer_ano,
    f.puntaje_promedio_equiv_paes,
    f.puntaje_corte_ultimo_equiv_paes,
    -- Detección de sobredemanda crítica
    CASE 
        WHEN f.flag_vacantes_declaradas = 1 AND f.matricula_primer_ano_total > f.vacantes THEN 1 
        ELSE 0 
    END AS flag_sobredemanda_critica,
    -- Número neto de estudiantes por sobre la capacidad declarada
    CASE 
        WHEN f.flag_vacantes_declaradas = 1 THEN (f.matricula_primer_ano_total - f.vacantes)
        ELSE NULL 
    END AS sobrecupo_estudiantes_neto,
    -- Estimación de paralelos requeridos (asumiendo 35 alumnos por aula de laboratorio estándar)
    CASE 
        WHEN f.matricula_primer_ano_total > 0 THEN CAST((f.matricula_primer_ano_total + 34) / 35 AS INTEGER)
        ELSE 0 
    END AS paralelos_laboratorio_estimados
FROM fact_matricula_admision f
JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
JOIN dim_sede_geografia g ON f.id_sede_geografia = g.id_sede_geografia
JOIN dim_institucion i ON f.id_institucion_sk = i.id_institucion_sk
JOIN dim_carrera_programa c ON f.id_carrera_programa_sk = c.id_carrera_programa_sk
WHERE f.es_region_metropolitana = 1;

-- VISTA 2: Selectividad y Evolucion de Puntajes PAES/PSU en la RM (Pregunta 2)
CREATE VIEW IF NOT EXISTS vw_rm_selectividad_puntajes AS
SELECT 
    t.ano,
    t.periodo_admision,
    i.nombre_institucion,
    i.tipo_institucion,
    c.carrera_generica,
    c.area_conocimiento,
    f.puntaje_promedio_original,
    f.puntaje_promedio_equiv_paes,
    f.puntaje_corte_primer_equiv_paes,
    f.puntaje_corte_ultimo_equiv_paes,
    f.puntaje_promedio_zscore_anual,
    f.vacantes,
    f.matricula_primer_ano_total,
    f.tasa_ocupacion_primer_ano
FROM fact_matricula_admision f
JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
JOIN dim_institucion i ON f.id_institucion_sk = i.id_institucion_sk
JOIN dim_carrera_programa c ON f.id_carrera_programa_sk = c.id_carrera_programa_sk
WHERE f.es_region_metropolitana = 1 AND f.flag_exige_prueba_admision = 1;

