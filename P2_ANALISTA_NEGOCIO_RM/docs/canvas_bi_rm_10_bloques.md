# Canvas BI de 10 Bloques — Entrega Final
## Sistema de BI para Capacidad Instalada, Sobredemanda y Selectividad
## Región Metropolitana de Santiago (2012–2026)

> **Cifras auditadas:** 58.926 registros RM | 69 IES activas 2026 (35 Universidades, 19 IP, 11 CFT, 4 FF.AA.)

---

| Bloque | Contenido |
|---|---|
| **1. Usuarios** | **Interno:** Dirección de Admisión y Planificación de IES en la RM. **Externo:** Subsecretaría Educación Superior, CNED, equipos de política pública regional Santiago. |
| **2. Problema** | Las IES deciden su oferta de vacantes sin observar simultáneamente: (a) presión real de demanda vs. capacidad instalada de laboratorios, (b) evolución de selectividad PAES ante esa presión y (c) absorción demográfica de la cohorte juvenil RM. Resultado: sobreocupación silenciosa, apertura no planificada de paralelos, aumento deserción. |
| **3. Decisiones** | (a) Ajustar vacantes por carrera/sede RM sin sobrepasar umbral de saturación de laboratorios (módulo 35 puestos). (b) Monitorear si puntaje PAES de corte cae ante picos de demanda y cuándo activar programas de nivelación. (c) Priorizar sedes y áreas con saturación frente a IES de baja acreditación SIES. |
| **4. Preguntas** | **P1:** ¿Qué carreras/áreas RM tienen sobredemanda crítica y cuántas secciones extra de laboratorio generan? **P2:** ¿Cómo evolucionan puntajes PAES de corte ante picos de sobredemanda? **P3:** ¿La oferta RM absorbe a la cohorte juvenil 18–24 (INE) o hay saturación demográfica frente a IES de baja acreditación? |
| **5. KPIs** | Tasa de Ocupación de Vacantes RM (%) · Secciones Extra por Sobrecupo · Tasa de Saturación Laboratorio Base 35 (%) · Puntaje PAES Ponderado RM · Tasa de Absorción Juvenil INE RM (%) · Tasa de Cobertura Bruta RM (%) · % IES en Cuadrante Líder (posicionamiento competitivo) |
| **6. Fuentes** | **Interna:** Base CNED/ÍNDICES 2012–2026 (58.926 registros RM, DataMart Persona 1). **Externa 1:** INE Proyecciones Demográficas RM 2002–2035 → `dim_tiempo_ine_rm`. **Externa 2:** SIES/CNA Acreditación IES 2018–2026 → `dim_institucion_sies`. |
| **7. Dimensiones** | `dim_tiempo_ine_rm` (Año + INE) · `dim_institucion_sies` (Institución + SIES SCD Tipo 2) · `dim_sede_geografia` (Sede/Comuna RM) · `dim_carrera_programa` (Carrera → Área → Programa) |
| **8. Medidas** | **Aditivas:** Matrícula, Vacantes, Secciones de laboratorio. **No aditivas (algebraicas):** Tasas de ocupación, sobredemanda, saturación, absorción → recalcular con `DIVIDE()` en DAX. **No aditivas (holísticas):** Puntajes PAES → promedio ponderado por matrícula, **nunca** `SUM`. |
| **9. Visualización** | **P1:** Barras apiladas vacantes vs. matrícula por área RM; mapa de calor saturación laboratorio por carrera. **P2:** Línea puntaje PAES promedio ponderado 2012–2026 con anotación quiebre PSU/PAES (2022). **P3:** Doble eje (vacantes RM + población 18–24 INE); KPI tasa absorción y cobertura bruta. |
| **10. Riesgos** | Matrícula por región de sede (no domicilio alumno) · Acreditación SIES: NULL 2012–2017 · Quiebre PSU→PAES (2022): usar `puntaje_promedio_equiv_paes` · Proxy INE 18–24: 14% de pob. 15–64 RM · Nulos vacantes (~25%): gobernados con `flag_vacantes_declaradas` |

---

## Mapa de Decisiones: KPI → Acción

| KPI | Umbral | Acción Concreta |
|---|---|---|
| `tasa_saturacion_lab_35_pct` | ≥100% rojo; ≥85% naranja | Abrir sección extra laboratorio; ajustar vacantes |
| `secciones_extra_por_sobrecupo` | ≥1 | Presupuestar docente y espacio para paralelo adicional |
| `tasa_ocupacion_primer_ano` | <75% ocioso; ≥100% sobrecupo | Revisar oferta vacantes ↑ o ↓ |
| `tasa_absorcion_juvenil_rm_pct` | Tendencia ↑ sostenida | Incrementar vacantes o mejorar retención cohortes sup. |
| `tasa_cobertura_bruta_rm_pct` | ≥80%: mercado saturado | Competir por cuota de mercado vs. demanda nueva |
| `posicionamiento_competitivo_rm` | Cuadrante 4 «Crítica» | Intervención regulatoria CNED / plan mejora institucional |
| `score_calidad_sies_pct` | <57% (<4 años) | Restricción nuevas vacantes hasta elevar estándar SIES |
| `puntaje_PAES_corte_ponderado` | Tendencia ↓ con ocupación ↑ | Activar nivelación académica 1er año |
| `tasa_heterogeneidad_paes_pct` | ≥30% | Evaluar asignaturas nivelación diferenciada |
| `cuota_mercado_matricula_rm_pct` | Declive >3 años | Revisar portafolio y estrategia admisión RM |
