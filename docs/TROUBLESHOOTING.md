# 🔧 Solución de Problemas (Troubleshooting)

<!-- Si encuentras dificultades al usar LCE, aquí tienes las soluciones a los problemas más comunes. -->

## 1. Ollama no se encuentra o no responde
**Error**: `Ollama connection error` o comandos que no terminan.
- **Solución**: Asegúrate de que Ollama esté instalado y ejecutándose. Prueba ejecutando `ollama list` en tu terminal. Si no responde, inicia la aplicación de Ollama.

## 2. Modelo no descargado
**Error**: `Model 'mistral' not found`.
- **Solución**: LCE usa `mistral` por defecto. Descárgalo con:
  ```bash
  ollama pull mistral
  ```

## 3. Errores de Importación (ModuleNotFoundError)
**Error**: `ModuleNotFoundError: No module named 'explainer'`.
- **Solución**: Asegúrate de haber instalado el proyecto en modo editable desde la raíz:
  ```bash
  pip install -e .
  ```

## 4. Rendimiento Lento
**Problema**: La explicación tarda demasiado (> 30s).
- **Causa**: Tu hardware puede estar limitado para el modelo elegido o no estás usando aceleración por GPU.
- **Solución**: 
  - Asegúrate de que Ollama tenga acceso a tu GPU.
  - Prueba un modelo más ligero como `phi3` o `tinyllama`.
  - Configura el modelo en LCE (próximamente en configuración).

## 5. El análisis AST falla
**Error**: `SyntaxError` al parsear archivos.
- **Causa**: LCE actualmente está optimizado para Python 3.11+. Si intentas parsear un archivo con sintaxis no soportada por tu versión actual de Python, fallará.
- **Solución**: Verifica que el archivo de entrada sea código Python válido.
