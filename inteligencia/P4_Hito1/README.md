# Entregables Hito 1 - Persona 4: Desarrollador BI

Este directorio contiene la solución completa y los entregables correspondientes al rol de **Persona 4 (Desarrollador BI)** en el **Hito 1** del Proyecto Práctico Final de Business Intelligence.

---

## Responsabilidad Asignada en el Hito 1
De acuerdo con la planificación oficial del equipo (*Planificación y Asignación de Roles*):
> **Persona 4 (Desarrollador BI):** *«Revisa la Propuesta de Valor para asegurar que las 3 preguntas de negocio propuestas puedan ser graficadas a futuro en el panel».*

---

## Estructura del Directorio `P4_Hito1/`

```text
inteligencia/P4_Hito1/
├── README.md                              # Documentación general y guía de navegación
├── docs/                                  # Informes formales, wireframes y catálogo DAX
│   ├── informe_hito1_persona4.pdf         # Informe Técnico Ejecutivo compilado en LaTeX
│   ├── informe_hito1_persona4.tex         # Código fuente LaTeX del informe (estilo corporativo)
│   ├── informe_hito1_persona4.md          # Versión completa del informe en Markdown
│   ├── especificacion_dashboard_wireframes.md # Arquitectura UX/UI, wireframes y directrices
│   └── catalogo_medidas_dax.md            # Catálogo formal de medidas y expresiones DAX
│
├── scripts/                               # Scripts reproducibles en Python
│   ├── 08_validar_viabilidad_visual_p4.py # Auditoría computacional de viabilidad de datos
│   └── 09_generar_visualizaciones_prototipo.py # Generación de prototipos visuales de alta resolución
│
└── data_validation/                       # Evidencia numérica y prototipos gráficos
    ├── auditoria_viabilidad_preguntas.json # Resumen estructurado en JSON de la auditoría
    ├── preview_visual_p1_equidad_territorial.csv # Datos agregados de P1 (tasa p/1.000 hab.)
    ├── preview_visual_p2_capacidad_ocupacion.csv # Matriz de ocupación tipo IES x Región (P2)
    ├── preview_visual_p3_calidad_acreditacion.csv # Serie histórica % acreditación SIES (P3)
    └── visual_prototypes/                 # Figuras de validación visual para Power BI
        ├── p1_equidad_territorial.png     # Prototipo gráfico P1 (Barras 2018 vs 2026)
        ├── p2_capacidad_ocupacion.png     # Prototipo gráfico P2 (Serie temporal + Heatmap)
        ├── p3_calidad_acreditacion.png     # Prototipo gráfico P3 (Barras 100% + Dispersión)
        └── dashboard_wireframe_arquitectura.png # Wireframe conceptual del Dashboard
```

---

## Cómo Ejecutar y Reproducir

Para ejecutar los scripts de auditoría y regenerar los prototipos visuales:

```bash
# 1. Ejecutar auditoría de datos y verificar viabilidad analítica:
python inteligencia/P4_Hito1/scripts/08_validar_viabilidad_visual_p4.py

# 2. Generar prototipos visuales de las 3 preguntas:
python inteligencia/P4_Hito1/scripts/09_generar_visualizaciones_prototipo.py

# 3. Compilar el informe en LaTeX (requiere MiKTeX/TeX Live):
pdflatex -output-directory=inteligencia/P4_Hito1/docs inteligencia/P4_Hito1/docs/informe_hito1_persona4.tex
```

---

## Resumen de Resultados de la Auditoría

1. **Veredicto Técnico General:** Las 3 preguntas de negocio son **100% factibles y graficables** en Power BI Desktop utilizando la base CNED consolidada y los cruces con INE y SIES.
2. **P1 (Equidad Territorial):** Se valida el uso de un mapa coroplético y gráfico de barras horizontales ordenadas. Se documenta la medida DAX `[Poblacion_15_64_INE]` con tratamiento de **semi-aditividad temporal** para evitar acumulaciones erróneas entre años.
3. **P2 (Uso de Capacidad):** Se confirma que la exclusión de nulos mediante `flag_vacantes_declaradas = 1` y `vacantes > 0` permite calcular la tasa de ocupación con total estabilidad matemática (84,4% en 2026), apta para matrices heatmap y series temporales con bandas de alerta.
4. **P3 (Calidad y Competencia):** Se valida el gráfico de barras 100% apiladas y el gráfico de dispersión (Scatter Plot) de años de acreditación vs. matrícula. Se establece como directriz de diseño fijar el filtro predeterminado de la página en `Año >= 2018` debido a la cobertura de los listados SIES oficiales.
5. **Arquitectura del Dashboard:** Estructuración de un panel de 4 páginas ejecutivas con filtros globales sincronizados y 3 jerarquías de drill-down (Geográfica, Institucional y Curricular).
