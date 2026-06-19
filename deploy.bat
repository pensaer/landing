@echo off
setlocal enabledelayedexpansion

echo.
echo [DEPLOYMENT] Preparar para servidor
echo.

if not exist "gen_landings.py" (
    echo [ERROR] Ejecuta desde la raiz del proyecto
    exit /b 1
)

set TEMP_DIR=temp_deployment
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set ZIP_NAME=Landings_Deployment_%mydate%_%mytime%.zip

if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"

echo [1/3] Copiando archivos...
mkdir "%TEMP_DIR%\server\bin"
mkdir "%TEMP_DIR%\server\config"
mkdir "%TEMP_DIR%\server\scripts"

copy /y server\bin\*.bat "%TEMP_DIR%\server\bin\" >/dev/null
copy /y server\config\config.json "%TEMP_DIR%\server\config\" >/dev/null
copy /y server\scripts\agent_service.py "%TEMP_DIR%\server\scripts\" >/dev/null
copy /y server\*.md "%TEMP_DIR%\server\" >/dev/null
copy /y server\requirements.txt "%TEMP_DIR%\server\" >/dev/null
echo   [OK] server/

copy /y gen_*.py "%TEMP_DIR%\" >/dev/null
copy /y index.html pensaer-logo.png "%TEMP_DIR%\" >/dev/null
if exist "politica-privacidad.html" copy /y politica-privacidad.html "%TEMP_DIR%\" >/dev/null
echo   [OK] Scripts + HTML

for /d %%d in (p14_* p15_* p16_* p17_* p18_* p20_* p7_* z_* plantas_* renders_*) do (
    if exist "%%d" (
        xcopy /e /i /y "%%d" "%TEMP_DIR%\%%d" >/dev/null 2>&1
    )
)
echo   [OK] Carpetas de unidades

echo [2/3] Git...
xcopy /e /i /y .git "%TEMP_DIR%\.git" >/dev/null 2>&1
copy /y .gitignore "%TEMP_DIR%\" >/dev/null
echo   [OK]

echo [3/3] Creando ZIP: %ZIP_NAME%
powershell -NoProfile -Command "Add-Type -AssemblyName 'System.IO.Compression.FileSystem'; [System.IO.Compression.ZipFile]::CreateFromDirectory('%cd%\%TEMP_DIR%', '%cd%\%ZIP_NAME%')"

rmdir /s /q "%TEMP_DIR%"

echo.
echo [OK] LISTO
echo Archivo: %ZIP_NAME%
echo.
