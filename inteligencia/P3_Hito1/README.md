# Entregables Hito 1 - Persona 3: Arquitecto de Bases de Datos
## Tarea Asignada: Normalización de Campos de Texto para Cruce de Fuentes Externas

Este directorio contiene el aporte específico y formal de la **Persona 3** para el **Hito 1** del Proyecto de Business Intelligence (Entrega: 21 de Octubre de 2026).

---

## 📁 Estructura del Directorio `P3_Hito1/`

```text
P3_Hito1/
├── README.md                               # Este archivo de descripción
├── informe_hito1_persona3_normalizacion.md # Informe técnico formal de normalización
├── auditoria_normalizacion_textos.json      # Métricas numéricas certificadas de cobertura
└── scripts/
    └── audit_normalization_p3.py          # Script de auditoría reproducible en Python
```

---

## 🚀 Cómo Reproducir la Auditoría

Para verificar las tasas de cobertura y la calidad de las tablas de texto:

```bash
python P3_Hito1/scripts/audit_normalization_p3.py
```

---

## 📊 Métricas Clave Certificadas

1. **Regiones (Cruce INE):**
   - 16 regiones oficiales mapeadas a códigos SUBDERE.
   - **100% de coincidencia** sobre los 158.211 registros consolidados.
   - 1.599 registros históricos de Ñuble (pre-2018) gobernados con flag.
2. **Instituciones (Cruce SIES):**
   - 259 grafías unificadas hacia códigos SIES mediante tabla puente.
   - **98,39% de los registros** y **99,00% de la matrícula de primer año** cubiertos con código oficial.
   - 19 registros sin código explicados: 15 extintos pre-2018 (ausencia estructural) y 4 vigentes preservados como miembros desconocidos sin pérdida de datos.
3. **Carreras y Programas:**
   - 284 carreras genéricas limpias sin espacios redundantes.
   - 3.209 nombres de programas estandarizados en 11 áreas de conocimiento.
