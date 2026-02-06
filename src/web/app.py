import gradio as gr
import os
from explainer.explainer import CodeExplainer


#
def explain_code_web(file_path, model):
    if not file_path or not os.path.exists(file_path):
        return "Error: Por favor proporciona una ruta de archivo válida.", {}

    try:
        explainer = CodeExplainer(model=model)
        result = explainer.explain(file_path)

        analysis = result["analysis"]
        explanation = result["explanation"]

        # Formatear el análisis para mostrarlo
        analysis_str = f"""
        **Archivo:** {analysis['file_name']}
        **Lenguaje:** {analysis['language']}
        **Líneas:** {analysis['total_lines']}
        **Funciones:** {len(analysis.get('functions', []))}
        **Clases:** {len(analysis.get('classes', []))}
        """

        return explanation, analysis_str
    except Exception as e:
        return f"Error: {str(e)}", ""


def launch_web():
    with gr.Blocks(title="Local Code Explainer") as demo:
        gr.Markdown("# 🚀 Local Code Explainer")
        gr.Markdown("Explica tu código localmente usando LLMs (Ollama).")

        with gr.Row():
            with gr.Column():
                file_input = gr.Textbox(
                    label="Ruta del archivo", placeholder="C:/ruta/a/tu/codigo.py"
                )
                model_dropdown = gr.Dropdown(
                    choices=["mistral", "llama2", "codellama"],
                    value="mistral",
                    label="Modelo Ollama",
                )
                submit_btn = gr.Button("Explicar Código", variant="primary")

            with gr.Column():
                analysis_output = gr.Markdown(label="Análisis Estructural")
                explanation_output = gr.Markdown(label="Explicación IA")

        submit_btn.click(
            fn=explain_code_web,
            inputs=[file_input, model_dropdown],
            outputs=[explanation_output, analysis_output],
        )

    demo.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    launch_web()
