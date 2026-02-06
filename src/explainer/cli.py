import typer
from typing import Optional
from explainer.explainer import CodeExplainer
from explainer.formatters import OutputFormatter
import os

app = typer.Typer(help="Local Code Explainer - Explica tu código localmente con privacidad.")

@app.command()
def explain(
    path: str = typer.Argument(..., help="Ruta al archivo de código a explicar."),
    model: str = typer.Option("mistral", "--model", "-m", help="Modelo de Ollama a usar."),
    format: str = typer.Option("cli", "--format", "-f", help="Formato de salida (cli, json)."),
    no_cache: bool = typer.Option(False, "--no-cache", help="Desactivar el uso de caché."),
):
    """Explica un archivo de código usando un LLM local."""
    if not os.path.exists(path):
        typer.echo(f"Error: El archivo '{path}' no existe.", err=True)
        raise typer.Exit(code=1)

    explainer = CodeExplainer(model=model, use_cache=not no_cache)
    formatter = OutputFormatter()

    with typer.progressbar(length=100, label="Analizando y generando explicación...") as progress:
        # Simulamos progreso para feedback visual
        result = explainer.explain(path)
        progress.update(100)

    if format == "json":
        print(formatter.to_json(result))
    else:
        formatter.to_cli(result)

@app.command()
def web():
    """Inicia la interfaz web (Gradio)."""
    typer.echo("Iniciando interfaz web...")
    from web.app import launch_web
    launch_web()

@app.command()
def server():
    """Inicia el servidor API (FastAPI)."""
    typer.echo("Iniciando servidor API...")
    import uvicorn
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    app()
