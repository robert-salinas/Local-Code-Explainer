import os
import json
from typing import Dict, Any

CONFIG_FILE = "config.json"

class AppConfig:
    def __init__(self):
        self.config_data: Dict[str, Any] = {
            "gemini_api_key": "",
            "enable_ai": False,
            "theme": "dark",
            "author_name": "Robert Salinas",
            "accent_color": "#FF7A3D"
        }
        self.load_config()

    def load_config(self) -> None:
        """Carga la configuración desde el archivo JSON si existe."""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.config_data.update(data)
            except Exception as e:
                print(f"Error al cargar la configuración: {e}")

    def save_config(self) -> None:
        """Guarda la configuración actual en el archivo JSON."""
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config_data, f, indent=4)
        except Exception as e:
            print(f"Error al guardar la configuración: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        return self.config_data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.config_data[key] = value
        self.save_config()
