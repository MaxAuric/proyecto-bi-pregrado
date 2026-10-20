import os
import pandas as pd
import json

DATA_PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data_processed")
DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")
os.makedirs(DOCS_DIR, exist_ok=True)

DICTIONARY_ENTRIES = [
    {
        "nombre_final": "ano",
        "nombre_orig_2012_2022": "Año",
        "nombre_orig_2023_2026": "Año",
        "tipo_dato": "INTEGER",
        "categoria": "Dimensión Temporal",
        "descripcion": "Año académico de referencia del registro de matrícula.",
        "regla_transformacion": "Conversión a entero estándar de 4 dígitos [2012-2026].",
        "tratamiento_nulos": "0% nulos. Clave temporal obligatoria."
    },
    {
        "nombre_final": "nombre_institucion",
        "nombre_orig_2012_2022": "Nombre Institución",
        "nombre_orig_2023_2026": "Nombre Institución",
        "tipo_dato": "VARCHAR(150)",
        "categoria": "Dimensión Institución",
        "descripcion": "Nombre oficial de la casa de estudios superiores.",
        "regla_transformacion": "Normalización de espacios y estandarización a mayúsculas consistentes.",
        "tratamiento_nulos": "0% nulos. Clave de entidad institucional."
    },
    {
        "nombre_final": "tipo_institucion",
        "nombre_orig_2012_2022": "Tipo Institución",
        "nombre_orig_2023_2026": "Tipo Institución",
        "tipo_dato": "VARCHAR(50)",
        "categoria": "Dimensión Institución",
        "descripcion": "Tipo de institución: Universidad (Univ.), Instituto Profesional (I.P.) o Centro de Formación Técnica (C.F.T.).",
        "regla_transformacion": "Limpieza de caracteres especiales y recorte de espacios.",
        "tratamiento_nulos": "0% nulos. Clasificación estructural del sistema de educación superior."
    },
    {
        "nombre_final": "clasificacion2",
        "nombre_orig_2012_2022": "Clasificación2",
        "nombre_orig_2023_2026": "Clasificación2",
        "tipo_dato": "VARCHAR(100)",
        "categoria": "Dimensión Institución",
        "descripcion": "Subclasificación institucional detallada (ej. Univ. Estatales CRUCH, Privadas CRUCH, Privadas no CRUCH).",
        "regla_transformacion": "Mapeo directo y limpieza de prefijos alfanuméricos.",
        "tratamiento_nulos": "Preservación de nulos si no aplica subclasificación."
    },
    {
        "nombre_final": "acreditacion",
        "nombre_orig_2012_2022": "Acreditación",
        "nombre_orig_2023_2026": "Clasificación3",
        "tipo_dato": "VARCHAR(50)",
        "categoria": "Dimensión Institución",
        "descripcion": "Estado de acreditación institucional según la CNA.",
        "regla_transformacion": "Mapeo de 'Clasificación3' del CNED 2023-2026 a 'acreditacion'.",
        "tratamiento_nulos": "Preservación del estado para modelar cambios en el tiempo (SCD Tipo 2)."
    },
    {
        "nombre_final": "autonomia",
        "nombre_orig_2012_2022": "Autonomía",
        "nombre_orig_2023_2026": "Clasificación4",
        "tipo_dato": "VARCHAR(50)",
        "categoria": "Dimensión Institución",
        "descripcion": "Condición de autonomía institucional otorgada por el CNED.",
        "regla_transformacion": "Mapeo de 'Clasificación4' del CNED 2023-2026 a 'autonomia'.",
        "tratamiento_nulos": "Preservación del estado institucional."
    },
    {
        "nombre_final": "gratuidad",
        "nombre_orig_2012_2022": "Gratuidad",
        "nombre_orig_2023_2026": "Clasificación5",
        "tipo_dato": "VARCHAR(50)",
        "categoria": "Dimensión Institución",
        "descripcion": "Adscripción a Gratuidad Universitaria (Ley 21.091).",
        "regla_transformacion": "Mapeo de 'Clasificación5' del CNED 2023-2026 a 'gratuidad'.",
        "tratamiento_nulos": "Nulos antes de 2016 reflejan inexistencia legal previa de la política."
    },
    {
        "nombre_final": "nombre_sede",
        "nombre_orig_2012_2022": "Nombre de la Sede",
        "nombre_orig_2023_2026": "Nombre de la Sede",
        "tipo_dato": "VARCHAR(100)",
        "categoria": "Dimensión Sede",
        "descripcion": "Nombre del campus o sede física donde se imparte el programa.",
        "regla_transformacion": "Normalización de textos y remoción de espacios redundantes.",
        "tratamiento_nulos": "0% nulos."
    },
    {
        "nombre_final": "nombre_region",
        "nombre_orig_2012_2022": "Nombre Region",
        "nombre_orig_2023_2026": "Nombre Region",
        "tipo_dato": "VARCHAR(80)",
        "categoria": "Dimensión Geográfica",
        "descripcion": "Nombre de la región político-administrativa de Chile.",
        "regla_transformacion": "Normalización ortográfica y compatibilización con estándares SUBDERE/INE.",
        "tratamiento_nulos": "0% nulos."
    },
    {
        "nombre_final": "region_codigo_subdere",
        "nombre_orig_2012_2022": "(Calculado)",
        "nombre_orig_2023_2026": "(Calculado)",
        "tipo_dato": "VARCHAR(2)",
        "categoria": "Dimensión Geográfica",
        "descripcion": "Código oficial de dos dígitos (01-16) según división territorial SUBDERE.",
        "regla_transformacion": "Mapeo determinista basado en nombre de región.",
        "tratamiento_nulos": "0% nulos. Llave canónica para cruces externos (INE, Casen)."
    },
    {
        "nombre_final": "flag_quiebre_nuble",
        "nombre_orig_2012_2022": "(Calculado)",
        "nombre_orig_2023_2026": "(Calculado)",
        "tipo_dato": "INTEGER (0/1)",
        "categoria": "Dimensión Geográfica",
        "descripcion": "Flag indicador de trazabilidad para la Región de Ñuble (Ley 21.033, creada en 2018).",
        "regla_transformacion": "1 si codigo='16' y ano < 2018; 0 en otro caso.",
        "tratamiento_nulos": "0% nulos."
    },
    {
        "nombre_final": "carrera_generica",
        "nombre_orig_2012_2022": "Carrera Genérica",
        "nombre_orig_2023_2026": "Carrera Genérica",
        "tipo_dato": "VARCHAR(120)",
        "categoria": "Dimensión Carrera",
        "descripcion": "Agrupación nacional de la carrera según taxonomía SIES.",
        "regla_transformacion": "Limpieza de tildes, caracteres especiales y mayúsculas.",
        "tratamiento_nulos": "0% nulos. Llave para cruce con mifuturo.cl."
    },
    {
        "nombre_final": "nombre_programa",
        "nombre_orig_2012_2022": "Nombre Programa",
        "nombre_orig_2023_2026": "Nombre Programa",
        "tipo_dato": "VARCHAR(200)",
        "categoria": "Dimensión Programa",
        "descripcion": "Nombre académico específico del programa ofrecido.",
        "regla_transformacion": "Limpieza de textos y normalización de mayúsculas.",
        "tratamiento_nulos": "0% nulos."
    },
    {
        "nombre_final": "horario",
        "nombre_orig_2012_2022": "Horario",
        "nombre_orig_2023_2026": "Horario",
        "tipo_dato": "VARCHAR(30)",
        "categoria": "Dimensión Programa",
        "descripcion": "Jornada: Diurno, Vespertino o A Distancia/Semipresencial.",
        "regla_transformacion": "Recorte de espacios y tipificación uniforme.",
        "tratamiento_nulos": "0% nulos."
    },
    {
        "nombre_final": "tipo_programa",
        "nombre_orig_2012_2022": "Tipo Programa",
        "nombre_orig_2023_2026": "Tipo Programa",
        "tipo_dato": "VARCHAR(50)",
        "categoria": "Dimensión Programa",
        "descripcion": "Nivel: Profesional con/sin Licenciatura, Técnico Nivel Superior.",
        "regla_transformacion": "Normalización de texto.",
        "tratamiento_nulos": "0% nulos."
    },
    {
        "nombre_final": "area_conocimiento",
        "nombre_orig_2012_2022": "Area Conocimiento",
        "nombre_orig_2023_2026": "Area Conocimiento",
        "tipo_dato": "VARCHAR(80)",
        "categoria": "Dimensión Programa",
        "descripcion": "Área de conocimiento según clasificación OCDE/SIES.",
        "regla_transformacion": "Limpieza de caracteres especiales.",
        "tratamiento_nulos": "0% nulos."
    },
    {
        "nombre_final": "tipo_prueba_admision",
        "nombre_orig_2012_2022": "(Calculado)",
        "nombre_orig_2023_2026": "(Calculado)",
        "tipo_dato": "VARCHAR(10)",
        "categoria": "Atributo de Hecho",
        "descripcion": "Instrumento oficial: PSU (<=2020), PDT (2021-2022), PAES (>=2023).",
        "regla_transformacion": "Mapeo condicional por año cronológico.",
        "tratamiento_nulos": "0% nulos. Esencial para segmentar análisis psicométrico."
    },
    {
        "nombre_final": "puntaje_promedio_original",
        "nombre_orig_2012_2022": "Promedio Puntaje",
        "nombre_orig_2023_2026": "Promedio Puntaje",
        "tipo_dato": "DECIMAL(6,2)",
        "categoria": "Hecho / Medida",
        "descripcion": "Puntaje promedio obtenido en la prueba en su escala nativa.",
        "regla_transformacion": "Casting numérico. Escala [150-850] en PSU/PDT y [100-1000] en PAES.",
        "tratamiento_nulos": "80.5% nulos justificados (CFT/IP). Preservados como NULL."
    },
    {
        "nombre_final": "puntaje_promedio_norm_0_100",
        "nombre_orig_2012_2022": "(Calculado)",
        "nombre_orig_2023_2026": "(Calculado)",
        "tipo_dato": "DECIMAL(5,2)",
        "categoria": "Hecho / Medida",
        "descripcion": "Puntaje promedio normalizado en escala estándar 0 a 100.",
        "regla_transformacion": "PSU/PDT: (Score-150)/700*100; PAES: (Score-100)/900*100.",
        "tratamiento_nulos": "Preservado como NULL para instituciones sin requisito de prueba."
    },
    {
        "nombre_final": "puntaje_promedio_equiv_paes",
        "nombre_orig_2012_2022": "(Calculado)",
        "nombre_orig_2023_2026": "(Calculado)",
        "tipo_dato": "DECIMAL(6,2)",
        "categoria": "Hecho / Medida",
        "descripcion": "Puntaje proyectado a escala moderna PAES [100-1000].",
        "regla_transformacion": "PSU/PDT: 100 + (Score-150)/700*900; PAES: Score nativo.",
        "tratamiento_nulos": "Preservado como NULL."
    },
    {
        "nombre_final": "puntaje_promedio_zscore_anual",
        "nombre_orig_2012_2022": "(Calculado)",
        "nombre_orig_2023_2026": "(Calculado)",
        "tipo_dato": "DECIMAL(5,3)",
        "categoria": "Hecho / Medida",
        "descripcion": "Puntaje estandarizado Z-Score relativo a la cohorte anual (media=0, desv=1).",
        "regla_transformacion": "(Score - Media_Anual) / Desv_Anual.",
        "tratamiento_nulos": "Preservado como NULL."
    },
    {
        "nombre_final": "flag_exige_prueba_admision",
        "nombre_orig_2012_2022": "(Calculado)",
        "nombre_orig_2023_2026": "(Calculado)",
        "tipo_dato": "INTEGER (0/1)",
        "categoria": "Atributo Dim.",
        "descripcion": "Indica si la carrera exige prueba centralizada de admisión.",
        "regla_transformacion": "1 si puntaje no es nulo; 0 en caso contrario.",
        "tratamiento_nulos": "0% nulos. Filtro indispensable para Power BI."
    },
    {
        "nombre_final": "vacantes",
        "nombre_orig_2012_2022": "Vacantes",
        "nombre_orig_2023_2026": "Vacantes",
        "tipo_dato": "INTEGER",
        "categoria": "Hecho / Medida",
        "descripcion": "Número total de vacantes de primer año declaradas.",
        "regla_transformacion": "Casting numérico a entero.",
        "tratamiento_nulos": "25.4% nulos en programas con admisión abierta. Preservados como NULL."
    },
    {
        "nombre_final": "flag_vacantes_declaradas",
        "nombre_orig_2012_2022": "(Calculado)",
        "nombre_orig_2023_2026": "(Calculado)",
        "tipo_dato": "INTEGER (0/1)",
        "categoria": "Atributo Dim.",
        "descripcion": "Indica si la carrera declaró vacantes finitas mayores a cero.",
        "regla_transformacion": "1 si vacantes > 0; 0 si es nulo o no informado.",
        "tratamiento_nulos": "0% nulos. Asegura cálculo correcto de tasas de ocupación."
    },
    {
        "nombre_final": "matricula_primer_ano_total",
        "nombre_orig_2012_2022": "Matrícula 1er Año",
        "nombre_orig_2023_2026": "Matrícula 1er Año",
        "tipo_dato": "INTEGER",
        "categoria": "Hecho / Medida",
        "descripcion": "Estudiantes matriculados en primer año.",
        "regla_transformacion": "Casting numérico entero. Imputación de nulos a 0.",
        "tratamiento_nulos": "0% nulos (medida aditiva)."
    },
    {
        "nombre_final": "matricula_total",
        "nombre_orig_2012_2022": "Matrícula Total",
        "nombre_orig_2023_2026": "Matrícula Total",
        "tipo_dato": "INTEGER",
        "categoria": "Hecho / Medida",
        "descripcion": "Total de estudiantes matriculados en todos los niveles.",
        "regla_transformacion": "Casting numérico entero. Imputación de nulos a 0.",
        "tratamiento_nulos": "0% nulos (medida aditiva)."
    },
    {
        "nombre_final": "tasa_ocupacion_primer_ano",
        "nombre_orig_2012_2022": "(Calculado)",
        "nombre_orig_2023_2026": "(Calculado)",
        "tipo_dato": "DECIMAL(6,2)",
        "categoria": "Métrica Analítica",
        "descripcion": "Porcentaje de ocupación de las vacantes declaradas en primer año.",
        "regla_transformacion": "(Matricula Primer Año / Vacantes) * 100.",
        "tratamiento_nulos": "Calculado solo cuando flag_vacantes_declaradas=1."
    }
]

def generate_dictionary():
    print("=== GENERANDO DICCIONARIO DE DATOS EXHAUSTIVO PARA HITO 1 ===")
    
    # JSON
    json_path = os.path.join(DOCS_DIR, "diccionario_datos_exhaustivo.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(DICTIONARY_ENTRIES, f, indent=2, ensure_ascii=False)
    
    # Markdown
    md_path = os.path.join(DOCS_DIR, "diccionario_datos_exhaustivo.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Diccionario de Datos Exhaustivo - Hito 1\n")
        f.write("## Proyecto Final de Business Intelligence - Ingeniería en Negocios\n\n")
        f.write("| Nombre Final | Nombre Orig. (12-22) | Nombre Orig. (23-26) | Tipo | Categoría | Regla de Transformación ETL | Tratamiento de Nulos y Justificación |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for item in DICTIONARY_ENTRIES:
            f.write(f"| `{item['nombre_final']}` | {item['nombre_orig_2012_2022']} | {item['nombre_orig_2023_2026']} | `{item['tipo_dato']}` | {item['categoria']} | {item['regla_transformacion']} | {item['tratamiento_nulos']} |\n")

    # LaTeX Table
    tex_path = os.path.join(DOCS_DIR, "tabla_diccionario_datos.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write("{\\small\n")
        f.write("\\begin{longtable}{|p{3.2cm}|p{2.2cm}|p{2.0cm}|p{1.8cm}|p{5.8cm}|}\n")
        f.write("\\hline\n")
        f.write("\\textbf{Campo Final} & \\textbf{Orig. 12-22} & \\textbf{Orig. 23-26} & \\textbf{Tipo} & \\textbf{Regla ETL y Tratamiento de Nulos} \\\\\n")
        f.write("\\hline\\endfirsthead\n")
        f.write("\\hline \\textbf{Campo Final} & \\textbf{Orig. 12-22} & \\textbf{Orig. 23-26} & \\textbf{Tipo} & \\textbf{Regla ETL y Tratamiento de Nulos} \\\\ \\hline \\endhead\n")
        for item in DICTIONARY_ENTRIES:
            clean_rule = item['regla_transformacion'].replace('&', '\\&').replace('%', '\\%').replace('_', '\\_')
            clean_null = item['tratamiento_nulos'].replace('&', '\\&').replace('%', '\\%').replace('_', '\\_')
            clean_final = item['nombre_final'].replace('_', '\\_')
            clean_o1 = item['nombre_orig_2012_2022'].replace('_', '\\_')
            clean_o2 = item['nombre_orig_2023_2026'].replace('_', '\\_')
            f.write(f"\\texttt{{\\footnotesize {clean_final}}} & {clean_o1} & {clean_o2} & \\texttt{{\\footnotesize {item['tipo_dato']}}} & {clean_rule} \\newline \\textit{{\\footnotesize {clean_null}}} \\\\\n")
            f.write("\\hline\n")
        f.write("\\end{longtable}\n")
        f.write("}\n")
    print("  [OK] Diccionarios generados con formato optimizado.")

if __name__ == "__main__":
    generate_dictionary()
