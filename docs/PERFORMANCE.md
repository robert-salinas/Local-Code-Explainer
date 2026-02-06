# Benchmarks de Rendimiento

Local Code Explainer depende fuertemente del hardware local para la velocidad de inferencia.

## Tiempos Estimados (Modelo Mistral-7B)

| Hardware | Tiempo Análisis | Tiempo Inferencia | Total |
|----------|-----------------|-------------------|-------|
| CPU (i7 12th Gen) | < 1s | 20-30s | ~31s |
| GPU (RTX 3060) | < 1s | 3-5s | ~6s |
| Apple M2 (8GB) | < 1s | 8-12s | ~13s |

## Optimizaciones
- El **Análisis AST** es instantáneo independientemente del hardware.
- El **Caché** reduce el tiempo total a **< 0.1s** para archivos previamente analizados.
