@echo off
REM Muestra los logs del servicio en tiempo real

set BASE_DIR=%~dp0..
set LOG_FILE=%BASE_DIR%\logs\agent_service.log

echo.
echo ========================================
echo [LOGS] Pensaer Landings Agent Service
echo ========================================
echo.
echo Archivo: %LOG_FILE%
echo.

if not exist "%LOG_FILE%" (
    echo [ERROR] Archivo de log no encontrado
    echo El servicio puede no haber iniciado aun
    pause
    exit /b 1
)

REM Mostrar ultimas 50 lineas y esperar nuevas
powershell -NoProfile -Command ^
    "Get-Content '%LOG_FILE%' -Tail 50 -Wait | ForEach-Object { Write-Host $_ }"

pause
