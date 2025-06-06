import logging
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
from pathlib import Path

from src.models.database import DatabaseManager
from src.utils.constants import Messages, SQLQueries, ExcelStyles

logger = logging.getLogger('facturacion')

class ExcelController:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def handle_excel_export(self, export_path: Path) -> Tuple[bool, str]:
        """
        Manejar la exportación de datos a Excel
        
        Args:
            export_path: Ruta donde se guardará el archivo Excel
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        try:
            success, message = self.db_manager.export_seguimiento_to_excel(export_path)
            if not success:
                return False, message
            
            return True, message
            
        except Exception as e:
            logger.error(f"Error en handle_excel_export: {str(e)}")
            return False, Messages.ERROR_EXPORT.format(str(e))
            
    def handle_pending_export(self, export_path: Path) -> Tuple[bool, str]:
        """
        Manejar la exportación de pendientes a Excel
        (Solo registros sin número de pago y con monto > 0)
        
        Args:
            export_path: Ruta donde se guardará el archivo Excel
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        try:
            success, message = self.db_manager.export_pending_to_excel(export_path)
            if not success:
                return False, message
            
            return True, message
            
        except Exception as e:
            logger.error(f"Error en handle_pending_export: {str(e)}")
            return False, Messages.ERROR_EXPORT.format(str(e))

    def handle_seguimiento_update_from_excel(self, file_path: Path, progress_callback: callable) -> Tuple[bool, str]:
        try:
            # Ensure file_path is a string if db_manager expects a string
            return self.db_manager.update_seguimiento_from_excel(str(file_path), progress_callback)
        except Exception as e:
            logger.error(f"Error en handle_seguimiento_update_from_excel: {str(e)}")
            # You might want to return a more generic error message or re-raise
            return False, Messages.ERROR_UPDATE.format(str(e))

    def handle_primary_excel_import(self, file_path: Path, progress_callback: callable) -> Tuple[bool, str]:
        """
        Manejar la importación primaria de datos de Excel a detalle_atenciones.
        
        Args:
            file_path: Ruta del archivo Excel.
            progress_callback: Función para actualizar el progreso.
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        try:
            # Ensure file_path is a string if db_manager expects a string
            return self.db_manager.process_excel(str(file_path), progress_callback)
        except Exception as e:
            logger.error(f"Error en handle_primary_excel_import: {str(e)}")
            return False, Messages.ERROR_UPDATE.format(str(e)) # Or a more specific message

    def get_app_title(self) -> str:
        # This assumes db_manager has a config dictionary with UI settings
        try:
            return self.db_manager.config['ui']['window']['title']
        except KeyError:
            logger.error("UI title not found in config.")
            return "Facturación App" # Fallback title

    def handle_clear_database(self) -> Tuple[bool, str]:
        try:
            return self.db_manager.clear_database_tables()
        except Exception as e:
            logger.error(f"Error in handle_clear_database (controller): {str(e)}")
            return False, "Error al limpiar la base de datos."

    def handle_get_stats(self) -> int:
        try:
            return self.db_manager.get_stats()
        except Exception as e:
            logger.error(f"Error in handle_get_stats (controller): {str(e)}")
            return 0 # Fallback stats
