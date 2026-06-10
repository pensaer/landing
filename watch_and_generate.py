"""
Agente inteligente que monitorea cambios en gen_landings.py
y ejecuta automáticamente el pipeline de generación.

Ejecutar con: python watch_and_generate.py
"""

import os
import sys
import subprocess
import time
import hashlib
from datetime import datetime
from pathlib import Path

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

BASE = r"C:\Users\marcelo\Documents\Landings"
os.chdir(BASE)

# Archivo a monitorear
WATCH_FILE = "gen_landings.py"
UNITS_DIR = Path(BASE)

def get_file_hash(filepath):
    """Obtiene el hash MD5 de un archivo."""
    try:
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        print(f"Error al leer {filepath}: {e}")
        return None

def count_unit_folders():
    """Cuenta carpetas de unidades (p14_*, p15_*, etc.)."""
    count = 0
    for item in UNITS_DIR.iterdir():
        if item.is_dir() and any(item.name.startswith(prefix) for prefix in ["p14_", "p15_", "p16_", "p17_", "p18_", "p20_", "p7_", "z_"]):
            count += 1
    return count

def run_pipeline():
    """Ejecuta el pipeline completo de generación."""
    print("\n" + "="*70)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] INICIANDO PIPELINE DE GENERACION")
    print("="*70)

    try:
        # 1. Ejecutar gen_landings.py
        print("\n[1/4] Ejecutando gen_landings.py...")
        result = subprocess.run(["python", "gen_landings.py"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[ERROR] gen_landings.py:\n{result.stderr}")
            return False
        print("[OK] gen_landings.py completado")

        # 2. Ejecutar gen_pdfs.py
        print("\n[2/4] Ejecutando gen_pdfs.py...")
        result = subprocess.run(["python", "gen_pdfs.py"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[ERROR] gen_pdfs.py:\n{result.stderr}")
            return False
        print("[OK] gen_pdfs.py completado")

        # 3. Ejecutar gen_index.py
        print("\n[3/4] Ejecutando gen_index.py...")
        result = subprocess.run(["python", "gen_index.py"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[ERROR] gen_index.py:\n{result.stderr}")
            return False
        print("[OK] gen_index.py completado")

        # 4. Git commit y push
        print("\n[4/4] Sincronizando con GitHub...")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Chequear si hay cambios
        status_result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if not status_result.stdout.strip():
            print("[INFO] No hay cambios para commitear")
            return True

        # Hacer add, commit y push
        subprocess.run(["git", "add", "-A"], check=True)
        commit_msg = f"Auto-update landings [{timestamp}]"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("[OK] Cambios sincronizados con GitHub")

        print("\n" + "="*70)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [OK] PIPELINE COMPLETADO EXITOSAMENTE")
        print("="*70)
        return True

    except Exception as e:
        print(f"\n[ERROR] Error durante el pipeline: {e}")
        return False

def monitor_and_generate():
    """Monitorea cambios y ejecuta pipeline cuando sea necesario."""
    print("\n[AGENTE INTELIGENTE DE GENERACION DE LANDINGS]")
    print("="*70)
    print(f"Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Monitorea: {WATCH_FILE}")
    print(f"Directorio base: {BASE}")
    print("Presiona Ctrl+C para detener")
    print("="*70 + "\n")

    last_hash = get_file_hash(WATCH_FILE)
    last_unit_count = count_unit_folders()

    check_interval = 10  # Chequear cada 10 segundos
    inactivity_timeout = 3600  # Ejecutar al menos cada 1 hora aunque no haya cambios
    last_run = time.time()

    try:
        while True:
            time.sleep(check_interval)

            # Chequear cambios en gen_landings.py
            current_hash = get_file_hash(WATCH_FILE)
            current_unit_count = count_unit_folders()

            changes_detected = False

            if current_hash != last_hash:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] [CAMBIO] Detectado en {WATCH_FILE}")
                changes_detected = True
                last_hash = current_hash

            if current_unit_count != last_unit_count:
                diff = current_unit_count - last_unit_count
                print(f"[{datetime.now().strftime('%H:%M:%S')}] [CARPETAS] Cambio: {diff:+d} (total: {current_unit_count})")
                changes_detected = True
                last_unit_count = current_unit_count

            # Chequear timeout de inactividad
            time_since_last_run = time.time() - last_run
            if time_since_last_run > inactivity_timeout:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] [TIMEOUT] Inactividad {int(time_since_last_run/60)}m. Ejecutando generacion preventiva...")
                changes_detected = True

            # Ejecutar pipeline si hay cambios
            if changes_detected:
                if run_pipeline():
                    last_run = time.time()
                else:
                    print("[AVISO] Pipeline fallo. Reintentando en 1 minuto...")
                    time.sleep(60)

    except KeyboardInterrupt:
        print("\n\n[DETENIDO] Agente interrumpido por el usuario")
        print(f"Finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    monitor_and_generate()
