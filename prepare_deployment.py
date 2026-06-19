#!/usr/bin/env python3
"""
Prepara archivos para deployment en servidor Windows 11
Crea un ZIP con solo los archivos necesarios
"""

import os
import shutil
import zipfile
import sys
from pathlib import Path
from datetime import datetime

def main():
    # Verificar que estamos en la raiz del proyecto
    if not os.path.exists("gen_landings.py"):
        print("[ERROR] Este script debe ejecutarse desde la raiz del proyecto")
        print("Ejecuta: cd C:\\Users\\marcelo\\Documents\\Landings")
        sys.exit(1)

    project_root = os.getcwd()
    temp_dir = os.path.join(project_root, "temp_deployment")

    # Generar nombre del ZIP con timestamp
    now = datetime.now()
    zip_name = f"Landings_Deployment_{now.strftime('%Y%m%d_%H%M')}.zip"

    print()
    print("=" * 40)
    print("[DEPLOYMENT] Preparar para servidor")
    print("=" * 40)
    print()

    # Limpiar carpeta temporal si existe
    if os.path.exists(temp_dir):
        print("[INFO] Limpiando carpeta temporal anterior...")
        try:
            shutil.rmtree(temp_dir)
        except PermissionError:
            import subprocess
            subprocess.run(f'rmdir /s /q "{temp_dir}"', shell=True, capture_output=True)

    # Crear estructura base
    os.makedirs(f"{temp_dir}/server/bin", exist_ok=True)
    os.makedirs(f"{temp_dir}/server/config", exist_ok=True)
    os.makedirs(f"{temp_dir}/server/scripts", exist_ok=True)

    print("[1/3] Copiando archivos necesarios...")

    # Copiar server/
    for file in ["install.bat", "start.bat", "stop.bat", "status.bat", "logs.bat", "uninstall.bat"]:
        src = f"server/bin/{file}"
        if os.path.exists(src):
            shutil.copy2(src, f"{temp_dir}/server/bin/")

    shutil.copy2("server/config/config.json", f"{temp_dir}/server/config/")
    shutil.copy2("server/scripts/agent_service.py", f"{temp_dir}/server/scripts/")

    for file in ["README.md", "INSTALACION.md", "requirements.txt"]:
        src = f"server/{file}"
        if os.path.exists(src):
            shutil.copy2(src, f"{temp_dir}/server/")

    print("   [OK] server/ copiado")

    # Copiar scripts generadores
    for file in ["gen_landings.py", "gen_pdfs.py", "gen_index.py"]:
        if os.path.exists(file):
            shutil.copy2(file, temp_dir)

    if os.path.exists("export_data.py"):
        shutil.copy2("export_data.py", temp_dir)

    print("   [OK] Scripts generadores copiados")

    # Copiar archivos publicos
    for file in ["index.html", "pensaer-logo.png", "politica-privacidad.html"]:
        if os.path.exists(file):
            shutil.copy2(file, temp_dir)

    print("   [OK] Archivos públicos copiados")

    # Copiar carpetas de unidades
    print("   Copiando carpetas de unidades...")
    prefixes = ["p14_", "p15_", "p16_", "p17_", "p18_", "p20_", "p7_", "z_"]
    for item in os.listdir("."):
        if os.path.isdir(item):
            if any(item.startswith(p) for p in prefixes):
                print(f"     - {item}")
                shutil.copytree(item, f"{temp_dir}/{item}", dirs_exist_ok=True)

    print("   [OK] Unidades copiadas")

    # Copiar plantas
    if any(d.startswith("plantas_") for d in os.listdir(".")):
        print("   Copiando plantas...")
        for item in os.listdir("."):
            if item.startswith("plantas_") and os.path.isdir(item):
                print(f"     - {item}")
                shutil.copytree(item, f"{temp_dir}/{item}", dirs_exist_ok=True)
        print("   [OK] Plantas copiadas")

    # Copiar renders (SOLO .jpg)
    print("   Copiando renders (solo imágenes públicas)...")
    for item in os.listdir("."):
        if item.startswith("renders_") and os.path.isdir(item):
            print(f"     - {item}")
            os.makedirs(f"{temp_dir}/{item}", exist_ok=True)
            for file in os.listdir(item):
                if file.endswith(".jpg"):
                    src = f"{item}/{file}"
                    dst = f"{temp_dir}/{item}/{file}"
                    shutil.copy2(src, dst)

    print("   [OK] Renders copiados")

    # Copiar .git y .gitignore
    print("[2/3] Copiando configuración de Git...")
    if os.path.exists(".git"):
        shutil.copytree(".git", f"{temp_dir}/.git", dirs_exist_ok=True)
    if os.path.exists(".gitignore"):
        shutil.copy2(".gitignore", temp_dir)
    print("   [OK] Git copiado")

    # Crear ZIP
    print("[3/3] Creando ZIP...")

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)

    print(f"   [OK] ZIP creado: {zip_name}")

    # Limpiar
    print()
    print("Limpiando archivos temporales...")
    try:
        shutil.rmtree(temp_dir)
    except PermissionError:
        # Git puede bloquear archivos temporalmente
        import subprocess
        subprocess.run(f'rmdir /s /q "{temp_dir}"', shell=True, capture_output=True)

    # Mostrar resultado
    zip_size_mb = os.path.getsize(zip_name) / (1024 * 1024)

    print()
    print("=" * 40)
    print("[OK] PREPARACION COMPLETADA")
    print("=" * 40)
    print()
    print(f"Archivo ZIP creado: {zip_name}")
    print(f"Tamaño: ~{int(zip_size_mb)} MB")
    print()
    print("Siguiente paso:")
    print(f"  1. Copia {zip_name} al servidor Windows 11")
    print("  2. Extrae en C:\\Landings\\")
    print("  3. Abre CMD como ADMINISTRADOR")
    print("  4. Ejecuta: cd C:\\Landings\\server\\bin")
    print("  5. Ejecuta: install.bat")
    print("  6. Ejecuta: start.bat")
    print()

if __name__ == "__main__":
    main()
