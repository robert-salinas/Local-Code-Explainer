# ADR-0002: Enfoque Privacy-First

## Estado
Aceptado

## Contexto
El código fuente es uno de los activos más valiosos de una empresa o desarrollador. Muchos usuarios son reacios a enviar su código a servicios de terceros (OpenAI, Anthropic) por razones de seguridad y cumplimiento.

## Decisión
El sistema se diseñará para ser **completamente offline**. No se realizarán llamadas a red externa durante el proceso de explicación. Todos los datos, incluyendo el caché y los metadatos de análisis, permanecerán en la máquina del usuario.

## Consecuencias
- **Positivas**: Confianza total del usuario, cumplimiento de normativas de seguridad de datos, funcionamiento sin conexión a internet.
- **Negativas**: Limitado por el hardware del usuario (CPU/GPU).
