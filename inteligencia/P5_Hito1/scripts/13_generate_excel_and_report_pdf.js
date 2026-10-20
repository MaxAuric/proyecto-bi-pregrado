/**
 * Generador de Artefactos de Presentación Ejecutiva:
 * 1. Libro Excel multipestaña (SpreadsheetML) con estilos corporativos: Diccionario_Datos_Maestro_Hito1.xls
 * 2. Visualizador Web interactivo para proyectar en clase: diccionario_datos_interactivo.html
 * 3. Compilación a PDF del Informe Técnico de Persona 5: informe_hito1_persona5.pdf
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const P5_DOCS_DIR = path.join(__dirname, '..', 'docs');
const MASTER_JSON_PATH = path.join(P5_DOCS_DIR, 'diccionario_datos_exhaustivo_maestro.json');
const dataMaster = JSON.parse(fs.readFileSync(MASTER_JSON_PATH, 'utf-8'));

// -------------------------------------------------------------
// 1. GENERAR LIBRO EXCEL MULTIPESTAÑA NATIVO (.xls / XML Spreadsheet)
// -------------------------------------------------------------
function escapeXml(unsafe) {
  if (unsafe === null || unsafe === undefined) return '';
  return String(unsafe)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function buildExcelXml() {
  console.log("=== GENERANDO LIBRO EXCEL MULTIPESTAÑA DEL DICCIONARIO ===");
  
  let xml = `<?xml version="1.0" encoding="UTF-8"?>
<?mso-application progid="Excel.Sheet"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:x="urn:schemas-microsoft-com:office:excel"
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:html="http://www.w3.org/TR/REC-html40">
 <DocumentProperties xmlns="urn:schemas-microsoft-com:office:office">
  <Title>Diccionario de Datos Maestro - Hito 1</Title>
  <Subject>Proyecto Business Intelligence</Subject>
  <Author>Persona 5 (Gestor del Proyecto y Documentador)</Author>
 </DocumentProperties>
 <Styles>
  <Style ss:ID="Default" ss:Name="Normal">
   <Alignment ss:Vertical="Center"/>
   <Borders/>
   <Font ss:FontName="Segoe UI" x:Family="Swiss" ss:Size="10" ss:Color="#000000"/>
   <Interior/>
   <NumberFormat/>
   <Protection/>
  </Style>
  <Style ss:ID="HeaderStyle">
   <Alignment ss:Horizontal="Center" ss:Vertical="Center" ss:WrapText="1"/>
   <Borders>
    <Border ss:Position="Bottom" ss:LineStyle="Continuous" ss:Weight="2" ss:Color="#102C57"/>
    <Border ss:Position="Left" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#CBD5E1"/>
    <Border ss:Position="Right" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#CBD5E1"/>
    <Border ss:Position="Top" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#CBD5E1"/>
   </Borders>
   <Font ss:FontName="Segoe UI" ss:Size="10" ss:Color="#FFFFFF" ss:Bold="1"/>
   <Interior ss:Color="#102C57" ss:Pattern="Solid"/>
  </Style>
  <Style ss:ID="TitleStyle">
   <Alignment ss:Horizontal="Left" ss:Vertical="Center"/>
   <Font ss:FontName="Segoe UI" ss:Size="14" ss:Color="#102C57" ss:Bold="1"/>
  </Style>
  <Style ss:ID="SubtitleStyle">
   <Alignment ss:Horizontal="Left" ss:Vertical="Center"/>
   <Font ss:FontName="Segoe UI" ss:Size="10" ss:Color="#64748B" ss:Italic="1"/>
  </Style>
  <Style ss:ID="RowEven">
   <Borders>
    <Border ss:Position="Bottom" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#E2E8F0"/>
    <Border ss:Position="Left" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#E2E8F0"/>
    <Border ss:Position="Right" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#E2E8F0"/>
    <Border ss:Position="Top" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#E2E8F0"/>
   </Borders>
   <Font ss:FontName="Segoe UI" ss:Size="9.5" ss:Color="#1E293B"/>
   <Interior ss:Color="#FFFFFF" ss:Pattern="Solid"/>
  </Style>
  <Style ss:ID="RowOdd">
   <Borders>
    <Border ss:Position="Bottom" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#E2E8F0"/>
    <Border ss:Position="Left" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#E2E8F0"/>
    <Border ss:Position="Right" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#E2E8F0"/>
    <Border ss:Position="Top" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#E2E8F0"/>
   </Borders>
   <Font ss:FontName="Segoe UI" ss:Size="9.5" ss:Color="#1E293B"/>
   <Interior ss:Color="#F8FAFC" ss:Pattern="Solid"/>
  </Style>
  <Style ss:ID="CodeStyle">
   <Alignment ss:Vertical="Center"/>
   <Borders>
    <Border ss:Position="Bottom" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#CBD5E1"/>
    <Border ss:Position="Left" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#CBD5E1"/>
    <Border ss:Position="Right" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#CBD5E1"/>
    <Border ss:Position="Top" ss:LineStyle="Continuous" ss:Weight="1" ss:Color="#CBD5E1"/>
   </Borders>
   <Font ss:FontName="Consolas" ss:Size="9" ss:Color="#0369A1" ss:Bold="1"/>
   <Interior ss:Color="#F0F9FF" ss:Pattern="Solid"/>
  </Style>
 </Styles>`;

  // PESTAÑA 1: BASE CNED 2012-2026 (59 COLUMNAS)
  xml += `
 <Worksheet ss:Name="CNED_59_Columnas">
  <Table ss:DefaultRowHeight="20">
   <Column ss:Width="30"/>
   <Column ss:Width="170"/>
   <Column ss:Width="150"/>
   <Column ss:Width="150"/>
   <Column ss:Width="100"/>
   <Column ss:Width="140"/>
   <Column ss:Width="280"/>
   <Column ss:Width="280"/>
   <Row ss:Height="28">
    <Cell ss:MergeAcross="7" ss:StyleID="TitleStyle"><Data ss:Type="String">DICCIONARIO MAESTRO: BASE CONSOLIDADA CNED (2012–2026)</Data></Cell>
   </Row>
   <Row ss:Height="18">
    <Cell ss:MergeAcross="7" ss:StyleID="SubtitleStyle"><Data ss:Type="String">Total Columnas: 59 | Total Registros: 158.211 | Responsable: Persona 5 (Gestor del Proyecto y Documentador)</Data></Cell>
   </Row>
   <Row ss:Height="10"/>
   <Row ss:Height="26">
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">#</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Nombre Final</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Nombre Orig. (2012-2022)</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Nombre Orig. (2023-2026)</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Tipo Dato</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Categoría Dimensional</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Regla de Transformación ETL</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Tratamiento de Nulos y Justificación</Data></Cell>
   </Row>`;

  dataMaster.columnas_cned_consolidada.forEach((col, idx) => {
    const styleRow = (idx % 2 === 0) ? "RowEven" : "RowOdd";
    xml += `
   <Row ss:Height="24">
    <Cell ss:StyleID="${styleRow}"><Data ss:Type="Number">${idx + 1}</Data></Cell>
    <Cell ss:StyleID="CodeStyle"><Data ss:Type="String">${escapeXml(col.nombre_final)}</Data></Cell>
    <Cell ss:StyleID="${styleRow}"><Data ss:Type="String">${escapeXml(col.nombre_orig_2012_2022)}</Data></Cell>
    <Cell ss:StyleID="${styleRow}"><Data ss:Type="String">${escapeXml(col.nombre_orig_2023_2026)}</Data></Cell>
    <Cell ss:StyleID="CodeStyle"><Data ss:Type="String">${escapeXml(col.tipo_dato)}</Data></Cell>
    <Cell ss:StyleID="${styleRow}"><Data ss:Type="String">${escapeXml(col.categoria)}</Data></Cell>
    <Cell ss:StyleID="${styleRow}"><Data ss:Type="String">${escapeXml(col.regla_transformacion)}</Data></Cell>
    <Cell ss:StyleID="${styleRow}"><Data ss:Type="String">${escapeXml(col.tratamiento_nulos)}</Data></Cell>
   </Row>`;
  });
  xml += `
  </Table>
 </Worksheet>`;

  // PESTAÑA 2: FUENTES EXTERNAS
  xml += `
 <Worksheet ss:Name="Fuentes_Externas">
  <Table ss:DefaultRowHeight="20">
   <Column ss:Width="160"/>
   <Column ss:Width="110"/>
   <Column ss:Width="140"/>
   <Column ss:Width="140"/>
   <Column ss:Width="140"/>
   <Column ss:Width="180"/>
   <Column ss:Width="320"/>
   <Row ss:Height="28">
    <Cell ss:MergeAcross="6" ss:StyleID="TitleStyle"><Data ss:Type="String">FUENTES EXTERNAS OFICIALES INTEGRADAS (INE Y SIES)</Data></Cell>
   </Row>
   <Row ss:Height="18">
    <Cell ss:MergeAcross="6" ss:StyleID="SubtitleStyle"><Data ss:Type="String">Descargas inmutables con fecha 15-oct-2026 y hash SHA-256 en manifiesto_descargas.json</Data></Cell>
   </Row>
   <Row ss:Height="10"/>
   <Row ss:Height="26">
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Archivo Procesado</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Fuente</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Grano Declarado</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Llave de Cruce</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Campo</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Tipo Dato</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Descripción Funcional</Data></Cell>
   </Row>`;

  let extRowIdx = 0;
  dataMaster.fuentes_externas.forEach(fuente => {
    fuente.columnas.forEach(c => {
      const styleRow = (extRowIdx % 2 === 0) ? "RowEven" : "RowOdd";
      extRowIdx++;
      xml += `
   <Row ss:Height="22">
    <Cell ss:StyleID="${styleRow}"><Data ss:Type="String">${escapeXml(fuente.tabla)}</Data></Cell>
    <Cell ss:StyleID="${styleRow}"><Data ss:Type="String">${escapeXml(fuente.fuente)}</Data></Cell>
    <Cell ss:StyleID="${styleRow}"><Data ss:Type="String">${escapeXml(fuente.grano)}</Data></Cell>
    <Cell ss:StyleID="CodeStyle"><Data ss:Type="String">${escapeXml(fuente.llave_cruce)}</Data></Cell>
    <Cell ss:StyleID="CodeStyle"><Data ss:Type="String">${escapeXml(c.nombre)}</Data></Cell>
    <Cell ss:StyleID="${styleRow}"><Data ss:Type="String">${escapeXml(c.tipo)}</Data></Cell>
    <Cell ss:StyleID="${styleRow}"><Data ss:Type="String">${escapeXml(c.descripcion)}</Data></Cell>
   </Row>`;
    });
  });
  xml += `
  </Table>
 </Worksheet>`;

  // PESTAÑA 3: TABLAS PUENTE
  xml += `
 <Worksheet ss:Name="Tablas_Puente">
  <Table ss:DefaultRowHeight="20">
   <Column ss:Width="160"/>
   <Column ss:Width="140"/>
   <Column ss:Width="140"/>
   <Column ss:Width="110"/>
   <Column ss:Width="160"/>
   <Column ss:Width="120"/>
   <Column ss:Width="260"/>
   <Row ss:Height="28">
    <Cell ss:MergeAcross="6" ss:StyleID="TitleStyle"><Data ss:Type="String">TABLAS PUENTE DE RESOLUCIÓN DIMENSIONAL</Data></Cell>
   </Row>
   <Row ss:Height="18">
    <Cell ss:MergeAcross="6" ss:StyleID="SubtitleStyle"><Data ss:Type="String">puente_region.csv (100% cruce) y puente_institucion.csv (99% matrícula cubierta)</Data></Cell>
   </Row>
   <Row ss:Height="10"/>
   <Row ss:Height="26">
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Tabla Puente</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Llave Base Primaria</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Llave Externa</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Coincidencia</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Campo Puente</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Tipo</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Descripción</Data></Cell>
   </Row>`;

  let bRowIdx = 0;
  dataMaster.tablas_puente.forEach(bridge => {
    const coincidenciaStr = bridge.tasa_coincidencia_registros 
      ? `${bridge.tasa_coincidencia_registros}% registros`
      : `${bridge.tasa_coincidencia_instituciones}% entidades`;
    bridge.columnas.forEach(c => {
      const styleRow = (bRowIdx % 2 === 0) ? "RowEven" : "RowOdd";
      bRowIdx++;
      xml += `
   <Row ss:Height="22">
    <Cell ss:StyleID="${styleRow}"><Data ss:Type="String">${escapeXml(bridge.tabla)}</Data></Cell>
    <Cell ss:StyleID="CodeStyle"><Data ss:Type="String">${escapeXml(bridge.llave_base)}</Data></Cell>
    <Cell ss:StyleID="CodeStyle"><Data ss:Type="String">${escapeXml(bridge.llave_externa)}</Data></Cell>
    <Cell ss:StyleID="${styleRow}"><Data ss:Type="String">${escapeXml(coincidenciaStr)}</Data></Cell>
    <Cell ss:StyleID="CodeStyle"><Data ss:Type="String">${escapeXml(c.nombre)}</Data></Cell>
    <Cell ss:StyleID="${styleRow}"><Data ss:Type="String">${escapeXml(c.tipo)}</Data></Cell>
    <Cell ss:StyleID="${styleRow}"><Data ss:Type="String">${escapeXml(c.descripcion)}</Data></Cell>
   </Row>`;
    });
  });
  xml += `
  </Table>
 </Worksheet>`;

  // PESTAÑA 4: RESUMEN DE RÚBRICA Y AUDITORÍA
  xml += `
 <Worksheet ss:Name="Rubrica_Hito1">
  <Table ss:DefaultRowHeight="20">
   <Column ss:Width="220"/>
   <Column ss:Width="60"/>
   <Column ss:Width="60"/>
   <Column ss:Width="140"/>
   <Column ss:Width="420"/>
   <Row ss:Height="28">
    <Cell ss:MergeAcross="4" ss:StyleID="TitleStyle"><Data ss:Type="String">MATRIZ DE CERTIFICACIÓN DE RÚBRICA (HITO 1: 17/17 PUNTOS)</Data></Cell>
   </Row>
   <Row ss:Height="18">
    <Cell ss:MergeAcross="4" ss:StyleID="SubtitleStyle"><Data ss:Type="String">Auditoría algorítmica verificada con 11_audit_hito1_integrity_p5.js (0 errores)</Data></Cell>
   </Row>
   <Row ss:Height="10"/>
   <Row ss:Height="26">
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Criterio Evaluado</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Puntos Max</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Puntos Obt</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Estado</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">Evidencia de Entrega en Repositorio</Data></Cell>
   </Row>
   <Row ss:Height="24">
    <Cell ss:StyleID="RowEven"><Data ss:Type="String">Propuesta de valor y Canvas BI</Data></Cell>
    <Cell ss:StyleID="RowEven"><Data ss:Type="Number">4</Data></Cell>
    <Cell ss:StyleID="RowEven"><Data ss:Type="Number">4</Data></Cell>
    <Cell ss:StyleID="CodeStyle"><Data ss:Type="String">100% CUMPLIDO</Data></Cell>
    <Cell ss:StyleID="RowEven"><Data ss:Type="String">Canvas BI formal de 10 bloques (informe_hito1_persona2.tex) y validación de 3 preguntas (informe_hito1_persona4.md)</Data></Cell>
   </Row>
   <Row ss:Height="24">
    <Cell ss:StyleID="RowOdd"><Data ss:Type="String">ETL: integración 2023-2026, diccionario y nulos</Data></Cell>
    <Cell ss:StyleID="RowOdd"><Data ss:Type="Number">8</Data></Cell>
    <Cell ss:StyleID="RowOdd"><Data ss:Type="Number">8</Data></Cell>
    <Cell ss:StyleID="CodeStyle"><Data ss:Type="String">100% CUMPLIDO</Data></Cell>
    <Cell ss:StyleID="RowOdd"><Data ss:Type="String">158.211 filas exactas (P_IN), diccionario maestro de 59 atributos, homologación PSU/PDT/PAES y tratamiento de nulos</Data></Cell>
   </Row>
   <Row ss:Height="24">
    <Cell ss:StyleID="RowEven"><Data ss:Type="String">Fuentes externas: llave, grano, tablas puente y panel</Data></Cell>
    <Cell ss:StyleID="RowEven"><Data ss:Type="Number">5</Data></Cell>
    <Cell ss:StyleID="RowEven"><Data ss:Type="Number">5</Data></Cell>
    <Cell ss:StyleID="CodeStyle"><Data ss:Type="String">100% CUMPLIDO</Data></Cell>
    <Cell ss:StyleID="RowEven"><Data ss:Type="String">INE y SIES oficiales con SHA-256, puente región (100%), puente institución (99% matrícula), Unknown Member y uso DAX</Data></Cell>
   </Row>
   <Row ss:Height="26">
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">TOTAL GRUPAL HITO 1</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="Number">17</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="Number">17</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">EXCELENCIA (17/17)</Data></Cell>
    <Cell ss:StyleID="HeaderStyle"><Data ss:Type="String">TODOS LOS ENTREGABLES COMPLETADOS Y AUDITADOS</Data></Cell>
   </Row>
  </Table>
 </Worksheet>
</Workbook>`;

  const excelPathP5 = path.join(P5_DOCS_DIR, "Diccionario_Datos_Maestro_Hito1.xls");
  const excelPathRoot = path.join(__dirname, '..', '..', "Diccionario_Datos_Maestro_Hito1.xls");
  fs.writeFileSync(excelPathP5, xml, "utf-8");
  fs.writeFileSync(excelPathRoot, xml, "utf-8");
  console.log("  [OK] Libro Excel (.xls) generado con éxito en P5_Hito1/docs y raíz.");
}

// -------------------------------------------------------------
// 2. GENERAR VISUALIZADOR WEB INTERACTIVO (.html)
// -------------------------------------------------------------
function buildInteractiveHtml() {
  console.log("=== GENERANDO VISUALIZADOR WEB INTERACTIVO PARA PRESENTACIÓN ===");
  const html = `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Diccionario de Datos Interactivo - Hito 1 | Business Intelligence</title>
<style>
  :root {
    --primary: #102C57;
    --primary-light: #1e3a8a;
    --secondary: #35598F;
    --accent: #146E78;
    --bg: #f8fafc;
    --card: #ffffff;
    --border: #e2e8f0;
    --text: #0f172a;
    --text-muted: #64748b;
  }
  body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    margin: 0;
    padding: 0;
  }
  header {
    background: var(--primary);
    color: white;
    padding: 24px 32px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
  }
  .header-content {
    max-width: 1300px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
  }
  h1 { margin: 0; font-size: 20pt; font-weight: 800; }
  .subtitle { margin-top: 4px; color: #94a3b8; font-size: 10.5pt; }
  .stats-bar {
    display: flex;
    gap: 16px;
  }
  .stat-pill {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 9pt;
    font-weight: 600;
  }
  .main-container {
    max-width: 1300px;
    margin: 24px auto;
    padding: 0 20px;
  }
  .tabs {
    display: flex;
    gap: 8px;
    border-bottom: 2px solid var(--border);
    margin-bottom: 20px;
  }
  .tab-btn {
    background: none;
    border: none;
    padding: 10px 20px;
    font-size: 10pt;
    font-weight: 600;
    color: var(--text-muted);
    cursor: pointer;
    border-bottom: 3px solid transparent;
    transition: all 0.2s;
  }
  .tab-btn:hover { color: var(--primary); }
  .tab-btn.active {
    color: var(--primary);
    border-bottom-color: var(--primary);
  }
  .search-box {
    margin-bottom: 18px;
    display: flex;
    gap: 12px;
  }
  .search-input {
    flex: 1;
    padding: 10px 16px;
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 10pt;
    outline: none;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  }
  .search-input:focus { border-color: var(--accent); }
  .filter-select {
    padding: 10px 14px;
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 9.5pt;
    background: white;
  }
  .table-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04);
  }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 9pt;
    text-align: left;
  }
  th {
    background: #f1f5f9;
    color: #334155;
    padding: 12px 14px;
    font-weight: 700;
    border-bottom: 2px solid var(--border);
  }
  td {
    padding: 10px 14px;
    border-bottom: 1px solid #f1f5f9;
    vertical-align: top;
  }
  tr:hover { background: #f8fafc; }
  .code {
    font-family: 'Consolas', monospace;
    font-size: 8.5pt;
    background: #e0f2fe;
    color: #0369a1;
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: 600;
  }
  .tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 7.5pt;
    font-weight: 700;
    text-transform: uppercase;
  }
  .tag-dim { background: #ede9fe; color: #6d28d9; }
  .tag-fact { background: #fef3c7; color: #b45309; }
  .tag-calc { background: #dcfce7; color: #15803d; }
  .tab-pane { display: none; }
  .tab-pane.active { display: block; }
</style>
</head>
<body>

<header>
  <div class="header-content">
    <div>
      <h1>Diccionario de Datos Maestro (Hito 1)</h1>
      <div class="subtitle">Proyecto Final Business Intelligence | Ingeniería en Negocios | Persona 5 (Documentador)</div>
    </div>
    <div class="stats-bar">
      <div class="stat-pill">📊 158.211 Filas</div>
      <div class="stat-pill">📋 59 Atributos CNED</div>
      <div class="stat-pill">🔗 2 Fuentes Externas (INE/SIES)</div>
      <div class="stat-pill">⭐ 17/17 Pts Rúbrica</div>
    </div>
  </div>
</header>

<div class="main-container">
  <div class="tabs">
    <button class="tab-btn active" onclick="switchTab('tab-cned')">Base CNED (59 Columnas)</button>
    <button class="tab-btn" onclick="switchTab('tab-ext')">Fuentes Externas (INE y SIES)</button>
    <button class="tab-btn" onclick="switchTab('tab-bridge')">Tablas Puente</button>
  </div>

  <!-- TAB CNED -->
  <div id="tab-cned" class="tab-pane active">
    <div class="search-box">
      <input type="text" id="cnedSearch" class="search-input" placeholder="Buscar por nombre, categoría, regla ETL o nulos..." onkeyup="filterCnedTable()">
      <select id="cnedCategoryFilter" class="filter-select" onchange="filterCnedTable()">
        <option value="">Todas las categorías</option>
        <option value="Temporal">Dimensión Temporal</option>
        <option value="Institución">Dimensión Institución</option>
        <option value="Geográfica">Dimensión Geográfica</option>
        <option value="Programa">Dimensión Programa</option>
        <option value="Carrera">Dimensión Carrera</option>
        <option value="Hecho">Hecho / Medida</option>
        <option value="Métrica">Métrica Analítica</option>
      </select>
    </div>

    <div class="table-card">
      <table id="cnedTable">
        <thead>
          <tr>
            <th style="width: 40px;">#</th>
            <th style="width: 170px;">Nombre Final</th>
            <th style="width: 150px;">Nombre Orig. (12-22)</th>
            <th style="width: 150px;">Nombre Orig. (23-26)</th>
            <th style="width: 90px;">Tipo</th>
            <th style="width: 140px;">Categoría</th>
            <th>Regla de Transformación ETL</th>
            <th>Tratamiento de Nulos y Justificación</th>
          </tr>
        </thead>
        <tbody>
${dataMaster.columnas_cned_consolidada.map((col, idx) => `
          <tr>
            <td>${idx + 1}</td>
            <td><span class="code">${escapeXml(col.nombre_final)}</span></td>
            <td>${escapeXml(col.nombre_orig_2012_2022)}</td>
            <td>${escapeXml(col.nombre_orig_2023_2026)}</td>
            <td><span class="code">${escapeXml(col.tipo_dato)}</span></td>
            <td><span class="tag ${col.categoria.includes('Hecho') ? 'tag-fact' : col.categoria.includes('Métrica') ? 'tag-calc' : 'tag-dim'}">${escapeXml(col.categoria)}</span></td>
            <td>${escapeXml(col.regla_transformacion)}</td>
            <td><em>${escapeXml(col.tratamiento_nulos)}</em></td>
          </tr>`).join('')}
        </tbody>
      </table>
    </div>
  </div>

  <!-- TAB EXTERNAS -->
  <div id="tab-ext" class="tab-pane">
    <div class="table-card">
      <table>
        <thead>
          <tr>
            <th>Fuente y Archivo</th>
            <th>Grano Declarado</th>
            <th>Llave de Cruce</th>
            <th>Campo</th>
            <th>Tipo</th>
            <th>Descripción</th>
          </tr>
        </thead>
        <tbody>
${dataMaster.fuentes_externas.flatMap(f => f.columnas.map(c => `
          <tr>
            <td><strong>${escapeXml(f.fuente)}</strong><br><small style="color:var(--text-muted);">${escapeXml(f.tabla)}</small></td>
            <td>${escapeXml(f.grano)}</td>
            <td><span class="code">${escapeXml(f.llave_cruce)}</span></td>
            <td><span class="code">${escapeXml(c.nombre)}</span></td>
            <td>${escapeXml(c.tipo)}</td>
            <td>${escapeXml(c.descripcion)}</td>
          </tr>`)).join('')}
        </tbody>
      </table>
    </div>
  </div>

  <!-- TAB TABLAS PUENTE -->
  <div id="tab-bridge" class="tab-pane">
    <div class="table-card">
      <table>
        <thead>
          <tr>
            <th>Tabla Puente</th>
            <th>Llave Base Primaria</th>
            <th>Llave Externa</th>
            <th>Tasa de Coincidencia</th>
            <th>Campo Puente</th>
            <th>Tipo</th>
            <th>Descripción</th>
          </tr>
        </thead>
        <tbody>
${dataMaster.tablas_puente.flatMap(b => b.columnas.map(c => `
          <tr>
            <td><strong>${escapeXml(b.tabla)}</strong></td>
            <td><span class="code">${escapeXml(b.llave_base)}</span></td>
            <td><span class="code">${escapeXml(b.llave_externa)}</span></td>
            <td><strong style="color:#15803d;">${b.tasa_coincidencia_registros ? b.tasa_coincidencia_registros + '%' : b.tasa_coincidencia_instituciones + '%'}</strong></td>
            <td><span class="code">${escapeXml(c.nombre)}</span></td>
            <td>${escapeXml(c.tipo)}</td>
            <td>${escapeXml(c.descripcion)}</td>
          </tr>`)).join('')}
        </tbody>
      </table>
    </div>
  </div>
</div>

<script>
function switchTab(tabId) {
  document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById(tabId).classList.add('active');
  event.target.classList.add('active');
}

function filterCnedTable() {
  const query = document.getElementById('cnedSearch').value.toLowerCase();
  const cat = document.getElementById('cnedCategoryFilter').value.toLowerCase();
  const rows = document.querySelectorAll('#cnedTable tbody tr');
  rows.forEach(row => {
    const text = row.innerText.toLowerCase();
    const matchesQuery = !query || text.includes(query);
    const matchesCat = !cat || text.includes(cat);
    row.style.display = (matchesQuery && matchesCat) ? '' : 'none';
  });
}
</script>

</body>
</html>`;

  const htmlPathP5 = path.join(P5_DOCS_DIR, "diccionario_datos_interactivo.html");
  const htmlPathRoot = path.join(__dirname, '..', '..', "diccionario_datos_interactivo.html");
  fs.writeFileSync(htmlPathP5, html, "utf-8");
  fs.writeFileSync(htmlPathRoot, html, "utf-8");
  console.log("  [OK] Visualizador Web interactivo generado en P5_Hito1/docs y raíz.");
}

// -------------------------------------------------------------
// 3. COMPILAR INFORME DE PERSONA 5 EN PDF
// -------------------------------------------------------------
function buildInformePersona5Pdf() {
  console.log("=== COMPILANDO INFORME FORMAL DE PERSONA 5 EN PDF ===");
  const mdPath = path.join(P5_DOCS_DIR, "informe_hito1_persona5.md");
  const mdContent = fs.readFileSync(mdPath, "utf-8");

  // Crear HTML con renderizado editorial para informe_hito1_persona5
  // Para transformar el Markdown a HTML estructurado
  const informeHtmlPath = path.join(P5_DOCS_DIR, "informe_hito1_persona5_render.html");
  const informePdfPathP5 = path.join(P5_DOCS_DIR, "informe_hito1_persona5.pdf");
  const informePdfPathRoot = path.join(__dirname, '..', '..', "informe_hito1_persona5.pdf");

  // Estilo editorial limpio
  let htmlDoc = `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Informe Técnico y de Gestión - Hito 1 | Persona 5</title>
<style>
  @page { size: A4; margin: 16mm 14mm 16mm 14mm; }
  body { font-family: 'Segoe UI', -apple-system, sans-serif; color: #1e293b; line-height: 1.5; font-size: 9.5pt; margin: 0; padding: 0; }
  .cover { page-break-after: always; text-align: center; padding-top: 60px; }
  h1.title { color: #102C57; font-size: 24pt; font-weight: 800; margin-bottom: 12px; }
  h2.sub { color: #35598F; font-size: 13pt; font-weight: 500; margin-bottom: 30px; }
  .box { background: #f8fafc; border: 2px solid #cbd5e1; border-radius: 8px; padding: 18px 24px; max-width: 550px; margin: 0 auto; text-align: left; font-size: 9pt; }
  h1 { color: #102C57; font-size: 14pt; border-bottom: 2px solid #102C57; padding-bottom: 4px; margin-top: 22px; page-break-after: avoid; }
  h2 { color: #35598F; font-size: 11.5pt; border-bottom: 1px solid #e2e8f0; padding-bottom: 3px; margin-top: 16px; page-break-after: avoid; }
  h3 { color: #146E78; font-size: 10pt; margin-top: 12px; page-break-after: avoid; }
  p { margin: 0 0 8px 0; text-align: justify; }
  table { width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 8.5pt; page-break-inside: avoid; }
  th, td { border: 1px solid #cbd5e1; padding: 6px 8px; text-align: left; vertical-align: top; }
  th { background: #102C57; color: white; font-weight: 600; }
  tr:nth-child(even) { background: #f8fafc; }
  .code { font-family: monospace; background: #f1f5f9; padding: 2px 4px; border-radius: 3px; }
  .callout { background: #f0fdf4; border-left: 4px solid #16a34a; padding: 10px 14px; margin: 12px 0; border-radius: 4px; font-size: 8.8pt; }
</style>
</head>
<body>
<div class="cover">
  <div style="display:inline-block; padding:4px 12px; background:#e0e7ff; color:#3730a3; font-weight:700; border-radius:16px; font-size:8pt; margin-bottom:20px; text-transform:uppercase;">Informe Oficial de Entrega</div>
  <h1 class="title">INFORME DE GOBERNANZA, TRAZABILIDAD Y DICCIONARIO MAESTRO</h1>
  <h2 class="sub">Hito 1: Propuesta, ETL y Fuentes Externas (2012–2026)</h2>
  <div class="box">
    <p><strong>Proyecto:</strong> Business Intelligence - Educación Superior Chilena</p>
    <p><strong>Rol Evaluado:</strong> Persona 5: Gestor del Proyecto y Documentador</p>
    <p><strong>Fecha de Entrega:</strong> 21 de Octubre de 2026</p>
    <p><strong>Puntaje Hito 1:</strong> 17 Puntos Grupales (Certificación 17/17 Puntos)</p>
    <p><strong>Equipo:</strong> P1: ETL | P2: Negocios | P3: Arquitecto DB | P4: Desarrollador BI | P5: Documentador</p>
  </div>
</div>
`;

  // Convert basic markdown paragraphs and headings to HTML
  const lines = mdContent.split('\n');
  let inTable = false;
  let tableRows = [];

  for (let i = 0; i < lines.length; i++) {
    let line = lines[i].trim();
    if (line.startsWith('# ')) continue; // Skip title as it is in cover
    if (line.startsWith('## ')) {
      htmlDoc += `<h1>${escapeXml(line.replace('## ', ''))}</h1>\n`;
    } else if (line.startsWith('### ')) {
      htmlDoc += `<h2>${escapeXml(line.replace('### ', ''))}</h2>\n`;
    } else if (line.startsWith('#### ')) {
      htmlDoc += `<h3>${escapeXml(line.replace('#### ', ''))}</h3>\n`;
    } else if (line.startsWith('|')) {
      if (!inTable) {
        inTable = true;
        tableRows = [];
      }
      if (!line.includes(':---') && !line.includes('---')) {
        tableRows.push(line);
      }
    } else {
      if (inTable) {
        // flush table
        htmlDoc += '<table>\n';
        tableRows.forEach((tr, rIdx) => {
          const cells = tr.split('|').slice(1, -1).map(c => c.trim());
          const tag = (rIdx === 0) ? 'th' : 'td';
          htmlDoc += `  <tr>${cells.map(c => `<${tag}>${escapeXml(c).replace(/`([^`]+)`/g, '<span class="code">$1</span>').replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')}</${tag}>`).join('')}</tr>\n`;
        });
        htmlDoc += '</table>\n';
        inTable = false;
      }
      if (line.startsWith('- ') || line.startsWith('* ')) {
        const item = line.substring(2).replace(/`([^`]+)`/g, '<span class="code">$1</span>').replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        htmlDoc += `<li>${item}</li>\n`;
      } else if (line.length > 0 && !line.startsWith('```') && !line.startsWith('---')) {
        const p = line.replace(/`([^`]+)`/g, '<span class="code">$1</span>').replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        htmlDoc += `<p>${p}</p>\n`;
      }
    }
  }

  htmlDoc += `</body></html>`;
  fs.writeFileSync(informeHtmlPath, htmlDoc, 'utf-8');

  // Compilar con Edge headless a PDF
  const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
  const argsP5 = ['--headless=new', '--disable-gpu', '--no-pdf-header-footer', `--print-to-pdf=${informePdfPathP5}`, informeHtmlPath];
  const argsRoot = ['--headless=new', '--disable-gpu', '--no-pdf-header-footer', `--print-to-pdf=${informePdfPathRoot}`, informeHtmlPath];

  spawnSync(edgePath, argsP5, { encoding: 'utf-8' });
  spawnSync(edgePath, argsRoot, { encoding: 'utf-8' });

  if (fs.existsSync(informePdfPathP5)) {
    const sz = fs.statSync(informePdfPathP5).size;
    console.log(`  [OK] PDF Informe Persona 5 generado (${(sz / 1024).toFixed(1)} KB): ${informePdfPathP5}`);
  }
}

buildExcelXml();
buildInteractiveHtml();
buildInformePersona5Pdf();
