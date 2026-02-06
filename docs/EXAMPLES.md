# 💡 Ejemplos de Uso

Aquí tienes ejemplos prácticos de cómo sacar el máximo provecho a **Local Code Explainer (LCE)**.

## 1. Análisis de archivos individuales

Si quieres una explicación rápida de un archivo Python:
```bash
explain-code explain src/explainer/explainer.py
```

## 2. Exportación a JSON para integración
Ideal para usar los resultados de LCE en otras herramientas:
```bash
explain-code explain src/explainer/cache.py --format json > cache_analysis.json
```

## 3. Uso de la Interfaz Web (Gradio)
Para una experiencia visual e interactiva:
```bash
explain-code web
```
Esto abrirá una pestaña en tu navegador donde podrás subir archivos y ver el análisis de forma organizada.

## 4. Integración vía API REST
LCE puede funcionar como un microservicio:
```bash
# Iniciar el servidor
explain-code server
```
Luego puedes hacer peticiones `POST` a `http://localhost:8000/explain`:
```bash
curl -X POST "http://localhost:8000/explain" \
     -H "Content-Type: application/json" \
     -d '{"file_path": "src/api/server.py"}'
```

## 5. Ejemplo de Salida (CLI)
Cuando analizas un archivo, LCE te muestra:
- **Resumen AST**: Funciones, Clases y Dependencias detectadas.
- **Explicación del LLM**: Un desglose detallado de la lógica del código generado por tu modelo local.
- **Estadísticas**: Número de tokens y tiempo de procesamiento.
