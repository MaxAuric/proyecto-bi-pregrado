"""
Script de Generación del Diagrama del Modelo Dimensional (Esquema Estrella)
Autor: Persona 3 - Arquitecto de Datos y Modelador Dimensional (Angel Pino)
Proyecto: Inteligencia de Negocios - Hito 2 (2012-2026)
Genera:
  1. diagrama_modelo_dimensional_estrella.png (Alta Resolución 300 DPI)
  2. diagrama_modelo_dimensional_estrella.svg (Vectorial Escalable)
  3. diagrama_modelo_dimensional_estrella.mmd (Mermaid Diagram)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def create_star_diagram(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # -------------------------------------------------------------
    # 1. GENERAR ARCHIVO MERMAID (.mmd)
    # -------------------------------------------------------------
    mmd_content = """erDiagram
    DIM_TIEMPO ||--o{ FACT_MATRICULA_ADMISION : "1 a N (ano)"
    DIM_SEDE_GEOGRAFIA ||--o{ FACT_MATRICULA_ADMISION : "1 a N (id_sede)"
    DIM_INSTITUCION ||--o{ FACT_MATRICULA_ADMISION : "1 a N (id_institucion_sk SCD2)"
    DIM_CARRERA_PROGRAMA ||--o{ FACT_MATRICULA_ADMISION : "1 a N (id_carrera_sk)"
    DIM_POBLACION_RM ||--o{ FACT_MATRICULA_ADMISION : "1 a N (ano contexto INE)"

    DIM_TIEMPO {
        int id_tiempo PK "Año cronológico (2012-2026)"
        int ano "Año calendario de referencia"
        string periodo_admision "PSU | PDT | PAES"
        string rango_quinquenio "2012-2016 | 2017-2021 | 2022-2026"
        int es_pandemia "1 si año in (2020, 2021)"
        int es_paes "1 si año >= 2023"
    }

    DIM_SEDE_GEOGRAFIA {
        int id_sede_geografia PK "Clave subrogada geográfica"
        string nombre_sede "Sede institucional"
        string region_codigo_subdere "Código SUBDERE ('13'=RM)"
        string region_nombre_estandar "Nombre oficial región"
        string macro_zona "Norte | Centro | RM | Sur | Austral"
        int es_region_metropolitana "1 si SUBDERE='13'"
        int flag_quiebre_nuble "1 si Ñuble pre-2018"
    }

    DIM_INSTITUCION {
        int id_institucion_sk PK "Surrogate Key SCD Tipo 2"
        string nombre_institucion "Nombre canónico IES"
        string tipo_institucion "Universidad | IP | CFT"
        string acreditacion "Acreditada | No Acreditada (SCD2)"
        string autonomia "Autónoma | En supervisión (SCD2)"
        string gratuidad "Adscrita | No Adscrita (SCD2)"
        int ano_vigencia "Año de vigencia histórica"
    }

    DIM_CARRERA_PROGRAMA {
        int id_carrera_programa_sk PK "Surrogate Key de programa"
        string nombre_programa "Nombre oficial del plan"
        string carrera_generica "Agrupador nacional genérico"
        string area_conocimiento "11 áreas oficiales CNED"
        string tipo_carrera "Profesional c/ Lic | Técnica"
        string tipo_programa "Plan Regular | Trabajador"
        string horario "Diurno | Vespertino | A distancia"
        int duracion_semestres "Duración teórica"
    }

    DIM_POBLACION_RM {
        int ano PK "Año calendario (2002-2035)"
        string region_codigo_subdere "Código '13' (RM)"
        int poblacion_total "Población total RM (INE)"
        int poblacion_15_64 "Población laboral 15-64"
        int est_pob_18_24_rm "Proxy demográfico 18-24 (14%)"
    }

    FACT_MATRICULA_ADMISION {
        int id_fact PK "Clave atómica subrogada"
        int id_tiempo FK "Año de corte"
        int id_sede_geografia FK "Sede física"
        int id_institucion_sk FK "Estado IES (SCD 2)"
        int id_carrera_programa_sk FK "Programa académico"
        int flag_exige_prueba_admision "1 si exige PSU/PAES"
        int flag_vacantes_declaradas "1 si vacantes > 0"
        int es_region_metropolitana "1 si pertenece a RM"
        int vacantes "Capacidad formal declarada"
        int matricula_primer_ano_total "Matrícula nueva ingresada"
        int matricula_total "Matrícula global vigente"
        float puntaje_promedio_equiv_paes "Promedio escala PAES"
        float puntaje_corte_ultimo_equiv_paes "Puntaje de corte PAES"
        float tasa_ocupacion_primer_ano "Ratio Matrícula/Vacantes %"
    }
"""
    mmd_path = os.path.join(output_dir, "diagrama_modelo_dimensional_estrella.mmd")
    with open(mmd_path, "w", encoding="utf-8") as f:
        f.write(mmd_content)
    print(f"  [MMD Creado] {mmd_path}")

    # -------------------------------------------------------------
    # 2. GENERAR ARCHIVO VECTORIAL SVG DIRECTO
    # -------------------------------------------------------------
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 950" width="1400" height="950" style="background:#F8FAFC; font-family:'Segoe UI', Helvetica, Arial, sans-serif;">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="2" dy="4" stdDeviation="4" flood-color="#0F172A" flood-opacity="0.12"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#3B82F6"/>
    </marker>
    <marker id="arrow-teal" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0D9488"/>
    </marker>
  </defs>

  <!-- TITULO Y CABECERA -->
  <text x="700" y="45" text-anchor="middle" font-size="24" font-weight="bold" fill="#0F172A">MODELO DIMENSIONAL FORMAL (ESQUEMA ESTRELLA)</text>
  <text x="700" y="72" text-anchor="middle" font-size="14" fill="#475569">DataMart de Educación Superior (2012–2026) | Enfoque Estratégico: Región Metropolitana | Autor: Persona 3 (Angel Pino)</text>
  
  <!-- LEYENDA SUPERIOR -->
  <rect x="180" y="90" width="1040" height="34" rx="6" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#shadow)"/>
  <rect x="200" y="100" width="14" height="14" rx="3" fill="#1E3A8A"/>
  <text x="222" y="112" font-size="12" font-weight="600" fill="#334155">Tabla de Hechos Central (158.211 filas)</text>
  <rect x="500" y="100" width="14" height="14" rx="3" fill="#0F766E"/>
  <text x="522" y="112" font-size="12" font-weight="600" fill="#334155">Tablas de Dimensiones Canónicas</text>
  <rect x="790" y="100" width="14" height="14" rx="3" fill="#7C3AED"/>
  <text x="812" y="112" font-size="12" font-weight="600" fill="#334155">Dimensión Externa INE (Demografía)</text>
  <text x="1060" y="112" font-size="12" font-weight="bold" fill="#2563EB">Relación 1 a N (Estrella)</text>

  <!-- ----------------------------------------------------------------- -->
  <!-- TABLA CENTRAL: FACT_MATRICULA_ADMISION -->
  <!-- ----------------------------------------------------------------- -->
  <g transform="translate(500, 290)" filter="url(#shadow)">
    <!-- Cabecera -->
    <rect x="0" y="0" width="400" height="52" rx="8" fill="#1E3A8A"/>
    <text x="200" y="24" text-anchor="middle" font-size="16" font-weight="bold" fill="#FFFFFF">FACT_MATRICULA_ADMISION</text>
    <text x="200" y="42" text-anchor="middle" font-size="11" fill="#93C5FD">Grano: Programa × Sede × Horario × Año (158.211 filas)</text>
    <!-- Cuerpo -->
    <rect x="0" y="52" width="400" height="370" fill="#FFFFFF" stroke="#1E3A8A" stroke-width="1.5"/>
    
    <!-- Claves Primarias y Foráneas -->
    <rect x="5" y="58" width="390" height="24" fill="#EFF6FF"/>
    <text x="15" y="74" font-size="12" font-weight="bold" fill="#1E40AF">PK</text>
    <text x="45" y="74" font-size="12" font-weight="bold" fill="#0F172A">id_fact</text>
    <text x="320" y="74" font-size="11" fill="#64748B">INTEGER AUTO</text>

    <text x="15" y="98" font-size="11" font-weight="bold" fill="#2563EB">FK</text>
    <text x="45" y="98" font-size="12" fill="#0F172A">id_tiempo</text>
    <text x="320" y="98" font-size="11" fill="#64748B">INTEGER (Año)</text>

    <text x="15" y="118" font-size="11" font-weight="bold" fill="#2563EB">FK</text>
    <text x="45" y="118" font-size="12" fill="#0F172A">id_sede_geografia</text>
    <text x="320" y="118" font-size="11" fill="#64748B">INTEGER</text>

    <text x="15" y="138" font-size="11" font-weight="bold" fill="#2563EB">FK</text>
    <text x="45" y="138" font-size="12" fill="#0F172A">id_institucion_sk</text>
    <text x="280" y="138" font-size="11" fill="#64748B">INTEGER (SCD 2)</text>

    <text x="15" y="158" font-size="11" font-weight="bold" fill="#2563EB">FK</text>
    <text x="45" y="158" font-size="12" fill="#0F172A">id_carrera_programa_sk</text>
    <text x="320" y="158" font-size="11" fill="#64748B">INTEGER</text>

    <line x1="10" y1="168" x2="390" y2="168" stroke="#E2E8F0" stroke-width="1"/>

    <!-- Flags Degenerados -->
    <text x="15" y="186" font-size="11" font-weight="600" fill="#0D9488">FLAG</text>
    <text x="50" y="186" font-size="11" fill="#334155">flag_exige_prueba_admision</text>
    <text x="340" y="186" font-size="11" fill="#64748B">INTEGER</text>

    <text x="15" y="204" font-size="11" font-weight="600" fill="#0D9488">FLAG</text>
    <text x="50" y="204" font-size="11" fill="#334155">flag_vacantes_declaradas</text>
    <text x="340" y="204" font-size="11" fill="#64748B">INTEGER</text>

    <text x="15" y="222" font-size="11" font-weight="600" fill="#0D9488">FLAG</text>
    <text x="50" y="222" font-size="11" fill="#334155">es_region_metropolitana</text>
    <text x="340" y="222" font-size="11" fill="#64748B">INTEGER</text>

    <line x1="10" y1="232" x2="390" y2="232" stroke="#E2E8F0" stroke-width="1"/>

    <!-- Medidas Aditivas -->
    <text x="15" y="250" font-size="11" font-weight="bold" fill="#15803D">MED (Aditiva)</text>
    <text x="110" y="250" font-size="11" fill="#0F172A">vacantes</text>
    <text x="330" y="250" font-size="11" fill="#64748B">INTEGER</text>

    <text x="15" y="268" font-size="11" font-weight="bold" fill="#15803D">MED (Aditiva)</text>
    <text x="110" y="268" font-size="11" fill="#0F172A">matricula_primer_ano_total</text>
    <text x="330" y="268" font-size="11" fill="#64748B">INTEGER</text>

    <text x="15" y="286" font-size="11" font-weight="bold" fill="#15803D">MED (Aditiva)</text>
    <text x="110" y="286" font-size="11" fill="#0F172A">matricula_total</text>
    <text x="330" y="286" font-size="11" fill="#64748B">INTEGER</text>

    <text x="15" y="304" font-size="11" font-weight="bold" fill="#15803D">MED (Aditiva)</text>
    <text x="110" y="304" font-size="11" fill="#0F172A">mat_1er_ano_hombres / mujeres</text>
    <text x="330" y="304" font-size="11" fill="#64748B">INTEGER</text>

    <line x1="10" y1="314" x2="390" y2="314" stroke="#E2E8F0" stroke-width="1"/>

    <!-- Medidas No Aditivas -->
    <text x="15" y="332" font-size="11" font-weight="bold" fill="#B91C1C">MED (No Aditiva)</text>
    <text x="125" y="332" font-size="11" fill="#0F172A">puntaje_promedio_equiv_paes</text>
    <text x="340" y="332" font-size="11" fill="#64748B">REAL</text>

    <text x="15" y="350" font-size="11" font-weight="bold" fill="#B91C1C">MED (No Aditiva)</text>
    <text x="125" y="350" font-size="11" fill="#0F172A">puntaje_corte_ultimo_equiv_paes</text>
    <text x="340" y="350" font-size="11" fill="#64748B">REAL</text>

    <text x="15" y="368" font-size="11" font-weight="bold" fill="#B91C1C">MED (No Aditiva)</text>
    <text x="125" y="368" font-size="11" fill="#0F172A">puntaje_promedio_zscore_anual</text>
    <text x="340" y="368" font-size="11" fill="#64748B">REAL</text>

    <line x1="10" y1="378" x2="390" y2="378" stroke="#E2E8F0" stroke-width="1"/>

    <!-- Ratios Semi-Aditivos -->
    <text x="15" y="396" font-size="11" font-weight="bold" fill="#C2410C">RATIO (Semi-Adit)</text>
    <text x="135" y="396" font-size="11" fill="#0F172A">tasa_ocupacion_primer_ano</text>
    <text x="340" y="396" font-size="11" fill="#64748B">REAL (%)</text>

    <text x="15" y="414" font-size="11" font-weight="bold" fill="#C2410C">RATIO (Semi-Adit)</text>
    <text x="135" y="414" font-size="11" fill="#0F172A">ratio_mujeres_primer_ano</text>
    <text x="340" y="414" font-size="11" fill="#64748B">REAL (%)</text>
  </g>

  <!-- ----------------------------------------------------------------- -->
  <!-- DIMENSION 1: DIM_TIEMPO (NOROESTE) -->
  <!-- ----------------------------------------------------------------- -->
  <g transform="translate(60, 160)" filter="url(#shadow)">
    <rect x="0" y="0" width="320" height="40" rx="6" fill="#0F766E"/>
    <text x="160" y="24" text-anchor="middle" font-size="14" font-weight="bold" fill="#FFFFFF">DIM_TIEMPO (15 filas)</text>
    <rect x="0" y="40" width="320" height="150" fill="#FFFFFF" stroke="#0F766E" stroke-width="1.5"/>

    <rect x="5" y="46" width="310" height="22" fill="#F0FDFA"/>
    <text x="15" y="61" font-size="11" font-weight="bold" fill="#0F766E">PK</text>
    <text x="45" y="61" font-size="12" font-weight="bold" fill="#0F172A">id_tiempo (ano)</text>
    <text x="240" y="61" font-size="11" fill="#64748B">INTEGER [2012-26]</text>

    <text x="15" y="83" font-size="11" fill="#334155">periodo_admision</text>
    <text x="240" y="83" font-size="11" fill="#64748B">PSU | PDT | PAES</text>

    <text x="15" y="103" font-size="11" fill="#334155">rango_quinquenio</text>
    <text x="240" y="103" font-size="11" fill="#64748B">2012-16, 17-21, 22-26</text>

    <text x="15" y="123" font-size="11" fill="#334155">es_pandemia</text>
    <text x="240" y="123" font-size="11" fill="#64748B">1 en 2020-21, 0 resto</text>

    <text x="15" y="143" font-size="11" fill="#334155">es_paes</text>
    <text x="240" y="143" font-size="11" fill="#64748B">1 si >= 2023, 0 resto</text>

    <text x="15" y="168" font-size="11" font-style="italic" fill="#0D9488">Jerarquía: Quinquenio &gt; Período &gt; Año</text>
  </g>

  <!-- ----------------------------------------------------------------- -->
  <!-- DIMENSION 2: DIM_SEDE_GEOGRAFIA (SUROESTE) -->
  <!-- ----------------------------------------------------------------- -->
  <g transform="translate(60, 480)" filter="url(#shadow)">
    <rect x="0" y="0" width="320" height="40" rx="6" fill="#0F766E"/>
    <text x="160" y="24" text-anchor="middle" font-size="14" font-weight="bold" fill="#FFFFFF">DIM_SEDE_GEOGRAFIA (116 filas)</text>
    <rect x="0" y="40" width="320" height="210" fill="#FFFFFF" stroke="#0F766E" stroke-width="1.5"/>

    <rect x="5" y="46" width="310" height="22" fill="#F0FDFA"/>
    <text x="15" y="61" font-size="11" font-weight="bold" fill="#0F766E">PK</text>
    <text x="45" y="61" font-size="12" font-weight="bold" fill="#0F172A">id_sede_geografia</text>
    <text x="240" y="61" font-size="11" fill="#64748B">INTEGER AUTO</text>

    <text x="15" y="83" font-size="11" fill="#334155">nombre_sede</text>
    <text x="230" y="83" font-size="11" fill="#64748B">SANTIAGO, MAIPÚ...</text>

    <text x="15" y="103" font-size="11" fill="#334155">region_codigo_subdere</text>
    <text x="250" y="103" font-size="11" fill="#64748B">'13' (RM), '01'-'16'</text>

    <text x="15" y="123" font-size="11" fill="#334155">region_nombre_estandar</text>
    <text x="230" y="123" font-size="11" fill="#64748B">Nombre canónico</text>

    <text x="15" y="143" font-size="11" fill="#334155">macro_zona</text>
    <text x="240" y="143" font-size="11" fill="#64748B">Norte, Centro, RM...</text>

    <text x="15" y="163" font-size="11" fill="#334155">es_region_metropolitana</text>
    <text x="250" y="163" font-size="11" fill="#64748B">1 si RM, 0 resto</text>

    <text x="15" y="183" font-size="11" fill="#334155">flag_quiebre_nuble</text>
    <text x="250" y="183" font-size="11" fill="#64748B">1 pre-2018 (Ley)</text>

    <text x="15" y="215" font-size="11" font-style="italic" fill="#0D9488">Jerarquía: Macro-zona &gt; Región &gt; Sede</text>
  </g>

  <!-- ----------------------------------------------------------------- -->
  <!-- DIMENSION 3: DIM_INSTITUCION (NORESTE - SCD TIPO 2) -->
  <!-- ----------------------------------------------------------------- -->
  <g transform="translate(1000, 160)" filter="url(#shadow)">
    <rect x="0" y="0" width="340" height="40" rx="6" fill="#0F766E"/>
    <text x="170" y="24" text-anchor="middle" font-size="14" font-weight="bold" fill="#FFFFFF">DIM_INSTITUCION [SCD TIPO 2]</text>
    <rect x="0" y="40" width="340" height="210" fill="#FFFFFF" stroke="#0F766E" stroke-width="1.5"/>

    <rect x="5" y="46" width="330" height="22" fill="#F0FDFA"/>
    <text x="15" y="61" font-size="11" font-weight="bold" fill="#0F766E">PK</text>
    <text x="45" y="61" font-size="12" font-weight="bold" fill="#0F172A">id_institucion_sk</text>
    <text x="240" y="61" font-size="11" fill="#64748B">INTEGER (1.994 filas)</text>

    <text x="15" y="83" font-size="11" fill="#334155">nombre_institucion</text>
    <text x="240" y="83" font-size="11" fill="#64748B">Nombre oficial IES</text>

    <text x="15" y="103" font-size="11" fill="#334155">tipo_institucion</text>
    <text x="240" y="103" font-size="11" fill="#64748B">Universidad | IP | CFT</text>

    <text x="15" y="123" font-size="11" font-weight="600" fill="#B45309">acreditacion (SCD2)</text>
    <text x="230" y="123" font-size="11" fill="#64748B">Acreditada / No Acred.</text>

    <text x="15" y="143" font-size="11" font-weight="600" fill="#B45309">autonomia (SCD2)</text>
    <text x="230" y="143" font-size="11" fill="#64748B">Autónoma / Supervisada</text>

    <text x="15" y="163" font-size="11" font-weight="600" fill="#B45309">gratuidad (SCD2)</text>
    <text x="230" y="163" font-size="11" fill="#64748B">Adscrita / No Adscrita</text>

    <rect x="5" y="174" width="330" height="20" fill="#FEF3C7"/>
    <text x="15" y="188" font-size="11" font-weight="bold" fill="#92400E">ano_vigencia (Snapshot)</text>
    <text x="240" y="188" font-size="11" fill="#92400E">2012 a 2026</text>

    <text x="15" y="215" font-size="11" font-style="italic" fill="#0D9488">Gobernanza: Preserva historia sin anacronismos</text>
  </g>

  <!-- ----------------------------------------------------------------- -->
  <!-- DIMENSION 4: DIM_CARRERA_PROGRAMA (SURESTE) -->
  <!-- ----------------------------------------------------------------- -->
  <g transform="translate(1000, 480)" filter="url(#shadow)">
    <rect x="0" y="0" width="340" height="40" rx="6" fill="#0F766E"/>
    <text x="170" y="24" text-anchor="middle" font-size="14" font-weight="bold" fill="#FFFFFF">DIM_CARRERA_PROGRAMA</text>
    <rect x="0" y="40" width="340" height="230" fill="#FFFFFF" stroke="#0F766E" stroke-width="1.5"/>

    <rect x="5" y="46" width="330" height="22" fill="#F0FDFA"/>
    <text x="15" y="61" font-size="11" font-weight="bold" fill="#0F766E">PK</text>
    <text x="45" y="61" font-size="12" font-weight="bold" fill="#0F172A">id_carrera_programa_sk</text>
    <text x="240" y="61" font-size="11" fill="#64748B">INTEGER (15.650)</text>

    <text x="15" y="83" font-size="11" fill="#334155">nombre_programa</text>
    <text x="220" y="83" font-size="11" fill="#64748B">Plan específico</text>

    <text x="15" y="103" font-size="11" fill="#334155">carrera_generica</text>
    <text x="220" y="103" font-size="11" fill="#64748B">284 genéricas únicas</text>

    <text x="15" y="123" font-size="11" fill="#334155">area_conocimiento</text>
    <text x="220" y="123" font-size="11" fill="#64748B">11 áreas oficiales</text>

    <text x="15" y="143" font-size="11" fill="#334155">tipo_carrera / tipo_programa</text>
    <text x="230" y="143" font-size="11" fill="#64748B">Regular / Especial</text>

    <text x="15" y="163" font-size="11" fill="#334155">horario</text>
    <text x="220" y="163" font-size="11" fill="#64748B">Diurno / Vespertino</text>

    <text x="15" y="183" font-size="11" fill="#334155">duracion_semestres</text>
    <text x="240" y="183" font-size="11" fill="#64748B">INTEGER</text>

    <text x="15" y="203" font-size="11" fill="#334155">ingreso_directo</text>
    <text x="230" y="203" font-size="11" fill="#64748B">'SI' / 'NO'</text>

    <text x="15" y="235" font-size="11" font-style="italic" fill="#0D9488">Jerarquía: Área &gt; Genérica &gt; Programa &gt; Horario</text>
  </g>

  <!-- ----------------------------------------------------------------- -->
  <!-- DIMENSION 5: DIM_POBLACION_RM (INFERIOR - FUENTE EXTERNA INE) -->
  <!-- ----------------------------------------------------------------- -->
  <g transform="translate(500, 770)" filter="url(#shadow)">
    <rect x="0" y="0" width="400" height="36" rx="6" fill="#6D28D9"/>
    <text x="200" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#FFFFFF">DIM_POBLACION_RM (Fuente Externa INE - 34 filas)</text>
    <rect x="0" y="36" width="400" height="95" fill="#FFFFFF" stroke="#6D28D9" stroke-width="1.5"/>

    <rect x="5" y="42" width="390" height="20" fill="#F5F3FF"/>
    <text x="15" y="56" font-size="11" font-weight="bold" fill="#6D28D9">PK</text>
    <text x="45" y="56" font-size="11" font-weight="bold" fill="#0F172A">ano</text>
    <text x="260" y="56" font-size="11" fill="#64748B">INTEGER [2002-2035]</text>

    <text x="15" y="76" font-size="11" fill="#334155">poblacion_total / poblacion_15_64</text>
    <text x="260" y="76" font-size="11" fill="#64748B">Censo 2017 INE RM</text>

    <text x="15" y="96" font-size="11" font-weight="600" fill="#6D28D9">est_pob_18_24_rm</text>
    <text x="250" y="96" font-size="11" fill="#6D28D9">Proxy 14% pob 15-64 RM (P3 Negocio)</text>

    <text x="15" y="118" font-size="10" font-style="italic" fill="#7C3AED">Responde P3: Capacidad de absorción de jóvenes en la RM</text>
  </g>

  <!-- ----------------------------------------------------------------- -->
  <!-- CONECTORES Y FLECHAS DE CARDINALIDAD (ESQUEMA ESTRELLA) -->
  <!-- ----------------------------------------------------------------- -->
  <!-- Tiempo -> Fact -->
  <path d="M 380 235 L 500 350" fill="none" stroke="#2563EB" stroke-width="2.5" marker-end="url(#arrow)"/>
  <text x="415" y="275" font-size="12" font-weight="bold" fill="#1E40AF">1 : N</text>

  <!-- Geografía -> Fact -->
  <path d="M 380 580 L 500 480" fill="none" stroke="#2563EB" stroke-width="2.5" marker-end="url(#arrow)"/>
  <text x="415" y="545" font-size="12" font-weight="bold" fill="#1E40AF">1 : N</text>

  <!-- Institución -> Fact -->
  <path d="M 1000 250 L 900 350" fill="none" stroke="#2563EB" stroke-width="2.5" marker-end="url(#arrow)"/>
  <text x="945" y="285" font-size="12" font-weight="bold" fill="#1E40AF">1 : N</text>

  <!-- Carrera -> Fact -->
  <path d="M 1000 580 L 900 480" fill="none" stroke="#2563EB" stroke-width="2.5" marker-end="url(#arrow)"/>
  <text x="945" y="545" font-size="12" font-weight="bold" fill="#1E40AF">1 : N</text>

  <!-- INE Población -> Fact (Contextual por Año) -->
  <path d="M 700 770 L 700 715" fill="none" stroke="#7C3AED" stroke-width="2.5" stroke-dasharray="6,4" marker-end="url(#arrow-teal)"/>
  <text x="710" y="745" font-size="12" font-weight="bold" fill="#6D28D9">Cruce por Año</text>

</svg>
"""
    svg_path = os.path.join(output_dir, "diagrama_modelo_dimensional_estrella.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"  [SVG Creado] {svg_path}")

    # -------------------------------------------------------------
    # 3. GENERAR ARCHIVO PNG EN ALTA RESOLUCIÓN MEDIANTE MATPLOTLIB
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')

    # Titulo
    ax.text(0.5, 0.965, "MODELO DIMENSIONAL FORMAL (ESQUEMA ESTRELLA)", 
            ha='center', va='center', fontsize=18, fontweight='bold', color='#0F172A')
    ax.text(0.5, 0.938, "DataMart de Educación Superior (2012–2026) | Enfoque RM | Rol: Persona 3 (Angel Pino - Arq. Datos)", 
            ha='center', va='center', fontsize=11, color='#475569')

    # Leyenda en la parte superior
    ax.add_patch(patches.Rectangle((0.15, 0.89), 0.70, 0.032, facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=1, zorder=2))
    ax.add_patch(patches.Rectangle((0.17, 0.896), 0.015, 0.02, facecolor='#1E3A8A', zorder=3))
    ax.text(0.19, 0.906, "Tabla de Hechos Central", fontsize=9, fontweight='bold', color='#334155', va='center')
    ax.add_patch(patches.Rectangle((0.37, 0.896), 0.015, 0.02, facecolor='#0F766E', zorder=3))
    ax.text(0.39, 0.906, "Dimensiones Canónicas (Estrella)", fontsize=9, fontweight='bold', color='#334155', va='center')
    ax.add_patch(patches.Rectangle((0.62, 0.896), 0.015, 0.02, facecolor='#6D28D9', zorder=3))
    ax.text(0.64, 0.906, "Dimensión Demográfica Externa (INE)", fontsize=9, fontweight='bold', color='#334155', va='center')

    # CAJA CENTRAL: FACT_MATRICULA_ADMISION
    # x: 0.36 a 0.64 (ancho 0.28), y: 0.28 a 0.78 (alto 0.50)
    fact_box = patches.FancyBboxPatch((0.36, 0.28), 0.28, 0.52, boxstyle="round,pad=0.01",
                                      facecolor='#FFFFFF', edgecolor='#1E3A8A', lw=2, zorder=3)
    ax.add_patch(fact_box)
    # Header Fact
    ax.add_patch(patches.FancyBboxPatch((0.36, 0.75), 0.28, 0.05, boxstyle="round,pad=0.01",
                                        facecolor='#1E3A8A', edgecolor='#1E3A8A', lw=2, zorder=4))
    ax.text(0.50, 0.78, "FACT_MATRICULA_ADMISION", ha='center', va='center', fontsize=12, fontweight='bold', color='#FFFFFF', zorder=5)
    ax.text(0.50, 0.76, "Grano: Programa × Sede × Horario × Año (158.211 filas)", ha='center', va='center', fontsize=8, color='#93C5FD', zorder=5)

    fact_text = (
        "PK  id_fact [INTEGER AUTOINCREMENT]\n"
        "───────────────────────────────────────\n"
        "FK  id_tiempo ──> dim_tiempo.id_tiempo\n"
        "FK  id_sede_geografia ──> dim_sede_geografia\n"
        "FK  id_institucion_sk ──> dim_institucion (SCD 2)\n"
        "FK  id_carrera_programa_sk ──> dim_carrera\n"
        "───────────────────────────────────────\n"
        "FLAGS DE NEGOCIO (DIM. DEGENERADAS):\n"
        " • flag_exige_prueba_admision (1/0)\n"
        " • flag_vacantes_declaradas (1/0)\n"
        " • es_region_metropolitana (1/0)\n"
        "───────────────────────────────────────\n"
        "MEDIDAS TOTALMENTE ADITIVAS:\n"
        " • vacantes (Cupos declarados)\n"
        " • matricula_primer_ano_total (Alumnos nuevos)\n"
        " • matricula_total (Alumnos vigentes)\n"
        " • mat_1er_ano_hombres / mujeres / extranj.\n"
        "───────────────────────────────────────\n"
        "MEDIDAS NO ADITIVAS (PROMEDIOS PAES):\n"
        " • puntaje_promedio_equiv_paes (100-1000)\n"
        " • puntaje_corte_ultimo_equiv_paes\n"
        " • puntaje_promedio_zscore_anual\n"
        "───────────────────────────────────────\n"
        "RATIOS SEMI-ADITIVOS (RECALCULAR EN DAX):\n"
        " • tasa_ocupacion_primer_ano (Matrícula/Vacantes %)\n"
        " • ratio_mujeres_primer_ano (%)"
    )
    ax.text(0.37, 0.735, fact_text, ha='left', va='top', fontsize=7.2, family='monospace', color='#0F172A', zorder=5)

    # DIM 1: TIEMPO (NOROESTE)
    t_box = patches.FancyBboxPatch((0.05, 0.62), 0.24, 0.22, boxstyle="round,pad=0.01",
                                   facecolor='#FFFFFF', edgecolor='#0F766E', lw=1.8, zorder=3)
    ax.add_patch(t_box)
    ax.add_patch(patches.FancyBboxPatch((0.05, 0.80), 0.24, 0.04, boxstyle="round,pad=0.01",
                                        facecolor='#0F766E', edgecolor='#0F766E', lw=1.8, zorder=4))
    ax.text(0.17, 0.82, "DIM_TIEMPO (15 filas)", ha='center', va='center', fontsize=10, fontweight='bold', color='#FFFFFF', zorder=5)
    t_text = (
        "PK  id_tiempo [INTEGER] (2012–2026)\n"
        "────────────────────────────────\n"
        " • ano (Año cronológico natural)\n"
        " • periodo_admision (PSU / PDT / PAES)\n"
        " • rango_quinquenio (2012-16, 17-21, 22-26)\n"
        " • es_pandemia (1 en 2020-2021)\n"
        " • es_paes (1 si >= 2023)\n"
        "────────────────────────────────\n"
        "Jerarquía: Quinquenio > Período > Año"
    )
    ax.text(0.06, 0.79, t_text, ha='left', va='top', fontsize=7.5, family='monospace', color='#0F172A', zorder=5)

    # DIM 2: SEDE Y GEOGRAFIA (SUROESTE)
    g_box = patches.FancyBboxPatch((0.05, 0.28), 0.24, 0.27, boxstyle="round,pad=0.01",
                                   facecolor='#FFFFFF', edgecolor='#0F766E', lw=1.8, zorder=3)
    ax.add_patch(g_box)
    ax.add_patch(patches.FancyBboxPatch((0.05, 0.51), 0.24, 0.04, boxstyle="round,pad=0.01",
                                        facecolor='#0F766E', edgecolor='#0F766E', lw=1.8, zorder=4))
    ax.text(0.17, 0.53, "DIM_SEDE_GEOGRAFIA (116 filas)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF', zorder=5)
    g_text = (
        "PK  id_sede_geografia [INTEGER AUTO]\n"
        "────────────────────────────────\n"
        " • nombre_sede (Sede institucional)\n"
        " • region_codigo_subdere ('13' = RM)\n"
        " • region_nombre_estandar (Oficial)\n"
        " • macro_zona (Norte, Centro, RM, Sur)\n"
        " • es_region_metropolitana (1 si RM)\n"
        " • flag_quiebre_nuble (1 pre-2018)\n"
        "────────────────────────────────\n"
        "Jerarquía: Macro-zona > Región > Sede"
    )
    ax.text(0.06, 0.50, g_text, ha='left', va='top', fontsize=7.5, family='monospace', color='#0F172A', zorder=5)

    # DIM 3: INSTITUCION (NORESTE - SCD TIPO 2)
    i_box = patches.FancyBboxPatch((0.71, 0.58), 0.24, 0.26, boxstyle="round,pad=0.01",
                                   facecolor='#FFFFFF', edgecolor='#0F766E', lw=1.8, zorder=3)
    ax.add_patch(i_box)
    ax.add_patch(patches.FancyBboxPatch((0.71, 0.80), 0.24, 0.04, boxstyle="round,pad=0.01",
                                        facecolor='#0F766E', edgecolor='#0F766E', lw=1.8, zorder=4))
    ax.text(0.83, 0.82, "DIM_INSTITUCION [SCD TIPO 2]", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF', zorder=5)
    i_text = (
        "PK  id_institucion_sk [INTEGER AUTO]\n"
        "    (1.994 estados históricos únicos)\n"
        "────────────────────────────────\n"
        " • nombre_institucion (Canónico)\n"
        " • tipo_institucion (Univ, IP, CFT)\n"
        " • acreditacion (Acred. / No Acred.)\n"
        " • autonomia (Autónoma / Supervisada)\n"
        " • gratuidad (Adscrita / No Adscrita)\n"
        " • ano_vigencia (Snapshot anual)\n"
        "────────────────────────────────\n"
        "SCD 2: Preserva historia sin anacronismo"
    )
    ax.text(0.72, 0.79, i_text, ha='left', va='top', fontsize=7.5, family='monospace', color='#0F172A', zorder=5)

    # DIM 4: CARRERA Y PROGRAMA (SURESTE)
    c_box = patches.FancyBboxPatch((0.71, 0.24), 0.24, 0.29, boxstyle="round,pad=0.01",
                                   facecolor='#FFFFFF', edgecolor='#0F766E', lw=1.8, zorder=3)
    ax.add_patch(c_box)
    ax.add_patch(patches.FancyBboxPatch((0.71, 0.49), 0.24, 0.04, boxstyle="round,pad=0.01",
                                        facecolor='#0F766E', edgecolor='#0F766E', lw=1.8, zorder=4))
    ax.text(0.83, 0.51, "DIM_CARRERA_PROGRAMA", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF', zorder=5)
    c_text = (
        "PK  id_carrera_programa_sk [INTEGER]\n"
        "    (15.650 programas únicos)\n"
        "────────────────────────────────\n"
        " • nombre_programa (Plan específico)\n"
        " • carrera_generica (284 canónicas)\n"
        " • area_conocimiento (11 áreas CNED)\n"
        " • tipo_carrera / tipo_programa\n"
        " • horario (Diurno / Vespertino)\n"
        " • duracion_semestres (Semestres teór.)\n"
        " • ingreso_directo (SI / NO)\n"
        "────────────────────────────────\n"
        "Jerarquía: Área > Carrera > Plan > Horario"
    )
    ax.text(0.72, 0.48, c_text, ha='left', va='top', fontsize=7.5, family='monospace', color='#0F172A', zorder=5)

    # DIM 5: DIM_POBLACION_RM (INFERIOR - INE)
    p_box = patches.FancyBboxPatch((0.36, 0.08), 0.28, 0.14, boxstyle="round,pad=0.01",
                                   facecolor='#FFFFFF', edgecolor='#6D28D9', lw=1.8, zorder=3)
    ax.add_patch(p_box)
    ax.add_patch(patches.FancyBboxPatch((0.36, 0.18), 0.28, 0.04, boxstyle="round,pad=0.01",
                                        facecolor='#6D28D9', edgecolor='#6D28D9', lw=1.8, zorder=4))
    ax.text(0.50, 0.20, "DIM_POBLACION_RM (Fuente Externa INE)", ha='center', va='center', fontsize=10, fontweight='bold', color='#FFFFFF', zorder=5)
    p_text = (
        "PK  ano [INTEGER] (2002–2035) | region_codigo_subdere = '13'\n"
        " • poblacion_total / poblacion_15_64 (Censo 2017 INE RM)\n"
        " • est_pob_18_24_rm (Proxy 14% de pob 15-64 años en RM)\n"
        "Conexión: Cruce por Año para evaluar Tasa de Absorción Juvenil"
    )
    ax.text(0.37, 0.17, p_text, ha='left', va='top', fontsize=7.5, family='monospace', color='#0F172A', zorder=5)

    # FLECHAS DE CONEXION (1 a N)
    arrow_props = dict(arrowstyle="->,head_length=0.4,head_width=0.3", color='#2563EB', lw=2)
    # Tiempo -> Fact
    ax.annotate("", xy=(0.36, 0.70), xytext=(0.29, 0.72), arrowprops=arrow_props, zorder=6)
    ax.text(0.32, 0.725, "1 : N", fontsize=9, fontweight='bold', color='#1E40AF')

    # Geografía -> Fact
    ax.annotate("", xy=(0.36, 0.42), xytext=(0.29, 0.42), arrowprops=arrow_props, zorder=6)
    ax.text(0.32, 0.43, "1 : N", fontsize=9, fontweight='bold', color='#1E40AF')

    # Institución -> Fact
    ax.annotate("", xy=(0.64, 0.70), xytext=(0.71, 0.72), arrowprops=arrow_props, zorder=6)
    ax.text(0.67, 0.725, "1 : N", fontsize=9, fontweight='bold', color='#1E40AF')

    # Carrera -> Fact
    ax.annotate("", xy=(0.64, 0.42), xytext=(0.71, 0.42), arrowprops=arrow_props, zorder=6)
    ax.text(0.67, 0.43, "1 : N", fontsize=9, fontweight='bold', color='#1E40AF')

    # INE Población -> Fact
    arrow_props_ine = dict(arrowstyle="->,head_length=0.4,head_width=0.3", color='#6D28D9', lw=2, linestyle='--')
    ax.annotate("", xy=(0.50, 0.28), xytext=(0.50, 0.22), arrowprops=arrow_props_ine, zorder=6)
    ax.text(0.51, 0.25, "Cruce Año (Contextual)", fontsize=8.5, fontweight='bold', color='#6D28D9')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    png_path = os.path.join(output_dir, "diagrama_modelo_dimensional_estrella.png")
    plt.tight_layout()
    plt.savefig(png_path, dpi=300, facecolor='#F8FAFC', bbox_inches='tight')
    plt.close()
    print(f"  [PNG Creado] {png_path}")

if __name__ == "__main__":
    base_dir = r"a:\Descargassss\proyecto-bi-pregrado-main\proyecto-bi-pregrado-main\Avance Hito 2\P3_MODELO_DIMENSIONAL_Y_ARQUITECTURA\diagramas"
    print("Iniciando generación de diagramas del Esquema Estrella...")
    create_star_diagram(base_dir)
    print("Todos los diagramas fueron generados con éxito.")
