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
) 

:: 2. Iniciar la aplicación 
echo [INFO] Iniciando Local Code Explainer GUI... 
start /b pythonw main.py 

:: 3. (Opcional) Crear acceso directo en el escritorio si no existe 
if not exist "%USERPROFILE%\Desktop\RS-LCE-Desktop.lnk" ( 
    echo [INFO] Creando acceso directo en el Escritorio... 
    powershell -ExecutionPolicy Bypass -File create_shortcut.ps1 
) 

echo [OK] Aplicacion en ejecucion. 
echo Puedes cerrar esta ventana. 
pause 
exit