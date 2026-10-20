"""
Script Maestro de Generación de Diccionarios y Gobernanza de Datos (Hito 1) - Versión Python
Autor: Persona 5 (Gestor del Proyecto y Documentador)
Proyecto: Business Intelligence - Análisis Estratégico Educación Superior
"""

import os
import json
import subprocess

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
JS_SCRIPT = os.path.join(SCRIPTS_DIR, "10_generate_master_dictionary_p5.js")

def main():
    print("=== EJECUTANDO GENERADOR MAESTRO DE DICCIONARIO P5 ===")
    res = subprocess.run(["node", JS_SCRIPT], capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print("ERROR:", res.stderr)
        raise SystemExit(res.returncode)
    print("=== DICCIONARIO MAESTRO GENERADO EXITOSAMENTE ===")

if __name__ == "__main__":
    main()
