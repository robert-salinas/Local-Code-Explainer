# ADR-0001: Uso de Ollama para LLMs Locales

## Estado
Aceptado

## Contexto
Necesitamos una forma de ejecutar modelos de lenguaje potentes (Mistral, Llama) localmente en la máquina del usuario para garantizar la privacidad y eliminar la dependencia de APIs externas costosas.

## Decisión
Utilizaremos **Ollama** como el motor de inferencia local. Ollama proporciona una API sencilla, gestión eficiente de modelos y soporte para una amplia variedad de arquitecturas de LLM.

## Consecuencias
- **Positivas**: Facilidad de instalación para el usuario, alto rendimiento en hardware local, API compatible con JSON.
- **Negativas**: El usuario debe tener Ollama instalado y espacio en disco para los modelos (~4GB+).
