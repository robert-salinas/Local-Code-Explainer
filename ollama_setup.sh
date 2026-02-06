#!/bin/bash

echo "🚀 Configurando Ollama para Local Code Explainer..."

# Verificar si ollama está instalado
if ! command -v ollama &> /dev/null
then
    echo "❌ Ollama no está instalado. Por favor, instálalo desde https://ollama.ai"
    exit
fi

# Descargar modelo por defecto
echo "📥 Descargando modelo Mistral (esto puede tardar unos minutos)..."
ollama pull mistral

echo "✅ ¡Configuración completada! Ya puedes usar explain-code."
