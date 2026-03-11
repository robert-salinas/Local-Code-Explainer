@echo off 
setlocal 
title RS Local Code Explainer - Desktop Launcher 

:: Configuración de colores (Naranja RS sobre fondo oscuro si se pudiera, pero CMD es limitado) 
color 06 

echo ============================================ 
echo      RS DIGITAL - LOCAL CODE EXPLAINER 
echo ============================================ 

:: 1. Verificar si existe el entorno virtual 
if not exist ".venv" ( 
    echo [INFO] Primera instalacion detectada... 
    echo [INFO] Creando entorno virtual Python... 
    python -m venv .venv 
    
    echo [INFO] Instalando dependencias en modo editable... 
    call .venv\Scripts\activate 
    pip install -e .
    pip install customtkinter
    
    echo [SUCCESS] Instalacion completada. 
) else ( 
    echo [INFO] Entorno virtual encontrado. 
    call .venv\Scripts\activate 
    :: Asegurar que las dependencias esten actualizadas incluso si el venv ya existe
    pip install customtkinter >nul 2>&1
) 

:: 2. Iniciar la aplicación 
echo [INFO] Iniciando Local Code Explainer GUI... 
start /b pythonw main.py 

:: 3. Crear o Actualizar acceso directo en el escritorio (para asegurar que el icono esté actualizado)
echo [INFO] Actualizando acceso directo...
powershell -ExecutionPolicy Bypass -File create_shortcut.ps1

echo [OK] Aplicacion en ejecucion. 
echo Puedes cerrar esta ventana. 
pause 
exit