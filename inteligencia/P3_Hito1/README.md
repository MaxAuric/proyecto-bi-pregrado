# Entregables Hito 1 - Persona 3: Arquitecto de Bases de Datos
## Tarea Asignada: Normalizacion de Campos de Texto para Cruce de Fuentes Externas

Este directorio contiene el aporte especifico y formal de la **Persona 3** para el **Hito 1** del Proyecto de Business Intelligence (Entrega: 21 de Octubre de 2026).

---

## 1. Estructura del Directorio `P3_Hito1/`

```text
P3_Hito1/
├── README.md                               # Este archivo de descripcion
├── informe_hito1_persona3_normalizacion.md # Informe tecnico formal de normalizacion
├── auditoria_normalizacion_textos.json      # Metricas numericas certificadas de cobertura
└── scripts/
    └── audit_normalization_p3.py          # Script de auditoria reproducible en Python
```

---

## 2. Como Reproducir la Auditoria

Para verificar las tasas de cobertura y la calidad de las tablas de texto:

```bash
python P3_Hito1/scripts/audit_normalization_p3.py
```

---

## 3. Metricas Clave Certificadas

1. **Regiones (Cruce INE):**
   - 16 regiones oficiales mapeadas a codigos SUBDERE.
   - **100% de coincidencia** sobre los 158.211 registros consolidados.
   - 1.599 registros historicos de Nuble (pre-2018) gobernados con flag.
2. **Instituciones (Cruce SIES):**
   - 259 grafias unificadas hacia codigos SIES mediante tabla puente.
   - **98,39% de los registros** y **99,00% de la matricula de primer ano** cubiertos con codigo oficial.
   - 19 registros sin codigo explicados: 15 extintos pre-2018 (ausencia estructural) y 4 vigentes preservados como miembros desconocidos sin perdida de datos.
3. **Carreras y Programas:**
   - 284 carreras genericas limpias sin espacios redundantes.
   - 3.209 nombres de programas estandarizados en 11 areas de conocimiento.
