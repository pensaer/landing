@echo off
REM Desinstalador de Pensaer Landings Auto-Generation Service

setlocal enabledelayedexpansion

REM Verificar privilegios de administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Este script debe ejecutarse como ADMINISTRADOR
    pause
    exit /b 1
)

REM Directorios
set BASE_DIR=%~dp0..
set NSSM_PATH=%BASE_DIR%\bin\nssm.exe

echo.
echo ========================================
echo [DESINSTALADOR] Pensaer Landings Agent
echo ========================================
echo.

REM Detener servicio
echo [1/2] Deteniendo servicio...
net stop PensaerLandingsAgent >nul 2>&1
timeout /t 2 /nobreak >nul

REM Remover servicio
echo [2/2] Removiendo servicio...
sc query PensaerLandingsAgent >nul 2>&1
if %errorlevel% equ 0 (
    if exist "%NSSM_PATH%" (
        "%NSSM_PATH%" remove PensaerLandingsAgent confirm
    ) else (
        sc delete PensaerLandingsAgent
    )
    echo [OK] Servicio removido
) else (
    echo [INFO] Servicio no encontrado (puede que no este instalado)
)

echo.
echo ========================================
echo [OK] DESINSTALACION COMPLETADA
echo ========================================
echo.
echo Nota: Los archivos de configuracion y logs se han conservado en:
echo   %BASE_DIR%\config\
echo   %BASE_DIR%\logs\
echo.
pause
