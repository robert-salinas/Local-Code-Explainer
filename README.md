# 🚀 Local Code Explainer (LCE) v0.1.0
**Python Version** | **License: MIT**

LCE es una herramienta de ingeniería diseñada para analizar y explicar código fuente de manera local, asegurando la privacidad absoluta de tu propiedad intelectual y proporcionando claridad técnica instantánea mediante LLMs locales.

---

## ✨ Características

*   🔒 **Privacy First**: Todo el procesamiento ocurre en tu máquina. Sin APIs externas, sin telemetría, sin enviar tu código a la nube.
*   🧠 **Análisis Inteligente**: Utiliza AST (Abstract Syntax Tree) para entender la estructura real del código (clases, funciones, dependencias), no solo texto plano.
*   ⚡ **Caché de Alto Rendimiento**: Sistema de persistencia local basado en hashing para evitar regenerar explicaciones de archivos que no han cambiado.
*   🛠️ **Ecosistema Multi-Interfaz**:
    *   **CLI**: Interfaz potente para terminal.
    *   **API REST**: Basada en FastAPI para integraciones.
    *   **Web UI**: Basada en Gradio para visualización rápida.
*   🌐 **Soporte Políglota**: Análisis profundo para Python y motor genérico para múltiples lenguajes de programación.

---

## 🚀 Instalación Rápida

Para poner en marcha el proyecto en tu entorno local:

```bash
# 1. Instalar Ollama (Prerrequisito)
# Visita https://ollama.ai para descargar e instalar

# 2. Descargar el modelo recomendado
ollama pull mistral

# 3. Clonar el repositorio
git clone https://github.com/robertesteban/Local-Code-Explainer.git
cd Local-Code-Explainer

# 4. Instalar dependencias en modo editable
pip install -e .
```

---

## 🛠️ Uso Básico

Para gestionar y obtener explicaciones de forma eficiente:

### Modo interactivo y CLI
```bash
# Registrar y explicar un archivo (Modo CLI)
explain-code explain src/explainer/code_parser.py

# Iniciar la interfaz Web interactiva
explain-code web

# Levantar el servidor API REST
explain-code server

# Exportar explicación a JSON
explain-code explain src/explainer/code_parser.py --format json > output.json
```

---

## 📝 Estructura de Decisiones (ADR)

LCE mantiene registros estructurados (Architecture Decision Records) que aseguran la trazabilidad y el rigor arquitectónico:

*   **ADR-0001**: [Uso de Ollama para LLMs Locales](docs/ADR/0001-use-ollama-for-local-llms.md) - Justificación del motor de inferencia local.
*   **ADR-0002**: [Enfoque Privacy-First](docs/ADR/0002-privacy-first-approach.md) - Racional detrás del procesamiento 100% offline.
*   **ADR-0003**: [Estrategia de Caché](docs/ADR/0003-caching-strategy.md) - Diseño del sistema de optimización de respuestas.

**Estados Soportados:**
*   `Proposed`: La decisión está en fase de revisión y discusión.
*   `Accepted`: La decisión ha sido aprobada e implementada.
*   `Deprecated`: La decisión ya no es relevante para el estado actual.
*   `Superseded`: La decisión ha sido reemplazada por una más reciente.

---

## 📖 Documentación Adicional

*   🏛️ [Arquitectura y Decisiones de Diseño](docs/ARCHITECTURE.md)
*   🚀 [Guía de Instalación Detallada](docs/INSTALLATION.md)
*   📊 [Benchmarks de Rendimiento](docs/PERFORMANCE.md)
*   🤝 [Guía de Contribución](docs/CONTRIBUTING.md)

---

> Desarrollado con ❤️ para ingenieros que valoran su privacidad y el rigor técnico en cada etapa del desarrollo.
