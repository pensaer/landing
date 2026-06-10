@echo off
REM Detiene el servicio Pensaer Landings Agent

echo Deteniendo servicio: PensaerLandingsAgent
net stop PensaerLandingsAgent

if %errorlevel% equ 0 (
    echo.
    echo [OK] Servicio detenido correctamente
) else (
    echo.
    echo [ERROR] No se pudo detener el servicio
    echo El servicio puede no estar corriendo
)

pause
