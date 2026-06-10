@echo off
REM Script para preparar archivos para copiar al servidor Windows 11
REM Crea un ZIP con solo los archivos necesarios

setlocal enabledelayedexpansion

echo.
echo ========================================
echo [DEPLOYMENT] Preparar para servidor
echo ========================================
echo.

REM Verificar que estamos en la carpeta correcta
if not exist "gen_landings.py" (
    echo [ERROR] Este script debe ejecutarse desde la raiz del proyecto
    echo Ejecuta: cd C:\Users\marcelo\Documents\Landings
    pause
    exit /b 1
)

REM Crear carpeta temporal
set TEMP_DIR=temp_deployment
set ZIP_NAME=Landings_Deployment_%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%.zip

if exist "%TEMP_DIR%" (
    echo [INFO] Limpiando carpeta temporal anterior...
    rmdir /s /q "%TEMP_DIR%" >nul 2>&1
)

mkdir "%TEMP_DIR%"

echo [1/3] Copiando archivos necesarios...

REM Crear estructura base
mkdir "%TEMP_DIR%\server"
mkdir "%TEMP_DIR%\server\bin"
mkdir "%TEMP_DIR%\server\config"
mkdir "%TEMP_DIR%\server\scripts"

REM Copiar archivos server
copy /y server\bin\install.bat "%TEMP_DIR%\server\bin\" >nul
copy /y server\bin\start.bat "%TEMP_DIR%\server\bin\" >nul
copy /y server\bin\stop.bat "%TEMP_DIR%\server\bin\" >nul
copy /y server\bin\status.bat "%TEMP_DIR%\server\bin\" >nul
copy /y server\bin\logs.bat "%TEMP_DIR%\server\bin\" >nul
copy /y server\bin\uninstall.bat "%TEMP_DIR%\server\bin\" >nul

copy /y server\config\config.json "%TEMP_DIR%\server\config\" >nul
copy /y server\scripts\agent_service.py "%TEMP_DIR%\server\scripts\" >nul
copy /y server\README.md "%TEMP_DIR%\server\" >nul
copy /y server\INSTALACION.md "%TEMP_DIR%\server\" >nul
copy /y server\requirements.txt "%TEMP_DIR%\server\" >nul

echo   [OK] server/ copiado

REM Copiar scripts generadores
copy /y gen_landings.py "%TEMP_DIR%\" >nul
copy /y gen_pdfs.py "%TEMP_DIR%\" >nul
copy /y gen_index.py "%TEMP_DIR%\" >nul

if exist "export_data.py" copy /y export_data.py "%TEMP_DIR%\" >nul

echo   [OK] Scripts generadores copiados

REM Copiar archivos publicos raiz
copy /y index.html "%TEMP_DIR%\" >nul
copy /y pensaer-logo.png "%TEMP_DIR%\" >nul

if exist "politica-privacidad.html" copy /y politica-privacidad.html "%TEMP_DIR%\" >nul

echo   [OK] Archivos públicos copiados

REM Copiar carpetas de unidades
echo   Copiando carpetas de unidades...
for /d %%d in (p14_* p15_* p16_* p17_* p18_* p20_* p7_* z_*) do (
    echo     - %%d
    xcopy /e /i /y "%%d" "%TEMP_DIR%\%%d" >nul 2>&1
)
echo   [OK] Unidades copiadas

REM Copiar plantas
if exist "plantas_p14" (
    echo   Copiando plantas...
    for /d %%d in (plantas_*) do (
        echo     - %%d
        xcopy /e /i /y "%%d" "%TEMP_DIR%\%%d" >nul 2>&1
    )
    echo   [OK] Plantas copiadas
)

REM Copiar renders (SOLO .jpg, NO inserts)
echo   Copiando renders (solo imágenes públicas)...
for /d %%d in (renders_*) do (
    echo     - %%d
    if not exist "%TEMP_DIR%\%%d" mkdir "%TEMP_DIR%\%%d"

    REM Copiar SOLO .jpg
    for %%f in ("%%d\*.jpg") do (
        copy /y "%%f" "%TEMP_DIR%\%%d\" >nul 2>&1
    )
)
echo   [OK] Renders copiados

REM Copiar .git y .gitignore
echo [2/3] Copiando configuracion de Git...
xcopy /e /i /y .git "%TEMP_DIR%\.git" >nul 2>&1
copy /y .gitignore "%TEMP_DIR%\" >nul
echo   [OK] Git copiado

echo [3/3] Creando ZIP...

REM Crear ZIP usando PowerShell
powershell -NoProfile -Command ^
    "Add-Type -AssemblyName 'System.IO.Compression.FileSystem'; ^
    [System.IO.Compression.ZipFile]::CreateFromDirectory('%cd%\%TEMP_DIR%', '%cd%\%ZIP_NAME%')"

if %errorlevel% equ 0 (
    echo   [OK] ZIP creado: %ZIP_NAME%
) else (
    echo   [ERROR] No se pudo crear el ZIP
    echo   Verifica que PowerShell este disponible
    pause
    exit /b 1
)

REM Limpiar
echo.
echo Limpiando archivos temporales...
rmdir /s /q "%TEMP_DIR%" >nul 2>&1

echo.
echo ========================================
echo [OK] PREPARACION COMPLETADA
echo ========================================
echo.
echo Archivo ZIP creado:
echo   %ZIP_NAME%
echo.
echo Tamaño:
for %%A in ("%ZIP_NAME%") do set SIZE=%%~zA
set /a SIZE_MB=SIZE/1024/1024
echo   ~%SIZE_MB% MB
echo.
echo Siguiente paso:
echo   1. Copia %ZIP_NAME% al servidor Windows 11
echo   2. Extrae en C:\Landings\
echo   3. Abre CMD como ADMINISTRADOR
echo   4. Ejecuta: cd C:\Landings\server\bin
echo   5. Ejecuta: install.bat
echo   6. Ejecuta: start.bat
echo.
echo Contenido del ZIP:
echo   - server/     (scripts + config)
echo   - gen_*.py    (generadores)
echo   - p*_*/       (unidades)
echo   - plantas_*/  (plantas)
echo   - renders_*/  (renders publicos, SOLO .jpg)
echo   - .git/       (historial)
echo.
pause
