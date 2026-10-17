import os
import sys
import time

def main():
    print("==========================================================================")
    print("=== EJECUCION INTEGRAL PIPELINE ETL - PERSONA 1 (INGENIERO DE DATOS) ===")
    print("=== HITO 1: EXTRACCION, LIMPIEZA, HOMOLOGACION Y DICCIONARIO (2012-2026) ===")
    print("==========================================================================\n")
    
    start_total = time.time()
    
    # 1. Descarga
    print(">>> FASE 1: DESCARGA Y VERIFICACION DE FUENTES OFICIALES (CNED)...")
    import importlib.util
    dir_path = os.path.dirname(os.path.abspath(__file__))
    
    # Ejecutar script 1
    os.system(f'python "{os.path.join(dir_path, "01_download_data.py")}"')
    
    # Ejecutar script 2
    print("\n>>> FASE 2: AUDITORIA, PERFILAMIENTO Y ANALISIS DE QUIEBRES...")
    os.system(f'python "{os.path.join(dir_path, "02_audit_and_mapping.py")}"')
    
    # Ejecutar script 3
    print("\n>>> FASE 3: CONSOLIDACION, TRANSFORMACION, NORMALIZACION Y EXPORTACION...")
    os.system(f'python "{os.path.join(dir_path, "03_clean_and_transform.py")}"')
    
    # Ejecutar script 4
    print("\n>>> FASE 4: GENERACION DE DICCIONARIOS Y DOCUMENTACION TECNICA...")
    os.system(f'python "{os.path.join(dir_path, "04_generate_dictionary.py")}"')
    
    elapsed = time.time() - start_total
    print("\n==========================================================================")
    print(f"=== PIPELINE ETL FINALIZADO EXITOSAMENTE EN {elapsed:.2f} SEGUNDOS ===")
    print("==========================================================================")

if __name__ == "__main__":
    main()
