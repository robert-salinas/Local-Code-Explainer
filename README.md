# 🚀 Local Code Explainer (LCE)
> **Tu código, tu privacidad, tu claridad técnica.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](pyproject.toml)
[![Tests](https://github.com/robert-salinas/Local-Code-Explainer/actions/workflows/tests.yml/badge.svg)](https://github.com/robert-salinas/Local-Code-Explainer/actions)

LCE es una herramienta de ingeniería diseñada para analizar y explicar código fuente de manera **100% local**. Resuelve el problema de la dependencia de APIs externas y la exposición de propiedad intelectual, proporcionando claridad técnica instantánea mediante LLMs locales.

---

## ✨ Características (Diferenciadores)

*   🔒 **Privacy First**: Todo el procesamiento ocurre en tu máquina. Sin APIs externas, sin telemetría, sin enviar tu código a la nube.
*   🧠 **Análisis Inteligente**: Utiliza AST (Abstract Syntax Tree) para entender la estructura real del código (clases, funciones, dependencias), no solo texto plano.
*   ⚡ **Caché de Alto Rendimiento**: Sistema de persistencia local basado en hashing para evitar regenerar explicaciones de archivos que no han cambiado.
*   🛠️ **Ecosistema Multi-Interfaz**: CLI potente, API REST (FastAPI) y Web UI (Gradio).
*   🌐 **Soporte Políglota**: Análisis profundo para Python y motor genérico para múltiples lenguajes.

---

## �️ Stack Tecnológico

*   **Backend**: Python 3.11+
*   **LLM Local**: [Ollama](https://ollama.ai/) (Mistral/Llama2)
*   **CLI**: Typer & Rich
*   **API**: FastAPI
*   **Web UI**: Gradio
*   **Análisis**: AST (Abstract Syntax Tree)

---

## 🚀 Instalación Rápida (< 5 min)

```bash
# 1. Instalar Ollama y descargar modelo
ollama pull mistral

# 2. Clonar el repositorio
git clone https://github.com/robert-salinas/Local-Code-Explainer.git
cd Local-Code-Explainer

# 3. Instalar dependencias
pip install -e .
```

---

## � Uso Básico

```bash
# Explicar un archivo por CLI
explain-code explain src/explainer/code_parser.py

# Iniciar interfaz Web
explain-code web

# Levantar servidor API
explain-code server
```

---

## 📝 Documentación y Decisiones

*   🏛️ [Arquitectura](docs/ARCHITECTURE.md)
*   📝 [ADRs (Architecture Decision Records)](docs/ADR/)
*   💡 [Ejemplos de Uso](docs/EXAMPLES.md)
*   🔧 [Solución de Problemas](docs/TROUBLESHOOTING.md)

---

## 🤝 Contribución y Conducta

¡Las contribuciones son bienvenidas! Por favor, revisa nuestra [Guía de Contribución](CONTRIBUTING.md) y nuestro [Código de Conducta](CODE_OF_CONDUCT.md).

---

**Licencia**: [MIT](LICENSE)  
Desarrollado con ❤️ por [Robert Salinas](https://github.com/robert-salinas)

