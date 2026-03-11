import ast
import os
import re
from typing import Dict, Any, List, TypedDict


class PythonStats(TypedDict):
    file_name: str
    language: str
    total_lines: int
    functions: List[Dict[str, Any]]
    classes: List[Dict[str, Any]]
    imports: List[str]


class UniversalAnalyzer:
    def parse(self, content: str, language: str) -> Dict[str, Any]:
        """Análisis basado en Regex para lenguajes tipo C (JS, Java, C++)."""
        stats = {
            "file_name": "input_code",
            "language": language,
            "total_lines": 0,
            "functions": [],
            "classes": [],
            "comments": 0
        }

        lines = content.splitlines()
        real_lines = 0
        comments = 0
        
        # Regex patrones
        class_pattern = re.compile(r'\bclass\s+(\w+)')
        func_pattern = re.compile(r'\b(?:function\s+(\w+)|(\w+)\s*\(.*\)\s*\{)')
        
        # Ajustes por lenguaje
        if language == "java":
             func_pattern = re.compile(r'\b(?:public|private|protected|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\) *(\{?|[^;])')

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            
            if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
                comments += 1
                continue
                
            real_lines += 1

            # Buscar clases
            class_match = class_pattern.search(line)
            if class_match:
                stats["classes"].append({"name": class_match.group(1)})

            # Buscar funciones
            func_match = func_pattern.search(line)
            if func_match:
                # Group 1 or 2 depending on pattern
                name = func_match.group(1) or func_match.group(2)
                if name and name not in ['if', 'for', 'while', 'switch', 'catch']:
                    stats["functions"].append({"name": name})

        stats["total_lines"] = real_lines
        stats["comments"] = comments
        return stats


class CodeParser:
    def __init__(self):
        self.universal = UniversalAnalyzer()

    def parse_text(self, content: str, language: str) -> Dict[str, Any]:
        """Analiza texto de código directamente según el lenguaje especificado."""
        language = language.lower()
        if language == "python":
            return self._parse_python(content, "input.py")
        elif language in ["javascript", "java", "cpp", "c++"]:
            return self.universal.parse(content, language)
        else:
            return self._parse_generic(content, "input.txt")


    def _parse_python(self, content: str, file_path: str) -> Dict[str, Any]:
        """Análisis específico para Python usando AST."""
        
        try:
            tree = ast.parse(content)
            
            # Calcular líneas de código reales (ignorando comentarios y líneas vacías)
            lines = content.splitlines()
            real_lines = 0
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    real_lines += 1

            stats: PythonStats = {
                "file_name": os.path.basename(file_path),
                "language": "python",
                "total_lines": real_lines,
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
                        if node.module:
                            stats["imports"].append(node.module)

            return dict(stats)
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
