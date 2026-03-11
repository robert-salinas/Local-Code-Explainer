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

### 🛡️ Auditoría de Calidad y Seguridad
El sistema evalúa automáticamente la "Salud del Código" (0-100 pts) detectando:
- **Funciones Monolíticas**: Alertas para funciones de >30 líneas.
- **Deuda Técnica**: Detección de falta de documentación (Docstrings).
- **Riesgos de Seguridad**: Escaneo proactivo de credenciales (`api_key`, `password`) hardcodeadas.

### � Reportes Profesionales
- **Exportación TXT**: Genera reportes detallados con un solo clic, incluyendo jerarquía de clases, métricas y alertas de seguridad.
- **Formato Estandarizado**: Encabezados ASCII, fecha de generación y firma del autor, listos para adjuntar a documentación técnica.

---

## 🛠️ Stack Tecnológico

*   **GUI**: Python + CustomTkinter
*   **Análisis**: `ast` (Python) + `re` (Universal)
*   **Configuración**: JSON Persistente
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

## � Capturas de Funcionalidad

1.  **Analizar Código**: Pega tu código, selecciona el lenguaje y pulsa `🚀 ANALIZAR CÓDIGO`.
2.  **Revisar KPIs**: Observa la puntuación de salud y las métricas en la barra superior.
3.  **Explorar Resultados**: Navega por los acordeones de *Jerarquía*, *Calidad* y *Seguridad*.
4.  **Exportar**: Guarda el análisis completo para tus registros.

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor, revisa nuestra [Guía de Contribución](CONTRIBUTING.md) y nuestro [Código de Conducta](CODE_OF_CONDUCT.md).

---

**Licencia**: [MIT](LICENSE)  
Desarrollado con ❤️ por [Robert Salinas](https://github.com/robert-salinas) | **RS Digital**
