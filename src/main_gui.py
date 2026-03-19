import customtkinter as ctk
import ast
import os
import threading
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from config import AppConfig
from explainer.code_parser import CodeParser

# Configuración del Tema RS (Dark + Naranja)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")  # Base oscura

class ConfigPanel(ctk.CTkFrame):
    def __init__(self, parent, config: AppConfig, on_close=None):
        super().__init__(parent, fg_color="#1A1F2E")
        self.config = config
        self.on_close = on_close
        
        # Colores RS
        self.rs_orange = "#FF7A3D"
        self.rs_dark_primary = "#2D3142"
        self.rs_text_white = "#FFFFFF"

        self._create_ui()

    def _create_ui(self):
        # Título y Botón de Cierre
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            header_frame, text="Configuración del Sistema", 
            font=("Roboto", 24, "bold"), text_color=self.rs_orange
        ).pack(side="left")

        if self.on_close:
            ctk.CTkButton(
                header_frame, text="✕", width=30, height=30,
                fg_color="transparent", hover_color="#374151",
                text_color="white", font=("Arial", 16),
                command=self.on_close
            ).pack(side="right")

        # Contenedor Scrolleable (Estilo Tarjeta Centrada)
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color=self.rs_dark_primary, corner_radius=15)
        scroll_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))

        # --- SECCIÓN GENERAL ---
        ctk.CTkLabel(scroll_frame, text="General", font=("Roboto", 14, "bold"), text_color=self.rs_text_white).pack(anchor="w", padx=10, pady=(10, 5))
        
        # Autor
        ctk.CTkLabel(scroll_frame, text="Nombre del Autor (Reportes)", font=("Roboto", 12)).pack(anchor="w", padx=20, pady=(5, 0))
        self.author_entry = ctk.CTkEntry(scroll_frame, width=300, fg_color="#1A1F2E", border_color=self.rs_orange)
        self.author_entry.insert(0, self.config.get("author_name", "Robert Salinas"))
        self.author_entry.pack(padx=20, anchor="w", pady=(0, 10))

        # Tamaño de Fuente
        ctk.CTkLabel(scroll_frame, text="Tamaño de Fuente (Editor)", font=("Roboto", 12)).pack(anchor="w", padx=20, pady=(5, 0))
        self.font_size_slider = ctk.CTkSlider(scroll_frame, from_=8, to=24, number_of_steps=16, button_color=self.rs_orange)
        self.font_size_slider.set(self.config.get("font_size", 12))
        self.font_size_slider.pack(padx=20, anchor="w", fill="x", pady=(0, 15))

        # --- SECCIÓN ANÁLISIS ---
        ctk.CTkLabel(scroll_frame, text="Análisis", font=("Roboto", 14, "bold"), text_color=self.rs_text_white).pack(anchor="w", padx=10, pady=(10, 5))

        # Modo Estricto
        self.strict_var = ctk.BooleanVar(value=self.config.get("strict_mode", False))
        ctk.CTkSwitch(
            scroll_frame, text="Modo Estricto (Penalizar más en Salud del Código)", 
            variable=self.strict_var, progress_color=self.rs_orange, button_color="white"
        ).pack(anchor="w", padx=20, pady=(5, 10))

        # Archivos Ignorados
        ctk.CTkLabel(scroll_frame, text="Archivos/Carpetas Ignorados", font=("Roboto", 12)).pack(anchor="w", padx=20, pady=(5, 0))
        self.ignored_entry = ctk.CTkEntry(scroll_frame, width=400, fg_color="#1A1F2E", border_color=self.rs_orange)
        default_ignored = "__pycache__, .DS_Store, .venv, *.log, node_modules"
        self.ignored_entry.insert(0, self.config.get("ignored_patterns", default_ignored))
        self.ignored_entry.pack(padx=20, anchor="w", pady=(0, 15))
        
        # --- SECCIÓN EXPORTACIÓN ---
        ctk.CTkLabel(scroll_frame, text="Exportación", font=("Roboto", 14, "bold"), text_color=self.rs_text_white).pack(anchor="w", padx=10, pady=(10, 5))

        # Ruta
        ctk.CTkLabel(scroll_frame, text="Ruta de Exportación", font=("Roboto", 12)).pack(anchor="w", padx=20, pady=(5, 0))
        path_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        path_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        self.export_path_entry = ctk.CTkEntry(path_frame, width=300, fg_color="#1A1F2E", border_color=self.rs_orange)
        self.export_path_entry.insert(0, self.config.get("export_path", os.getcwd()))
        self.export_path_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        ctk.CTkButton(path_frame, text="📂", width=40, fg_color="#3B82F6", command=self._browse_path).pack(side="left")

        # Auto-abrir
        self.auto_open_var = ctk.CTkCheckBox(
            scroll_frame, text="Abrir reporte automáticamente al finalizar", 
            fg_color=self.rs_orange, hover_color="#E86A2A"
        )
        if self.config.get("auto_open_report", True): self.auto_open_var.select()
        self.auto_open_var.pack(anchor="w", padx=20, pady=(5, 10))

        # --- SECCIÓN REGLAS MOTOR ---
        ctk.CTkLabel(scroll_frame, text="Reglas de Auditoría (⚙️ Motor)", font=("Roboto", 14, "bold"), text_color=self.rs_orange).pack(anchor="w", padx=10, pady=(15, 5))

        # Max Líneas Función
        ctk.CTkLabel(scroll_frame, text="Líneas Máximas por Función (Umbral)", font=("Roboto", 12)).pack(anchor="w", padx=20, pady=(5, 0))
        self.rule_lines_entry = ctk.CTkEntry(scroll_frame, width=100, fg_color="#1A1F2E", border_color=self.rs_orange)
        self.rule_lines_entry.insert(0, str(self.config.get_rule("max_function_lines", 30)))
        self.rule_lines_entry.pack(padx=20, anchor="w", pady=(0, 10))

        # Palabras Prohibidas
        ctk.CTkLabel(scroll_frame, text="Palabras Prohibidas (Seguridad - Coma separated)", font=("Roboto", 12)).pack(anchor="w", padx=20, pady=(5, 0))
        self.rule_banned_entry = ctk.CTkEntry(scroll_frame, width=400, fg_color="#1A1F2E", border_color=self.rs_orange)
        self.rule_banned_entry.insert(0, ", ".join(self.config.get_rule("banned_keywords", [])))
        self.rule_banned_entry.pack(padx=20, anchor="w", pady=(0, 15))

        # Botonera Inferior (Fuera del scroll)
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))

        ctk.CTkButton(
            btn_frame, text="Guardar Cambios", 
            fg_color=self.rs_orange, hover_color="#E86A2A",
            font=("Roboto", 14, "bold"), height=40, width=200,
            command=self._save_config
        ).pack()

    def _browse_path(self):
        directory = ctk.filedialog.askdirectory()
        if directory:
            self.export_path_entry.delete(0, "end")
            self.export_path_entry.insert(0, directory)

    def _save_config(self):
        # Guardar todo
        self.config.set("author_name", self.author_entry.get())
        self.config.set("font_size", int(self.font_size_slider.get()))
        self.config.set("strict_mode", self.strict_var.get())
        self.config.set("ignored_patterns", self.ignored_entry.get())
        self.config.set("export_path", self.export_path_entry.get())
        self.config.set("auto_open_report", bool(self.auto_open_var.get()))
        
        # Guardar Reglas
        try:
            self.config.set_rule("max_function_lines", int(self.rule_lines_entry.get()))
        except ValueError:
            pass
            
        banned_list = [k.strip() for k in self.rule_banned_entry.get().split(",") if k.strip()]
        self.config.set_rule("banned_keywords", banned_list)

        if self.on_close:
            self.on_close()



class RSLocalCodeExplainerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.config = AppConfig()
        self.parser = CodeParser()
        self.last_analysis = ""  # Store analysis for exportw
        
        # Icono (Si existe) y AppID para barra de tareas
        try:
            import ctypes
            myappid = 'rs.localcodeexplainer.app.1.0' # Arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

        icon_path = os.path.join(os.path.dirname(__file__), "web", "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)


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
        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=0) # KPIs
        self.grid_rowconfigure(2, weight=1) # Paneles
        self.grid_rowconfigure(3, weight=0) # Progress Bar
        self.grid_rowconfigure(4, weight=0) # Botones
        self.grid_rowconfigure(5, weight=0) # Footer

        self._create_header()
        self._create_kpi_bar()
        self._create_panels()
        
        # ProgressBar (UX)
        self.progress_bar = ctk.CTkProgressBar(self, height=4, progress_color=self.rs_orange, fg_color="#1A1F2E")
        self.progress_bar.grid(row=3, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="ew")
        self.progress_bar.set(0)

        self._create_action_bar()
        self._create_footer()
        
        # Inicializar panel de configuración (oculto)
        self.config_panel = ConfigPanel(self, self.config, on_close=self.toggle_config)
        self.config_panel.grid(row=0, column=0, columnspan=2, rowspan=5, sticky="nsew")
        self.config_panel.grid_remove()

    def _create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="ew")
        
        # Título y Autor
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left")
        
        ctk.CTkLabel(
            title_frame, text="Local Code Explainer", 
            font=("Roboto", 24, "bold"), text_color=self.rs_orange
        ).pack(anchor="w")
        
        author = self.config.get("author_name", "Robert Salinas")
        self.header_author_label = ctk.CTkLabel(
            title_frame, text=f"by {author}", font=("Roboto", 10), text_color="#9CA3AF"
        )
        self.header_author_label.pack(anchor="w", pady=(0, 0))
        
        # Botón Configuración
        ctk.CTkButton(
            header_frame, text="⚙ Configuración", width=120,
            fg_color="#374151", hover_color="#4B5563",
            command=self.toggle_config
        ).pack(side="right", anchor="n", pady=5)

    def toggle_config(self):
        if self.config_panel.winfo_viewable():
            self.config_panel.grid_remove()
            self.refresh_ui_settings()
        else:
            self.config_panel.grid()
            self.config_panel.lift()

    def refresh_ui_settings(self):
        """Actualiza la interfaz con la nueva configuración."""
        author = self.config.get("author_name", "Robert Salinas")
        
        # Actualizar Header
        if hasattr(self, 'header_author_label'):
            self.header_author_label.configure(text=f"by {author}")

        # Actualizar Footer
        # (Ya no mostramos el autor en el footer, pero si existiera la referencia, la actualizamos o la ocultamos)
        if hasattr(self, 'footer_author_label'):
            self.footer_author_label.pack_forget() # Ocultar si existe
            
        # Actualizar Fuente del Editor
        new_size = self.config.get("font_size", 12)
        self.code_input.configure(font=("Consolas", new_size))



    def _create_kpi_bar(self):
        self.kpi_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.kpi_frame.grid(row=1, column=0, columnspan=2, padx=15, pady=(15, 5), sticky="ew")
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
        self.left_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        
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
            self.left_frame, font=("Consolas", self.config.get("font_size", 12)), fg_color=self.rs_dark_secondary,
            text_color="#E0E0E0", border_width=0, corner_radius=6
        )
        self.code_input.pack(expand=True, fill="both", padx=5, pady=5)
        self.code_input.bind("<KeyRelease>", self.highlight_syntax)

        # Panel Derecho (Acordeones)
        self.right_frame = ctk.CTkScrollableFrame(self, fg_color=self.rs_dark_primary, corner_radius=10, label_text="📊 ANÁLISIS TÉCNICO")
        self.right_frame.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")
        self.right_frame._label.configure(font=("Roboto", 12, "bold"), text_color=self.rs_orange)
        
        # Chart Contenedor
        self.chart_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent", height=150)
        self.chart_frame.pack(fill="x", padx=5, pady=5)
        
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
        action_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        action_frame.grid_columnconfigure((0,1,2,3), weight=1)

        self.analyze_btn = ctk.CTkButton(
            action_frame, text="🚀 ANALIZAR CÓDIGO", font=("Roboto", 14, "bold"),
            fg_color=self.rs_orange, hover_color="#E86A2A", text_color="#FFFFFF",
            height=40, corner_radius=8, command=self.analyze_code_action
        )
        self.analyze_btn.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.analyze_folder_btn = ctk.CTkButton(
            action_frame, text="📂 ANALIZAR CARPETA", font=("Roboto", 14, "bold"),
            fg_color="#3B82F6", hover_color="#2563EB", text_color="#FFFFFF",
            height=40, corner_radius=8, command=self.analyze_folder_action
        )
        self.analyze_folder_btn.grid(row=0, column=1, padx=(0, 5), sticky="ew")

        self.ai_btn = ctk.CTkButton(
            action_frame, text="🧠 IA EXPLICACIÓN", font=("Roboto", 14, "bold"),
            fg_color="#10B981", hover_color="#059669", text_color="#FFFFFF",
            height=40, corner_radius=8, command=self.ai_explain_action
        )
        self.ai_btn.grid(row=0, column=2, padx=(0, 5), sticky="ew")

        self.export_btn = ctk.CTkButton(
            action_frame, text="💾 EXPORTAR REPORTE", font=("Roboto", 12, "bold"),
            fg_color="#4B5563", hover_color="#374151", text_color="#FFFFFF",
            height=40, corner_radius=8, command=self.export_report_action
        )
        self.export_btn.grid(row=0, column=3, sticky="ew")

        # Tooltip/Aviso UX
        ctk.CTkLabel(
            action_frame, text="💡 IA requiere Ollama activo en puerto 11434", 
            font=("Roboto", 10), text_color="#9CA3AF"
        ).grid(row=1, column=2, columnspan=2, sticky="e", padx=10, pady=(2, 0))

    def _create_footer(self):
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=5, column=0, columnspan=2, pady=(0, 10))
        
        ctk.CTkLabel(
            footer_frame, text="", font=("Roboto", 10, "bold"), text_color="#6B7280"
        ).pack()
        
        # El "by author" se movió al header, así que lo quitamos de aquí.

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
        
        # UI Loading states
        self.progress_bar.start()
        self.analyze_btn.configure(text="⏳ ANALIZANDO...", state="disabled")
        self._update_output_text(self.text_hierarchy, "Analizando estructura...")
        self._update_output_text(self.text_quality, "Calculando métricas...")
        self._update_output_text(self.text_security, "Escaneando vulnerabilidades...")

        threading.Thread(target=self._run_analysis_thread, args=(code_text, lang), daemon=True).start()

    def _run_analysis_thread(self, code_text, lang):
        try:
            stats = self.parser.parse_text(code_text, lang)
            self.last_analysis = stats
            
            # Puntuación de Salud (Score)
            score = 100
            quality_warnings = []
            strict_mode = self.config.get("strict_mode", False)
            
            # 1. Jerarquía
            hierarchy_text = f"📦 Clases Detectadas ({len(stats['classes'])}):\n"
            for cls in stats['classes']:
                hierarchy_text += f"   - {cls['name']}\n"
            
            hierarchy_text += f"\n🔧 Funciones Detectadas ({len(stats['functions'])}):\n"
            for func in stats['functions']:
                hierarchy_text += f"   - {func['name']}\n"
            
            # 2. Calidad & Seguridad
            
            # Cargar reglas dinámicas
            max_lines = self.config.get_rule("max_function_lines", 30)
            pen_lines = self.config.get_rule("penalty_long_function", 5)
            req_docs = self.config.get_rule("require_docstrings", True)
            pen_docs = self.config.get_rule("penalty_missing_docstring", 2)
            banned_keywords = self.config.get_rule("banned_keywords", ["password", "api_key", "secret_key"])
            pen_banned = self.config.get_rule("penalty_banned_keyword", 20)
            
            # Seguridad
            security_issues = []
            for kw in banned_keywords:
                if kw in code_text.lower():
                    security_issues.append(f"Palabra prohibida detectada '{kw}'")
                    score -= pen_banned if strict_mode else pen_banned // 2
            
            security_text = "✅ No se detectaron patrones obvios de riesgo."
            if security_issues:
                security_text = "⚠ ALERTAS DE SEGURIDAD:\n" + "\n".join([f"   • {i}" for i in security_issues])

            # Calidad y Funciones largas
            long_funcs = [f for f in stats['functions'] if isinstance(f, dict) and (f.get('line_end', 0) - f.get('line_start', 0)) > max_lines]
            if long_funcs:
                score -= len(long_funcs) * pen_lines
                quality_warnings.append(f"{len(long_funcs)} función(es) > {max_lines} líneas")

            if req_docs and lang.lower() == "python":
                missing_docs = [f for f in stats['functions'] + stats.get('classes', []) if isinstance(f, dict) and not f.get('has_docstring', True)]
                if missing_docs:
                    score -= len(missing_docs) * pen_docs
                    quality_warnings.append(f"{len(missing_docs)} elemento(s) sin docstrings (Python)")
            
            score = max(0, score)
            quality_text = f"💚 Puntuación de Salud: {score}/100\n\n"
            if strict_mode:
                quality_text += "🔴 Modo Estricto Activado\n"
            
            quality_text += f"📏 Líneas Reales: {stats['total_lines']}\n"
            quality_text += f"💬 Comentarios: {stats.get('comments', 0)}\n\n"

            if quality_warnings:
                quality_text += "⚠ ALERTAS DE CALIDAD:\n" + "\n".join([f"   • {w}" for w in quality_warnings])

            # Use after to sync UI updates
            self.after(0, lambda: self._update_ui_post_analysis(stats, score, hierarchy_text, security_text, quality_text))

        except Exception as e:
            self.after(0, lambda e=e: self._handle_analysis_error(str(e)))

    def _update_ui_post_analysis(self, stats, score, hierarchy_text, security_text, quality_text):
        self._update_output_text(self.text_hierarchy, hierarchy_text)
        self._update_output_text(self.text_security, security_text)
        self._update_output_text(self.text_quality, quality_text)

        # Actualizar KPIs
        self.kpi_lines.configure(text=str(stats['total_lines']))
        self.kpi_funcs.configure(text=str(len(stats['functions'])))
        self.kpi_warns.configure(text=str(100 - score)) # Usamos Score inverso o número de warnings
        
        self.progress_bar.stop()
        self.analyze_btn.configure(text="🚀 ANALIZAR CÓDIGO", state="normal")
        self._draw_chart(score)

    def _draw_chart(self, score):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        fig, ax = plt.subplots(figsize=(3, 3), dpi=80)
        fig.patch.set_facecolor('#2D3142')
        
        colors = ['#10B981', '#FF7A3D'] if score >= 70 else ['#FF7A3D', '#EF4444']
        ax.pie([score, max(0, 100-score)], labels=['Salud', 'Deuda'], colors=colors, 
               autopct='%1.1f%%', startangle=90, textprops={'color':"w"})
        ax.set_title("Puntuación de Salud", color="w")
        
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _handle_analysis_error(self, error_msg):
        self._update_output_text(self.text_hierarchy, f"❌ Error: {error_msg}")
        self.progress_bar.stop()
        self.analyze_btn.configure(text="🚀 ANALIZAR CÓDIGO", state="normal")

    def _update_output_text(self, widget, text):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def analyze_folder_action(self):
        folder_path = ctk.filedialog.askdirectory()
        if not folder_path:
            return
            
        self.progress_bar.start()
        self.analyze_btn.configure(state="disabled")
        self.analyze_folder_btn.configure(text="⏳ ANALIZANDO...", state="disabled")
        self._update_output_text(self.text_hierarchy, f"Analizando directorio:\n{folder_path}")
        
        threading.Thread(target=self._run_folder_analysis_thread, args=(folder_path,), daemon=True).start()

    def _run_folder_analysis_thread(self, folder_path):
        try:
            total_files = 0
            total_lines = 0
            total_funcs = 0
            total_classes = 0
            
            ignored = [i.strip() for i in self.config.get("ignored_patterns", "").split(",")]
            
            for root, dirs, files in os.walk(folder_path):
                dirs[:] = [d for d in dirs if not any(ign.replace("*", "") in d for ign in ignored) and "venv" not in d and ".git" not in d]
                
                for file in files:
                    if file.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c')):
                        if any(ign.replace("*", "") in file for ign in ignored):
                            continue
                        
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                content = f.read()
                            
                            ext = file.split('.')[-1]
                            lang_map = {'py': 'python', 'js': 'javascript', 'ts': 'javascript', 'java': 'java', 'cpp': 'cpp', 'c': 'cpp'}
                            lang = lang_map.get(ext, 'generic')
                            
                            stats = self.parser.parse_text(content, lang)
                            total_files += 1
                            total_lines += stats.get('total_lines', 0)
                            total_funcs += len(stats.get('functions', []))
                            total_classes += len(stats.get('classes', []))
                        except:
                            continue
                            
            score = max(0, min(100, int(100 - (total_funcs/max(1, total_files))))) 
            
            sum_text = f"📂 Análisis Lote Completado\nArchivos procesados: {total_files}\n"
            sum_text += f"Líneas totales: {total_lines}\nFunciones detectadas: {total_funcs}\nClases detectadas: {total_classes}\n"
            
            self.after(0, lambda: self._update_ui_post_folder(total_lines, total_funcs, score, sum_text))
            
        except Exception as e:
            self.after(0, lambda e=e: self._handle_analysis_error(str(e)))
            
    def _update_ui_post_folder(self, lines, funcs, score, text):
        self._update_output_text(self.text_hierarchy, text)
        self.kpi_lines.configure(text=str(lines))
        self.kpi_funcs.configure(text=str(funcs))
        self.kpi_warns.configure(text=str(100 - score))
        
        self.progress_bar.stop()
        self.analyze_btn.configure(state="normal")
        self.analyze_folder_btn.configure(text="📂 ANALIZAR CARPETA", state="normal")
        self._draw_chart(score)

    def ai_explain_action(self):
        code_text = self.code_input.get("1.0", "end-1c")
        if not code_text.strip():
            self._update_output_text(self.text_hierarchy, "⚠️ Ingresa código primero.")
            return

        self.progress_bar.start()
        self.ai_btn.configure(text="🧠 PENSANDO...", state="disabled")
        self._update_output_text(self.text_quality, "Contactando LLM local (Ollama)...")
        
        threading.Thread(target=self._run_ai_thread, args=(code_text,), daemon=True).start()

    def _run_ai_thread(self, code_text):
        try:
            model = self.config.get("llm_model", "llama3")
            response = requests.post('http://localhost:11434/api/generate', 
                                     json={
                                         "model": model, 
                                         "prompt": "Explica la funcionalidad del siguiente código y menciona cómo optimizarlo brevemente:\n\n" + code_text, 
                                         "stream": False
                                     }, timeout=60)
            
            if response.status_code == 200:
                explanation = response.json().get('response', 'Sin respuesta.')
            else:
                explanation = f"Error del modelo: HTTP {response.status_code}"
                
            self.after(0, lambda: self._update_ui_post_ai(explanation))
        except Exception as e:
            self.after(0, lambda e=e: self._handle_ai_error(str(e)))
            
    def _update_ui_post_ai(self, explanation):
        self._update_output_text(self.text_quality, f"🧠 IA Explains:\n\n{explanation}")
        self.progress_bar.stop()
        self.ai_btn.configure(text="🧠 IA EXPLICACIÓN", state="normal")

    def _handle_ai_error(self, error):
        self._update_output_text(self.text_quality, f"❌ Error de IA Local (Arranca Ollama en tu PC):\n{error}")
        self.progress_bar.stop()
        self.ai_btn.configure(text="🧠 IA EXPLICACIÓN", state="normal")

    def export_report_action(self):
        if not self.last_analysis:
            return
            
        try:
            import datetime
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            export_dir = self.config.get("export_path", os.getcwd())
            filename = os.path.join(export_dir, "RS_Code_Report.html")
            
            self.export_btn.configure(text="💾 GUARDANDO...", state="disabled")
            
            html_content = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>RS Digital | Code Report</title>
                <style>
                    body {{ font-family: 'Segoe UI', Roboto, sans-serif; background-color: #1A1F2E; color: #FFFFFF; padding: 40px; }}
                    .container {{ max-width: 800px; margin: auto; background-color: #2D3142; padding: 30px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
                    h1 {{ color: #FF7A3D; border-bottom: 2px solid #FF7A3D; padding-bottom: 10px; }}
                    .kpi-row {{ display: flex; justify-content: space-between; margin: 20px 0; }}
                    .kpi-card {{ background: #1A1F2E; padding: 20px; border-radius: 8px; text-align: center; width: 22%; border-top: 3px solid #10B981; }}
                    .kpi-card h2 {{ margin: 0; font-size: 24px; color: #FF7A3D; }}
                    .kpi-card p {{ margin: 5px 0 0; font-size: 12px; color: #9CA3AF; }}
                    h3 {{ color: #10B981; }}
                    ul {{ list-style-type: none; padding: 0; }}
                    li {{ background: #374151; margin: 5px 0; padding: 10px; border-radius: 4px; }}
                    .footer {{ text-align: center; margin-top: 40px; font-size: 12px; color: #6B7280; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>RS Digital | Code Report</h1>
                    <p><strong>Fecha Generación:</strong> {now}</p>
                    <p><strong>Auditor:</strong> {self.config.get('author_name')}</p>
                    <p><strong>Lenguaje Base:</strong> {self.last_analysis.get('language', 'N/A').upper()}</p>
                    
                    <div class="kpi-row">
                        <div class="kpi-card">
                            <h2>{self.last_analysis.get('total_lines', 0)}</h2>
                            <p>LÍNEAS</p>
                        </div>
                        <div class="kpi-card">
                            <h2>{len(self.last_analysis.get('functions', []))}</h2>
                            <p>FUNCIONES</p>
                        </div>
                        <div class="kpi-card">
                            <h2>{len(self.last_analysis.get('classes', []))}</h2>
                            <p>CLASES</p>
                        </div>
                    </div>
                    
                    <h3>Estructura Detectada</h3>
                    <h4>Clases</h4>
                    <ul>
                        {''.join(f"<li>📦 {c['name']}</li>" for c in self.last_analysis.get('classes', [])) or '<li>Ninguna</li>'}
                    </ul>
                    
                    <h4>Funciones Principales</h4>
                    <ul>
                        {''.join(f"<li>🔧 {f['name']}</li>" for f in self.last_analysis.get('functions', [])) or '<li>Ninguna</li>'}
                    </ul>
                    
                    <div class="footer">
                        Generado automáticamente por RS Local Code Explainer Enterprise v2.0
                    </div>
                </div>
            </body>
            </html>
            """
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            if self.config.get("auto_open_report", True):
                os.startfile(filename) 
            self.export_btn.configure(text="💾 EXPORTAR REPORTE", state="normal")
        except Exception as e:
            print(f"Error exportando: {e}")
            self.export_btn.configure(text="💾 EXPORTAR REPORTE", state="normal")

if __name__ == "__main__":
    app = RSLocalCodeExplainerApp()
    app.mainloop()
