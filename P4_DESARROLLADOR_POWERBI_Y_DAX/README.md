# Persona 4 - Desarrollador BI y Especialista DAX
## Entrega Final - Business Intelligence - Region Metropolitana de Santiago
**Fecha:** 18 de Noviembre 2026  
**Autor:** Joaquin Aguilera  
**Alcance:** 100% Region Metropolitana (58.926 registros 2012-2026, 69 IES activas 2026)

---

## Estructura de la Carpeta

```
Final/P4_DESARROLLADOR_POWERBI_Y_DAX/
|-- docs/
|   |-- medidas_dax_completas_rm.dax              # 40+ medidas DAX (COPIAR A POWER BI)
|   |-- diseno_dashboard_3_vistas_rm.md           # Especificacion tecnica 3 vistas ejecutivas
|   |-- informe_final_persona4_powerbi_dax.md     # Informe tecnico final completo
|   |-- validacion_modelo_powerbi.json            # Reporte certificado 8/8 validaciones
|-- powerbi_templates/
|   |-- guia_conexion_datamart_estrella_rm.md     # Paso a paso conexion + modelo + jerarquias
|-- scripts/
|   |-- validar_modelo_powerbi.py                 # Validacion automatica (ejecutar en Python)
|-- capturas_dashboard/                           # PNGs 1920x1080 para Informe/PPT (generar)
|-- README.md                                     # Este archivo
```

---

## Inicio Rapido: Construir Dashboard_Final_RM.pbix

### 1. Conectar DataMart

Abrir Power BI Desktop, ir a Obtener datos y seleccionar Excel. Buscar el archivo:

```
Final/00_DATAMART_LISTO_PARA_POWERBI/DataMart_Estrella_RM_PowerBI.xlsx
```

Marcar las 7 tablas que aparecen:

1. dim_tiempo_ine_rm
2. dim_sede_geografia
3. dim_institucion_sies
4. dim_carrera_programa
5. fact_matricula_admision
6. agg_resumen_institucion_rm
7. puente_institucion_sies

La tabla puente_institucion_sies conecta los nombres abreviados de institucion de la base CNED con los codigos del SIES. Es necesaria para que las relaciones del modelo estrella funcionen correctamente.

Hacer clic en Cargar (no en Transformar datos).

### 2. Crear Medidas DAX
- Abrir `docs/medidas_dax_completas_rm.dax`
- Ir a Modelado, Nueva tabla, ponerle de nombre `Medidas DAX RM` y escribir `{ BLANK() }`
- Click derecho sobre esa tabla, Nueva medida, pegar cada bloque y dar Enter
- Asignar carpetas de visualizacion segun la guia

### 3. Configurar Jerarquias y Segmentadores
- Ver `powerbi_templates/guia_conexion_datamart_estrella_rm.md` secciones 5 y 6
- 4 jerarquias: Geografica, Institucional, Academica, Temporal
- 4 slicers obligatorios: Ano, Institucion, Sede/Comuna RM, Tramo SIES

### 4. Construir 3 Vistas
- Seguir `docs/diseno_dashboard_3_vistas_rm.md` (layout exacto, medidas, filtros, bookmarks)

### 5. Validar
```bash
python scripts/validar_modelo_powerbi.py
# Debe mostrar: 8/8 validaciones APROBADAS
```

### 6. Generar Capturas
- Exportar cada vista como PNG 1920x1080 a `capturas_dashboard/`
- Para Informe Ejecutivo y PPT de defensa

---

## Archivos Clave de Referencia

| Archivo | Descripcion |
|---------|-------------|
| `Final/00_DATAMART_LISTO_PARA_POWERBI/DataMart_Estrella_RM_PowerBI.xlsx` | Fuente principal (7 hojas: modelo estrella + tabla puente) |
| `Final/00_DATAMART_LISTO_PARA_POWERBI/datamart_estrella_rm_final.db` | Respaldo SQLite |
| `Final/contexto a tomar en cuenta persona 3/02_CATALOGO_NUEVAS_TASAS_KPIS_Y_DAX_RM.md` | Catalogo maestro tasas/KPIs/DAX |

---

## Cumplimiento Pauta Oficial (Rubrica Final)

| Criterio | Puntaje | Estado |
|----------|---------|--------|
| Panel Power BI conectado al DataMart (no Excel crudo) | 8 grupales | COMPLETO |
| Responde 3 preguntas de negocio Canvas | 8 grupales | 3 Vistas dedicadas |
| Filtros: Ano, Institucion, Region | 8 grupales | 4 Slicers + Sede/Tramo |
| Al menos 1 medida DAX creada | 8 grupales | 40+ medidas con DIVIDE |
| Aditividad correcta (SUM vs DIVIDE ponderado) | 8 grupales | Documentado |
| Cero abreviaturas en dimensiones/filtros | 8 grupales | Nombres completos |

---

## Preguntas Tecnicas Preparadas para Defensa Individual

Ver `docs/informe_final_persona4_powerbi_dax.md` Seccion 6.4 (6 preguntas con respuestas clave)

---

## Contacto
**Persona 4:** Joaquin Aguilera  
**Rol:** Desarrollador BI y Especialista DAX  
**Entrega:** Final - 18 Noviembre 2026
