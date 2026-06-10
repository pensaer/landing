@echo off
REM Instalador de Pensaer Landings Auto-Generation Service

setlocal enabledelayedexpansion

REM Verificar privilegios de administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Este script debe ejecutarse como ADMINISTRADOR
    echo.
    echo Haz clic derecho en install.bat y selecciona "Ejecutar como administrador"
    pause
    exit /b 1
)

REM Directorios
set BASE_DIR=%~dp0..
set SCRIPTS_DIR=%BASE_DIR%\scripts
set CONFIG_DIR=%BASE_DIR%\config
set LOGS_DIR=%BASE_DIR%\logs

REM Crear directorios si no existen
if not exist "%LOGS_DIR%" mkdir "%LOGS_DIR%"

echo.
echo ========================================
echo [INSTALADOR] Pensaer Landings Agent
echo ========================================
echo.

REM 1. Verificar Python
echo [1/3] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado en PATH
    echo Por favor instala Python o agrega su ruta a PATH
    pause
    exit /b 1
)
echo [OK] Python encontrado

REM 2. Instalar dependencias Python
echo.
echo [2/3] Verificando dependencias Python...
python -c "import logging.handlers" >nul 2>&1
if %errorlevel% neq 0 (
    echo [AVISO] Algunas dependencias pueden no estar disponibles
    echo (logging.handlers deberia estar en stdlib)
)
echo [OK] Dependencias verificadas

REM 3. Instalar servicio de Windows
echo.
echo [3/3] Instalando servicio de Windows...

REM Descargar NSSM si no existe
set NSSM_PATH=%BASE_DIR%\bin\nssm.exe
if not exist "%NSSM_PATH%" (
    echo [AVISO] Descargando NSSM (herramienta para servicios Windows)...
    powershell -NoProfile -Command ^
        "try { Invoke-WebRequest -Uri 'https://nssm.cc/download/nssm-2.24-101-g897c7f7.zip' -OutFile '%BASE_DIR%\nssm.zip' } catch { Write-Host 'No se pudo descargar NSSM. Descargalo manualmente desde https://nssm.cc'; exit 1 }"

    if %errorlevel% neq 0 (
        echo.
        echo [INSTALACION MANUAL REQUERIDA]
        echo 1. Descarga NSSM desde: https://nssm.cc/download
        echo 2. Extrae el contenido en: %BASE_DIR%\bin\
        echo 3. Ejecuta este script nuevamente
        echo.
        pause
        exit /b 1
    )

    REM Extraer ZIP
    powershell -NoProfile -Command "Expand-Archive -Path '%BASE_DIR%\nssm.zip' -DestinationPath '%BASE_DIR%\bin\' -Force"
    del "%BASE_DIR%\nssm.zip"
)

REM Instalar/actualizar servicio
echo [INFO] Configurando servicio: PensaerLandingsAgent

REM Si existe, removelo primero
sc query PensaerLandingsAgent >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Removiendo servicio existente...
    "%NSSM_PATH%" remove PensaerLandingsAgent confirm
)

REM Instalar nuevo servicio
echo [INFO] Instalando nuevo servicio...
"%NSSM_PATH%" install PensaerLandingsAgent python "%SCRIPTS_DIR%\agent_service.py"

REM Configurar
"%NSSM_PATH%" set PensaerLandingsAgent AppDirectory "%BASE_DIR%"
"%NSSM_PATH%" set PensaerLandingsAgent AppStdout "%LOGS_DIR%\stdout.log"
"%NSSM_PATH%" set PensaerLandingsAgent AppStderr "%LOGS_DIR%\stderr.log"
"%NSSM_PATH%" set PensaerLandingsAgent AppRotateFiles 1
"%NSSM_PATH%" set PensaerLandingsAgent AppRotateSeconds 3600

REM Configurar reinicio automatico
"%NSSM_PATH%" set PensaerLandingsAgent AppExit Default Restart

echo [OK] Servicio instalado

REM 4. Resumen
echo.
echo ========================================
echo [OK] INSTALACION COMPLETADA
echo ========================================
echo.
echo Siguiente paso:
echo   1. Inicia el servicio:
echo      net start PensaerLandingsAgent
echo.
echo   2. Verifica el estado:
echo      net start
echo.
echo   3. Ve a los logs:
echo      %LOGS_DIR%\agent_service.log
echo.
echo Control del servicio:
echo   - Iniciar:  net start PensaerLandingsAgent
echo   - Detener:  net stop PensaerLandingsAgent
echo   - Estado:   sc query PensaerLandingsAgent
echo.
echo Para desinstalar:
echo   - Ejecuta: uninstall.bat
echo.
pause
