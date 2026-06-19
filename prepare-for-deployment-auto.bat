@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo [DEPLOYMENT] Preparar para servidor
echo ========================================
echo.

if not exist "gen_landings.py" (
    echo [ERROR] Este script debe ejecutarse desde la raiz del proyecto
    exit /b 1
)

set TEMP_DIR=temp_deployment
set ZIP_NAME=Landings_Deployment_%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%.zip

if exist "%TEMP_DIR%" (
    echo [INFO] Limpiando carpeta temporal anterior...
    rmdir /s /q "%TEMP_DIR%" >nul 2>&1
)

mkdir "%TEMP_DIR%"

echo [1/3] Copiando archivos necesarios...

mkdir "%TEMP_DIR%\server"
mkdir "%TEMP_DIR%\server\bin"
mkdir "%TEMP_DIR%\server\config"
mkdir "%TEMP_DIR%\server\scripts"

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

copy /y gen_landings.py "%TEMP_DIR%\" >nul
copy /y gen_pdfs.py "%TEMP_DIR%\" >nul
copy /y gen_index.py "%TEMP_DIR%\" >nul

if exist "export_data.py" copy /y export_data.py "%TEMP_DIR%\" >nul

echo   [OK] Scripts generadores copiados

copy /y index.html "%TEMP_DIR%\" >nul
copy /y pensaer-logo.png "%TEMP_DIR%\" >nul

if exist "politica-privacidad.html" copy /y politica-privacidad.html "%TEMP_DIR%\" >nul

echo   [OK] Archivos publicos copiados

echo   Copiando carpetas de unidades...
for /d %%d in (p14_* p15_* p16_* p17_* p18_* p20_* p7_* z_*) do (
    echo     - %%d
    xcopy /e /i /y "%%d" "%TEMP_DIR%\%%d" >nul 2>&1
)
echo   [OK] Unidades copiadas

if exist "plantas_p14" (
    echo   Copiando plantas...
    for /d %%d in (plantas_*) do (
        echo     - %%d
        xcopy /e /i /y "%%d" "%TEMP_DIR%\%%d" >nul 2>&1
    )
    echo   [OK] Plantas copiadas
)

echo   Copiando renders (solo imagenes publicas)...
for /d %%d in (renders_*) do (
    echo     - %%d
    if not exist "%TEMP_DIR%\%%d" mkdir "%TEMP_DIR%\%%d"
    for %%f in ("%%d\*.jpg") do (
        copy /y "%%f" "%TEMP_DIR%\%%d\" >nul 2>&1
    )
)
echo   [OK] Renders copiados

echo [2/3] Copiando configuracion de Git...
xcopy /e /i /y .git "%TEMP_DIR%\.git" >nul 2>&1
copy /y .gitignore "%TEMP_DIR%\" >nul
echo   [OK] Git copiado

echo [3/3] Creando ZIP...

powershell -NoProfile -Command "Add-Type -AssemblyName 'System.IO.Compression.FileSystem'; [System.IO.Compression.ZipFile]::CreateFromDirectory('%cd%\%TEMP_DIR%', '%cd%\%ZIP_NAME%')"

if %errorlevel% equ 0 (
    echo   [OK] ZIP creado: %ZIP_NAME%
) else (
    echo   [ERROR] No se pudo crear el ZIP
    exit /b 1
)

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
for %%A in ("%ZIP_NAME%") do set SIZE=%%~zA
set /a SIZE_MB=SIZE/1024/1024
echo Tamaño: ~%SIZE_MB% MB
echo.
echo Siguiente paso:
echo   1. Copia %ZIP_NAME% al servidor Windows 11
echo   2. Extrae en C:\Landings\
echo   3. Abre CMD como ADMINISTRADOR
echo   4. Ejecuta: cd C:\Landings\server\bin
echo   5. Ejecuta: install.bat
echo   6. Ejecuta: start.bat
echo.
