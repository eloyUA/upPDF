#!/usr/bin/env python3

"""
======================================================
    SCRIPT GENERADO CON CHAT  GPT-4o
======================================================
"""

"""
----- Desinstalador completo -----
    - Tesseract OCR + todos los idiomas
    - Librerías Python: pytesseract
"""
PYTHON_PACKAGES = [
    "pytesseract"
]

import platform
import subprocess
import sys
import shutil

def run_ignore_error(cmd: list[str]):
    """Ejecuta un comando mostrando la salida. Si falla, muestra advertencia y continúa."""
    print(f"> {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(f"Advertencia: El comando falló con código {e.returncode} (se continúa).")

def uninstall_pip_dependencies():
    run_ignore_error([sys.executable, "-m", "pip", "uninstall"] + PYTHON_PACKAGES)

def windows():
    print("→ Desinstalando en Windows...")

    # Tesseract
    if shutil.which("winget"):
        run_ignore_error(["winget", "uninstall", "UB-Mannheim.TesseractOCR"])
    elif shutil.which("choco"):
        run_ignore_error(["choco", "uninstall", "-y", "tesseract"])
    else:
        print("No se encontró winget ni Chocolatey. Instala Tesseract manualmente.")

def mac():
    print("→ Desinstalando en macOS...")
    if not shutil.which("brew"):
        sys.exit("Homebrew no está instalado. Instálalo desde https://brew.sh/")
    
    run_ignore_error(["brew", "uninstall", "--ignore-dependencies", "tesseract"])
    run_ignore_error(["brew", "uninstall", "--ignore-dependencies", "tesseract-lang"])

def linux():
    print("→ Desinstalando en Linux...")
    if shutil.which("apt"):
        pkgs = [
            "tesseract-ocr",
            "tesseract-ocr-all"
        ]
        run_ignore_error(["sudo", "apt-get", "purge"] + pkgs)

    elif shutil.which("dnf"):
        pkgs = [
            "tesseract",
            "tesseract-langpack\*"
        ]
        run_ignore_error(["sudo", "dnf", "remove"] + pkgs)

    elif shutil.which("pacman"):
        pkgs = [
            "tesseract",
            "tesseract-data"
        ]
        run_ignore_error(["sudo", "pacman", "-Rns"] + pkgs)
    else:
        sys.exit("No se reconoce tu gestor de paquetes (apt, dnf, pacman).")

def main():
    osname = platform.system()
    try:
        if osname == "Windows":
            windows()
        elif osname == "Darwin":
            mac()
        elif osname == "Linux":
            linux()
        else:
            sys.exit(f"SO no reconocido: {osname}")

        uninstall_pip_dependencies()

        print("\nDesinstalación completada con éxito.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"\nEl comando falló con código {e.returncode}")

if __name__ == "__main__":
    main()