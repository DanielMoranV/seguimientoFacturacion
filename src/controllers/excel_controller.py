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
    
    def handle_excel_import(self, file_path: Path, progress_callback: callable) -> Tuple[bool, str]:
        """
        Manejar la importación de datos desde Excel
        
        Args:
            file_path: Ruta del archivo Excel
            progress_callback: Función para actualizar el progreso
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        try:
            # Leer Excel
            df = pd.read_excel(file_path, dtype={'Número de Documento': str, 'Historia Clínica': str})
            
            # Validar columnas requeridas
            required_columns = [
                'Número de Documento', 'Estado Aseguradora', 
                'Fecha de Envío', 'Fecha de Recepción',
                'Observaciones', 'Acciones'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return False, Messages.MISSING_COLUMNS.format(', '.join(missing_columns))
            
            # Limpiar y procesar datos
            df_clean = df[required_columns].copy()
            df_clean = df_clean.fillna('')
            
            # Convertir fechas
            date_columns = ['Fecha de Envío', 'Fecha de Recepción']
            for col in date_columns:
                try:
                    df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce').dt.strftime('%Y-%m-%d')
                    df_clean[col] = df_clean[col].fillna('')
                except Exception as e:
                    logger.error(f"Error al convertir fechas: {str(e)}")
                    df_clean[col] = ''
            
            # Procesar registros
            total_rows = len(df_clean)
            if total_rows == 0:
                return False, Messages.NO_DATA
            
            updated = 0
            inserted = 0
            errors = 0
            
            for index, row in df_clean.iterrows():
                try:
                    success, message = self._process_row(row)
                    if success:
                        updated += 1
                    else:
                        errors += 1
                    
                    progress = ((index + 1) / total_rows) * 100
                    progress_callback(progress, Messages.PROCESSING_DOC.format(row['Número de Documento']))
                    
                except Exception as e:
                    logger.error(f"Error al procesar fila: {str(e)}")
                    errors += 1
            
            summary = Messages.SUCCESS_UPDATE.format(updated, inserted, errors)
            return True, summary
            
        except Exception as e:
            logger.error(f"Error en handle_excel_import: {str(e)}")
            return False, Messages.ERROR_UPDATE.format(str(e))
    
    def _process_row(self, row: pd.Series) -> Tuple[bool, str]:
        """Procesar una fila individual del Excel"""
        try:
            num_doc = str(row['Número de Documento']).strip()
            if not num_doc or num_doc == 'nan':
                return False, "Número de documento inválido"
            
            # Buscar el detalle_atencion_id
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute(SQLQueries.SELECT_BY_DOC, (num_doc,))
            detalle_record = cursor.fetchone()
            
            if not detalle_record:
                conn.close()
                return False, "Documento no encontrado en la base de datos"
            
            detalle_id = detalle_record[0]
            
            # Verificar si existe seguimiento
            cursor.execute(SQLQueries.SELECT_BY_ID, (detalle_id,))
            seguimiento_record = cursor.fetchone()
            
            # Preparar datos
            estado = str(row['Estado Aseguradora']).strip()
            fecha_envio = str(row['Fecha de Envío']).strip() if row['Fecha de Envío'] else ''
            fecha_recepcion = str(row['Fecha de Recepción']).strip() if row['Fecha de Recepción'] else ''
            observaciones = str(row['Observaciones']).strip()
            acciones = str(row['Acciones']).strip()
            
            if seguimiento_record:
                # Actualizar seguimiento existente
                seguimiento_id = seguimiento_record[0]
                cursor.execute("""
                    UPDATE seguimiento_facturacion 
                    SET estado_aseguradora = ?,
                        fecha_envio = ?,
                        fecha_recepcion = ?,
                        observaciones = ?,
                        acciones = ?
                    WHERE id = ?
                """, (estado, fecha_envio, fecha_recepcion, observaciones, acciones, seguimiento_id))
                conn.commit()
                conn.close()
                return True, "Registro actualizado"
            else:
                # Crear nuevo seguimiento
                cursor.execute("""
                    INSERT INTO seguimiento_facturacion 
                    (detalle_atencion_id, estado_aseguradora, fecha_envio, fecha_recepcion, observaciones, acciones)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (detalle_id, estado, fecha_envio, fecha_recepcion, observaciones, acciones))
                conn.commit()
                conn.close()
                return True, "Nuevo registro creado"
            
        except Exception as e:
            logger.error(f"Error en _process_row: {str(e)}")
            return False, str(e)
