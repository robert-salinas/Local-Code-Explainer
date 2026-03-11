import customtkinter as ctk
import ast
import os
from config import AppConfig
from explainer.code_parser import CodeParser

# Configuración del Tema RS (Dark + Naranja)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")  # Base oscura

class RSLocalCodeExplainerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.config = AppConfig()
        self.parser = CodeParser()
        self.last_analysis = ""  # Store analysis for exportw
        
        # Colores RS
        self.rs_orange = self.config.get("accent_color", "#FF7A3D")
        self.rs_dark_primary = "#2D3142"
        self.rs_dark_secondary = "#1A1F2E"
        self.rs_text_white = "#FFFFFF"

        # Configuración de la Ventana Principal
        self.title("RS | Local Code Explainer")
        self.geometry("1100x800")
        self.configure(fg_color=self.rs_dark_secondary)
        
        # Layout Grid Compacto
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0) # KPIs
        self.grid_rowconfigure(1, weight=1) # Paneles
        self.grid_rowconfigure(2, weight=0) # Botón
        self.grid_rowconfigure(3, weight=0) # Footer

        self._create_kpi_bar()
        self._create_panels()
        self._create_action_bar()
        self._create_footer()

    def _create_kpi_bar(self):
        self.kpi_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.kpi_frame.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 5), sticky="ew")
        self.kpi_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # KPIs
        self.kpi_lines = self._create_kpi_card(self.kpi_frame, "LÍNEAS", "0", 0)
        self.kpi_funcs = self._create_kpi_card(self.kpi_frame, "FUNCIONES", "0", 1)
        self.kpi_warns = self._create_kpi_card(self.kpi_frame, "AVISOS", "0", 2)

    def _create_kpi_card(self, parent, title, value, col):
        card = ctk.CTkFrame(parent, fg_color=self.rs_dark_primary, corner_radius=8)
        card.grid(row=0, column=col, padx=5, sticky="ew")
        
        val_label = ctk.CTkLabel(card, text=value, font=("Roboto", 24, "bold"), text_color=self.rs_orange)
        val_label.pack(pady=(5, 0))
        
        title_label = ctk.CTkLabel(card, text=title, font=("Roboto", 10), text_color="#9CA3AF")
        title_label.pack(pady=(0, 5))
        
        return val_label

    def _create_panels(self):
        # Panel Izquierdo
        self.left_frame = ctk.CTkFrame(self, fg_color=self.rs_dark_primary, corner_radius=10)
        self.left_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        # Header Compacto Izquierda
        header_frame_l = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        header_frame_l.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(header_frame_l, text="💻 CÓDIGO", font=("Roboto", 12, "bold"), text_color=self.rs_orange).pack(side="left")
        
        self.lang_selector = ctk.CTkOptionMenu(
            header_frame_l, values=["Python", "JavaScript", "Java", "C++"], 
            width=100, height=20, font=("Roboto", 10),
            fg_color=self.rs_dark_secondary, button_color=self.rs_orange,
            command=self.on_lang_change
        )
        self.lang_selector.pack(side="right")

        self.code_input = ctk.CTkTextbox(
            self.left_frame, font=("Consolas", 12), fg_color=self.rs_dark_secondary,
            text_color="#E0E0E0", border_width=0, corner_radius=6
        )
        self.code_input.pack(expand=True, fill="both", padx=5, pady=5)
        self.code_input.bind("<KeyRelease>", self.highlight_syntax)

        # Panel Derecho (Acordeones)
        self.right_frame = ctk.CTkScrollableFrame(self, fg_color=self.rs_dark_primary, corner_radius=10, label_text="📊 ANÁLISIS TÉCNICO")
        self.right_frame.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        self.right_frame._label.configure(font=("Roboto", 12, "bold"), text_color=self.rs_orange)
        
        # 1. Jerarquía
        self.acc_hierarchy = self._create_accordion_section(self.right_frame, "🌳 Jerarquía del Código")
        self.text_hierarchy = self._create_output_text(self.acc_hierarchy)
        
        # 2. Calidad
        self.acc_quality = self._create_accordion_section(self.right_frame, "⚠ Avisos de Calidad")
        self.text_quality = self._create_output_text(self.acc_quality)
        
        # 3. Seguridad
        self.acc_security = self._create_accordion_section(self.right_frame, "🔒 Seguridad Básica")
        self.text_security = self._create_output_text(self.acc_security)

    def _create_accordion_section(self, parent, title):
        frame = ctk.CTkFrame(parent, fg_color=self.rs_dark_secondary, corner_radius=6)
        frame.pack(fill="x", padx=5, pady=5)
        
        label = ctk.CTkLabel(frame, text=title, font=("Roboto", 12, "bold"), text_color="#FFFFFF")
        label.pack(anchor="w", padx=10, pady=(5, 0))
        
        return frame

    def _create_output_text(self, parent):
        textbox = ctk.CTkTextbox(
            parent, font=("Roboto", 11), fg_color="transparent",
            text_color="#CCCCCC", height=150, state="disabled"
        )
        textbox.pack(fill="both", padx=5, pady=5)
        
        # Tags para interactividad
        textbox.tag_config("highlight", background=self.rs_orange, foreground="white")
        textbox.bind("<Button-1>", lambda event: self._on_text_click(event, textbox))
        
        return textbox

    def _on_text_click(self, event, widget):
        """Maneja clics en el texto para resaltar líneas en el código (simulado)."""
        # index = widget.index(f"@{event.x},{event.y}")
        # line_info = widget.get(index + " linestart", index + " lineend")
        pass # Placeholder para interactividad avanzada

    def _create_action_bar(self):
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        action_frame.grid_columnconfigure(0, weight=3)
        action_frame.grid_columnconfigure(1, weight=1)

        self.analyze_btn = ctk.CTkButton(
            action_frame, text="🚀 ANALIZAR CÓDIGO", font=("Roboto", 14, "bold"),
            fg_color=self.rs_orange, hover_color="#E86A2A", text_color="#FFFFFF",
            height=40, corner_radius=8, command=self.analyze_code_action
        )
        self.analyze_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.export_btn = ctk.CTkButton(
            action_frame, text="💾 EXPORTAR REPORTE", font=("Roboto", 12, "bold"),
            fg_color="#4B5563", hover_color="#374151", text_color="#FFFFFF",
            height=40, corner_radius=8, command=self.export_report_action
        )
        self.export_btn.grid(row=0, column=1, sticky="ew")

    def _create_footer(self):
        author = self.config.get("author_name", "Robert Salinas")
        ctk.CTkLabel(
            self, text=f"RS Digital | {author}", font=("Roboto", 9), text_color="#6B7280"
        ).grid(row=3, column=0, columnspan=2, pady=(0, 5))

    def on_lang_change(self, choice):
        self.highlight_syntax()

    def highlight_syntax(self, event=None):
        """Resaltado de sintaxis básico."""
        self.code_input.tag_remove("keyword", "1.0", "end")
        
        text = self.code_input.get("1.0", "end")
        lang = self.lang_selector.get().lower()
        
        keywords = []
        if lang == "python":
            keywords = ["def", "class", "import", "from", "return", "if", "else", "elif", "for", "while", "try", "except"]
        elif lang in ["javascript", "java", "cpp", "c++"]:
            keywords = ["function", "class", "import", "return", "if", "else", "for", "while", "const", "let", "var", "public", "private"]

        for word in keywords:
            start_idx = "1.0"
            while True:
                start_idx = self.code_input.search(word, start_idx, stopindex="end")
                if not start_idx:
                    break
                
                end_idx = f"{start_idx}+{len(word)}c"
                self.code_input.tag_add("keyword", start_idx, end_idx)
                start_idx = end_idx
        
        self.code_input.tag_config("keyword", foreground=self.rs_orange)

    def analyze_code_action(self):
        code_text = self.code_input.get("1.0", "end-1c")
        if not code_text.strip():
            self._update_output_text(self.text_hierarchy, "⚠️ Ingresa código para analizar.")
            return

        lang = self.lang_selector.get()
        
        try:
            stats = self.parser.parse_text(code_text, lang)
            self.last_analysis = stats
            
            # Puntuación de Salud (Score)
            score = 100
            quality_warnings = []
            
            # 1. Jerarquía
            hierarchy_text = f"📦 Clases Detectadas ({len(stats['classes'])}):\n"
            for cls in stats['classes']:
                hierarchy_text += f"   - {cls['name']}\n"
            
            hierarchy_text += f"\n🔧 Funciones Detectadas ({len(stats['functions'])}):\n"
            for func in stats['functions']:
                hierarchy_text += f"   - {func['name']}\n"
                
            self._update_output_text(self.text_hierarchy, hierarchy_text)
            
            # 2. Calidad & Seguridad
            
            # Seguridad
            security_issues = []
            if "api_key" in code_text.lower() or "password" in code_text.lower():
                security_issues.append("Posibles credenciales expuestas (api_key/password)")
                score -= 10
            
            security_text = "✅ No se detectaron patrones obvios de riesgo."
            if security_issues:
                security_text = "⚠ ALERTAS DE SEGURIDAD:\n" + "\n".join([f"   • {i}" for i in security_issues])
            
            self._update_output_text(self.text_security, security_text)

            # Calidad
            # Penalización por falta de docstrings (simulado para regex, real para python)
            # Penalización por funciones largas (si el parser lo soporta)
            
            quality_text = f"💚 Puntuación de Salud: {score}/100\n\n"
            quality_text += f"📏 Líneas Reales: {stats['total_lines']}\n"
            quality_text += f"💬 Comentarios: {stats.get('comments', 0)}\n"
            
            self._update_output_text(self.text_quality, quality_text)

            # Actualizar KPIs
            self.kpi_lines.configure(text=str(stats['total_lines']))
            self.kpi_funcs.configure(text=str(len(stats['functions'])))
            self.kpi_warns.configure(text=str(100 - score)) # Usamos Score inverso o número de warnings

        except Exception as e:
            self._update_output_text(self.text_hierarchy, f"❌ Error: {str(e)}")

    def _update_output_text(self, widget, text):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def export_report_action(self):
        if not self.last_analysis:
            return
            
        try:
            import datetime
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            filename = "RS_Code_Report.txt"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write("==================================================\n")
                f.write("          RS DIGITAL | REPORTE DE CÓDIGO          \n")
                f.write("==================================================\n")
                f.write(f"Fecha: {now}\n")
                f.write(f"Autor del Reporte: {self.config.get('author_name')}\n")
                f.write("--------------------------------------------------\n\n")
                
                f.write(f"LENGUAJE: {self.last_analysis.get('language').upper()}\n")
                f.write(f"LÍNEAS TOTALES: {self.last_analysis.get('total_lines')}\n")
                f.write(f"FUNCIONES: {len(self.last_analysis.get('functions', []))}\n")
                f.write(f"CLASES: {len(self.last_analysis.get('classes', []))}\n\n")
                
                f.write("--- ESTRUCTURA ---\n")
                if self.last_analysis.get('classes'):
                    f.write("Clases:\n")
                    for c in self.last_analysis['classes']:
                        f.write(f"  - {c['name']}\n")
                else:
                    f.write("Clases: Ninguna\n")
                    
                f.write("\nFunciones:\n")
                for fn in self.last_analysis.get('functions', []):
                    f.write(f"  - {fn['name']}\n")
                    
                f.write("\n==================================================\n")
                f.write("       Fin del Reporte - RS Local Code Explainer  \n")
                f.write("==================================================\n")
            
            os.startfile(filename) 
        except Exception as e:
            print(f"Error exportando: {e}")

if __name__ == "__main__":
    app = RSLocalCodeExplainerApp()
    app.mainloop()
