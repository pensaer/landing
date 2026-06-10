@echo off
REM Inicia el servicio Pensaer Landings Agent

echo Iniciando servicio: PensaerLandingsAgent
net start PensaerLandingsAgent

if %errorlevel% equ 0 (
    echo.
    echo [OK] Servicio iniciado correctamente
) else (
    echo.
    echo [ERROR] No se pudo iniciar el servicio
    echo Verifica que este instalado: install.bat
)

pause
