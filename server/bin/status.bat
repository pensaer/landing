@echo off
REM Muestra el estado del servicio

echo.
echo ========================================
echo [STATUS] Pensaer Landings Agent Service
echo ========================================
echo.

sc query PensaerLandingsAgent

echo.
echo ========================================

REM Mostrar ultimas lineas del log
set BASE_DIR=%~dp0..
set LOG_FILE=%BASE_DIR%\logs\agent_service.log

if exist "%LOG_FILE%" (
    echo.
    echo [ULTIMAS LINEAS DEL LOG]
    powershell -NoProfile -Command "Get-Content '%LOG_FILE%' -Tail 10"
) else (
    echo.
    echo [LOG NO ENCONTRADO] %LOG_FILE%
)

echo.
pause
