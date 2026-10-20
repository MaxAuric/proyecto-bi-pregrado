# Arquitectura del Modelo Dimensional - Hito 2
## Rol: Persona 3 (Arquitecto de Bases de Datos)
**Proyecto:** Análisis de Demanda, Capacidad y Equidad Territorial en la Educación Superior Chilena (2012–2026)  
**Esquema:** Constelación de Hechos (Fact Constellation) con Dimensiones Conformadas

---

### 1. Diagrama Entidad-Relación Dimensional (Mermaid)

```mermaid
erDiagram
    dim_tiempo ||--o{ fact_matricula_oferta : "1 a N (id_tiempo)"
    dim_geografia ||--o{ fact_matricula_oferta : "1 a N (id_geografia)"
    dim_sede ||--o{ fact_matricula_oferta : "1 a N (id_sede)"
    dim_institucion ||--o{ fact_matricula_oferta : "1 a N (id_institucion)"
    dim_programa ||--o{ fact_matricula_oferta : "1 a N (id_programa)"
    
    dim_geografia ||--o{ dim_sede : "1 a N (id_geografia)"
    
    dim_tiempo ||--o{ dim_institucion_calidad_anual : "1 a N (id_tiempo)"
    dim_institucion ||--o{ dim_institucion_calidad_anual : "1 a N (id_institucion)"
    
    dim_geografia ||--o{ fact_poblacion_regional : "1 a N (id_geografia)"
    dim_tiempo ||--o{ fact_poblacion_regional : "1 a N (id_tiempo)"

    dim_tiempo {
        int id_tiempo PK
        int ano
        string periodo_quinquenal
        string tipo_prueba_admision
        int flag_gratuidad_vigente
        int flag_reforma_nuble
        int flag_pandemia
    }

    dim_geografia {
        int id_geografia PK
        string region_codigo_subdere UK
        string region_nombre_estandar
        string region_numero_romano
        string zona_geografica
        int orden_geografico
    }

    dim_sede {
        int id_sede PK
        string nombre_sede UK
        int id_geografia FK
        string region_codigo_subdere
        string region_nombre
    }

    dim_institucion {
        int id_institucion PK
        string nombre_institucion UK
        string nombre_normalizado
        int codigo_ies
        string nombre_sies
        string tipo_institucion
        string clasificacion2
        string metodo_cruce_sies
    }

    dim_institucion_calidad_anual {
        int id_institucion_calidad PK
        int id_institucion FK
        int id_tiempo FK
        int codigo_ies
        string acreditacion_cned
        string autonomia_cned
        string gratuidad_cned
        string acreditacion_sies
        float anos_acreditacion_sies
        string vigencia_sies
        string autonomia_sies
        string fuente_calidad
    }

    dim_programa {
        int id_programa PK
        string nombre_programa
        string carrera_generica
        string area_conocimiento
        string tipo_programa
        string tipo_carrera
        string horario
        int duracion_semestres
        string titulo
        string grado_academico
    }

    fact_matricula_oferta {
        int id_fact PK
        int id_tiempo FK
        int id_geografia FK
        int id_sede FK
        int id_institucion FK
        int id_programa FK
        int vacantes
        int matricula_primer_ano_total
        int matricula_primer_ano_hombres
        int matricula_primer_ano_mujeres
        int matricula_primer_ano_extranjeros
        int matricula_total
        int matricula_total_hombres
        int matricula_total_mujeres
        int matricula_total_extranjeros
        float puntaje_promedio_original
        float puntaje_promedio_norm_0_100
        float puntaje_promedio_equiv_paes
        float puntaje_promedio_zscore_anual
        float tasa_ocupacion_primer_ano
        float ratio_mujeres_primer_ano
        float ratio_extranjeros_total
        int flag_exige_prueba_admision
        int flag_vacantes_declaradas
        int flag_quiebre_nuble
    }

    fact_poblacion_regional {
        int id_poblacion PK
        int id_geografia FK
        int id_tiempo FK
        int poblacion_total
        int poblacion_hombres
        int poblacion_mujeres
        int poblacion_0_14
        int poblacion_15_64
        int poblacion_65_mas
    }
```

---

### 2. Jerarquías de Análisis para Power BI (Persona 4)

1. **Jerarquía Geográfica:**
   `Zona Geográfica` $\rightarrow$ `Región` (`region_nombre_estandar`) $\rightarrow$ `Sede` (`nombre_sede`).
2. **Jerarquía Institucional:**
   `Tipo de Institución` (Univ, IP, CFT) $\rightarrow$ `Clasificación2` (CRUCH, Privada) $\rightarrow$ `Institución` (`nombre_institucion`).
3. **Jerarquía Académica:**
   `Área de Conocimiento` $\rightarrow$ `Carrera Genérica` $\rightarrow$ `Nombre Programa` $\rightarrow$ `Horario`.
4. **Jerarquía Temporal:**
   `Período Quinquenal` $\rightarrow$ `Año Calendario`.
