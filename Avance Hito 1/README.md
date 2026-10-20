# 📁 Directorio Oficial de Entrega: Avance Hito 1
## Proyecto Práctico Final de Business Intelligence - Educación Superior Chilena (2012–2026)

Este directorio contiene **exclusivamente los entregables limpios, consolidados y auditados del Hito 1**, estructurados para facilitar la exposición oral, la navegación docente y la defensa individual ante la interrogación de avance.

---

## 🗂️ Estructura de Navegación del Avance

### 📍 [00_DOCUMENTOS_PARA_PRESENTAR_Y_DEFENDER/](file:///c:/Users/lucas/Desktop/inteligencia/proyecto-bi-pregrado-main/Avance%20Hito%201/00_DOCUMENTOS_PARA_PRESENTAR_Y_DEFENDER/)
*Documentos principales listos para abrir y proyectar en clase o enviar por correo/buzón:*
- **`Guia_Maestra_Estudio_y_Defensa_Hito1.pdf`**: Guía pedagógica de 8 páginas para estudiar antes de la presentación. Incluye resumen por roles, preguntas trampa del profesor y respuestas exactas.
- **`Informe_Ejecutivo_Hito1_Persona5.pdf`**: Informe formal de cierre del Hito 1 con la certificación de los 17 puntos de la rúbrica.
- **`Diccionario_Datos_Maestro_Hito1.xls`**: Libro Excel interactivo de 4 pestañas formateadas para mostrar el diccionario con filtros y colores.
- **`Diccionario_Datos_Interactivo.html`**: Visor web interactivo con buscador en vivo en el navegador.
- **`Informe_Hito1_Persona1_ETL.pdf`**: Informe técnico de Persona 1 sobre el pipeline ETL y homologación.
- **`Informe_Hito1_Persona4_Visualizacion.pdf`**: Informe técnico de Persona 4 sobre graficabilidad en Power BI.

---

### 📍 [01_PROPUESTA_VALOR_Y_CANVAS_BI/](file:///c:/Users/lucas/Desktop/inteligencia/proyecto-bi-pregrado-main/Avance%20Hito%201/01_PROPUESTA_VALOR_Y_CANVAS_BI/) *(Criterio 1 de Rúbrica - 4 Pts)*
- Enfoque de negocio para Directores de Admisión y Planificación Universitaria.
- **Canvas BI de 10 bloques** formalizado.
- **Tres Preguntas de Negocio:** P1 (Equidad Territorial), P2 (Uso de Capacidad) y P3 (Calidad y Acreditación).
- **Prototipos visuales** de alta resolución y catálogo de medidas DAX con control de semi-aditividad.

---

### 📍 [02_ETL_Y_BASE_CONSOLIDADA_2012_2026/](file:///c:/Users/lucas/Desktop/inteligencia/proyecto-bi-pregrado-main/Avance%20Hito%201/02_ETL_Y_BASE_CONSOLIDADA_2012_2026/) *(Criterio 2 de Rúbrica - 8 Pts)*
- **`base_indices_consolidada_2012_2026.csv`** (79 MB) y **`.parquet`** (4.2 MB) con **158.211 filas exactas y 59 columnas gobernadas**.
- Cero datos simulados: 114.265 filas históricas (2012–2022) + 43.946 del portal CNED oficial (2023–2026).
- Pipeline de scripts en Python (`pipeline_scripts/`) y bases crudas inmutables (`fuentes_crudas_oficiales/`).
- Homologación psicométrica cuádruple de puntajes (PSU, PDT, PAES) y justificación matemática de nulos con flags.

---

### 📍 [03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE/](file:///c:/Users/lucas/Desktop/inteligencia/proyecto-bi-pregrado-main/Avance%20Hito%201/03_FUENTES_EXTERNAS_Y_TABLAS_PUENTE/) *(Criterio 3 de Rúbrica - 5 Pts)*
- **Fuente 1 INE:** Proyecciones de población por región (Censo 2017). Tasa de coincidencia del **100,00%** mediante `puente_region.csv`.
- **Fuente 2 SIES:** Acreditación de IES vigentes (2018–2026). Tasa de coincidencia del **98,39% de filas** y **99,00% de la matrícula** mediante `puente_institucion.csv`.
- Trazabilidad criptográfica con fecha 15-oct-2026 y hash SHA-256 en `manifiesto_descargas_sha256.json`.
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
