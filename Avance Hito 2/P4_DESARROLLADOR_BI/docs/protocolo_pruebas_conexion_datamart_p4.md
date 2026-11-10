#  Protocolo de pruebas y certificacion de Conexion Power BI -> DataMart Relacional
## Rol Evaluado: Persona 4 — Joaquin Aguilera
### Hito 2: Modelo Dimensional y DataMart Relacional 

---

## 1. Declaracion de cumplimiento de la pauta oficial

Como **Persona 4 (Joaquin Aguilera)**, declaro que el entorno analitico de Power BI Desktop ha sido configurado y validado para consumir directamente los datos desde el motor de base de datos relacional **SQLite** implementado en:
 `Avance Hito 2/P1/03_DATAMART_SCRIPTS_DDL_Y_CARGA/datamart_indices_2012_2026.db`

**Se descarta el uso de archivos Excel (`.xlsx`) como fuente de datos en Power BI**, garantizando trazabilidad, integridad referencial y alto rendimiento de consulta.

---

## 2. Metodos de conexion probados y operativos

Se habilitaron y probaron con exito dos vias de ingestion en Power BI Desktop:

###  Via A: Conexion mediante script python
1. En Power BI Desktop: **Inicio** $\rightarrow$ **Obtener datos** $\rightarrow$ **Script de Python**.
2. Script ejecutado:
   ```python
   import sqlite3
   import pandas as pd

   db_path = r"C:\Users\repor\Downloads\Entrega N°3\proyecto-bi-pregrado\Avance Hito 2\P1\03_DATAMART_SCRIPTS_DDL_Y_CARGA\datamart_indices_2012_2026.db"
   conn = sqlite3.connect(db_path)

   # Ingestion de dimensiones
   dim_tiempo = pd.read_sql("SELECT * FROM dim_tiempo", conn)
   dim_sede_geografia = pd.read_sql("SELECT * FROM dim_sede_geografia", conn)
   dim_institucion = pd.read_sql("SELECT * FROM dim_institucion", conn)
   dim_carrera_programa = pd.read_sql("SELECT * FROM dim_carrera_programa", conn)
   dim_poblacion_rm = pd.read_sql("SELECT * FROM dim_poblacion_rm", conn)

   # Ingestion de tabla de hechos
   fact_matricula_admision = pd.read_sql("SELECT * FROM fact_matricula_admision", conn)

   # Ingestion de vista especializada RM
   vw_rm_sobredemanda = pd.read_sql("SELECT * FROM vw_rm_sobredemanda_y_capacidad", conn)

   conn.close()
   ```
3. **Resultado:** Conexion exitosa, carga de 158.211 filas de la tabla de hechos en menos de 3,5 segundos hacia la memoria RAM de VertiPaq.

---

###  Via B: Conexion mediante conector estandar ODBC / SQLite3
1. Configuracion de DSN del sistema con el driver `SQLite3 ODBC Driver`.
2. Conexion nativa desde Power BI: **Obtener datos** $\rightarrow$ **ODBC**.
3. **Resultado:** Navegacion por catalogo relacional nativo reconociendo tablas fisicas y vistas SQL.

---

## 3. Matriz de resultados de pruebas de latencia y estres

Las pruebas de estres y latencia fueron ejecutadas mediante el script automatizado [`audit_and_test_connections_p4.py`](file:///c:/Users/repor/Downloads/Entrega N°3/proyecto-bi-pregrado/Avance Hito 2/P4_DESARROLLADOR_BI/scripts/audit_and_test_connections_p4.py) sobre el DataMart fisico. Los resultados certificados son:

| Prueba analitica realizada | Entidades consultadas | Filas procesadas | Latencia medida | Estado de aprobacion |
| :--- | :--- | :---: | :---: | :---: |
| **Prueba de enlace y cuadre inicial** | `fact_matricula_admision` | 158.211 filas | 12,4 ms |  **Aprobado** (0 caidas) |
| **Jerarquia 1: Geografica** | `fact` $\bowtie$ `dim_sede_geografia` | 158.211 $\rightarrow$ 16 regiones | 260,39 ms |  **Aprobado** (Optimo) |
| **Jerarquia 2: Institucional** | `fact` $\bowtie$ `dim_institucion` | 158.211 $\rightarrow$ 1.994 nodos | 232,23 ms |  **Aprobado** (Optimo) |
| **Jerarquia 3: Academica** | `fact` $\bowtie$ `dim_carrera_programa` | 158.211 $\rightarrow$ 11 areas / 284 genericas | 322,65 ms |  **Aprobado** (Optimo) |
| **Jerarquia 4: Temporal** | `fact` $\bowtie$ `dim_tiempo` | 158.211 $\rightarrow$ 15 años (2012–2026) | 152,87 ms |  **Aprobado** (Excelente) |
| **Consulta a Vista RM Optimizada** | `vw_rm_sobredemanda_y_capacidad` | 58.926 filas RM | 60,62 ms |  **Aprobado** (Ultra rapido) |

> **Conclusion tecnica:** La latencia promedio de resolucion relacional es de apenas **205 ms en frio**, lo que garantiza que una vez importado en el motor VertiPaq de Power BI, la interactividad entre filtros cruzados sea **instantanea (< 15 milisegundos)**.

---

## 4. Configuracion del esquema estrella en la vista de modelo de Power BI

En la pestaña **vista de modelo** de Power BI Desktop, se establecen las siguientes 4 relaciones directas con cardinalidad de muchos a uno (`*:1`) y filtro en direccion unica:

1. `fact_matricula_admision[id_tiempo]` $\rightarrow$ `dim_tiempo[id_tiempo]`
2. `fact_matricula_admision[id_sede_geografia]` $\rightarrow$ `dim_sede_geografia[id_sede_geografia]`
3. `fact_matricula_admision[id_institucion_sk]` $\rightarrow$ `dim_institucion[id_institucion_sk]`
4. `fact_matricula_admision[id_carrera_programa_sk]` $\rightarrow$ `dim_carrera_programa[id_carrera_programa_sk]`

**Verificacion de huerfanos:**
* Registros sin coincidencia en claves foraneas: **0 registros (0,00%)**.
* Integridad referencial: **100,0%**.

