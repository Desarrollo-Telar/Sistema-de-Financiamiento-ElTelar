@echo off
setlocal enabledelayedexpansion

:: Cambiar a tu directorio del repositorio local
cd C:\ruta\a\tu\repositorio

:: Verificar si hay cambios en el repositorio remoto
git fetch

:: Verificar si hay cambios nuevos para descargar
git status | findstr /C:"Your branch is behind"

:: Si hay cambios, ejecutar git pull
if %errorlevel% equ 0 (
    echo Hay nuevos cambios. Ejecutando git pull...
    git pull
) else (
    echo No hay cambios nuevos.
)

endlocal
pause