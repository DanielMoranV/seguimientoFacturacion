import customtkinter as ctk
import logging
from pathlib import Path

from src.core.config import get_config
from src.core.logging_config import setup_logging
from src.models.database import DatabaseManager
from src.controllers.excel_controller import ExcelController
from src.views.main_view import MainView
from src.utils.constants import Messages

# Configuración de la aplicación
def setup_app():
    """Configurar y ejecutar la aplicación"""
    try:
        CONFIG = get_config()
        logger = setup_logging() # Use the centralized logging

        # Inicializar el gestor de base de datos
        db_manager = DatabaseManager(config=CONFIG, logger=logger)
        
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
