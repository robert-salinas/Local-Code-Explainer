import gradio as gr
import os
from explainer.explainer import CodeExplainer
from explainer.code_parser import CodeParser
from config import AppConfig

# Instancia de configuración global
config = AppConfig()

def get_parser():
    return CodeParser()

def analyze_code_structure(code_text):
    """Realiza el análisis AST local sin IA."""
    if not code_text.strip():
        return "⚠️ Por favor ingresa código para analizar."
    
    # Usamos un archivo temporal virtual o parseamos directamente si el parser lo permite
    # CodeParser.parse_file espera un path, así que adaptaremos o guardaremos temporalmente
    # Para simplicidad y seguridad, parsearemos el texto simulando ser Python
    
    parser = get_parser()
    
    # Hack: CodeParser._parse_python toma content y file_path. 
    # Podemos llamar directamente a _parse_python si es python
    try:
        # Asumimos Python para este MVP o detectamos
        stats = parser._parse_python(code_text, "input_code.py")
        
        # Formatear salida limpia
        output = f"### 📊 Análisis Estructural\n\n"
        output += f"**Clases Detectadas ({len(stats['classes'])}):**\n"
        for cls in stats['classes']:
            methods = ', '.join(cls['methods']) or 'Ninguno'
            output += f"- `{cls['name']}` (Métodos: {methods})\n"
            
        output += f"\n**Funciones Detectadas ({len(stats['functions'])}):**\n"
        for func in stats['functions']:
            args = ', '.join(func['args']) or 'Ninguno'
            output += f"- `{func['name']}` (Args: {args})\n"
            
        output += f"\n**Métricas:**\n"
        output += f"- Líneas Reales (sin comentarios/vacías): `{stats['total_lines']}`\n"
        output += f"- Importaciones: {len(stats['imports'])}\n"
        
        return output
    except Exception as e:
        return f"❌ Error en análisis: {str(e)}\n Asegúrate de que es código Python válido."

def explain_code_ai(code_text, model, api_key, enable_ai):
    """Genera explicación con IA si está habilitada."""
    if not enable_ai:
        return "🤖 La IA está deshabilitada en la configuración."
    
    if not code_text.strip():
        return "⚠️ Esperando código..."

    # Guardar API Key si cambió
    if api_key != config.get("gemini_api_key"):
        config.set("gemini_api_key", api_key)
        
    try:
        # Aquí normalmente usaríamos la API Key de Gemini si fuera el backend
        # Pero LCE usa Ollama local. Respetamos la arquitectura actual pero
        # preparamos el terreno para Gemini si se implementara.z
        # Guardar en archivo temporal para usar el flujo existente de CodeExplainer
        temp_file = "temp_analysis.py"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(code_text)
            
        explainer = CodeExplainer(model=model)
        result = explainer.explain(temp_file)
        
        # Limpiar
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
        return result["explanation"]
        
    except Exception as e:
        return f"❌ Error de IA: {str(e)}"

def clear_inputs():
    return "", "", ""

def launch_web():
    # Cargar CSS
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    with open(css_path, "r", encoding="utf-8") as f:
        rs_css = f.read()

    with gr.Blocks(title="RS | Local Code Explainer", css=rs_css, theme=gr.themes.Base()) as demo:
        
        # Header / Navbar simulado
        with gr.Row(elem_classes=["rs-navbar"]):
            gr.Markdown("## 🍊 RS | Local Code Explainer")
        
        with gr.Row():
            # Panel Izquierdo: Input
            with gr.Column(scale=1):
                gr.Markdown("### 💻 Código Fuente")
                code_input = gr.Code(
                    label="Pega tu código aquí",
                    language="python",
                    lines=20,
                    elem_classes=["rs-input"]
                )
                
                with gr.Row():
                    clear_btn = gr.Button("🗑️ Limpiar", variant="secondary")
                    analyze_btn = gr.Button("🚀 Analizar", variant="primary", elem_classes=["rs-btn-primary"])

                # Configuración Compacta
                with gr.Accordion("⚙️ Configuración", open=False):
                    gemini_key = gr.Textbox(
                        label="Gemini API Key", 
                        value=config.get("gemini_api_key"),
                        type="password",
                        elem_classes=["rs-input"]
                    )
                    enable_ai_toggle = gr.Checkbox(
                        label="Habilitar Funciones de IA", 
                        value=config.get("enable_ai"),
                        interactive=True
                    )
                    model_selector = gr.Dropdown(
                        choices=["mistral", "llama2", "codellama"], 
                        value="mistral", 
                        label="Modelo Local"
                    )

            # Panel Derecho: Output
            with gr.Column(scale=1):
                gr.Markdown("### 🔍 Resultados")
                with gr.Tabs():
                    with gr.TabItem("📊 Análisis Estructural"):
                        structural_output = gr.Markdown("Esperando análisis...")
                    
                    with gr.TabItem("🤖 Explicación IA"):
                        ai_output = gr.Markdown("La IA está lista para explicar...")

        # Eventos
        analyze_btn.click(
            fn=analyze_code_structure,
            inputs=[code_input],
            outputs=[structural_output]
        ).then(
            fn=explain_code_ai,
            inputs=[code_input, model_selector, gemini_key, enable_ai_toggle],
            outputs=[ai_output]
        )
        
        clear_btn.click(
            fn=clear_inputs,
            inputs=[],
            outputs=[code_input, structural_output, ai_output]
        )
        
        # Guardar config al cambiar toggle
        def update_ai_config(enabled):
            config.set("enable_ai", enabled)
            
        enable_ai_toggle.change(fn=update_ai_config, inputs=[enable_ai_toggle], outputs=[])

    demo.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    launch_web()
