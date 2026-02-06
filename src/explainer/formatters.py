from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
import json
from typing import Dict, Any


class OutputFormatter:
    def __init__(self):
        self.console = Console()

    def to_cli(self, result: Dict[str, Any]):
        """Formatea el resultado para la terminal usando Rich."""
        analysis = result["analysis"]
        explanation = result["explanation"]
        is_cached = result.get("cached", False)

        # Encabezado
        self.console.print(
            f"\n[bold blue]📄 Archivo:[/bold blue] {analysis['file_name']}"
        )
        if is_cached:
            self.console.print("[italic yellow](Obtenido del caché)[/italic yellow]")

        # Tabla de análisis
        table = Table(title="🔍 Análisis Estructural")
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", style="magenta")

        table.add_row("Lenguaje", analysis["language"])
        table.add_row("Líneas totales", str(analysis["total_lines"]))
        table.add_row("Funciones", str(len(analysis.get("functions", []))))
        table.add_row("Clases", str(len(analysis.get("classes", []))))

        self.console.print(table)

        # Explicación IA
        self.console.print("\n[bold green]💡 Explicación IA:[/bold green]")
        self.console.print(Panel(Markdown(explanation), border_style="green"))

    def to_json(self, result: Dict[str, Any]) -> str:
        """Devuelve el resultado en formato JSON."""
        return json.dumps(result, indent=4)
