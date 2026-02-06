# Guía de Instalación

## Paso 1: Instalar Ollama
Visita [ollama.ai](https://ollama.ai) y descarga la versión para tu sistema operativo.

Una vez instalado, abre una terminal y descarga el modelo recomendado:
```bash
ollama pull mistral
```

## Paso 2: Clonar el Repositorio
```bash
git clone https://github.com/robertesteban/Local-Code-Explainer.git
cd Local-Code-Explainer
```

## Paso 3: Crear Entorno Virtual (Recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

## Paso 4: Instalar Dependencias
```bash
pip install -e .
```

## Paso 5: Verificar Instalación
```bash
explain-code --help
```
