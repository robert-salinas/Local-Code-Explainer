# ADR-0003: Estrategia de Caché

## Estado
Aceptado

## Contexto
La inferencia de LLMs locales puede ser lenta (entre 5 y 30 segundos dependiendo del hardware). Los desarrolladores suelen consultar el mismo código repetidamente.

## Decisión
Implementar un sistema de **caché basado en archivos** utilizando hashes SHA-256 del contenido del código. Si el código no ha cambiado, se servirá la explicación almacenada instantáneamente.

## Consecuencias
- **Positivas**: Respuesta instantánea para consultas repetidas, menor consumo de recursos.
- **Negativas**: Necesidad de gestionar la invalidación del caché (aunque el hashing lo soluciona de forma inherente).
