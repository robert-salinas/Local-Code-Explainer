# Arquitectura del Sistema - Local Code Explainer

## Descripción General
LCE está diseñado como una aplicación modular que separa la lógica de análisis, la inferencia del modelo y las interfaces de usuario.

## Componentes Principales

1. **CodeParser (Análisis Estático)**:
   - Utiliza el módulo `ast` de Python para descomponer el código en estructuras lógicas (clases, funciones, imports).
   - Proporciona metadatos que enriquecen el prompt del LLM.

2. **LLMHandler (Inferencia)**:
   - Capa de abstracción sobre la API local de Ollama.
   - Gestiona la construcción de prompts y la comunicación con el modelo (Mistral por defecto).

3. **ExplanationCache (Persistencia)**:
   - Almacena hashes de archivos y sus explicaciones correspondientes en el sistema de archivos local.
   - Optimiza el rendimiento al evitar llamadas redundantes al LLM.

4. **Interfaces (CLI, API, Web)**:
   - **CLI**: Construida con Typer para una experiencia de desarrollador fluida.
   - **API**: Implementada con FastAPI para permitir integraciones externas.
   - **Web**: Basada en Gradio para una visualización rápida y prototipado.

## Flujo de Datos
1. El usuario proporciona una ruta de archivo.
2. `CodeParser` analiza el archivo y extrae metadatos.
3. Se genera un hash del contenido del archivo.
4. `ExplanationCache` verifica si ya existe una explicación para ese hash.
5. Si no existe, `LLMHandler` envía el código + metadatos a Ollama.
6. La respuesta se guarda en caché y se entrega al usuario a través de la interfaz elegida.
