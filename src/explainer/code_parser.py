import ast
import os
from typing import Dict, List, Any


class CodeParser:
    def __init__(self):
        pass

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Analiza un archivo de código y devuelve su estructura."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no existe.")

        extension = os.path.splitext(file_path)[1].lower()

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if extension == ".py":
            return self._parse_python(content, file_path)
        else:
            return self._parse_generic(content, file_path)

    def _parse_python(self, content: str, file_path: str) -> Dict[str, Any]:
        """Análisis específico para Python usando AST."""
        try:
            tree = ast.parse(content)

            stats = {
                "file_name": os.path.basename(file_path),
                "language": "python",
                "total_lines": len(content.splitlines()),
                "functions": [],
                "classes": [],
                "imports": [],
            }

            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    stats["functions"].append(
                        {
                            "name": node.name,
                            "line_start": node.lineno,
                            "line_end": getattr(node, "end_lineno", node.lineno),
                            "args": [arg.arg for arg in node.args.args],
                        }
                    )
                elif isinstance(node, ast.ClassDef):
                    stats["classes"].append(
                        {
                            "name": node.name,
                            "line_start": node.lineno,
                            "line_end": getattr(node, "end_lineno", node.lineno),
                            "methods": [
                                n.name
                                for n in node.body
                                if isinstance(n, ast.FunctionDef)
                            ],
                        }
                    )
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for n in node.names:
                            stats["imports"].append(n.name)
                    else:
                        stats["imports"].append(node.module)

            return stats
        except SyntaxError:
            return self._parse_generic(content, file_path)

    def _parse_generic(self, content: str, file_path: str) -> Dict[str, Any]:
        """Análisis genérico para otros lenguajes."""
        lines = content.splitlines()
        return {
            "file_name": os.path.basename(file_path),
            "language": "generic",
            "total_lines": len(lines),
            "content_preview": content[:500] + "..." if len(content) > 500 else content,
        }
