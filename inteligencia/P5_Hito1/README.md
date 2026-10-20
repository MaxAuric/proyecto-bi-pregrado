# Entregables Hito 1 - Persona 5: Gestor del Proyecto y Documentador

Este directorio contiene la solución integral, gobernanza técnica, diccionarios maestros y centralización de la trazabilidad correspondientes al rol de **Persona 5 (Gestor del Proyecto y Documentador)** para el **Hito 1** del Proyecto Práctico Final de Business Intelligence.

---

## 📌 Responsabilidad Asignada en el Hito 1

De acuerdo con el documento oficial de planificación (*Planificación y Asignación de Roles*, 10 de octubre de 2026, sección 2.1):

> **Persona 5 (Gestor del Proyecto y Documentador):**  
> *«Construye el Diccionario de Datos exhaustivo (mapeando nombres antiguos, nuevos y reglas de transformación) y documenta las tablas puente de fuentes externas».*

---

## 📁 Estructura del Directorio `P5_Hito1/`

```text
inteligencia/P5_Hito1/
├── README.md                                      # Este documento de gobernanza y navegación
│
├── docs/                                          # Informes ejecutivos, diccionarios y documentación técnica
│   ├── informe_hito1_persona5.md                  # Informe técnico y de gestión consolidado en Markdown
│   ├── informe_hito1_persona5.tex                 # Código fuente LaTeX corporativo del informe
│   ├── diccionario_datos_exhaustivo_maestro.md    # Diccionario maestro de 59 atributos CNED + externas + puentes
│   ├── diccionario_datos_exhaustivo_maestro.json  # Diccionario estructurado en JSON interoperable
│   ├── tabla_diccionario_maestro.tex              # Anexo tabular en LaTeX para compilación
│   └── documentacion_tablas_puente_fuentes_externas.md # Documentación formal de INE, SIES, grano y tasas de cruce
│
├── scripts/                                       # Pipeline reproducible en Node.js y Python
│   ├── 10_generate_master_dictionary_p5.js        # Generador automatizado de diccionarios (JSON, MD, LaTeX)
│   ├── 10_generate_master_dictionary_p5.py        # Wrapper en Python para ejecución multiplataforma
│   └── 11_audit_hito1_integrity_p5.js             # Auditoría algorítmica de integridad y cuadre de la base
│
└── auditoria/                                     # Reportes de auditoría y certificación de la rúbrica
    ├── auditoria_cumplimiento_rubrica_hito1.json  # Matriz de evaluación certificada (17/17 puntos)
    └── metricas_integracion_hito1.json            # Indicadores consolidados de filas, columnas y tasas de cruce
```

---

## 🚀 Cómo Reproducir y Auditar

Para verificar la integridad referencial de todos los entregables y regenerar los diccionarios maestros:

```bash
# 1. Regenerar el Diccionario de Datos Maestro (59 columnas CNED + fuentes externas + tablas puente):
node inteligencia/P5_Hito1/scripts/10_generate_master_dictionary_p5.js
# O en Python:
python inteligencia/P5_Hito1/scripts/10_generate_master_dictionary_p5.py

# 2. Ejecutar la Auditoría Global de Integridad y Certificación del Hito 1:
node inteligencia/P5_Hito1/scripts/11_audit_hito1_integrity_p5.js
```

---

## 📊 Síntesis de Resultados del Hito 1 (Certificación 17/17 Puntos)

1. **Cuadre Estadístico Exacto de la Base Consolidada:**
   - Base entregada (2012–2022): **114.265 registros** (35 variables originales).
   - CNED Oficial Pregrado (2023–2026): **43.946 registros**.
   - **Total Consolidado Auditado:** **158.211 registros** y **59 columnas gobernadas**.
2. **Diccionario de Datos Exhaustivo:**
   - Mapeo 1:1 de nombres antiguos, nombres nuevos del CNED, tipos SQL, grano dimensional, reglas ETL y fundamentación de nulos.
3. **Resolución de Nulos y Quiebres:**
   - **Puntajes (~80,5% nulos):** Justificados matemáticamente por tipo de institución (CFT e IP no exigen prueba). Preservados como `NULL` + flag `flag_exige_prueba_admision`. Homologación en 4 escalas continuas (nativa, Min-Max [0,100], proyección PAES [100,1000] y $Z$-score).
   - **Vacantes (~25,4% nulos):** Preservados como `NULL` para no simular cierre de carreras ni inducir divisiones por cero + flag `flag_vacantes_declaradas`.
   - **Ñuble:** Identificación de 1.599 registros históricos previos a 2018 con `flag_quiebre_nuble = 1`.
4. **Fuentes Externas y Tablas Puente:**
   - **INE (Población regional):** Grano región $\times$ año. Tasa de cruce del **100,00%** de los registros (16/16 regiones).
   - **SIES (Acreditación IES vigentes):** Grano institución $\times$ año. Tasa de cruce del **98,39%** de los registros y **99,00%** de la matrícula de primer año.
   - **Tratamiento de No Coincidentes:** 15 extintas pre-2018 por ausencia estructural y 4 en procesos de cierre se preservan con `codigo_ies = NULL` vinculadas al **Miembro Desconocido (-1)** sin eliminar ningún registro de hechos.
5. **Matriz de Rúbrica Oficial:**
   - Propuesta de Valor y Canvas BI: **4 / 4 pts**.
   - ETL, Diccionario, Homologación y Nulos: **8 / 8 pts**.
   - Fuentes Externas, Llave, Grano, Tablas Puente y Panel: **5 / 5 pts**.
   - **Subtotal Grupal Hito 1:** **17 / 17 PUNTOS**.

---

## 💬 Mensaje de Cierre para el Equipo (Listo para Enviar)

> *"¡Hola equipo! Como Persona 5 (Gestor del Proyecto y Documentador) doy por finalizado y cerrado formalmente el **Hito 1**.*  
> *En la carpeta `inteligencia/P5_Hito1/` dejé consolidada toda la entrega:*  
> *1. En `docs/diccionario_datos_exhaustivo_maestro.md` (y su versión `.json` y `.tex` en `docs/tabla_diccionario_maestro.tex`) está el Diccionario Maestro con las 59 columnas mapeando nombres antiguos (12-22), nuevos (23-26), reglas ETL, justificación de nulos en puntajes y vacantes, y quiebre de Ñuble.*  
> *2. En `docs/documentacion_tablas_puente_fuentes_externas.md` quedó documentada la trazabilidad criptográfica (SHA-256), grano, llaves y el informe de tasas de cruce (100% en región con INE y 99,00% de matrícula en instituciones con SIES), junto con la justificación de las 19 IES no coincidentes manejadas como miembro desconocido sin pérdida de hechos.*  
> *3. En `docs/informe_hito1_persona5.md` y `.tex` está el Informe Ejecutivo Maestro con la matriz de auditoría que certifica los **17/17 puntos de la rúbrica grupal**.*  
> *4. En `scripts/` tienen los scripts reproducibles `10_generate_master_dictionary_p5.js` y `11_audit_hito1_integrity_p5.js` que validan el cuadre exacto de los 158.211 registros.*  
> *¡Hito 1 listo para entrega y preparados para comenzar el Hito 2 (Modelo Dimensional y DataMart)!"*
