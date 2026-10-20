# Informe Técnico Hito 1 - Normalización de Textos y Homologación de Llaves de Cruce
## Rol Evaluado: Persona 3 (Arquitecto de Bases de Datos)
**Proyecto:** Análisis de Demanda, Capacidad y Equidad Territorial en la Educación Superior Chilena (2012–2026)  
**Entrega:** Hito 1 (Propuesta, ETL y Fuentes) — 21 de Octubre de 2026  
**Equipo de Trabajo:** Personas 1, 2, 3, 4 y 5

---

## 1. Resumen Ejecutivo

En el marco del **Hito 1**, la pauta oficial del proyecto exige:
> *"Normalizar textos (institución, región, carrera) para permitir los cruces con fuentes externas."*  
> *(Pauta Trabajo Práctico Final BI, Requisito 2.e y División de Trabajo Persona 3).*

Dado que la base histórica del CNED (158.211 registros) **no incluye códigos numéricos institucionales ni geográficos canónicos**, el cruce con fuentes externas (INE y SIES/MINEDUC) depende exclusivamente de la calidad y rigor en la normalización de cadenas de texto.

La **Persona 3 (Arquitecto de Bases de Datos)** colaboró activamente en el diseño e implementación de las reglas heurísticas, tablas de mapeo y auditoría de calidad de datos para tres entidades fundamentales:
1. **Regiones:** Estandarización de 16 regiones oficiales según código SUBDERE (coincidencia del **100,00%** con proyecciones INE).
2. **Instituciones:** Homologación de 259 grafías institucionales hacia el catálogo oficial de códigos SIES (cobertura del **98,39%** de las filas y **99,00%** de la matrícula de primer año).
3. **Carreras y Programas:** Limpieza de 284 carreras genéricas, 3.209 nombres de programa y 11 áreas de conocimiento, garantizando consistencia tipográfica y ausencia de caracteres anómalos.

---

## 2. Metodología de Normalización de Texto

Para asegurar reproducibilidad y evitar falsos positivos o duplicaciones en las llaves primarias/foráneas, se aplicó un pipeline de limpieza algorítmica en cuatro fases:

```
[Texto Crudo CNED] 
       │
       ▼ (Fase 1: Limpieza básica y desapilado de espacios)
[Texto Uniforme ASCII] 
       │
       ▼ (Fase 2: Expansión léxica de abreviaciones y siglas)
[Nombre Normalizado Canónico]
       │
       ▼ (Fase 3: Cruce determinista y manual verificado)
[Código Oficial SIES / SUBDERE]
       │
       ▼ (Fase 4: Coincidencia difusa asistida difflib con umbral >= 0.92)
[Tabla Puente Certificada]
```

1. **Descomposición Unicode NFKD:** Eliminación sistemática de tildes, diéresis y caracteres especiales, preservando la letra base (ej. `ÑUBLE` $\rightarrow$ `NUBLE` para comparación binaria, conservando el texto formal con tilde para la capa de presentación).
2. **Trim y Desduplicación de Espacios:** Eliminación de espacios iniciales, finales y dobles espacios intermedios (`"  "` $\rightarrow$ `" "`).
3. **Conversión a Mayúsculas:** Estandarización universal a caja alta (`UPPERCASE`) para anular discrepancias por capitalización entre los diferentes años de la serie (2012–2026).
4. **Expansión Léxica de Prefijos Institucionales:** Reemplazo determinista de siglas ambiguas:
   - `U.` / `UNIV.` $\rightarrow$ `UNIVERSIDAD`
   - `I.P.` / `IP` $\rightarrow$ `INSTITUTO PROFESIONAL`
   - `C.F.T.` / `CFT` $\rightarrow$ `CENTRO DE FORMACION TECNICA`

---

## 3. Normalización Geográfica (Cruce con INE)

### 3.1. Esquema de Codificación SUBDERE
Para vincular los datos de matrícula con las proyecciones de población del INE (base Censo 2017), se descartó el cruce directo por texto plano debido a las variaciones históricas en los nombres de las regiones (ej. `"Región del Bío-Bío"`, `"Región del Biobío"`, `"Región del Libertador Gral. Bernardo O'Higgins"` vs `"O'Higgins"`).

Se implementó una llave determinista basada en el **Código Oficial SUBDERE de 2 dígitos**:

| Cód. SUBDERE | Nombre Canónico Base CNED | Hoja Libro INE | Coincidencia |
| :---: | :--- | :--- | :---: |
| `15` | Región de Arica y Parinacota | Arica y Parinacota | 100% |
| `01` | Región de Tarapacá | Tarapacá | 100% |
| `02` | Región de Antofagasta | Antofagasta | 100% |
| `03` | Región de Atacama | Atacama | 100% |
| `04` | Región de Coquimbo | Coquimbo | 100% |
| `05` | Región de Valparaíso | Valparaíso | 100% |
| `13` | Región Metropolitana de Santiago | Metropolitana | 100% |
| `06` | Región del Libertador Gral. Bernardo O'Higgins | O'Higgins | 100% |
| `07` | Región del Maule | Maule | 100% |
| `16` | Región de Ñuble | Ñuble | 100% |
| `08` | Región del Biobío | Biobío | 100% |
| `09` | Región de La Araucanía | La Araucanía | 100% |
| `14` | Región de Los Ríos | Los Ríos | 100% |
| `10` | Región de Los Lagos | Los Lagos | 100% |
| `11` | Región de Aysén del Gral. Carlos Ibáñez del Campo | Aysén | 100% |
| `12` | Región de Magallanes y de la Antártica Chilena | Magallanes | 100% |

### 3.2. Gobernanza del Quiebre Administrativo de Ñuble (Ley 21.033)
La Región de Ñuble inició su vigencia legal en septiembre de 2018 (anteriormente provincia de la Región del Biobío).
- La serie del INE publica proyecciones retrospectivas separadas para Ñuble desde 2002.
- La base consolidada del CNED reporta registros para Ñuble a lo largo de toda la serie.
- **Solución implementada:** Se mantuvo el código `'16'` para todos los registros geográficamente pertenecientes al territorio de Ñuble y se creó el flag booleano `flag_quiebre_nuble = 1` para los **1.599 registros previos a 2018**, advirtiendo que en ese período la región no existía como unidad político-administrativa independiente.
- **Resultado:** **158.211 de 158.211 registros cruzados exitosamente (100,00%)**.

---

## 4. Normalización Institucional (Cruce con SIES)

### 4.1. El Desafío de Homologación Institucional
La base consolidada contiene **259 grafías institucionales distintas**. Una misma casa de estudios puede aparecer con nombres distintos según el corte anual (ej. `I.P. INACAP` entre 2012 y 2022, e `IP INACAP` a partir de 2023; cambios de razón social o fusión de sedes).

### 4.2. Niveles de Emparejamiento y Auditoría
Se estructuró la tabla `puente_institucion.csv` clasificando cada coincidencia según su nivel de certidumbre:

| Método de Cruce | Grafías | % Grafías | Descripción y Regla de Negocio |
| :--- | :---: | :---: | :--- |
| `exacto_normalizado` | **168** | 64,86% | Coincidencia exacta tras remoción de puntuación y expansión de siglas. |
| `manual` | **47** | 18,15% | Asignación directa tras revisión documental (ej. Centros Estatales `CFTE`, escuelas de FFAA). |
| `aproximado_>=0.92` | **25** | 9,65% | Coincidencia difusa por distancia de Levenshtein con umbral $\ge 0,92$, validada caso a caso. |
| `sin_coincidencia` | **19** | 7,34% | Registros sin correspondencia en los listados vigentes de SIES (2018–2026). |
| **Total** | **259** | **100,00%** | **240 instituciones con código oficial asignado (92,66%).** |

#### Control de Calidad: Falsos Positivos Rechazados
En la etapa de coincidencia difusa, el algoritmo identificó similitudes léxicas elevadas que correspondían a instituciones jurídicamente distintas. La Persona 3 auditó y **rechazó explícitamente 7 emparejamientos erróneos**:
- `CFT CEPONAL` $\neq$ `CFT ICEL`
- `CFT LOS LEONES` $\neq$ `CFT LOS LAGOS`
- `CFT CROWNLIET` $\neq$ `CFT CRECIC`
- Evitando contaminar la asignación de acreditación institucional.

### 4.3. Tratamiento de los Registros Sin Coincidencia (19 Casos)
El análisis forense de los 19 casos no coincidentes arrojó:
- **15 instituciones son históricas extintas:** Desaparecieron de la base CNED antes de 2018 (año del primer corte oficial del SIES disponible). Su ausencia no obedece a un error de texto, sino a un **desfase temporal estructural** (*CFT Simón Bolívar, CFT La Araucana, U. La Araucana, etc.*).
- **4 instituciones con actividad post-2018:** *CFT ICCE* (2 variantes) e *IP IPEGE* (2 variantes). Se mantuvieron con `codigo_ies = NULL` y clasificados como `'Sin Información'` para que sus matrículas no se descarten.
- **Impacto en el Sistema:**
  - Registros de la base cubiertos por SIES: **98,39%** (155.663 / 158.211).
  - Matrícula de primer año cubierta: **99,00%** (5.134.251 / 5.186.123 alumnos).
  - Pérdida de registros: **0,00%** (todos se preservan para el DataMart del Hito 2).

---

## 5. Normalización de Carreras y Programas

En preparación para el modelo dimensional y posibles cruces con mifuturo.cl:
1. **Carrera Genérica:** Se auditaron las **284 carreras genéricas únicas**. Se verificó que ninguna presente espacios duplicados, saltos de línea ni caracteres corruptos de codificación (UTF-8 validado).
2. **Programas Únicos:** Se tipificaron **3.209 nombres de programa** y **11 áreas de conocimiento** oficiales del CNED.
3. **Régimen Horario:** Se consolidó en 3 categorías unívocas: `Diurno`, `Vespertino` y `Otro`.

---

## 6. Conclusiones y Conexión con el Hito 2

1. **Cumplimiento de la Pauta:** La normalización de textos requerida para el Hito 1 fue completada y certificada mediante el script `scripts/audit_normalization_p3.py`.
2. **Tablas Puente Entregadas:**
   - `puente_region.csv` (16 filas, 100% coincidencia).
   - `puente_institucion.csv` (259 filas, 98,39% de registros con código canónico).
3. **Habilitación Inmediata del DataMart:** La limpieza y estructuración de estas tablas de texto constituyó el cimiento directo para construir el DataMart en el **Hito 2**, garantizando integridad referencial absoluta (0 huérfanos) entre las tablas de hechos y dimensiones.
