import ollama
from typing import Dict, Any, Optional


class LLMHandler:
    def __init__(self, model: str = "mistral"):
        self.model = model

    def generate_explanation(self, code: str, context: Dict[str, Any]) -> str:
        """Genera una explicación del código usando el modelo local de Ollama."""
        prompt = self._build_prompt(code, context)

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto ingeniero de software que explica código de forma clara y técnica.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            return response["message"]["content"]
        except Exception as e:
            return f"Error al generar la explicación con Ollama: {str(e)}"

    def _build_prompt(self, code: str, context: Dict[str, Any]) -> str:
        """Construye un prompt detallado para el LLM."""
        file_name = context.get("file_name", "archivo desconocido")
        language = context.get("language", "desconocido")

        prompt = f"""Analiza el siguiente código fuente del archivo '{file_name}' ({language}):

```
{code}
```

Estructura detectada:
- Funciones: {', '.join([f['name'] for f in context.get('functions', [])]) or 'Ninguna'}
- Clases: {', '.join([c['name'] for c in context.get('classes', [])]) or 'Ninguna'}

Por favor, proporciona:
1. Un resumen del propósito del código.
2. Un análisis de la lógica principal.
3. Sugerencias de mejora (rendimiento, legibilidad, seguridad).
"""
        return prompt

    def check_model_availability(self) -> bool:
        """Verifica si el modelo está disponible localmente."""
        try:
            models = ollama.list()
            return any(m["name"].startswith(self.model) for m in models["models"])
        except Exception:
            return False
