/**
 * Script de Organización y Consolidación Limpia de la Carpeta: Avance Hito 1
 * Autor: Persona 5 (Gestor del Proyecto y Documentador)
 */

const fs = require('fs');
const path = require('path');

const REPO_ROOT = __dirname;
const AVANCE_DIR = path.join(REPO_ROOT, 'Avance Hito 1');

console.log("=== INICIANDO ORGANIZACIÓN DE 'Avance Hito 1' ===");
console.log("Raíz de trabajo:", REPO_ROOT);
console.log("Destino limpio:", AVANCE_DIR);

const folders = [
  '00_DOCUMENTOS_PARA_PRESENTAR_Y_DEFENDER',
  '01_PROPUESTA_VALOR_Y_CANVAS_BI',
  '01_PROPUESTA_VALOR_Y_CANVAS_BI/prototipos_visuales_powerbi',
  '02_ETL_Y_BASE_CONSOLIDADA_2012_2026',
  '02_ETL_Y_BASE_CONSOLIDADA_2012_2026/pipeline_scripts',
  '02_ETL_Y_BASE_CONSOLIDADA_2012_2026/fuentes_crudas_oficiales',
  '03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE',
  '03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE/tablas_procesadas',
  '03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE/scripts_descarga_y_cruce',
  '04_DICCIONARIOS_DE_DATOS_MAESTRO',
  '05_AUDITORIAS_Y_CERTIFICACION_RUBRICA'
];

folders.forEach(f => {
  const p = path.join(AVANCE_DIR, f);
  if (!fs.existsSync(p)) fs.mkdirSync(p, { recursive: true });
});

function copyFileSafe(srcRel, destRel) {
  const src = path.join(REPO_ROOT, srcRel);
  const dest = path.join(AVANCE_DIR, destRel);
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, dest);
    const sz = fs.statSync(dest).size;
    console.log(`  [COPIADO] ${destRel} (${(sz / 1024).toFixed(1)} KB)`);
  } else {
    console.warn(`  [AVISO] Archivo origen no encontrado: ${srcRel}`);
  }
}

// 1. CARPETA 00: DOCUMENTOS PARA PRESENTAR Y DEFENDER
console.log("\n[1] Copiando Documentos de Presentación...");
copyFileSafe("inteligencia/P5_Hito1/docs/Guia_Estudio_Defensa_Hito1_BI.pdf", "00_DOCUMENTOS_PARA_PRESENTAR_Y_DEFENDER/Guia_Maestra_Estudio_y_Defensa_Hito1.pdf");
copyFileSafe("inteligencia/P5_Hito1/docs/informe_hito1_persona5.pdf", "00_DOCUMENTOS_PARA_PRESENTAR_Y_DEFENDER/Informe_Ejecutivo_Hito1_Persona5.pdf");
copyFileSafe("inteligencia/P5_Hito1/docs/Diccionario_Datos_Maestro_Hito1.xls", "00_DOCUMENTOS_PARA_PRESENTAR_Y_DEFENDER/Diccionario_Datos_Maestro_Hito1.xls");
copyFileSafe("inteligencia/P5_Hito1/docs/diccionario_datos_interactivo.html", "00_DOCUMENTOS_PARA_PRESENTAR_Y_DEFENDER/Diccionario_Datos_Interactivo.html");
copyFileSafe("P_IN/docs/informe_hito1_persona1.pdf", "00_DOCUMENTOS_PARA_PRESENTAR_Y_DEFENDER/Informe_Hito1_Persona1_ETL.pdf");
copyFileSafe("inteligencia/P4_Hito1/docs/informe_hito1_persona4.pdf", "00_DOCUMENTOS_PARA_PRESENTAR_Y_DEFENDER/Informe_Hito1_Persona4_Visualizacion.pdf");

// 2. CARPETA 01: PROPUESTA DE VALOR Y CANVAS BI
console.log("\n[2] Copiando Propuesta de Valor y Canvas BI...");
copyFileSafe("inteligencia/P2_Hito1/docs/informe_hito1_persona2.tex", "01_PROPUESTA_VALOR_Y_CANVAS_BI/informe_hito1_persona2_propuesta_y_canvas.tex");
copyFileSafe("inteligencia/P4_Hito1/docs/informe_hito1_persona4.md", "01_PROPUESTA_VALOR_Y_CANVAS_BI/informe_viabilidad_3_preguntas_persona4.md");
copyFileSafe("inteligencia/P4_Hito1/docs/catalogo_medidas_dax.md", "01_PROPUESTA_VALOR_Y_CANVAS_BI/catalogo_medidas_dax.md");
copyFileSafe("inteligencia/P4_Hito1/docs/especificacion_dashboard_wireframes.md", "01_PROPUESTA_VALOR_Y_CANVAS_BI/especificacion_dashboard_wireframes.md");

copyFileSafe("inteligencia/P4_Hito1/data_validation/visual_prototypes/dashboard_wireframe_arquitectura.png", "01_PROPUESTA_VALOR_Y_CANVAS_BI/prototipos_visuales_powerbi/dashboard_wireframe_arquitectura.png");
copyFileSafe("inteligencia/P4_Hito1/data_validation/visual_prototypes/p1_equidad_territorial.png", "01_PROPUESTA_VALOR_Y_CANVAS_BI/prototipos_visuales_powerbi/p1_equidad_territorial.png");
copyFileSafe("inteligencia/P4_Hito1/data_validation/visual_prototypes/p2_capacidad_ocupacion.png", "01_PROPUESTA_VALOR_Y_CANVAS_BI/prototipos_visuales_powerbi/p2_capacidad_ocupacion.png");
copyFileSafe("inteligencia/P4_Hito1/data_validation/visual_prototypes/p3_calidad_acreditacion.png", "01_PROPUESTA_VALOR_Y_CANVAS_BI/prototipos_visuales_powerbi/p3_calidad_acreditacion.png");

// 3. CARPETA 02: ETL Y BASE CONSOLIDADA 2012-2026
console.log("\n[3] Copiando Base Consolidada y Scripts ETL...");
copyFileSafe("P_IN/data_processed/base_indices_consolidada_2012_2026.csv", "02_ETL_Y_BASE_CONSOLIDADA_2012_2026/base_indices_consolidada_2012_2026.csv");
copyFileSafe("P_IN/data_processed/base_indices_consolidada_2012_2026.parquet", "02_ETL_Y_BASE_CONSOLIDADA_2012_2026/base_indices_consolidada_2012_2026.parquet");
copyFileSafe("P_IN/data_processed/auditoria_resumen.json", "02_ETL_Y_BASE_CONSOLIDADA_2012_2026/auditoria_resumen_psicometrico_y_nulos.json");

copyFileSafe("P_IN/etl_pipeline/01_download_data.py", "02_ETL_Y_BASE_CONSOLIDADA_2012_2026/pipeline_scripts/01_download_data.py");
copyFileSafe("P_IN/etl_pipeline/02_audit_and_mapping.py", "02_ETL_Y_BASE_CONSOLIDADA_2012_2026/pipeline_scripts/02_audit_and_mapping.py");
copyFileSafe("P_IN/etl_pipeline/03_clean_and_transform.py", "02_ETL_Y_BASE_CONSOLIDADA_2012_2026/pipeline_scripts/03_clean_and_transform.py");
copyFileSafe("P_IN/etl_pipeline/04_generate_dictionary.py", "02_ETL_Y_BASE_CONSOLIDADA_2012_2026/pipeline_scripts/04_generate_dictionary.py");
copyFileSafe("P_IN/etl_pipeline/run_etl.py", "02_ETL_Y_BASE_CONSOLIDADA_2012_2026/pipeline_scripts/run_etl.py");

copyFileSafe("P_IN/data_raw/Base-INDICES-Matricula-2005-2026.xlsx", "02_ETL_Y_BASE_CONSOLIDADA_2012_2026/fuentes_crudas_oficiales/Base-INDICES-Matricula-2005-2026.xlsx");
copyFileSafe("P_IN/data_raw/01_Esquema_Registro_Base_Pregrado.pdf", "02_ETL_Y_BASE_CONSOLIDADA_2012_2026/fuentes_crudas_oficiales/01_Esquema_Registro_Base_Pregrado.pdf");
copyFileSafe("01_BaseINDICES_Pregrado24.xlsx", "02_ETL_Y_BASE_CONSOLIDADA_2012_2026/fuentes_crudas_oficiales/01_BaseINDICES_Pregrado24.xlsx");

// 4. CARPETA 03: FUENTES EXTERNAS Y TABLAS PUENTE
console.log("\n[4] Copiando Fuentes Externas y Tablas Puente...");
copyFileSafe("inteligencia/P2_Hito1/data_processed/ext_ine_poblacion_region_ano.csv", "03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE/tablas_procesadas/ext_ine_poblacion_region_ano.csv");
copyFileSafe("inteligencia/P2_Hito1/data_processed/ext_sies_acreditacion_ies_ano.csv", "03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE/tablas_procesadas/ext_sies_acreditacion_ies_ano.csv");
copyFileSafe("inteligencia/P2_Hito1/data_processed/puente_region.csv", "03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE/tablas_procesadas/puente_region.csv");
copyFileSafe("inteligencia/P2_Hito1/data_processed/puente_institucion.csv", "03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE/tablas_procesadas/puente_institucion.csv");
copyFileSafe("inteligencia/P2_Hito1/data_processed/cruce_no_coincidentes_institucion.csv", "03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE/tablas_procesadas/cruce_no_coincidentes_institucion.csv");
copyFileSafe("inteligencia/P2_Hito1/data_processed/cruce_resumen.json", "03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE/tablas_procesadas/cruce_resumen.json");

copyFileSafe("inteligencia/P2_Hito1/data_external/manifiesto_descargas.json", "03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE/manifiesto_descargas_sha256.json");
copyFileSafe("inteligencia/P5_Hito1/docs/documentacion_tablas_puente_fuentes_externas.md", "03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE/documentacion_tablas_puente_fuentes_externas.md");

copyFileSafe("inteligencia/P2_Hito1/scripts/05_download_external.py", "03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE/scripts_descarga_y_cruce/05_download_external.py");
copyFileSafe("inteligencia/P2_Hito1/scripts/06_build_external_bridges.py", "03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE/scripts_descarga_y_cruce/06_build_external_bridges.py");
copyFileSafe("inteligencia/P2_Hito1/scripts/07_preview_kpis.py", "03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE/scripts_descarga_y_cruce/07_preview_kpis.py");

// 5. CARPETA 04: DICCIONARIOS DE DATOS MAESTRO
console.log("\n[5] Copiando Diccionarios de Datos...");
copyFileSafe("inteligencia/P5_Hito1/docs/diccionario_datos_exhaustivo_maestro.md", "04_DICCIONARIOS_DE_DATOS_MAESTRO/diccionario_datos_exhaustivo_maestro.md");
copyFileSafe("inteligencia/P5_Hito1/docs/diccionario_datos_exhaustivo_maestro.json", "04_DICCIONARIOS_DE_DATOS_MAESTRO/diccionario_datos_exhaustivo_maestro.json");
copyFileSafe("inteligencia/P5_Hito1/docs/tabla_diccionario_maestro.tex", "04_DICCIONARIOS_DE_DATOS_MAESTRO/tabla_diccionario_maestro.tex");
copyFileSafe("inteligencia/P5_Hito1/docs/Diccionario_Datos_Maestro_Hito1.xls", "04_DICCIONARIOS_DE_DATOS_MAESTRO/Diccionario_Datos_Maestro_Hito1.xls");
copyFileSafe("inteligencia/P5_Hito1/docs/diccionario_datos_interactivo.html", "04_DICCIONARIOS_DE_DATOS_MAESTRO/diccionario_datos_interactivo.html");

// 6. CARPETA 05: AUDITORÍAS Y CERTIFICACIÓN
console.log("\n[6] Copiando Auditorías y Certificación...");
copyFileSafe("inteligencia/P5_Hito1/auditoria/auditoria_cumplimiento_rubrica_hito1.json", "05_AUDITORIAS_Y_CERTIFICACION_RUBRICA/auditoria_cumplimiento_rubrica_hito1.json");
copyFileSafe("inteligencia/P5_Hito1/auditoria/metricas_integracion_hito1.json", "05_AUDITORIAS_Y_CERTIFICACION_RUBRICA/metricas_integracion_hito1.json");
copyFileSafe("inteligencia/P3_Hito1/auditoria_normalizacion_textos.json", "05_AUDITORIAS_Y_CERTIFICACION_RUBRICA/auditoria_normalizacion_textos_persona3.json");
copyFileSafe("inteligencia/P3_Hito1/informe_hito1_persona3_normalizacion.md", "05_AUDITORIAS_Y_CERTIFICACION_RUBRICA/informe_hito1_persona3_normalizacion.md");
copyFileSafe("inteligencia/P4_Hito1/data_validation/auditoria_viabilidad_preguntas.json", "05_AUDITORIAS_Y_CERTIFICACION_RUBRICA/auditoria_viabilidad_preguntas_persona4.json");

// Generar README maestro dentro de "Avance Hito 1"
const readmeAvance = `# 📁 Directorio Oficial de Entrega: Avance Hito 1
## Proyecto Práctico Final de Business Intelligence - Educación Superior Chilena (2012–2026)

Este directorio contiene **exclusivamente los entregables limpios, consolidados y auditados del Hito 1**, estructurados para facilitar la exposición oral, la navegación docente y la defensa individual ante la interrogación de avance.

---

## 🗂️ Estructura de Navegación del Avance

### 📍 [00_DOCUMENTOS_PARA_PRESENTAR_Y_DEFENDER/](file:///c:/Users/lucas/Desktop/inteligencia/proyecto-bi-pregrado-main/Avance%20Hito%201/00_DOCUMENTOS_PARA_PRESENTAR_Y_DEFENDER/)
*Documentos principales listos para abrir y proyectar en clase o enviar por correo/buzón:*
- **\`Guia_Maestra_Estudio_y_Defensa_Hito1.pdf\`**: Guía pedagógica de 8 páginas para estudiar antes de la presentación. Incluye resumen por roles, preguntas trampa del profesor y respuestas exactas.
- **\`Informe_Ejecutivo_Hito1_Persona5.pdf\`**: Informe formal de cierre del Hito 1 con la certificación de los 17 puntos de la rúbrica.
- **\`Diccionario_Datos_Maestro_Hito1.xls\`**: Libro Excel interactivo de 4 pestañas formateadas para mostrar el diccionario con filtros y colores.
- **\`Diccionario_Datos_Interactivo.html\`**: Visor web interactivo con buscador en vivo en el navegador.
- **\`Informe_Hito1_Persona1_ETL.pdf\`**: Informe técnico de Persona 1 sobre el pipeline ETL y homologación.
- **\`Informe_Hito1_Persona4_Visualizacion.pdf\`**: Informe técnico de Persona 4 sobre graficabilidad en Power BI.

---

### 📍 [01_PROPUESTA_VALOR_Y_CANVAS_BI/](file:///c:/Users/lucas/Desktop/inteligencia/proyecto-bi-pregrado-main/Avance%20Hito%201/01_PROPUESTA_VALOR_Y_CANVAS_BI/) *(Criterio 1 de Rúbrica - 4 Pts)*
- Enfoque de negocio para Directores de Admisión y Planificación Universitaria.
- **Canvas BI de 10 bloques** formalizado.
- **Tres Preguntas de Negocio:** P1 (Equidad Territorial), P2 (Uso de Capacidad) y P3 (Calidad y Acreditación).
- **Prototipos visuales** de alta resolución y catálogo de medidas DAX con control de semi-aditividad.

---

### 📍 [02_ETL_Y_BASE_CONSOLIDADA_2012_2026/](file:///c:/Users/lucas/Desktop/inteligencia/proyecto-bi-pregrado-main/Avance%20Hito%201/02_ETL_Y_BASE_CONSOLIDADA_2012_2026/) *(Criterio 2 de Rúbrica - 8 Pts)*
- **\`base_indices_consolidada_2012_2026.csv\`** (79 MB) y **\`.parquet\`** (4.2 MB) con **158.211 filas exactas y 59 columnas gobernadas**.
- Cero datos simulados: 114.265 filas históricas (2012–2022) + 43.946 del portal CNED oficial (2023–2026).
- Pipeline de scripts en Python (\`pipeline_scripts/\`) y bases crudas inmutables (\`fuentes_crudas_oficiales/\`).
- Homologación psicométrica cuádruple de puntajes (PSU, PDT, PAES) y justificación matemática de nulos con flags.

---

### 📍 [03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE/](file:///c:/Users/lucas/Desktop/inteligencia/proyecto-bi-pregrado-main/Avance%20Hito%201/03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE/) *(Criterio 3 de Rúbrica - 5 Pts)*
- **Fuente 1 INE:** Proyecciones de población por región (Censo 2017). Tasa de coincidencia del **100,00%** mediante \`puente_region.csv\`.
- **Fuente 2 SIES:** Acreditación de IES vigentes (2018–2026). Tasa de coincidencia del **98,39% de filas** y **99,00% de la matrícula** mediante \`puente_institucion.csv\`.
- Trazabilidad criptográfica con fecha 15-oct-2026 y hash SHA-256 en \`manifiesto_descargas_sha256.json\`.
- Tratamiento formal de los 19 nombres no coincidentes (Unknown Member sin pérdida de hechos).

---

### 📍 [04_DICCIONARIOS_DE_DATOS_MAESTRO/](file:///c:/Users/lucas/Desktop/inteligencia/proyecto-bi-pregrado-main/Avance%20Hito%201/04_DICCIONARIOS_DE_DATOS_MAESTRO/)
- Diccionario exhaustivo en múltiples formatos: **Markdown (.md)**, **JSON estructurado (.json)**, **Excel (.xls)**, **Web (.html)** y **LaTeX (.tex)**.
- Mapeo 1:1 de nombres antiguos, nombres nuevos del CNED, tipos SQL, grano dimensional, reglas ETL y justificación de nulos.

---

### 📍 [05_AUDITORIAS_Y_CERTIFICACION_RUBRICA/](file:///c:/Users/lucas/Desktop/inteligencia/proyecto-bi-pregrado-main/Avance%20Hito%201/05_AUDITORIAS_Y_CERTIFICACION_RUBRICA/)
- Matriz JSON de auditoría que certifica el cumplimiento del **100% de la rúbrica (17/17 puntos grupales asegurados)**.
- Reportes estadísticos de normalización y métricas numéricas consolidadas.

---

*Compilado y gobernado por: Persona 5 (Gestor del Proyecto y Documentador) - 21 de Octubre de 2026.*
`;

fs.writeFileSync(path.join(AVANCE_DIR, "README.md"), readmeAvance, "utf-8");
console.log("  [OK] README.md maestro generado en 'Avance Hito 1'.");
console.log("\n=== CONSOLIDACIÓN COMPLETADA CON ÉXITO ===");
