@echo off
echo ===================================================
echo   DESVINCULAR DE LA PLANTILLA (RESET GIT)
echo ===================================================
echo.
echo ESTO BORRARA EL HISTORIAL DE GIT ACTUAL Y CREARA UNO NUEVO.
echo Usalo solo si acabas de clonar la plantilla para un nuevo proyecto.
echo.
set /p confirm="Estas seguro? (S/N): "
if /i "%confirm%" neq "S" goto cancelled

echo.
echo 1. Eliminando carpeta .git...
rmdir /s /q .git

echo.
echo 2. Inicializando nuevo repositorio...
git init

echo.
echo 3. Agregando archivos...
git add .
git commit -m "Initial commit from template"

echo.
echo LISTO! El proyecto ahora es independiente.
goto end

:cancelled
echo Operacion cancelada.

:end
pause
