import customtkinter as ctk
import logging
from pathlib import Path

from src.models.database import DatabaseManager
from src.controllers.excel_controller import ExcelController
from src.views.main_view import MainView
from src.utils.constants import Messages

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('seguimiento.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('facturacion')

# Configuración de la aplicación
def setup_app():
    """Configurar y ejecutar la aplicación"""
    try:
        # Inicializar el gestor de base de datos
        db_manager = DatabaseManager(Path('facturacion.db'))
        
        # Inicializar el controlador
        controller = ExcelController(db_manager)
        
        # Configurar la interfaz
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        # Crear la ventana principal
        root = ctk.CTk()
        
        # Crear y mostrar la vista principal
        view = MainView(root, controller)
        
        # Ejecutar la aplicación
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Error en setup_app: {str(e)}")
        raise

if __name__ == "__main__":
    setup_app()
