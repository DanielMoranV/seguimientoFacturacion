#!/usr/bin/env python3
"""
Script de configuración e instalación
"""

import subprocess
import sys
import os

def install_requirements():
    """Instalar dependencias"""
    print("📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False

def create_directories():
    """Crear directorios necesarios"""
    directories = ["exports", "samples"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Directorio creado: {directory}")

def main():
    print("🚀 Configurando Excel to SQLite Importer...")
    print("=" * 50)
    
    # Verificar Python
    if sys.version_info < (3, 7):
        print("❌ Se requiere Python 3.7 o superior")
        return
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Instalar dependencias
    if not install_requirements():
        return
    
    # Crear directorios
    create_directories()
    
    print("\n" + "=" * 50)
    print("🎉 Configuración completada!")
    print("\nPara ejecutar la aplicación:")
    print("  python gui_app.py")
    print("\nPara usar la versión de línea de comandos:")
    print("  python main.py archivo.xlsx")

if __name__ == "__main__":
    main()