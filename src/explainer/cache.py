import json
import hashlib
import os
from typing import Optional, Dict, Any

class ExplanationCache:
    def __init__(self, cache_dir: str = ".explainer_cache"):
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _get_hash(self, code: str, model: str) -> str:
        """Genera un hash único para el código y el modelo."""
        content = f"{code}:{model}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, code: str, model: str) -> Optional[str]:
        """Recupera una explicación del caché si existe."""
        cache_key = self._get_hash(code, model)
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_path):
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("explanation")
        return None

    def set(self, code: str, model: str, explanation: str):
        """Guarda una explicación en el caché."""
        cache_key = self._get_hash(code, model)
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump({
                "explanation": explanation,
                "model": model,
                "timestamp": os.path.getmtime(cache_path) if os.path.exists(cache_path) else 0 # Simple timestamp
            }, f, indent=4)
