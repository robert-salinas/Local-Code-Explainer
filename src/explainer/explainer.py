from explainer.code_parser import CodeParser
from explainer.llm_handler import LLMHandler
from explainer.cache import ExplanationCache
from typing import Dict, Any


class CodeExplainer:
    """Clase principal que orquestra el análisis AST y la generación de explicaciones vía LLM."""

    def __init__(self, model: str = "mistral", use_cache: bool = True) -> None:
        """
        Inicializa el explicador de código.

        Args:
            model: Nombre del modelo de Ollama a utilizar.
            use_cache: Si se debe utilizar el sistema de caché local.
        """
        self.parser = CodeParser()
        self.llm = LLMHandler(model=model)
        self.cache = ExplanationCache() if use_cache else None
        self.model = model

    def explain(self, file_path: str) -> Dict[str, Any]:
        """
        Analiza un archivo de código y genera una explicación técnica detallada.

        Args:
            file_path: Ruta absoluta o relativa al archivo a analizar.

        Returns:
            Dict con el análisis estructural, la explicación del LLM y metadatos de caché.
        """
        # 1. Parsear el código
        analysis = self.parser.parse_file(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 2. Verificar caché
        if self.cache:
            cached_explanation = self.cache.get(content, self.model)
            if cached_explanation:
                return {
                    "analysis": analysis,
                    "explanation": cached_explanation,
                    "cached": True,
                }

        # 3. Generar nueva explicación
        explanation = self.llm.generate_explanation(content, analysis)

        # 4. Guardar en caché
        if self.cache:
            self.cache.set(content, self.model, explanation)

        return {"analysis": analysis, "explanation": explanation, "cached": False}
