@echo off
echo.
echo ========================================
echo  Seguimiento de Facturación
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en PATH
    echo Por favor instala Python 3.7+ desde https://python.org
    pause
    exit /b 1
)

REM Verificar si las dependencias están instaladas
python -c "import customtkinter" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

echo Iniciando aplicación...
echo.

@REM REM Limpiar la base de datos antes de iniciar
@REM python -c "from src.models.database import DatabaseManager; import logging; logging.basicConfig(level=logging.INFO); db = DatabaseManager({"paths": {"db_path": 'facturacion.db'}}, logging.getLogger()); db.clear_database_tables()"

REM Ejecutar la aplicación desde el directorio raíz
python -m src.main

if errorlevel 1 (
    echo.
    echo ERROR: La aplicación terminó con errores
    pause
)

echo.
echo Aplicación cerrada.
pause