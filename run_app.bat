@echo off
echo.
echo ========================================
echo  Excel to SQLite Importer
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

REM Ejecutar la aplicación
python main.py

if errorlevel 1 (
    echo.
    echo ERROR: La aplicación terminó con errores
    pause
)

echo.
echo Aplicación cerrada.
pause