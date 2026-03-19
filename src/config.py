import os
import json
from typing import Dict, Any

CONFIG_FILE = "config.json"
RULES_FILE = "rs_rules.json"

class AppConfig:
    def __init__(self):
        self.config_data: Dict[str, Any] = {
            "gemini_api_key": "",
            "enable_ai": False,
            "theme": "dark",
            "author_name": "Robert Salinas",
            "font_size": 12,
            "accent_color": "#FF7A3D",
            "export_path": os.getcwd(),
            "auto_open_report": True,
            "ignored_patterns": "__pycache__, .DS_Store, .venv, *.log, node_modules",
            "strict_mode": False
        }
        self.rules_data: Dict[str, Any] = {
            "max_function_lines": 30,
            "penalty_long_function": 5,
            "require_docstrings": True,
            "penalty_missing_docstring": 2,
            "banned_keywords": ["password", "api_key", "secret_key"],
            "penalty_banned_keyword": 20
        }
        self.load_config()
        self.load_rules()

    def load_config(self) -> None:
        """Carga la configuración desde el archivo JSON si existe."""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.config_data.update(data)
            except Exception as e:
                print(f"Error al cargar la configuración: {e}")

    def load_rules(self) -> None:
        """Carga las reglas de auditoría dinámicas."""
        if os.path.exists(RULES_FILE):
            try:
                with open(RULES_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.rules_data.update(data)
            except Exception as e:
                print(f"Error al cargar reglas: {e}")
        else:
            self.save_rules()

    def save_config(self) -> None:
        """Guarda la configuración actual en el archivo JSON."""
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config_data, f, indent=4)
        except Exception as e:
            print(f"Error al guardar la configuración: {e}")

    def save_rules(self) -> None:
        try:
            with open(RULES_FILE, "w", encoding="utf-8") as f:
                json.dump(self.rules_data, f, indent=4)
        except Exception as e:
            print(f"Error guardando reglas: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        return self.config_data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.config_data[key] = value
        self.save_config()

    def get_rule(self, key: str, default: Any = None) -> Any:
        return self.rules_data.get(key, default)

    def set_rule(self, key: str, value: Any) -> None:
        self.rules_data[key] = value
        self.save_rules()
