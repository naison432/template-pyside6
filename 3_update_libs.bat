@echo off
echo Actualizando librerias del proyecto...

REM Verificar si existe el entorno virtual
if not exist ".venv" (
    echo Creando entorno virtual...
    python -m venv .venv
)

REM Activar entorno
call .venv\Scripts\activate

REM Instalar/Actualizar requerimientos
echo Instalando dependencias desde requirements.txt...
pip install -r requirements.txt

echo.
echo Proceso completado.
pause
