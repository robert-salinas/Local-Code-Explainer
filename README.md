# 🍊 RS | Local Code Explainer (LCE)
> **Auditoría de código profesional, 100% local y segura.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](pyproject.toml)
[![Status: Stable](https://img.shields.io/badge/Status-Stable-success.svg)]()

**RS Local Code Explainer** es una suite de escritorio nativa diseñada para auditar, analizar y documentar código fuente sin enviar un solo byte a la nube. Combina la potencia del análisis estático (AST/Regex) con una interfaz moderna en **Dark Mode** optimizada para desarrolladores.

---

## ✨ Características Principales

### �️ Interfaz de Escritorio (RS Design System)
- **Modo Oscuro Nativo**: Interfaz gráfica moderna construida con `customtkinter`, con acentos en **RS Orange**.
- **Layout de Auditoría**: Paneles divididos para código y resultados, optimizados para lectura rápida.
- **Dashboard de KPIs**: Métricas clave (Líneas, Funciones, Avisos) en tiempo real.

### 🌍 Soporte Multilenguaje Universal
Gracias a nuestro nuevo motor `UniversalAnalyzer`, LCE soporta análisis estructural para:
- 🐍 **Python** (AST Avanzado)
- 📜 **JavaScript / TypeScript** (Regex Engine)
- ☕ **Java**
- 🚀 **C++**

### 🛡️ Auditoría de Calidad y Seguridad (Motor de Reglas)
El sistema evalúa automáticamente la "Salud del Código" (0-100 pts) basándose en reglas configurables (`rs_rules.json`):
- **Funciones Monolíticas**: Alertas personalizables para funciones que exceden el límite de líneas.
- **Deuda Técnica**: Detección de falta de documentación (Docstrings) en Python usando análisis AST.
- **Riesgos de Seguridad**: Escaneo proactivo de palabras prohibidas (`api_key`, `password`, `secret`).

### 📂 Análisis por Lotes (Carpetas)
- **Análisis Recursivo**: Procesa directorios enteros excluyendo automáticamente `.git`, `venv` y patrones configurados en ignorados.
- **Score Global**: Genera métricas consolidadas para proyectos completos en cuestión de segundos.

### 📊 Visualización de Datos (Analytics)
- **Gráficos Integrados**: Visualiza la salud de tu código mediante gráficos circulares embebidos (`matplotlib`) en tiempo real.

### 📜 Reportes Profesionales HTML
- **Exportación HTML**: Genera reportes estéticos en formato Web con RS Design, listos para adjuntar a auditorías técnicas formales.

---

## 🛠️ Stack Tecnológico

*   **GUI**: Python + CustomTkinter
*   **Análisis**: `ast` (Python) + `re` (Universal)
*   **IA Local**: Ollama API (localhost:11434)
*   **Gráficos**: Matplotlib
*   **Configuración**: JSON Dinámico (`rs_rules.json`)
*   **Packaging**: Scripts nativos (.bat / .ps1)

---

## 🚀 Instalación y Uso

### Prerrequisitos
- Python 3.11 o superior instalado.

### Instalación Rápida
1.  **Clonar el repositorio**:
    ```bash
    git clone https://github.com/robert-salinas/Local-Code-Explainer.git
    cd Local-Code-Explainer
    ```

2.  **Iniciar la Aplicación (Windows)**:
    Simplemente ejecuta el script de lanzamiento. Se encargará de crear el entorno virtual e instalar dependencias automáticamente.
    ```cmd
    run_app.bat
    ```

3.  **Acceso Directo**:
    El script generará un acceso directo `RS-LCE-Desktop` en tu escritorio con el icono oficial.

---

## 🤖 Integración con IA Local (Ollama)

Para habilitar el botón **`🧠 IA EXPLICACIÓN`**, debes tener Ollama corriendo en tu PC:

1.  **Descargar Ollama**: Consíguelo en [ollama.com](https://ollama.com).
2.  **Descargar Modelo**: Abre tu CMD o PowerShell y escribe:
    ```bash
    ollama pull llama3
    ```
3.  **Iniciar**: Asegúrate de que Ollama esté en ejecución (aparece un icono de llama junto al reloj de Windows). La aplicación se conectará automáticamente.

---

## 📸 Capturas de Funcionalidad

1.  **Analizar Código**: Pega tu código, selecciona el lenguaje y pulsa `🚀 ANALIZAR CÓDIGO`.
2.  **Analizar Carpeta**: Pulsa `📂 ANALIZAR CARPETA` para escanear un repositorio completo.
3.  **IA Explicación**: Obtén consejos de optimización y lógica usando el motor local Ollama.
4.  **Revisar KPIs y Gráficos**: Observa las puntuaciones en el gráfico dinámico de Matplotlib.
5.  **Exportar**: Guarda un reporte HTML con RS Design para tus registros.

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor, revisa nuestra [Guía de Contribución](CONTRIBUTING.md) y nuestro [Código de Conducta](CODE_OF_CONDUCT.md).

---

**Licencia**: [MIT](LICENSE)  
Desarrollado con ❤️ por [Robert Salinas](https://github.com/robert-salinas) | **RS Digital**
