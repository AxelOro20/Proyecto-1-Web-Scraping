#!/usr/bin/env python
"""
Script de verificacion y diagnostico para Scraper Profesional v5.0
=========================================================

Este script verifica que todo esté instalado correctamente
"""

import sys
import subprocess
from pathlib import Path
import platform

def print_header(titulo):
    print("\n" + "="*60)
    print(f"  {titulo}")
    print("="*60 + "\n")

def verificar_modulo(nombre, import_name=None):
    """Verifica si un módulo está instalado."""
    import_name = import_name or nombre
    try:
        __import__(import_name)
        print(f"✅ {nombre:20s} - Instalado")
        return True
    except ImportError:
        print(f"❌ {nombre:20s} - NO instalado")
        return False

def verificar_archivos():
    """Verifica archivos necesarios."""
    archivos = [
        'scraper_profesional.py',
        'scraper_config.json',
        'requirements.txt',
    ]
    
    print("\n📁 Verificando archivos...")
    todos_ok = True
    for archivo in archivos:
        if Path(archivo).exists():
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - FALTA")
            todos_ok = False
    
    return todos_ok

def verificar_directorios():
    """Verifica directorios necesarios."""
    directorios = ['logs', 'cookies', 'excel']
    
    print("\n📂 Creando directorios necesarios...")
    for directorio in directorios:
        Path(directorio).mkdir(exist_ok=True)
        print(f"✅ {directorio}/")

def main():
    print_header("DIAGNOSTICO - SCRAPER PROFESIONAL v5.0")
    
    print(f"🖥️  Sistema: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📍 Ubicación: {Path.cwd()}")
    
    print_header("Verificando módulos Python")
    
    modulos = [
        ('Playwright', 'playwright'),
        ('Pandas', 'pandas'),
        ('OpenPyXL', 'openpyxl'),
        ('TKinter', 'tkinter'),
    ]
    
    todos_instalados = True
    for nombre, import_name in modulos:
        if not verificar_modulo(nombre, import_name):
            todos_instalados = False
    
    verificar_archivos()
    verificar_directorios()
    
    print_header("RESULTADO")
    
    if todos_instalados:
        print("✅ TODO ESTÁ LISTO!")
        print("\nEjecuta:")
        print("  python scraper_profesional.py")
        return 0
    else:
        print("❌ FALTAN MÓDULOS")
        print("\nInstala dependencias con:")
        print("  pip install -r requirements.txt")
        print("  python -m playwright install chromium")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
