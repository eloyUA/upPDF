#!/usr/bin/env python3

"""
======================================================
    SCRIPT GENERADO CON CHAT  GPT-4o
======================================================
"""

"""
----- Instalador completo -----
    - Tesseract OCR + todos los idiomas
    - Librerías Python:
        {
            pytesseract,
            pyspellchecker,
            customtkinter,
            pillow,
            pymupdf,
            pypdf,
            fpdf,
            numpy,
            ...
        }
"""

import platform
import subprocess
import sys
import shutil
import os

# Dependencias de PyPI
PYTHON_PACKAGES = [
    "pytesseract",
    "pyspellchecker",
    "customtkinter==5.2.2",
    "pillow==11.3.0",
    "pymupdf==1.26.3",
    "pypdf==5.7.0",
    "fpdf2",
    "numpy",
]

def run_ignore_error(cmd: list[str]):
    """Ejecuta un comando mostrando la salida. Si falla, muestra advertencia y continúa."""
    print(f"> {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(f"Advertencia: El comando falló con código {e.returncode} (se continúa).")

def install_pip_dependencies():
    """Instala los paquetes de PyPI."""
    run_ignore_error([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    run_ignore_error([sys.executable, "-m", "pip", "install"] + PYTHON_PACKAGES)

def verificar_path_en_windows():
    # Verificar tesseract en el path
    if not shutil.which("tesseract"):
        # Intentar ruta por defecto
        ruta_defecto = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        if not os.path.isfile(ruta_defecto):
            print("❌ No se encontró tesseract.exe. ¿Seguro que se instaló correctamente?")
        else:
            print("⚠️ tesseract.exe instalado pero no está en PATH.")
            print("Puedes usar pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'")
            print("Agrega la anterior linea de codigo en upPDF\modelo\imagen_escaner.py debajo de todas las importaciones de paquetes")
    else:
        print("✔️ Tesseract está en el PATH.")

def windows():
    print("→ Instalando en Windows...")

    # Tesseract
    if shutil.which("winget"):
        run_ignore_error(["winget", "install", "--exact", "--silent", "--id", "UB-Mannheim.TesseractOCR"])
        verificar_path_en_windows()
    elif shutil.which("choco"):
        run_ignore_error(["choco", "install", "-y", "tesseract"])
        verificar_path_en_windows()
    else:
        print("No se encontró winget ni Chocolatey. Instala Tesseract manualmente.")

def mac():
    print("→ Instalando en macOS...")
    if not shutil.which("brew"):
        sys.exit("Homebrew no está instalado. Instálalo desde https://brew.sh/")
    
    run_ignore_error(["brew", "update"])
    run_ignore_error(["brew", "install", "tesseract", "tesseract-lang"])

def linux():
    print("→ Instalando en Linux...")
    if shutil.which("apt"):
        pkgs = [
            "tesseract-ocr",
            "tesseract-ocr-all"
        ]
        run_ignore_error(["sudo", "apt-get", "update"])
        run_ignore_error(["sudo", "apt-get", "install", "-y"] + pkgs)

    elif shutil.which("dnf"):
        pkgs = [
            "tesseract",
            "tesseract-langpack*"
        ]
        run_ignore_error(["sudo", "dnf", "install", "-y"] + pkgs)

    elif shutil.which("pacman"):
        pkgs = [
            "tesseract",
            "tesseract-data"
        ]
        run_ignore_error(["sudo", "pacman", "-Sy", "--needed"] + pkgs)
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

        install_pip_dependencies()

        print("\nInstalación completada con éxito.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"\nEl comando falló con código {e.returncode}")

if __name__ == "__main__":
    main()