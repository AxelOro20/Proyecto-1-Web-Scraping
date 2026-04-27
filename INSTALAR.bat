@echo off
REM Script de instalacion rapida para Scraper Profesional v5.0

echo.
echo ==========================================
echo  Scraper Profesional v5.0 - Instalacion
echo ==========================================
echo.

REM Detectar venv
if exist ".venv\Scripts\python.exe" (
    set PYTHON_PATH=.venv\Scripts\python.exe
    echo [OK] Entorno virtual encontrado
) else if exist "venv\Scripts\python.exe" (
    set PYTHON_PATH=venv\Scripts\python.exe
    echo [OK] Entorno virtual encontrado
) else (
    set PYTHON_PATH=python
    echo [!] Usando Python global
)

echo.
echo [1/3] Instalando dependencias...
call %PYTHON_PATH% -m pip install -q --upgrade pip
call %PYTHON_PATH% -m pip install -q -r requirements.txt

echo [2/3] Instalando navegador Chromium para Playwright...
call %PYTHON_PATH% -m playwright install chromium

echo.
echo [3/3] Creando directorios necesarios...
if not exist "logs" mkdir logs
if not exist "cookies" mkdir cookies
if not exist "excel" mkdir excel

echo.
echo ==========================================
echo  Instalacion completada!
echo ==========================================
echo.
echo Ejecuta el scraper con:
echo   %PYTHON_PATH% scraper_profesional.py
echo.
pause
