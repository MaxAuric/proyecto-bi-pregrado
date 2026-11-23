"""
Script de Generación del Diagrama del Esquema Estrella Enriquecido (Región Metropolitana)
Autor: Persona 3 - Arquitecto Dimensional y Diccionario de Tasas/KPIs (Angel Pino)
Proyecto: Inteligencia de Negocios - Entrega Final (2012-2026)

Genera:
  1. diagrama_modelo_dimensional_estrella_rm.mmd (Mermaid Diagram formal)
  2. diagrama_modelo_dimensional_estrella_rm.svg (Gráfico vectorial escalable de alta definición)
  3. diagrama_modelo_dimensional_estrella_rm.png (Render de alta resolución 300 DPI)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_mermaid_code(output_dir):
    mmd_content = """erDiagram
    %% =========================================================================
    %% ESQUEMA ESTRELLA FORMAL ENRIQUECIDO — REGIÓN METROPOLITANA (2012-2026)
    %% Autor: Persona 3 (Angel Pino) — Cumplimiento Clase 4 DW y Feedback Hito 2
    %% =========================================================================

    DIM_TIEMPO_INE_RM ||--o{ FACT_MATRICULA_ADMISION : "1 a N (id_tiempo)"
    DIM_SEDE_GEOGRAFIA ||--o{ FACT_MATRICULA_ADMISION : "1 a N (id_sede_geografia)"
    DIM_INSTITUCION_SIES ||--o{ FACT_MATRICULA_ADMISION : "1 a N (id_institucion_sk SCD2)"
    DIM_CARRERA_PROGRAMA ||--o{ FACT_MATRICULA_ADMISION : "1 a N (id_carrera_programa_sk)"
    DIM_INSTITUCION_SIES ||--o{ AGG_RESUMEN_ANUAL_INSTITUCION_RM : "1 a N (Optimizacion OLAP)"
    PUENTE_INSTITUCION_SIES ||--o{ DIM_INSTITUCION_SIES : "Gobernanza CNED-SIES"

    DIM_TIEMPO_INE_RM {
        int id_tiempo PK "Año cronológico (2012-2026)"
        int ano "Año calendario"
        string periodo_admision "PSU (2012-20) | PDT (2021-22) | PAES (2023-26)"
        string rango_quinquenio "2012-2016 | 2017-2021 | 2022-2026"
        string estado_sanitario "Pre-Pandemia | COVID-19 | Post-Pandemia"
        int es_paes "1 si >= 2023 (Escala 100-1000)"
        int poblacion_total_rm "Población total RM (INE)"
        int poblacion_15_64_rm "Población 15 a 64 años RM (INE)"
        int poblacion_joven_18_24_rm "Población 18 a 24 años RM (INE)"
        float tasa_absorcion_juvenil_rm_pct "Matrícula 1er Año / Pob 18-24 RM %"
        float tasa_cobertura_bruta_rm_pct "Matrícula Total / Pob 18-24 RM %"
        float tasa_oferta_vacantes_1000_jovenes_rm "Vacantes por cada 1.000 jóvenes"
        float tasa_ocupacion_anual_rm_pct "Ocupación de vacantes anual RM %"
        float tasa_crecimiento_matricula_rm_yoy_pct "Crecimiento anual matrícula %"
    }

    DIM_SEDE_GEOGRAFIA {
        int id_sede_geografia PK "Surrogate Key sede"
        string nombre_sede "Comuna o sede en Santiago"
        string region_codigo_subdere "Código SUBDERE ('13' = RM)"
        string region_nombre_estandar "Región Metropolitana de Santiago"
        string macro_zona "Región Metropolitana de Santiago"
        int es_region_metropolitana "1 = 100% Santiago"
        float tasa_ocupacion_historica_sede_pct "Ocupación histórica sede %"
        float tasa_sobredemanda_sede_pct "Ofertas con sobrecupo en sede %"
        float participacion_matricula_rm_sede_pct "Cuota de matrícula de la sede %"
        string nivel_saturacion_sede "1. Saturada | 2. Equilibrio | 3. Ociosa"
    }

    DIM_INSTITUCION_SIES {
        int id_institucion_sk PK "Surrogate Key SCD Tipo 2 (1.298 fotos)"
        int codigo_ies_sies "Código oficial SIES / MINEDUC"
        string nombre_institucion "Nombre canónico de la institución"
        string tipo_institucion "Universidad | IP | CFT | FF.AA."
        string subtipo_institucion "Sin prefijos regulatorios ni abreviaturas"
        string acreditacion_cned "Institución Acreditada / No Acreditada"
        float anos_acreditacion_sies "Años acreditados CNA/SIES (0 a 7)"
        float score_calidad_sies_pct "Score oficial de calidad (0% a 100%)"
        string tramo_acreditacion_sies "Excelencia | Avanzada | Básica | No Acred"
        string autonomia "Autónoma / En supervisión"
        string gratuidad "Adscrita / No Adscrita / No Aplica"
        int ano_vigencia "Año fotografía histórica (SCD Tipo 2)"
        float tasa_ocupacion_inst_anual_pct "Ocupación anual institucional %"
        float tasa_programas_sobredemanda_inst_pct "Carreras con sobrecupo %"
        float cuota_mercado_matricula_rm_pct "Market Share matrícula RM %"
        float tasa_permanencia_cohortes_sup_pct "Retención de cursos superiores %"
        string posicionamiento_competitivo_rm "Cuadrante Calidad vs Demanda"
    }

    DIM_CARRERA_PROGRAMA {
        int id_carrera_programa_sk PK "Surrogate Key del programa (5.184 filas)"
        string nombre_programa "Plan de estudios curricular"
        string carrera_generica "Agrupador genérico oficial CNED"
        string area_conocimiento "11 áreas CNED (sin abreviaturas)"
        string es_area_stem "STEM vs Otras Áreas"
        string tipo_carrera "Profesional c/ Lic | Técnica Superior"
        string tipo_programa "Plan Regular | Trabajadores"
        string horario "Diurno | Vespertino | A Distancia"
        string titulo "Título profesional / técnico"
        string grado_academico "Sin abreviatura M/ (con Mención en)"
        int duracion_semestres "Duración teórica formal"
        float tasa_ocupacion_historica_prog_pct "Ocupación acumulada programa %"
        float tasa_frecuencia_sobredemanda_prog_pct "Años con sobrecupo %"
        float tasa_presion_lab_base35_prog_pct "Presión módulos lab base 35 %"
        string clasificacion_presion_capacidad "Sobredemanda | Óptima | Subutilizada"
    }

    FACT_MATRICULA_ADMISION {
        int id_fact PK "Clave primaria atómica subrogada"
        int id_tiempo FK "Año de corte (FK dim_tiempo_ine_rm)"
        int id_sede_geografia FK "Sede física (FK dim_sede_geografia)"
        int id_institucion_sk FK "Estado IES (FK dim_institucion_sies SCD2)"
        int id_carrera_programa_sk FK "Programa (FK dim_carrera_programa)"
        int es_region_metropolitana "Flag 1 = Región Metropolitana"
        int flag_exige_prueba_admision "Flag 1 = Prueba válida reportada"
        int flag_vacantes_declaradas "Flag 1 = Vacantes > 0"
        int flag_sobredemanda_critica "Flag 1 = Matrícula > Vacantes"
        int codigo_estado_ocupacion "1=Sobrecupo, 2=Óptima, 3=Subcupo, 4=Sin vac."
        int vacantes "Capacidad declarada (Aditiva)"
        int matricula_primer_ano_total "Matrícula nueva (Aditiva)"
        int matricula_total "Matrícula total vigente (Aditiva)"
        int mat_primer_ano_hombres "Matrícula 1er año hombres (Aditiva)"
        int mat_primer_ano_mujeres "Matrícula 1er año mujeres (Aditiva)"
        int sobrecupo_neto_alumnos "Alumnos en sobrecupo (Aditiva)"
        int vacantes_ociosas_netas "Cupos ociosos no llenados (Aditiva)"
        int secciones_lab_planificadas_35 "Secciones lab de 35 presupuestadas"
        int secciones_lab_reales_35 "Secciones lab de 35 requeridas"
        int secciones_extra_por_sobrecupo "Paralelos extra forzados por sobrecupo"
        float tasa_saturacion_lab_35_pct "Matrícula / (Secciones * 35) %"
        float puntaje_promedio_equiv_paes "Puntaje promedio PAES (No Aditiva)"
        float puntaje_corte_ultimo_equiv_paes "Puntaje corte PAES (No Aditiva)"
        float tasa_ocupacion_primer_ano "Matrícula / Vacantes % (No Aditiva)"
        float tasa_sobredemanda_oferta_pct "Sobrecupo porcentual % (No Aditiva)"
        float tasa_renovacion_primer_ano_pct "Matrícula 1er Año / Total % (No Aditiva)"
        float tasa_retencion_aparente_pct "Permanencia superior % (No Aditiva)"
        float brecha_dispersa_max_min_paes "Máx PAES - Mín PAES (Heterogeneidad)"
        float tasa_heterogeneidad_paes_pct "Brecha / Promedio PAES %"
    }

    AGG_RESUMEN_ANUAL_INSTITUCION_RM {
        int ano PK "Año de agregación"
        string nombre_institucion PK "Institución resumida"
        string tipo_institucion "Tipo IES"
        string tramo_acreditacion_sies "Tramo SIES"
        int vacantes_totales_rm "Suma vacantes en Santiago"
        int matricula_primer_ano_rm "Suma matrícula nueva en Santiago"
        int matricula_total_rm "Suma matrícula total en Santiago"
        int secciones_extra_sobrecupo_rm "Suma secciones extra lab"
        float tasa_ocupacion_rm_pct "Ocupación agregada IES %"
        float cuota_mercado_rm_pct "Market share anual IES %"
    }

    PUENTE_INSTITUCION_SIES {
        string nombre_institucion_cned PK "Nombre original en INDICES CNED"
        int codigo_ies_sies "Código oficial SIES"
        string nombre_institucion_sies "Nombre canónico en SIES"
        string metodo_cruce "Directo | Homologado"
        string estado_cruce "Auditado y Certificado"
    }
"""
    mmd_path = os.path.join(output_dir, "diagrama_modelo_dimensional_estrella_rm.mmd")
    with open(mmd_path, "w", encoding="utf-8") as f:
        f.write(mmd_content)
    print(f"  [MMD Creado] {mmd_path}")

def generate_svg_diagram(output_dir):
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1560 1080" width="1560" height="1080" style="background:#F8FAFC; font-family:'Segoe UI', system-ui, -apple-system, sans-serif;">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="2" dy="5" stdDeviation="5" flood-color="#0F172A" flood-opacity="0.14"/>
    </filter>
    <filter id="shadow-accent" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="3" dy="6" stdDeviation="6" flood-color="#1E3A8A" flood-opacity="0.22"/>
    </filter>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#1D4ED8"/>
    </marker>
    <marker id="arrow-amber" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#D97706"/>
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#7C3AED"/>
    </marker>
  </defs>

  <!-- ===================================================================== -->
  <!-- TITULO Y METADATOS SUPERIORES                                         -->
  <!-- ===================================================================== -->
  <text x="780" y="42" text-anchor="middle" font-size="25" font-weight="800" fill="#0F172A" letter-spacing="-0.5">ESQUEMA ESTRELLA FORMAL ENRIQUECIDO (REGIÓN METROPOLITANA DE SANTIAGO)</text>
  <text x="780" y="68" text-anchor="middle" font-size="13.5" fill="#475569">
    DataMart BI 2012–2026 | 58.926 Ofertas Académicas (100% RM) | 69 IES Activas en 2026 | Arquitecto Dimensional: Persona 3 (Angel Pino)
  </text>
  
  <!-- BARRA DE LEYENDA -->
  <rect x="120" y="85" width="1320" height="36" rx="8" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#shadow)"/>
  
  <rect x="145" y="97" width="14" height="14" rx="3" fill="#1E3A8A"/>
  <text x="166" y="108" font-size="12" font-weight="700" fill="#1E293B">Tabla de Hechos (100% Numérica, Cero VARCHAR)</text>
  
  <rect x="475" y="97" width="14" height="14" rx="3" fill="#0F766E"/>
  <text x="496" y="108" font-size="12" font-weight="700" fill="#1E293B">Dimensiones Canónicas Enriquecidas con Tasas/KPIs</text>
  
  <rect x="850" y="97" width="14" height="14" rx="3" fill="#7C3AED"/>
  <text x="871" y="108" font-size="12" font-weight="700" fill="#1E293B">Fuentes Externas Integradas (INE RM y SIES Acreditación)</text>
  
  <rect x="1230" y="97" width="14" height="14" rx="3" fill="#D97706"/>
  <text x="1251" y="108" font-size="12" font-weight="700" fill="#1E293B">Tablas OLAP y Gobernanza</text>

  <!-- ===================================================================== -->
  <!-- TABLA CENTRAL: FACT_MATRICULA_ADMISION (100% NUMERICA)                -->
  <!-- ===================================================================== -->
  <g transform="translate(560, 260)" filter="url(#shadow-accent)">
    <!-- Cabecera -->
    <rect x="0" y="0" width="440" height="56" rx="8" fill="#1E3A8A"/>
    <text x="220" y="24" text-anchor="middle" font-size="16" font-weight="800" fill="#FFFFFF">FACT_MATRICULA_ADMISION</text>
    <text x="220" y="44" text-anchor="middle" font-size="11.5" fill="#BFDBFE">Grano: Programa × Sede × Horario × Año (58.926 filas RM, Cero VARCHAR)</text>
    
    <!-- Cuerpo -->
    <rect x="0" y="56" width="440" height="520" fill="#FFFFFF" stroke="#1E3A8A" stroke-width="2"/>
    
    <!-- Bloque PK y FKs -->
    <rect x="6" y="62" width="428" height="24" fill="#EFF6FF" rx="4"/>
    <text x="16" y="78" font-size="11" font-weight="800" fill="#1E40AF">PK</text>
    <text x="46" y="78" font-size="12" font-weight="700" fill="#0F172A">id_fact</text>
    <text x="350" y="78" font-size="11" fill="#64748B">INTEGER AUTO</text>

    <text x="16" y="102" font-size="11" font-weight="800" fill="#2563EB">FK</text>
    <text x="46" y="102" font-size="12" fill="#0F172A">id_tiempo</text>
    <text x="310" y="102" font-size="11" fill="#64748B">INTEGER (2012–26)</text>

    <text x="16" y="122" font-size="11" font-weight="800" fill="#2563EB">FK</text>
    <text x="46" y="122" font-size="12" fill="#0F172A">id_sede_geografia</text>
    <text x="310" y="122" font-size="11" fill="#64748B">INTEGER (22 sedes)</text>

    <text x="16" y="142" font-size="11" font-weight="800" fill="#2563EB">FK</text>
    <text x="46" y="142" font-size="12" fill="#0F172A">id_institucion_sk</text>
    <text x="290" y="142" font-size="11" fill="#64748B">INTEGER (SCD 2, 1.298)</text>

    <text x="16" y="162" font-size="11" font-weight="800" fill="#2563EB">FK</text>
    <text x="46" y="162" font-size="12" fill="#0F172A">id_carrera_programa_sk</text>
    <text x="290" y="162" font-size="11" fill="#64748B">INTEGER (5.184 prog.)</text>

    <line x1="10" y1="172" x2="430" y2="172" stroke="#E2E8F0" stroke-width="1.2"/>

    <!-- Flags numéricos -->
    <text x="16" y="190" font-size="10.5" font-weight="700" fill="#0D9488">FLAG</text>
    <text x="56" y="190" font-size="11" fill="#334155">es_region_metropolitana</text>
    <text x="345" y="190" font-size="11" fill="#64748B">INTEGER (1=RM)</text>

    <text x="16" y="208" font-size="10.5" font-weight="700" fill="#0D9488">FLAG</text>
    <text x="56" y="208" font-size="11" fill="#334155">flag_exige_prueba_admision | flag_vacantes</text>
    <text x="375" y="208" font-size="11" fill="#64748B">INTEGER</text>

    <text x="16" y="226" font-size="10.5" font-weight="700" fill="#0D9488">FLAG</text>
    <text x="56" y="226" font-size="11" fill="#334155">flag_sobredemanda_critica (Mat > Vac)</text>
    <text x="375" y="226" font-size="11" fill="#64748B">INTEGER</text>

    <line x1="10" y1="236" x2="430" y2="236" stroke="#E2E8F0" stroke-width="1.2"/>

    <!-- Medidas Aditivas Puras -->
    <text x="16" y="254" font-size="10.5" font-weight="800" fill="#15803D">MED (Aditiva)</text>
    <text x="120" y="254" font-size="11" font-weight="600" fill="#0F172A">vacantes | matricula_primer_ano_total</text>
    <text x="375" y="254" font-size="11" fill="#64748B">INTEGER</text>

    <text x="16" y="272" font-size="10.5" font-weight="800" fill="#15803D">MED (Aditiva)</text>
    <text x="120" y="272" font-size="11" font-weight="600" fill="#0F172A">matricula_total | mat_hombres / mujeres</text>
    <text x="375" y="272" font-size="11" fill="#64748B">INTEGER</text>

    <line x1="10" y1="282" x2="430" y2="282" stroke="#E2E8F0" stroke-width="1.2"/>

    <!-- Caso Capacidad Lab Base 35 (Feedback Profesor) -->
    <rect x="6" y="288" width="428" height="88" fill="#FEF3C7" rx="4"/>
    <text x="14" y="304" font-size="11" font-weight="800" fill="#B45309">★ GESTIÓN DE CAPACIDAD Y LABORATORIOS (BASE 35 PUESTOS)</text>
    
    <text x="16" y="322" font-size="10.5" font-weight="700" fill="#92400E">MED</text>
    <text x="52" y="322" font-size="11" fill="#78350F">secciones_lab_planificadas_35 = CEIL(vac/35)</text>
    <text x="375" y="322" font-size="11" fill="#92400E">INTEGER</text>

    <text x="16" y="338" font-size="10.5" font-weight="700" fill="#92400E">MED</text>
    <text x="52" y="338" font-size="11" fill="#78350F">secciones_lab_reales_35 = CEIL(mat_1er/35)</text>
    <text x="375" y="338" font-size="11" fill="#92400E">INTEGER</text>

    <text x="16" y="354" font-size="10.5" font-weight="700" fill="#92400E">MED</text>
    <text x="52" y="354" font-size="11" font-weight="700" fill="#78350F">secciones_extra_por_sobrecupo (Caso 120→140)</text>
    <text x="375" y="354" font-size="11" fill="#92400E">INTEGER</text>

    <text x="16" y="370" font-size="10.5" font-weight="700" fill="#92400E">TASA</text>
    <text x="52" y="370" font-size="11" font-weight="700" fill="#78350F">tasa_saturacion_lab_35_pct (Tope 100% saturado)</text>
    <text x="375" y="370" font-size="11" fill="#92400E">REAL (%)</text>

    <line x1="10" y1="382" x2="430" y2="382" stroke="#E2E8F0" stroke-width="1.2"/>

    <!-- Medidas No Aditivas (Puntajes PAES) -->
    <text x="16" y="400" font-size="10.5" font-weight="800" fill="#DC2626">NO ADITIVA</text>
    <text x="110" y="400" font-size="11" fill="#0F172A">puntaje_promedio_equiv_paes (100–1000)</text>
    <text x="380" y="400" font-size="11" fill="#64748B">REAL</text>

    <text x="16" y="418" font-size="10.5" font-weight="800" fill="#DC2626">NO ADITIVA</text>
    <text x="110" y="418" font-size="11" fill="#0F172A">puntaje_corte_ultimo_equiv_paes</text>
    <text x="380" y="418" font-size="11" fill="#64748B">REAL</text>

    <text x="16" y="436" font-size="10.5" font-weight="800" fill="#DC2626">NO ADITIVA</text>
    <text x="110" y="436" font-size="11" fill="#0F172A">brecha_dispersa_max_min_paes | heterogeneidad</text>
    <text x="380" y="436" font-size="11" fill="#64748B">REAL</text>

    <line x1="10" y1="446" x2="430" y2="446" stroke="#E2E8F0" stroke-width="1.2"/>

    <!-- Tasas Operativas No Aditivas (DIVIDE en DAX) -->
    <text x="16" y="464" font-size="10.5" font-weight="800" fill="#EA580C">TASA NO ADIT</text>
    <text x="120" y="464" font-size="11" font-weight="600" fill="#0F172A">tasa_ocupacion_primer_ano (Mat/Vac %)</text>
    <text x="375" y="464" font-size="11" fill="#64748B">REAL (%)</text>

    <text x="16" y="482" font-size="10.5" font-weight="800" fill="#EA580C">TASA NO ADIT</text>
    <text x="120" y="482" font-size="11" font-weight="600" fill="#0F172A">tasa_sobredemanda_oferta_pct (Exceso %)</text>
    <text x="375" y="482" font-size="11" fill="#64748B">REAL (%)</text>

    <text x="16" y="500" font-size="10.5" font-weight="800" fill="#EA580C">TASA NO ADIT</text>
    <text x="120" y="500" font-size="11" font-weight="600" fill="#0F172A">tasa_renovacion_primer_ano_pct (Nueva/Tot %)</text>
    <text x="375" y="500" font-size="11" fill="#64748B">REAL (%)</text>

    <text x="16" y="518" font-size="10.5" font-weight="800" fill="#EA580C">TASA NO ADIT</text>
    <text x="120" y="518" font-size="11" font-weight="600" fill="#0F172A">tasa_retencion_aparente_pct (Superior/Tot %)</text>
    <text x="375" y="518" font-size="11" fill="#64748B">REAL (%)</text>

    <rect x="0" y="540" width="440" height="36" fill="#F1F5F9"/>
    <text x="220" y="563" text-anchor="middle" font-size="11" font-weight="700" fill="#475569">
      ⚠ Justificación DAX: Se recalculan con DIVIDE() al agregar (Clase 4 DW Pág. 29)
    </text>
  </g>

  <!-- ===================================================================== -->
  <!-- DIMENSION 1: DIM_TIEMPO_INE_RM (NOROESTE)                             -->
  <!-- ===================================================================== -->
  <g transform="translate(60, 160)" filter="url(#shadow)">
    <rect x="0" y="0" width="420" height="46" rx="6" fill="#0F766E"/>
    <text x="210" y="22" text-anchor="middle" font-size="14.5" font-weight="800" fill="#FFFFFF">DIM_TIEMPO_INE_RM</text>
    <text x="210" y="38" text-anchor="middle" font-size="10.5" fill="#CCFBF1">15 Años (2012–2026) + Demografía Juvenil INE RM</text>
    
    <rect x="0" y="46" width="420" height="270" fill="#FFFFFF" stroke="#0F766E" stroke-width="1.8"/>

    <rect x="6" y="52" width="408" height="22" fill="#F0FDFA" rx="3"/>
    <text x="16" y="67" font-size="11" font-weight="800" fill="#0F766E">PK</text>
    <text x="46" y="67" font-size="11.5" font-weight="700" fill="#0F172A">id_tiempo (ano)</text>
    <text x="290" y="67" font-size="11" fill="#64748B">INTEGER [2012–2026]</text>

    <text x="16" y="90" font-size="11" fill="#334155">periodo_admision</text>
    <text x="280" y="90" font-size="11" fill="#64748B">PSU | PDT | PAES</text>

    <text x="16" y="110" font-size="11" fill="#334155">rango_quinquenio | estado_sanitario</text>
    <text x="280" y="110" font-size="11" fill="#64748B">Pre | COVID | Post</text>

    <text x="16" y="130" font-size="11" fill="#334155">es_paes (1 si año >= 2023)</text>
    <text x="320" y="130" font-size="11" fill="#64748B">INTEGER [0/1]</text>

    <line x1="10" y1="140" x2="410" y2="140" stroke="#CCFBF1" stroke-width="1.2"/>

    <!-- Fuente Externa 1: INE RM -->
    <rect x="6" y="146" width="408" height="42" fill="#F5F3FF" rx="4"/>
    <text x="14" y="161" font-size="10.5" font-weight="800" fill="#6D28D9">FUENTE EXTERNA 1: PROYECCIONES DEMOGRÁFICAS INE RM</text>
    <text x="16" y="178" font-size="11" fill="#4C1D95">poblacion_total_rm | poblacion_15_64_rm | pob_joven_18_24_rm</text>

    <line x1="10" y1="196" x2="410" y2="196" stroke="#E2E8F0" stroke-width="1.2"/>

    <!-- Tasas Macro Anuales RM -->
    <text x="16" y="214" font-size="11" font-weight="700" fill="#0F766E">tasa_absorcion_juvenil_rm_pct</text>
    <text x="270" y="214" font-size="10.5" fill="#64748B">(Mat 1er / Pob 18-24) * 100</text>

    <text x="16" y="234" font-size="11" font-weight="700" fill="#0F766E">tasa_cobertura_bruta_rm_pct</text>
    <text x="270" y="234" font-size="10.5" fill="#64748B">(Mat Tot / Pob 18-24) * 100</text>

    <text x="16" y="254" font-size="11" font-weight="700" fill="#0F766E">tasa_oferta_vacantes_1000_jovenes_rm</text>
    <text x="280" y="254" font-size="10.5" fill="#64748B">Vacantes por 1.000 jóvenes</text>

    <text x="16" y="274" font-size="11" font-weight="700" fill="#0F766E">tasa_ocupacion_anual_rm_pct</text>
    <text x="270" y="274" font-size="10.5" fill="#64748B">Benchmark anual Santiago %</text>

    <text x="16" y="294" font-size="11" font-weight="700" fill="#0F766E">tasa_crecimiento_matricula_rm_yoy_pct</text>
    <text x="280" y="294" font-size="10.5" fill="#64748B">Variación interanual %</text>

    <rect x="0" y="306" width="420" height="24" fill="#F0FDFA"/>
    <text x="210" y="322" text-anchor="middle" font-size="10.5" font-style="italic" fill="#0F766E">
      Jerarquía Temporal: Quinquenio > Período Admisión > Año
    </text>
  </g>

  <!-- ===================================================================== -->
  <!-- DIMENSION 2: DIM_SEDE_GEOGRAFIA (SUROESTE)                            -->
  <!-- ===================================================================== -->
  <g transform="translate(60, 520)" filter="url(#shadow)">
    <rect x="0" y="0" width="420" height="46" rx="6" fill="#0F766E"/>
    <text x="210" y="22" text-anchor="middle" font-size="14.5" font-weight="800" fill="#FFFFFF">DIM_SEDE_GEOGRAFIA</text>
    <text x="210" y="38" text-anchor="middle" font-size="10.5" fill="#CCFBF1">22 Sedes en RM | Desnormalizada según Clase 4 DW Pág. 62</text>
    
    <rect x="0" y="46" width="420" height="260" fill="#FFFFFF" stroke="#0F766E" stroke-width="1.8"/>

    <rect x="6" y="52" width="408" height="22" fill="#F0FDFA" rx="3"/>
    <text x="16" y="67" font-size="11" font-weight="800" fill="#0F766E">PK</text>
    <text x="46" y="67" font-size="11.5" font-weight="700" fill="#0F172A">id_sede_geografia</text>
    <text x="310" y="67" font-size="11" fill="#64748B">INTEGER AUTO</text>

    <text x="16" y="90" font-size="11" font-weight="600" fill="#334155">nombre_sede (Comuna/Campus)</text>
    <text x="270" y="90" font-size="11" fill="#64748B">SANTIAGO, LAS CONDES...</text>

    <text x="16" y="110" font-size="11" fill="#334155">region_codigo_subdere | region_romano</text>
    <text x="290" y="110" font-size="11" fill="#64748B">'13' | 'RM' (100% Santiago)</text>

    <text x="16" y="130" font-size="11" fill="#334155">region_nombre_estandar</text>
    <text x="235" y="130" font-size="10.5" fill="#64748B">Región Metropolitana de Santiago</text>

    <text x="16" y="150" font-size="11" fill="#334155">macro_zona | estado_territorial</text>
    <text x="250" y="150" font-size="10.5" fill="#64748B">Foco Estudio Metropolitano</text>

    <line x1="10" y1="160" x2="410" y2="160" stroke="#CCFBF1" stroke-width="1.2"/>

    <!-- Tasas de Sede -->
    <text x="16" y="180" font-size="11" font-weight="700" fill="#0F766E">tasa_ocupacion_historica_sede_pct</text>
    <text x="280" y="180" font-size="10.5" fill="#64748B">(Mat Sede / Vac Sede) * 100</text>

    <text x="16" y="200" font-size="11" font-weight="700" fill="#0F766E">tasa_sobredemanda_sede_pct</text>
    <text x="280" y="200" font-size="10.5" fill="#64748B">% ofertas con sobrecupo</text>

    <text x="16" y="220" font-size="11" font-weight="700" fill="#0F766E">participacion_matricula_rm_sede_pct</text>
    <text x="290" y="220" font-size="10.5" fill="#64748B">Cuota matrícula sede RM %</text>

    <rect x="6" y="230" width="408" height="26" fill="#FEF3C7" rx="3"/>
    <text x="14" y="247" font-size="10.5" font-weight="700" fill="#92400E">
      Semáforo: nivel_saturacion_sede (1. Saturada &gt;=95% | 2. Equilibrio | 3. Ociosa)
    </text>

    <rect x="0" y="280" width="420" height="26" fill="#F0FDFA"/>
    <text x="210" y="297" text-anchor="middle" font-size="10.5" font-style="italic" fill="#0F766E">
      Jerarquía Geográfica: Macro-zona > Región Santiago (13) > Sede / Comuna
    </text>
  </g>

  <!-- ===================================================================== -->
  <!-- DIMENSION 3: DIM_INSTITUCION_SIES (NORESTE - SCD TIPO 2)              -->
  <!-- ===================================================================== -->
  <g transform="translate(1080, 160)" filter="url(#shadow)">
    <rect x="0" y="0" width="420" height="46" rx="6" fill="#0F766E"/>
    <text x="210" y="22" text-anchor="middle" font-size="14.5" font-weight="800" fill="#FFFFFF">DIM_INSTITUCION_SIES [SCD TIPO 2]</text>
    <text x="210" y="38" text-anchor="middle" font-size="10.5" fill="#CCFBF1">1.298 Registros Históricos | 69 IES Activas en 2026</text>
    
    <rect x="0" y="46" width="420" height="340" fill="#FFFFFF" stroke="#0F766E" stroke-width="1.8"/>

    <rect x="6" y="52" width="408" height="22" fill="#F0FDFA" rx="3"/>
    <text x="16" y="67" font-size="11" font-weight="800" fill="#0F766E">PK</text>
    <text x="46" y="67" font-size="11.5" font-weight="700" fill="#0F172A">id_institucion_sk</text>
    <text x="260" y="67" font-size="11" fill="#64748B">INTEGER (Surrogate Key)</text>

    <text x="16" y="90" font-size="11" font-weight="600" fill="#334155">nombre_institucion (Canónico)</text>
    <text x="280" y="90" font-size="11" fill="#64748B">U. DE CHILE, PUC...</text>

    <text x="16" y="110" font-size="11" font-weight="700" fill="#0F766E">tipo_institucion (Cero Abreviaturas)</text>
    <text x="260" y="110" font-size="10.5" fill="#0F766E">Universidad | IP | CFT | FF.AA.</text>

    <text x="16" y="130" font-size="11" fill="#334155">subtipo_institucion (Cero Prefijos (a)/(b))</text>
    <text x="290" y="130" font-size="11" fill="#64748B">Limpieza 100%</text>

    <text x="16" y="150" font-size="11" fill="#334155">autonomia | gratuidad | ano_vigencia</text>
    <text x="280" y="150" font-size="11" fill="#64748B">Snapshot Anual SCD2</text>

    <line x1="10" y1="160" x2="410" y2="160" stroke="#CCFBF1" stroke-width="1.2"/>

    <!-- Fuente Externa 2: SIES Acreditación -->
    <rect x="6" y="166" width="408" height="52" fill="#F5F3FF" rx="4"/>
    <text x="14" y="181" font-size="10.5" font-weight="800" fill="#6D28D9">FUENTE EXTERNA 2: ACREDITACIÓN OFICIAL SIES / CNA</text>
    <text x="16" y="198" font-size="11" fill="#4C1D95">codigo_ies_sies | anos_acreditacion_sies (0 a 7 años)</text>
    <text x="16" y="213" font-size="11" font-weight="700" fill="#4C1D95">score_calidad_sies_pct (0–100%) | tramo_acreditacion_sies</text>

    <line x1="10" y1="226" x2="410" y2="226" stroke="#E2E8F0" stroke-width="1.2"/>

    <!-- Tasas Competitivas Institucionales -->
    <text x="16" y="244" font-size="11" font-weight="700" fill="#0F766E">tasa_ocupacion_inst_anual_pct</text>
    <text x="280" y="244" font-size="10.5" fill="#64748B">Llenado anual de cupos %</text>

    <text x="16" y="264" font-size="11" font-weight="700" fill="#0F766E">tasa_programas_sobredemanda_inst_pct</text>
    <text x="300" y="264" font-size="10.5" fill="#64748B">% carreras con sobrecupo</text>

    <text x="16" y="284" font-size="11" font-weight="700" fill="#0F766E">cuota_mercado_matricula_rm_pct</text>
    <text x="290" y="284" font-size="10.5" fill="#64748B">Market Share anual Santiago %</text>

    <text x="16" y="304" font-size="11" font-weight="700" fill="#0F766E">tasa_permanencia_cohortes_sup_pct</text>
    <text x="290" y="304" font-size="10.5" fill="#64748B">Retención cohortes sup. %</text>

    <rect x="6" y="316" width="408" height="28" fill="#EFF6FF" rx="3"/>
    <text x="14" y="334" font-size="10.5" font-weight="700" fill="#1E40AF">
      posicionamiento_competitivo_rm (Cuadrante Calidad SIES × Demanda)
    </text>

    <rect x="0" y="360" width="420" height="26" fill="#F0FDFA"/>
    <text x="210" y="377" text-anchor="middle" font-size="10.5" font-style="italic" fill="#0F766E">
      SCD Tipo 2: Preserva cambios de acreditación y gratuidad sin sobrescribir historia
    </text>
  </g>

  <!-- ===================================================================== -->
  <!-- DIMENSION 4: DIM_CARRERA_PROGRAMA (SURESTE)                           -->
  <!-- ===================================================================== -->
  <g transform="translate(1080, 560)" filter="url(#shadow)">
    <rect x="0" y="0" width="420" height="46" rx="6" fill="#0F766E"/>
    <text x="210" y="22" text-anchor="middle" font-size="14.5" font-weight="800" fill="#FFFFFF">DIM_CARRERA_PROGRAMA</text>
    <text x="210" y="38" text-anchor="middle" font-size="10.5" fill="#CCFBF1">5.184 Programas Curriculares en la RM</text>
    
    <rect x="0" y="46" width="420" height="310" fill="#FFFFFF" stroke="#0F766E" stroke-width="1.8"/>

    <rect x="6" y="52" width="408" height="22" fill="#F0FDFA" rx="3"/>
    <text x="16" y="67" font-size="11" font-weight="800" fill="#0F766E">PK</text>
    <text x="46" y="67" font-size="11.5" font-weight="700" fill="#0F172A">id_carrera_programa_sk</text>
    <text x="290" y="67" font-size="11" fill="#64748B">INTEGER (Surrogate Key)</text>

    <text x="16" y="90" font-size="11" font-weight="600" fill="#334155">nombre_programa (Plan de estudios)</text>
    <text x="290" y="90" font-size="11" fill="#64748B">Denominación oficial</text>

    <text x="16" y="110" font-size="11" fill="#334155">carrera_generica | area_conocimiento</text>
    <text x="280" y="110" font-size="11" fill="#64748B">11 Áreas oficiales CNED</text>

    <text x="16" y="130" font-size="11" fill="#334155">es_area_stem | tipo_carrera | horario</text>
    <text x="270" y="130" font-size="11" fill="#64748B">STEM vs Otras | Diurno/Vesp</text>

    <text x="16" y="150" font-size="11" fill="#334155">titulo | grado_academico (sin 'M/')</text>
    <text x="290" y="150" font-size="11" fill="#64748B">con Mención en...</text>

    <text x="16" y="170" font-size="11" fill="#334155">duracion_semestres | ingreso_directo</text>
    <text x="290" y="170" font-size="11" fill="#64748B">Duración teórica formal</text>

    <line x1="10" y1="180" x2="410" y2="180" stroke="#CCFBF1" stroke-width="1.2"/>

    <!-- Tasas de Presión Curricular -->
    <text x="16" y="200" font-size="11" font-weight="700" fill="#0F766E">tasa_ocupacion_historica_prog_pct</text>
    <text x="290" y="200" font-size="10.5" fill="#64748B">Ocupación histórica carrera %</text>

    <text x="16" y="220" font-size="11" font-weight="700" fill="#0F766E">tasa_frecuencia_sobredemanda_prog_pct</text>
    <text x="310" y="220" font-size="10.5" fill="#64748B">% de años con sobrecupo</text>

    <rect x="6" y="230" width="408" height="38" fill="#FEF3C7" rx="3"/>
    <text x="14" y="246" font-size="10.5" font-weight="800" fill="#92400E">
      tasa_presion_lab_base35_prog_pct = (Mat 1er Promedio / 35 puestos) * 100
    </text>
    <text x="14" y="261" font-size="10" fill="#78350F">
      Semáforo: clasificacion_presion_capacidad (Sobredemanda &gt;100% | Óptima | Subutilizada)
    </text>

    <text x="16" y="286" font-size="11" fill="#334155">promedio_historico_paes_prog</text>
    <text x="280" y="286" font-size="11" fill="#64748B">Selectividad acumulada</text>

    <rect x="0" y="326" width="420" height="30" fill="#F0FDFA"/>
    <text x="210" y="345" text-anchor="middle" font-size="10.5" font-style="italic" fill="#0F766E">
      Jerarquía Curricular: Área Conocimiento > Carrera Genérica > Programa > Horario
    </text>
  </g>

  <!-- ===================================================================== -->
  <!-- TABLAS COMPLEMENTARIAS: OLAP AGREGADA Y PUENTE SIES                   -->
  <!-- ===================================================================== -->
  <!-- 1. Tabla Agregada OLAP -->
  <g transform="translate(300, 840)" filter="url(#shadow)">
    <rect x="0" y="0" width="450" height="36" rx="6" fill="#D97706"/>
    <text x="225" y="22" text-anchor="middle" font-size="13" font-weight="800" fill="#FFFFFF">
      AGG_RESUMEN_ANUAL_INSTITUCION_RM (1.298 filas)
    </text>
    <rect x="0" y="36" width="450" height="96" fill="#FFFFFF" stroke="#D97706" stroke-width="1.5"/>
    <text x="14" y="55" font-size="10.5" fill="#78350F">PK: ano + nombre_institucion | Grano: Resumen anual por IES</text>
    <text x="14" y="73" font-size="10.5" fill="#334155">• vacantes_totales_rm | matricula_primer_ano_rm | matricula_total_rm</text>
    <text x="14" y="91" font-size="10.5" fill="#334155">• secciones_extra_sobrecupo_rm | tasa_ocupacion_rm_pct | cuota_mercado_rm_pct</text>
    <text x="14" y="112" font-size="10" font-weight="700" fill="#D97706">
      Cumple Clase 4 DW Pág. 63: Tabla agregada para aceleración analítica OLAP
    </text>
  </g>

  <!-- 2. Tabla Puente SIES -->
  <g transform="translate(810, 840)" filter="url(#shadow)">
    <rect x="0" y="0" width="450" height="36" rx="6" fill="#7C3AED"/>
    <text x="225" y="22" text-anchor="middle" font-size="13" font-weight="800" fill="#FFFFFF">
      PUENTE_INSTITUCION_SIES (259 IES Mapeadas)
    </text>
    <rect x="0" y="36" width="450" height="96" fill="#FFFFFF" stroke="#7C3AED" stroke-width="1.5"/>
    <text x="14" y="55" font-size="10.5" fill="#5B21B6">PK: nombre_institucion_cned | FK: codigo_ies_sies</text>
    <text x="14" y="73" font-size="10.5" fill="#334155">• metodo_cruce (Directo / Homologado) | estado_cruce (Certificado)</text>
    <text x="14" y="91" font-size="10.5" fill="#334155">• 98,25% cruce directo con código SIES en la RM (Pauta Oficial Pág. 3)</text>
    <text x="14" y="112" font-size="10" font-weight="700" fill="#7C3AED">
      Gobernanza de Datos: Conciliación histórica entre CNED INDICES y SIES CNA
    </text>
  </g>

  <!-- ===================================================================== -->
  <!-- LINEAS Y FLECHAS DE CONEXIÓN 1 A N (ESQUEMA ESTRELLA PURO)           -->
  <!-- ===================================================================== -->
  <!-- Tiempo -> Fact -->
  <path d="M 480 270 L 520 270 L 520 380 L 560 380" fill="none" stroke="#1D4ED8" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
  <rect x="495" y="315" width="50" height="20" rx="3" fill="#EFF6FF" stroke="#3B82F6"/>
  <text x="520" y="329" text-anchor="middle" font-size="10" font-weight="800" fill="#1E40AF">1 : N</text>

  <!-- Geografía -> Fact -->
  <path d="M 480 650 L 520 650 L 520 540 L 560 540" fill="none" stroke="#1D4ED8" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
  <rect x="495" y="585" width="50" height="20" rx="3" fill="#EFF6FF" stroke="#3B82F6"/>
  <text x="520" y="599" text-anchor="middle" font-size="10" font-weight="800" fill="#1E40AF">1 : N</text>

  <!-- Institución -> Fact -->
  <path d="M 1080 330 L 1040 330 L 1040 380 L 1000 380" fill="none" stroke="#1D4ED8" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
  <rect x="1015" y="345" width="50" height="20" rx="3" fill="#EFF6FF" stroke="#3B82F6"/>
  <text x="1040" y="359" text-anchor="middle" font-size="10" font-weight="800" fill="#1E40AF">1 : N</text>

  <!-- Carrera -> Fact -->
  <path d="M 1080 700 L 1040 700 L 1040 540 L 1000 540" fill="none" stroke="#1D4ED8" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
  <rect x="1015" y="615" width="50" height="20" rx="3" fill="#EFF6FF" stroke="#3B82F6"/>
  <text x="1040" y="629" text-anchor="middle" font-size="10" font-weight="800" fill="#1E40AF">1 : N</text>

  <!-- Conexión a Tabla Agregada -->
  <path d="M 700 780 L 700 810 L 525 810 L 525 840" fill="none" stroke="#D97706" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow-amber)"/>
  <text x="612" y="805" text-anchor="middle" font-size="9.5" font-weight="700" fill="#B45309">Agregación Anual OLAP</text>

  <!-- Conexión Puente -> Institución -->
  <path d="M 1035 840 L 1035 770 L 1200 770 L 1200 500" fill="none" stroke="#7C3AED" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow-purple)"/>
  <text x="1117" y="765" text-anchor="middle" font-size="9.5" font-weight="700" fill="#6D28D9">Puente Oficial SIES</text>

  <!-- PIE DE PAGINA -->
  <text x="780" y="1065" text-anchor="middle" font-size="12" fill="#64748B">
    Modelo Certificado: 0 Registros Huérfanos | 100% Integridad Referencial | 0 Columnas VARCHAR en Hechos (Clase 4 DW Pág. 62) | Generado el 16-Nov-2026
  </text>
</svg>
"""
    svg_path = os.path.join(output_dir, "diagrama_modelo_dimensional_estrella_rm.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"  [SVG Creado] {svg_path}")

def generate_png_diagram(output_dir):
    fig = plt.figure(figsize=(20, 13.5), dpi=300, facecolor='#F8FAFC')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#F8FAFC')
    
    # Titulo y Subtitulo
    ax.text(0.5, 0.97, "ESQUEMA ESTRELLA FORMAL ENRIQUECIDO — REGIÓN METROPOLITANA", 
            ha='center', va='center', fontsize=18, fontweight='heavy', color='#0F172A')
    ax.text(0.5, 0.945, "DataMart BI 2012–2026 | 58.926 Filas RM | 69 IES Activas en 2026 | Arquitecto: Persona 3 (Angel Pino)", 
            ha='center', va='center', fontsize=11, color='#475569')

    # Leyenda Superior
    leg_box = patches.FancyBboxPatch((0.08, 0.905), 0.84, 0.026, boxstyle="round,pad=0.005",
                                     facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=1.2, zorder=2)
    ax.add_patch(leg_box)
    ax.text(0.18, 0.918, "■ Tabla de Hechos (100% Numérica, 0 VARCHAR)", fontsize=9, fontweight='bold', color='#1E3A8A', ha='center', va='center')
    ax.text(0.45, 0.918, "■ Dimensiones Enriquecidas con Tasas/KPIs", fontsize=9, fontweight='bold', color='#0F766E', ha='center', va='center')
    ax.text(0.72, 0.918, "■ Fuentes Externas Integradas (INE y SIES)", fontsize=9, fontweight='bold', color='#7C3AED', ha='center', va='center')

    # 1. TABLA CENTRAL: FACT_MATRICULA_ADMISION
    f_box = patches.FancyBboxPatch((0.36, 0.28), 0.28, 0.60, boxstyle="round,pad=0.01",
                                   facecolor='#FFFFFF', edgecolor='#1E3A8A', lw=2.2, zorder=3)
    ax.add_patch(f_box)
    ax.add_patch(patches.FancyBboxPatch((0.36, 0.83), 0.28, 0.05, boxstyle="round,pad=0.01",
                                        facecolor='#1E3A8A', edgecolor='#1E3A8A', lw=2.2, zorder=4))
    ax.text(0.50, 0.86, "FACT_MATRICULA_ADMISION", ha='center', va='center', fontsize=12, fontweight='heavy', color='#FFFFFF', zorder=5)
    ax.text(0.50, 0.84, "Grano: Programa × Sede × Horario × Año (58.926 filas RM)", ha='center', va='center', fontsize=8, color='#BFDBFE', zorder=5)

    f_text = (
        "PK  id_fact [INTEGER AUTOINCREMENT]\n"
        "──────────────────────────────────────────\n"
        "FK  id_tiempo -> dim_tiempo_ine_rm (2012-26)\n"
        "FK  id_sede_geografia -> dim_sede_geografia\n"
        "FK  id_institucion_sk -> dim_institucion_sies\n"
        "FK  id_carrera_programa_sk -> dim_carrera\n"
        "──────────────────────────────────────────\n"
        "FLAGS: es_region_metropolitana = 1 (100% RM)\n"
        "       flag_exige_prueba | flag_vacantes\n"
        "       flag_sobredemanda_critica (Mat > Vac)\n"
        "──────────────────────────────────────────\n"
        "MEDIDAS ADITIVAS (SUM, COUNT):\n"
        " • vacantes | matricula_primer_ano_total\n"
        " • matricula_total | mat_hombres / mujeres\n"
        "──────────────────────────────────────────\n"
        "★ CAPACIDAD LABORATORIOS (BASE 35 PUESTOS):\n"
        " • secciones_lab_planificadas_35 = CEIL(vac/35)\n"
        " • secciones_lab_reales_35 = CEIL(mat_1er/35)\n"
        " • secciones_extra_por_sobrecupo (Caso 120->140)\n"
        " • tasa_saturacion_lab_35_pct (Tope 100% sat.)\n"
        "──────────────────────────────────────────\n"
        "NO ADITIVAS (Selectividad PAES 100-1000):\n"
        " • puntaje_promedio_equiv_paes (Ponderado DAX)\n"
        " • puntaje_corte_ultimo_equiv_paes\n"
        " • brecha_dispersa_max_min_paes | heterogeneidad\n"
        "──────────────────────────────────────────\n"
        "TASAS Y RATIOS OPERATIVOS (DIVIDE en DAX):\n"
        " • tasa_ocupacion_primer_ano (Mat/Vac %)\n"
        " • tasa_sobredemanda_oferta_pct (Exceso %)\n"
        " • tasa_renovacion_primer_ano_pct\n"
        " • tasa_retencion_aparente_pct (Superior/Tot %)\n"
        "──────────────────────────────────────────\n"
        "Cero columnas VARCHAR (Clase 4 DW Pág. 62)"
    )
    ax.text(0.368, 0.825, f_text, ha='left', va='top', fontsize=7.2, family='monospace', color='#0F172A', zorder=5)

    # 2. DIM_TIEMPO_INE_RM (NOROESTE)
    t_box = patches.FancyBboxPatch((0.04, 0.58), 0.28, 0.30, boxstyle="round,pad=0.01",
                                   facecolor='#FFFFFF', edgecolor='#0F766E', lw=2.0, zorder=3)
    ax.add_patch(t_box)
    ax.add_patch(patches.FancyBboxPatch((0.04, 0.84), 0.28, 0.04, boxstyle="round,pad=0.01",
                                        facecolor='#0F766E', edgecolor='#0F766E', lw=2.0, zorder=4))
    ax.text(0.18, 0.86, "DIM_TIEMPO_INE_RM (15 Años)", ha='center', va='center', fontsize=11, fontweight='bold', color='#FFFFFF', zorder=5)

    t_text = (
        "PK  id_tiempo (ano) [INTEGER 2012-2026]\n"
        "──────────────────────────────────────────\n"
        " • periodo_admision (PSU | PDT | PAES)\n"
        " • rango_quinquenio (2012-16, 17-21, 22-26)\n"
        " • estado_sanitario (Pre | COVID | Post)\n"
        " • es_paes (1 si >= 2023, escala 100-1000)\n"
        "──────────────────────────────────────────\n"
        "★ FUENTE EXTERNA 1: DEMOGRAFÍA INE RM\n"
        " • poblacion_total_rm | poblacion_15_64_rm\n"
        " • poblacion_joven_18_24_rm (Target Univ.)\n"
        "──────────────────────────────────────────\n"
        "TASAS Y KPIS MACRO ANUALES RM:\n"
        " • tasa_absorcion_juvenil_rm_pct (Mat/Pob 18-24)\n"
        " • tasa_cobertura_bruta_rm_pct (Tot/Pob 18-24)\n"
        " • tasa_oferta_vacantes_1000_jovenes_rm\n"
        " • tasa_ocupacion_anual_rm_pct (Benchmark RM)\n"
        " • tasa_crecimiento_matricula_rm_yoy_pct"
    )
    ax.text(0.048, 0.835, t_text, ha='left', va='top', fontsize=7.2, family='monospace', color='#0F172A', zorder=5)

    # 3. DIM_SEDE_GEOGRAFIA (SUROESTE)
    s_box = patches.FancyBboxPatch((0.04, 0.24), 0.28, 0.29, boxstyle="round,pad=0.01",
                                   facecolor='#FFFFFF', edgecolor='#0F766E', lw=2.0, zorder=3)
    ax.add_patch(s_box)
    ax.add_patch(patches.FancyBboxPatch((0.04, 0.49), 0.28, 0.04, boxstyle="round,pad=0.01",
                                        facecolor='#0F766E', edgecolor='#0F766E', lw=2.0, zorder=4))
    ax.text(0.18, 0.51, "DIM_SEDE_GEOGRAFIA (22 Sedes)", ha='center', va='center', fontsize=11, fontweight='bold', color='#FFFFFF', zorder=5)

    s_text = (
        "PK  id_sede_geografia [INTEGER AUTO]\n"
        "──────────────────────────────────────────\n"
        " • nombre_sede (SANTIAGO, LAS CONDES...)\n"
        " • region_codigo_subdere ('13' = RM)\n"
        " • region_nombre_estandar (Canónico)\n"
        " • macro_zona (Región Metropolitana)\n"
        " • es_region_metropolitana = 1\n"
        "──────────────────────────────────────────\n"
        "TASAS Y CAPACIDAD POR SEDE:\n"
        " • tasa_ocupacion_historica_sede_pct\n"
        " • tasa_sobredemanda_sede_pct\n"
        " • participacion_matricula_rm_sede_pct\n"
        " • nivel_saturacion_sede (Semáforo)\n"
        "   - 1. Sede Saturada (>=95%)\n"
        "   - 2. Sede en Equilibrio (80-95%)\n"
        "   - 3. Sede con Capacidad Ociosa (<80%)"
    )
    ax.text(0.048, 0.485, s_text, ha='left', va='top', fontsize=7.2, family='monospace', color='#0F172A', zorder=5)

    # 4. DIM_INSTITUCION_SIES (NORESTE - SCD TIPO 2)
    i_box = patches.FancyBboxPatch((0.68, 0.54), 0.28, 0.34, boxstyle="round,pad=0.01",
                                   facecolor='#FFFFFF', edgecolor='#0F766E', lw=2.0, zorder=3)
    ax.add_patch(i_box)
    ax.add_patch(patches.FancyBboxPatch((0.68, 0.84), 0.28, 0.04, boxstyle="round,pad=0.01",
                                        facecolor='#0F766E', edgecolor='#0F766E', lw=2.0, zorder=4))
    ax.text(0.82, 0.86, "DIM_INSTITUCION_SIES [SCD TIPO 2]", ha='center', va='center', fontsize=11, fontweight='bold', color='#FFFFFF', zorder=5)

    i_text = (
        "PK  id_institucion_sk [INTEGER] (1.298 fotos)\n"
        "    69 IES Activas en 2026 (35 U, 19 IP, 11 CFT, 4 FA)\n"
        "──────────────────────────────────────────\n"
        " • nombre_institucion (Nombre oficial canónico)\n"
        " • tipo_institucion (Universidad | IP | CFT | FFAA)\n"
        " • subtipo_institucion (Cero prefijos (a)/(b))\n"
        " • autonomia | gratuidad | ano_vigencia\n"
        "──────────────────────────────────────────\n"
        "★ FUENTE EXTERNA 2: SIES / CNA ACREDITACIÓN\n"
        " • codigo_ies_sies (Código oficial MINEDUC)\n"
        " • anos_acreditacion_sies (0 a 7 años)\n"
        " • score_calidad_sies_pct (0% a 100%)\n"
        " • tramo_acreditacion_sies (Excelencia|Avanz|Bás)\n"
        "──────────────────────────────────────────\n"
        "TASAS COMPETITIVAS INSTITUCIONALES:\n"
        " • tasa_ocupacion_inst_anual_pct\n"
        " • tasa_programas_sobredemanda_inst_pct\n"
        " • cuota_mercado_matricula_rm_pct (Market Share)\n"
        " • tasa_permanencia_cohortes_sup_pct\n"
        " • posicionamiento_competitivo_rm (4 Cuadrantes)"
    )
    ax.text(0.688, 0.835, i_text, ha='left', va='top', fontsize=7.2, family='monospace', color='#0F172A', zorder=5)

    # 5. DIM_CARRERA_PROGRAMA (SURESTE)
    c_box = patches.FancyBboxPatch((0.68, 0.19), 0.28, 0.31, boxstyle="round,pad=0.01",
                                   facecolor='#FFFFFF', edgecolor='#0F766E', lw=2.0, zorder=3)
    ax.add_patch(c_box)
    ax.add_patch(patches.FancyBboxPatch((0.68, 0.46), 0.28, 0.04, boxstyle="round,pad=0.01",
                                        facecolor='#0F766E', edgecolor='#0F766E', lw=2.0, zorder=4))
    ax.text(0.82, 0.48, "DIM_CARRERA_PROGRAMA (5.184 Prog)", ha='center', va='center', fontsize=11, fontweight='bold', color='#FFFFFF', zorder=5)

    c_text = (
        "PK  id_carrera_programa_sk [INTEGER AUTO]\n"
        "──────────────────────────────────────────\n"
        " • nombre_programa (Plan curricular formal)\n"
        " • carrera_generica (Agrupador CNED)\n"
        " • area_conocimiento (11 áreas canónicas)\n"
        " • es_area_stem (STEM vs Otras Áreas)\n"
        " • tipo_carrera | tipo_programa | horario\n"
        " • titulo | grado_academico (sin abreviatura M/)\n"
        " • duracion_semestres | ingreso_directo\n"
        "──────────────────────────────────────────\n"
        "TASAS Y PRESIÓN DE LABORATORIOS:\n"
        " • tasa_ocupacion_historica_prog_pct\n"
        " • tasa_frecuencia_sobredemanda_prog_pct\n"
        " • tasa_presion_lab_base35_prog_pct (Base 35)\n"
        " • clasificacion_presion_capacidad (Semáforo)\n"
        " • promedio_historico_paes_prog"
    )
    ax.text(0.688, 0.455, c_text, ha='left', va='top', fontsize=7.2, family='monospace', color='#0F172A', zorder=5)

    # TABLAS RESUMEN Y GOBERNANZA (INFERIOR)
    # Tabla Agregada OLAP
    agg_box = patches.FancyBboxPatch((0.15, 0.05), 0.32, 0.12, boxstyle="round,pad=0.008",
                                     facecolor='#FFFFFF', edgecolor='#D97706', lw=1.5, zorder=3)
    ax.add_patch(agg_box)
    ax.add_patch(patches.FancyBboxPatch((0.15, 0.14), 0.32, 0.03, boxstyle="round,pad=0.008",
                                        facecolor='#D97706', edgecolor='#D97706', lw=1.5, zorder=4))
    ax.text(0.31, 0.155, "AGG_RESUMEN_ANUAL_INSTITUCION_RM (1.298)", ha='center', va='center', fontsize=9, fontweight='bold', color='#FFFFFF', zorder=5)
    agg_txt = (
        "PK: ano + nombre_institucion (Clase 4 DW Pág. 63)\n"
        " • Resumen anual de vacantes, matrículas y secciones extra\n"
        " • Optimización OLAP de alta velocidad para Power BI"
    )
    ax.text(0.158, 0.13, agg_txt, ha='left', va='top', fontsize=7, family='monospace', color='#78350F', zorder=5)

    # Tabla Puente SIES
    pue_box = patches.FancyBboxPatch((0.53, 0.05), 0.32, 0.12, boxstyle="round,pad=0.008",
                                     facecolor='#FFFFFF', edgecolor='#7C3AED', lw=1.5, zorder=3)
    ax.add_patch(pue_box)
    ax.add_patch(patches.FancyBboxPatch((0.53, 0.14), 0.32, 0.03, boxstyle="round,pad=0.008",
                                        facecolor='#7C3AED', edgecolor='#7C3AED', lw=1.5, zorder=4))
    ax.text(0.69, 0.155, "PUENTE_INSTITUCION_SIES (259 Mapeadas)", ha='center', va='center', fontsize=9, fontweight='bold', color='#FFFFFF', zorder=5)
    pue_txt = (
        "PK: nombre_institucion_cned -> codigo_ies_sies\n"
        " • 98,25% cruce directo con código SIES (Pauta Pág. 3)\n"
        " • Auditoría formal de homologación CNED INDICES a SIES"
    )
    ax.text(0.538, 0.13, pue_txt, ha='left', va='top', fontsize=7, family='monospace', color='#4C1D95', zorder=5)

    # FLECHAS DE RELACION 1 A N
    arrow_props = dict(arrowstyle="->,head_length=0.4,head_width=0.3", color='#1D4ED8', lw=2.2)
    
    # Tiempo -> Fact
    ax.annotate("", xy=(0.36, 0.72), xytext=(0.32, 0.72), arrowprops=arrow_props, zorder=6)
    ax.text(0.34, 0.735, "1 : N", fontsize=9, fontweight='heavy', color='#1E40AF', ha='center')

    # Geografía -> Fact
    ax.annotate("", xy=(0.36, 0.40), xytext=(0.32, 0.40), arrowprops=arrow_props, zorder=6)
    ax.text(0.34, 0.415, "1 : N", fontsize=9, fontweight='heavy', color='#1E40AF', ha='center')

    # Institución -> Fact
    ax.annotate("", xy=(0.64, 0.72), xytext=(0.68, 0.72), arrowprops=arrow_props, zorder=6)
    ax.text(0.66, 0.735, "1 : N", fontsize=9, fontweight='heavy', color='#1E40AF', ha='center')

    # Carrera -> Fact
    ax.annotate("", xy=(0.64, 0.40), xytext=(0.68, 0.40), arrowprops=arrow_props, zorder=6)
    ax.text(0.66, 0.415, "1 : N", fontsize=9, fontweight='heavy', color='#1E40AF', ha='center')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    png_path = os.path.join(output_dir, "diagrama_modelo_dimensional_estrella_rm.png")
    plt.tight_layout()
    plt.savefig(png_path, dpi=300, facecolor='#F8FAFC', bbox_inches='tight')
    plt.close()
    print(f"  [PNG Creado] {png_path}")

if __name__ == "__main__":
    out_dir = r"a:\Descargassss\proyecto-bi-pregrado-main\proyecto-bi-pregrado-main\Final\P3_ARQUITECTO_MODELO_ESTRELLA\diagramas"
    os.makedirs(out_dir, exist_ok=True)
    print("Iniciando generación de diagramas del Esquema Estrella RM...")
    generate_mermaid_code(out_dir)
    generate_svg_diagram(out_dir)
    generate_png_diagram(out_dir)
    print("¡Diagramas del Esquema Estrella RM generados exitosamente!")

