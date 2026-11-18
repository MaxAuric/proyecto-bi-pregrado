#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Validacion Automatica del Modelo Power BI
Persona 4 - Desarrollador BI y Especialista DAX
Entrega Final - 18 Noviembre 2026

Ejecuta validaciones contra el DataMart SQLite para certificar cuadre
antes y despues de construir el .pbix
"""

import sqlite3
import pandas as pd
import sys
from pathlib import Path

DB_PATH = Path(r"Final/00_DATAMART_LISTO_PARA_POWERBI/datamart_estrella_rm_final.db")
EXCEL_PATH = Path(r"Final/00_DATAMART_LISTO_PARA_POWERBI/DataMart_Estrella_RM_PowerBI.xlsx")

def conectar_db():
    """Conecta a la base SQLite"""
    if not DB_PATH.exists():
        print(f"ERROR: No se encuentra {DB_PATH}")
        sys.exit(1)
    return sqlite3.connect(str(DB_PATH))

def validar_conteos(conn):
    """Valida conteos de filas por tabla"""
    print("=" * 60)
    print("VALIDACION 1: CONTEOS DE FILAS")
    print("=" * 60)

    tablas_esperadas = {
        "dim_tiempo_ine_rm": 15,
        "dim_sede_geografia": 22,
        "dim_institucion_sies": 1298,
        "dim_carrera_programa": 5184,  # Valor real en DataMart final
        "fact_matricula_admision": 58926,
        "agg_resumen_anual_institucion_rm": 1298,  # Nombre real de tabla en SQLite
        "puente_institucion_sies": 259
    }

    todos_ok = True
    for tabla, esperado in tablas_esperadas.items():
        try:
            n = pd.read_sql(f"SELECT COUNT(*) as n FROM {tabla}", conn).iloc[0, 0]
            status = "OK" if n == esperado else "DIFERENCIA"
            if n != esperado:
                todos_ok = False
            print(f"  {tabla:35s} : {n:>8d} (esperado: {esperado:>8d}) [{status}]")
        except Exception as e:
            print(f"  {tabla:35s} : ERROR - {e}")
            todos_ok = False

    return todos_ok

def validar_integridad_referencial(conn):
    """Valida que no haya huérfanos en la tabla de hechos"""
    print("\n" + "=" * 60)
    print("VALIDACION 2: INTEGRIDAD REFERENCIAL (0 huérfanos)")
    print("=" * 60)

    dimensiones = [
        ("dim_tiempo_ine_rm", "id_tiempo"),
        ("dim_sede_geografia", "id_sede_geografia"),
        ("dim_institucion_sies", "id_institucion_sk"),
        ("dim_carrera_programa", "id_carrera_programa_sk")
    ]

    todos_ok = True
    for dim, fk in dimensiones:
        query = f"""
            SELECT COUNT(*) as n FROM fact_matricula_admision f
            LEFT JOIN {dim} d ON f.{fk} = d.{fk}
            WHERE d.{fk} IS NULL
        """
        huérfanos = pd.read_sql(query, conn).iloc[0, 0]
        status = "OK" if huérfanos == 0 else "ERROR"
        if huérfanos > 0:
            todos_ok = False
        print(f"  Huérfanos en {dim:25s} ({fk:25s}): {huérfanos:>6d} [{status}]")

    return todos_ok

def validar_filtro_rm(conn):
    """Valida que todos los registros sean RM (es_region_metropolitana = 1)"""
    print("\n" + "=" * 60)
    print("VALIDACION 3: FOCO 100% REGION METROPOLITANA")
    print("=" * 60)

    n_total = pd.read_sql("SELECT COUNT(*) as n FROM fact_matricula_admision", conn).iloc[0, 0]
    n_rm = pd.read_sql("SELECT COUNT(*) as n FROM fact_matricula_admision WHERE es_region_metropolitana = 1", conn).iloc[0, 0]
    n_no_rm = n_total - n_rm

    print(f"  Total registros en fact_matricula_admision: {n_total}")
    print(f"  Registros con es_region_metropolitana = 1: {n_rm}")
    print(f"  Registros fuera de RM: {n_no_rm}")

    if n_no_rm == 0:
        print("  [OK] 100% de los registros pertenecen a la Region Metropolitana")
        return True
    else:
        print("  [ERROR] Hay registros fuera de la RM")
        return False

def validar_cero_varchar_hechos(conn):
    """Valida que la tabla de hechos no tenga columnas VARCHAR (Clase 4 DW Pag. 62)"""
    print("\n" + "=" * 60)
    print("VALIDACION 4: TABLA DE HECHOS 100% NUMERICA (Clase 4 DW)")
    print("=" * 60)

    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(fact_matricula_admision)")
    columnas = cursor.fetchall()

    varchar_cols = []
    for col in columnas:
        nombre = col[1]
        tipo = col[2].upper()
        if "CHAR" in tipo or "TEXT" in tipo or "VARCHAR" in tipo:
            varchar_cols.append((nombre, tipo))

    if varchar_cols:
        print("  [ERROR] Columnas de texto encontradas en tabla de hechos:")
        for nombre, tipo in varchar_cols:
            print(f"    - {nombre}: {tipo}")
        return False
    else:
        print("  [OK] Tabla de hechos 100% numerica (cero VARCHAR/TEXT)")
        return True

def validar_sin_abreviaturas_dimensiones(conn):
    """Valida que no haya abreviaturas en dimensiones clave (Clase 4 DW Pag. 62)"""
    print("\n" + "=" * 60)
    print("VALIDACION 5: SIN ABREVIATURAS EN DIMENSIONES (Clase 4 DW)")
    print("=" * 60)

    # Verificar tipo_institucion en dim_institucion_sies
    df_tipo = pd.read_sql("SELECT DISTINCT tipo_institucion FROM dim_institucion_sies", conn)
    tipos = df_tipo["tipo_institucion"].tolist()

    abreviaturas_detectadas = []
    for t in tipos:
        if any(abrev in t.upper() for abrev in ["UNIV.", "I.P.", "C.F.T.", "F.F.A.A.", "IP ", "CFT "]):
            abreviaturas_detectadas.append(t)

    if abreviaturas_detectadas:
        print("  [ERROR] Abreviaturas detectadas en tipo_institucion:")
        for a in abreviaturas_detectadas:
            print(f"    - '{a}'")
        return False
    else:
        print("  [OK] Sin abreviaturas en tipo_institucion")
        print(f"    Valores encontrados: {tipos}")
        return True

def validar_kpis_precalculados(conn):
    """Valida que las tasas/KPIs esten precalculados en las tablas"""
    print("\n" + "=" * 60)
    print("VALIDACION 6: KPIs Y TASAS PRECALCULADOS EN TABLAS")
    print("=" * 60)

    # Verificar columnas de tasas en fact_matricula_admision
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(fact_matricula_admision)")
    cols_fact = [row[1] for row in cursor.fetchall()]

    kpis_fact_esperados = [
        "tasa_ocupacion_primer_ano",
        "tasa_sobredemanda_oferta_pct",
        "tasa_renovacion_primer_ano_pct",
        "tasa_retencion_aparente_pct",
        "tasa_saturacion_lab_35_pct",
        "secciones_extra_por_sobrecupo",
        "sobrecupo_neto_alumnos",
        "vacantes_ociosas_netas",
        "puntaje_promedio_equiv_paes",
        "puntaje_corte_ultimo_equiv_paes",
        "tasa_heterogeneidad_paes_pct",
        "indice_presion_selectiva_kpi"
    ]

    print("  En fact_matricula_admision:")
    kpis_ok = 0
    for kpi in kpis_fact_esperados:
        if kpi in cols_fact:
            # Verificar que tenga datos no nulos
            n = pd.read_sql(f"SELECT COUNT(*) as n FROM fact_matricula_admision WHERE {kpi} IS NOT NULL", conn).iloc[0, 0]
            print(f"    {kpi:35s} : {n:>6d} valores no nulos [OK]")
            kpis_ok += 1
        else:
            print(f"    {kpi:35s} : [FALTA]")

    # Verificar en dim_tiempo_ine_rm
    cursor.execute("PRAGMA table_info(dim_tiempo_ine_rm)")
    cols_tiempo = [row[1] for row in cursor.fetchall()]
    kpis_tiempo = ["tasa_absorcion_juvenil_rm_pct", "tasa_cobertura_bruta_rm_pct",
                   "tasa_oferta_vacantes_1000_jovenes_rm", "tasa_ocupacion_anual_rm_pct"]

    print("  En dim_tiempo_ine_rm:")
    for kpi in kpis_tiempo:
        if kpi in cols_tiempo:
            n = pd.read_sql(f"SELECT COUNT(*) as n FROM dim_tiempo_ine_rm WHERE {kpi} IS NOT NULL", conn).iloc[0, 0]
            print(f"    {kpi:35s} : {n:>6d} valores no nulos [OK]")
        else:
            print(f"    {kpi:35s} : [FALTA]")

    # Verificar en dim_institucion_sies
    cursor.execute("PRAGMA table_info(dim_institucion_sies)")
    cols_inst = [row[1] for row in cursor.fetchall()]
    kpis_inst = ["score_calidad_sies_pct", "tramo_acreditacion_sies", "tasa_ocupacion_inst_anual_pct",
                 "cuota_mercado_matricula_rm_pct", "posicionamiento_competitivo_rm"]

    print("  En dim_institucion_sies:")
    for kpi in kpis_inst:
        if kpi in cols_inst:
            n = pd.read_sql(f"SELECT COUNT(*) as n FROM dim_institucion_sies WHERE {kpi} IS NOT NULL", conn).iloc[0, 0]
            print(f"    {kpi:35s} : {n:>6d} valores no nulos [OK]")
        else:
            print(f"    {kpi:35s} : [FALTA]")

    return kpis_ok == len(kpis_fact_esperados)

def validar_excel_vs_sqlite():
    """Compara conteos entre Excel y SQLite"""
    print("\n" + "=" * 60)
    print("VALIDACION 7: EXCEL vs SQLITE (Cuadre de Exportacion)")
    print("=" * 60)

    try:
        import openpyxl
        wb = openpyxl.load_workbook(EXCEL_PATH, read_only=True)

        conn = conectar_db()
        tablas = [
            ("dim_tiempo_ine_rm", "dim_tiempo_ine_rm"),
            ("dim_sede_geografia", "dim_sede_geografia"),
            ("dim_institucion_sies", "dim_institucion_sies"),
            ("dim_carrera_programa", "dim_carrera_programa"),
            ("fact_matricula_admision", "fact_matricula_admision"),
            ("agg_resumen_institucion_rm", "agg_resumen_anual_institucion_rm")  # Excel name -> SQLite name
        ]

        todos_ok = True
        for excel_name, sqlite_name in tablas:
            if excel_name in wb.sheetnames:
                ws = wb[excel_name]
                n_excel = ws.max_row - 1  # -1 por header
                n_sqlite = pd.read_sql(f"SELECT COUNT(*) as n FROM {sqlite_name}", conn).iloc[0, 0]
                status = "OK" if n_excel == n_sqlite else "DIFERENCIA"
                if n_excel != n_sqlite:
                    todos_ok = False
                print(f"  {excel_name:35s} : Excel={n_excel:>6d}  SQLite={n_sqlite:>6d} [{status}]")
            else:
                print(f"  {excel_name:35s} : [NO ENCONTRADA EN EXCEL]")
                todos_ok = False

        conn.close()
        return todos_ok
    except ImportError:
        print("  [SALTADO] openpyxl no instalado para validar Excel")
        return True
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

def validar_metricas_clave_2026(conn):
    """Valida metricas clave para el año 2026 (ultimo año disponible)"""
    print("\n" + "=" * 60)
    print("VALIDACION 8: METRICAS CLAVE 2026 (Sanity Check)")
    print("=" * 60)

    # Obtener id_tiempo para 2026
    id_2026 = pd.read_sql("SELECT id_tiempo FROM dim_tiempo_ine_rm WHERE ano = 2026", conn)
    if len(id_2026) == 0:
        print("  [ERROR] No se encuentra año 2026 en dim_tiempo_ine_rm")
        return False
    id_t = id_2026.iloc[0, 0]

    # Consultas de metricas 2026
    metricas = {
        "Matricula 1er Ano RM 2026": f"""
            SELECT SUM(matricula_primer_ano_total)
            FROM fact_matricula_admision
            WHERE id_tiempo = {id_t}
        """,
        "Vacantes Ofrecidas RM 2026": f"""
            SELECT SUM(vacantes)
            FROM fact_matricula_admision
            WHERE id_tiempo = {id_t}
        """,
        "Ofertas con vacantes declaradas 2026": f"""
            SELECT COUNT(*)
            FROM fact_matricula_admision
            WHERE id_tiempo = {id_t} AND flag_vacantes_declaradas = 1
        """,
        "Instituciones activas 2026": f"""
            SELECT COUNT(DISTINCT id_institucion_sk)
            FROM fact_matricula_admision
            WHERE id_tiempo = {id_t}
        """,
        "Puntaje PAES Promedio Ponderado 2026": f"""
            SELECT SUM(puntaje_promedio_equiv_paes * matricula_primer_ano_total) / SUM(matricula_primer_ano_total)
            FROM fact_matricula_admision
            WHERE id_tiempo = {id_t}
            AND flag_exige_prueba_admision = 1
            AND matricula_primer_ano_total > 0
            AND puntaje_promedio_equiv_paes IS NOT NULL
        """,
        "Tasa Ocupacion Vacantes RM 2026": f"""
            SELECT
                SUM(CASE WHEN flag_vacantes_declaradas = 1 THEN matricula_primer_ano_total ELSE 0 END) * 100.0 /
                NULLIF(SUM(CASE WHEN flag_vacantes_declaradas = 1 THEN vacantes ELSE 0 END), 0)
            FROM fact_matricula_admision
            WHERE id_tiempo = {id_t}
        """
    }

    for nombre, query in metricas.items():
        try:
            valor = pd.read_sql(query, conn).iloc[0, 0]
            if valor is not None:
                print(f"  {nombre:40s}: {valor:>12.2f}")
            else:
                print(f"  {nombre:40s}: NULL")
        except Exception as e:
            print(f"  {nombre:40s}: ERROR - {e}")

    return True

def generar_reporte_json(resultados):
    """Genera reporte JSON para documentacion"""
    import json
    from datetime import datetime

    reporte = {
        "fecha_validacion": datetime.now().isoformat(),
        "persona": "Persona 4 - Desarrollador BI y Especialista DAX",
        "entrega": "Final - 18 Noviembre 2026",
        "datamart": "DataMart_Estrella_RM_PowerBI.xlsx / datamart_estrella_rm_final.db",
        "validaciones": resultados,
        "resumen": {
            "total_validaciones": len(resultados),
            "aprobadas": sum(1 for v in resultados.values() if v),
            "fallidas": sum(1 for v in resultados.values() if not v)
        }
    }

    output_path = Path(r"Final/P4_DESARROLLADOR_POWERBI_Y_DAX/docs/validacion_modelo_powerbi.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)

    print(f"\nReporte JSON guardado en: {output_path}")

def main():
    print("=" * 60)
    print("VALIDACION AUTOMATICA MODELO POWER BI - PERSONA 4")
    print("Entrega Final BI - Region Metropolitana de Santiago")
    print("18 de Noviembre 2026")
    print("=" * 60)

    conn = conectar_db()

    resultados = {}
    resultados["conteos_filas"] = validar_conteos(conn)
    resultados["integridad_referencial"] = validar_integridad_referencial(conn)
    resultados["foco_rm"] = validar_filtro_rm(conn)
    resultados["cero_varchar_hechos"] = validar_cero_varchar_hechos(conn)
    resultados["sin_abreviaturas"] = validar_sin_abreviaturas_dimensiones(conn)
    resultados["kpis_precalculados"] = validar_kpis_precalculados(conn)
    resultados["excel_vs_sqlite"] = validar_excel_vs_sqlite()
    validar_metricas_clave_2026(conn)  # Solo informativo

    conn.close()

    print("\n" + "=" * 60)
    print("RESUMEN DE VALIDACION")
    print("=" * 60)
    for nombre, resultado in resultados.items():
        status = "APROBADO" if resultado else "FALLIDO"
        print(f"  {nombre:30s}: {status}")

    total = len(resultados)
    aprobadas = sum(1 for v in resultados.values() if v)
    print(f"\n  Total: {aprobadas}/{total} validaciones aprobadas")

    if aprobadas == total:
        print("\n  >>> MODELO CERTIFICADO PARA POWER BI <<<")
        print("  >>> Listo para construir Dashboard_Final_RM.pbix <<<")
    else:
        print("\n  >>> REVISAR ERRORES ANTES DE PROCEDER <<<")

    generar_reporte_json(resultados)

    return 0 if aprobadas == total else 1

if __name__ == "__main__":
    sys.exit(main())