import sys
import os

# Asegurar que el directorio src está en el path para importaciones correctas
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from main_gui import RSLocalCodeExplainerApp

if __name__ == "__main__":
    print("🍊 Iniciando RS | Local Code Explainer (Desktop)...")
    app = RSLocalCodeExplainerApp()
    app.mainloop()
