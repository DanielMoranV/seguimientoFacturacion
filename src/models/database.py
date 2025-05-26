import sqlite3
import logging
from pathlib import Path
from typing import Tuple, Any, Dict, List
import pandas as pd
from datetime import datetime

from src.utils.constants import Messages, SQLQueries, ExcelStyles

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, NamedStyle
    from openpyxl.utils import get_column_letter
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False
    # logger.warning(Messages.ERROR_OPENPYXL) # Logger not yet available at module level

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, config: Dict, logger: logging.Logger):
        """Iniciar DatabaseManager"""
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.config = config
            self.logger = logger
            self.db_path = self.config['paths']['db_path']
            self.required_columns = self.config['db']['required_columns']
            self.seguimiento_columns = self.config['db']['seguimiento_columns']
            self._setup_database()
            self.logger.info("DatabaseManager inicializado correctamente")
    
    def _setup_database(self):
        """Crear la base de datos SQLite con las tablas necesarias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detalle_atenciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_doc VARCHAR(10) NOT NULL UNIQUE,
                fec_doc DATE NOT NULL,
                nh_pac VARCHAR(255) NOT NULL,
                nom_pac VARCHAR(255) NOT NULL,
                nom_emp VARCHAR(255) NOT NULL,
                nom_cia VARCHAR(255) NOT NULL,
                ta_doc VARCHAR(1) NOT NULL,
                nom_ser VARCHAR(255) NOT NULL,
                tot_doc DECIMAL(8, 2) NOT NULL,
                num_fac VARCHAR(11) NOT NULL,
                fec_fac DATE NOT NULL,
                num_pag VARCHAR(10) NOT NULL,
                fec_pag DATE NOT NULL,
                usu_sis VARCHAR(255) NOT NULL,
                cod_dx VARCHAR(255) NOT NULL,
                facturador VARCHAR(255) NOT NULL,
                producto VARCHAR(255) NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS seguimiento_facturacion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                detalle_atencion_id INTEGER NOT NULL,
                estado_aseguradora VARCHAR(255) NOT NULL,
                fecha_envio DATE NOT NULL,
                fecha_recepcion DATE NOT NULL,
                observaciones TEXT NOT NULL,
                acciones VARCHAR(255) NOT NULL,
                FOREIGN KEY (detalle_atencion_id) REFERENCES detalle_atenciones (id)
                    ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        conn.close()

    def get_stats(self):
        """Obtener estadísticas de la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM detalle_atenciones")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def clear_database_tables(self) -> Tuple[bool, str]:
        """Limpiar todas las tablas de la base de datos."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM detalle_atenciones")
            cursor.execute("DELETE FROM seguimiento_facturacion") 
            conn.commit()
            conn.close()
            self.logger.info("Todas las tablas de la base de datos han sido limpiadas.")
            return True, "Base de datos limpiada exitosamente."
        except Exception as e:
            self.logger.error(f"Error al limpiar base de datos: {str(e)}")
            return False, f"Error al limpiar base de datos: {str(e)}"

    def export_seguimiento_to_excel(self, export_path: Path) -> Tuple[bool, str]:
        """
        Exportar seguimiento a Excel con formato personalizado
        
        Args:
            export_path: Ruta donde se guardará el archivo Excel
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(SQLQueries.SELECT_ALL, conn)
            conn.close()

            self.logger.info("Consulta SQL ejecutada correctamente")
            self.logger.info(df.head()) # Log head instead of full df for brevity
            
            total_rows = len(df)
            self.logger.info(f"Total de registros para exportar: {total_rows}")
            
            return self._format_excel(df, export_path)
            
        except Exception as e:
            self.logger.error(f"Error en export_seguimiento_to_excel: {str(e)}")
            return False, Messages.ERROR_EXPORT.format(str(e))
    
    def _format_excel(self, df: pd.DataFrame, export_path: Path) -> Tuple[bool, str]:
        """Aplicar formato al Excel"""
        try:
            # Renombrar columnas usando mapeo de configuración
            column_mapping = self.config['export_columns']
            
            df = df.rename(columns=column_mapping)
            
            # Convertir campos de fecha
            date_columns = self.config['excel']['date_columns']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            
            # Convertir campos monetarios
            money_columns = self.config['excel']['money_columns']
            for col in money_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            if not OPENPYXL_AVAILABLE:
                self.logger.warning(Messages.ERROR_OPENPYXL + " No se aplicará formato avanzado.")
                df.to_excel(export_path, index=False, sheet_name=self.config['ui']['export_sheet_name'])
                return True, Messages.SUCCESS_EXPORT.format(str(export_path))

            # Crear el archivo Excel con formato personalizado usando openpyxl
            with pd.ExcelWriter(export_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=self.config['ui']['export_sheet_name'], index=False)
                
                workbook = writer.book
                worksheet = writer.sheets[self.config['ui']['export_sheet_name']]
                
                header_style_config = self.config['excel']['styles']['header']
                header_font = Font(**header_style_config['font'])
                header_fill = PatternFill(start_color=header_style_config['fill']['color'], 
                                          end_color=header_style_config['fill']['color'], 
                                          fill_type='solid') # Corrected fill
                header_alignment = Alignment(**header_style_config['alignment'])
                
                date_style = NamedStyle(name='date_style', number_format=self.config['excel']['styles']['date_format'])
                currency_style = NamedStyle(name='currency_style', number_format=self.config['excel']['styles']['currency_format'])
                
                if 'date_style' not in workbook.named_styles:
                    workbook.add_named_style(date_style)
                if 'currency_style' not in workbook.named_styles:
                    workbook.add_named_style(currency_style)
                
                for col_num, column_title in enumerate(df.columns, 1):
                    cell = worksheet.cell(row=1, column=col_num)
                    cell.font = header_font
                    cell.fill = header_fill
                    cell.alignment = header_alignment
                
                for col_num, column_title in enumerate(df.columns, 1):
                    column_letter = get_column_letter(col_num)
                    max_length = max(
                        len(str(column_title)),
                        df[column_title].astype(str).str.len().max() if not df.empty else 0
                    )
                    adjusted_width = min(max(max_length + 2, 10), 50) # Basic auto-adjust
                    worksheet.column_dimensions[column_letter].width = adjusted_width

                    if column_title in date_columns:
                        for row_idx in range(2, len(df) + 2):
                            cell = worksheet.cell(row=row_idx, column=col_num)
                            if cell.value is not None: cell.style = date_style
                    elif column_title in money_columns:
                        for row_idx in range(2, len(df) + 2):
                            cell = worksheet.cell(row=row_idx, column=col_num)
                            if cell.value is not None: cell.style = currency_style
                
                worksheet.auto_filter.ref = worksheet.dimensions
                worksheet.freeze_panes = 'A2'
            
            return True, Messages.SUCCESS_EXPORT.format(str(export_path))
            
        except Exception as e:
            self.logger.error(f"Error en _format_excel: {str(e)}")
            return False, Messages.ERROR_EXPORT.format(str(e))

    def validate_excel(self, file_path: str) -> Tuple[bool, pd.DataFrame | None, List[str] | str]:
        """Validar archivo Excel"""
        try:
            df = pd.read_excel(file_path, dtype={'num_doc': str, 'nh_pac': str, 'num_pag': str})
            missing_columns = [col for col in self.required_columns if col not in df.columns]
            if missing_columns:
                return True, df, missing_columns # Return True for valid read, but with missing columns
            return True, df, [] 
        except Exception as e:
            self.logger.error(f"Error al validar Excel {file_path}: {str(e)}")
            return False, None, str(e)

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpiar y preparar datos"""
        df_clean = df[self.required_columns].copy()
        df_clean = df_clean.fillna('')
        
        date_columns = ['fec_doc', 'fec_fac', 'fec_pag']
        for col in date_columns:
            try:
                df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce').dt.strftime('%Y-%m-%d')
                df_clean[col] = df_clean[col].fillna('')
            except Exception: # Catch any parsing error
                df_clean[col] = ''
        
        text_fields = ['num_doc', 'nh_pac', 'num_pag']
        for col in text_fields:
            df_clean[col] = df_clean[col].apply(lambda x: str(x).strip() if pd.notna(x) and str(x).strip().lower() != 'nan' else '')
        
        try:
            df_clean['tot_doc'] = pd.to_numeric(df_clean['tot_doc'], errors='coerce').fillna(0)
        except Exception:
            df_clean['tot_doc'] = 0
        
        return df_clean

    def insert_record(self, cursor: sqlite3.Cursor, row: pd.Series):
        """Insertar registro"""
        query = f'''
            INSERT INTO detalle_atenciones 
            ({', '.join(self.required_columns)})
            VALUES ({', '.join(['?'] * len(self.required_columns))})
        '''
        cursor.execute(query, tuple(row))

    def update_record(self, cursor: sqlite3.Cursor, row: pd.Series, record_id: int):
        """Actualizar registro solo si no está marcado como 'Pagado' en seguimiento"""
        cursor.execute(SQLQueries.SELECT_CURRENT_STATUS, (record_id,)) # This query was on seguimiento, need to adapt
        # This logic needs to be re-evaluated as record_id is for detalle_atenciones
        # For now, let's assume we always update if found
        
        # query = f'''
        #     UPDATE detalle_atenciones 
        #     SET {', '.join([f'{col}=?' for col in self.required_columns if col != 'num_doc'])}
        #     WHERE id=?
        # '''
        # values = tuple(row[col] for col in self.required_columns if col != 'num_doc') + (record_id,)
        
        # Simplified update, num_doc is unique and should not change for an existing record_id
        update_cols = [col for col in self.required_columns if col != 'num_doc']
        query = f'''
            UPDATE detalle_atenciones 
            SET {', '.join([f'{col}=?' for col in update_cols])}
            WHERE id=?
        '''
        values = tuple(row[col] for col in update_cols) + (record_id,)
        cursor.execute(query, values)

    def process_excel(self, file_path: str, progress_callback: callable) -> Tuple[bool, str]:
        """Procesar archivo Excel con callback de progreso"""
        try:
            is_valid, df, validation_info = self.validate_excel(file_path)
            if not is_valid:
                return False, f"Error al leer archivo: {validation_info}"
            
            if isinstance(validation_info, list) and validation_info: # Check if it's the list of missing columns
                return False, Messages.MISSING_COLUMNS.format(', '.join(validation_info))
            
            if df is None: # Should not happen if is_valid is True, but as a safeguard
                 return False, "Error desconocido al validar el archivo Excel."

            df_clean = self.clean_data(df.copy()) # Use a copy to avoid SettingWithCopyWarning
            total_rows = len(df_clean)
            
            if total_rows == 0:
                return False, Messages.NO_DATA
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            inserted = 0
            updated = 0
            errors = 0
            
            for index, row in df_clean.iterrows():
                try:
                    num_doc = str(row['num_doc']).strip()
                    if not num_doc: # num_doc was already cleaned
                        errors += 1
                        continue
                    
                    cursor.execute(SQLQueries.SELECT_BY_DOC, (num_doc,))
                    existing = cursor.fetchone()
                    
                    if existing:
                        self.update_record(cursor, row, existing[0])
                        updated += 1
                    else:
                        self.insert_record(cursor, row)
                        inserted += 1
                    
                    progress = ((index + 1) / total_rows) * 100
                    progress_callback(progress, f"Procesando: {num_doc}")
                    
                except Exception as e_row:
                    self.logger.error(f"Error procesando fila {index} (num_doc: {num_doc}): {str(e_row)}")
                    errors += 1
                    continue # Continue with the next row
            
            conn.commit()
            conn.close()

            # Actualizar estados de pago después de importar
            payment_success, payment_result = self.update_payment_status()

            summary = f"Insertados: {inserted}, Actualizados: {updated}, Errores: {errors}"

            if payment_success:
                summary += f"\n{payment_result}"
            else:
                summary += f"\nError al actualizar estados de pago: {payment_result}"

            return True, summary
            
        except Exception as e_main:
            self.logger.error(f"Error general en process_excel: {str(e_main)}")
            return False, Messages.ERROR_UPDATE.format(str(e_main))

    def update_seguimiento_from_excel(self, file_path: str, progress_callback: callable) -> Tuple[bool, str]:
        """
        Actualizar seguimiento desde archivo Excel
        """
        try:
            self.logger.info(f"Iniciando actualización de seguimiento desde Excel: {file_path}")
            
            # Leer Excel con nombres de columnas amigables
            # The dtype mapping here should use the friendly names from the Excel file
            df = pd.read_excel(file_path, dtype={'Número de Documento': str, 'Historia Clínica': str})
            
            # Mapear nombres amigables a nombres de BD usando configuración
            # seguimiento_columns in config is {'Friendly Name': 'db_column_name'}
            
            # Verificar columnas requeridas (using friendly names)
            missing_columns = [col for col in self.seguimiento_columns.keys() if col not in df.columns]
            if missing_columns:
                return False, Messages.MISSING_COLUMNS.format(', '.join(missing_columns))
            
            # Select and rename columns to DB names
            df_to_process = df[list(self.seguimiento_columns.keys())].copy()
            df_to_process.rename(columns=self.seguimiento_columns, inplace=True)

            df_clean = df_to_process.fillna('') # Fill NA after renaming
            
            # Convertir fechas (using DB names)
            date_columns_db = ['fecha_envio', 'fecha_recepcion']
            for col in date_columns_db:
                if col in df_clean.columns:
                    try:
                        df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce').dt.strftime('%Y-%m-%d')
                        df_clean[col] = df_clean[col].fillna('') # Ensure NAs are empty strings post-conversion
                    except Exception:
                         df_clean[col] = ''
            
            total_rows = len(df_clean)
            if total_rows == 0:
                return False, Messages.NO_DATA
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            updated_count = 0
            inserted_count = 0
            errors_count = 0
            
            for index, row in df_clean.iterrows():
                try:
                    num_doc = str(row['num_doc']).strip() # num_doc is now a DB column name
                    if not num_doc:
                        errors_count += 1
                        continue
                    
                    cursor.execute(SQLQueries.SELECT_BY_DOC, (num_doc,))
                    detalle_record = cursor.fetchone()
                    
                    if not detalle_record:
                        errors_count += 1
                        self.logger.warning(f"No se encontró detalle_atencion para num_doc: {num_doc}")
                        continue
                    
                    detalle_id = detalle_record[0]
                    
                    cursor.execute(SQLQueries.SELECT_BY_ID, (detalle_id,)) # Query for seguimiento_facturacion by detalle_id
                    seguimiento_record = cursor.fetchone()
                    
                    # Prepare data for SQL (all are DB column names now)
                    # Ensure all fields from seguimiento_columns (DB version) are present in row
                    estado = str(row['estado_aseguradora']).strip()
                    fecha_envio_val = str(row['fecha_envio']).strip() if row['fecha_envio'] else None
                    fecha_recepcion_val = str(row['fecha_recepcion']).strip() if row['fecha_recepcion'] else None
                    observaciones_val = str(row['observaciones']).strip()
                    acciones_val = str(row['acciones']).strip()

                    if seguimiento_record:
                        seguimiento_id = seguimiento_record[0]
                        cursor.execute("""
                            UPDATE seguimiento_facturacion 
                            SET estado_aseguradora = ?, fecha_envio = ?, fecha_recepcion = ?, 
                                observaciones = ?, acciones = ?
                            WHERE id = ?
                        """, (estado, fecha_envio_val, fecha_recepcion_val, observaciones_val, acciones_val, seguimiento_id))
                        updated_count += 1
                    else:
                        cursor.execute("""
                            INSERT INTO seguimiento_facturacion 
                            (detalle_atencion_id, estado_aseguradora, fecha_envio, fecha_recepcion, observaciones, acciones)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (detalle_id, estado, fecha_envio_val, fecha_recepcion_val, observaciones_val, acciones_val))
                        inserted_count += 1
                    
                    progress = ((index + 1) / total_rows) * 100
                    progress_callback(progress, Messages.PROCESSING_DOC.format(num_doc))
                    
                except Exception as e_row_seguimiento:
                    self.logger.error(f"Error procesando seguimiento para num_doc {row.get('num_doc', 'N/A')}: {str(e_row_seguimiento)}")
                    errors_count += 1
                    continue
            
            conn.commit()
            conn.close()
            
            summary = Messages.SUCCESS_UPDATE.format(updated_count, inserted_count, errors_count)
            self.logger.info(summary)
            return True, summary
            
        except Exception as e_main_seguimiento:
            self.logger.error(f"Error general en update_seguimiento_from_excel: {str(e_main_seguimiento)}")
            return False, Messages.ERROR_UPDATE.format(str(e_main_seguimiento))

    def update_payment_status(self) -> Tuple[bool, str]:
        """Actualizar automáticamente el estado a 'Pagado' en seguimiento_facturacion si hay info de pago en detalle_atenciones."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(SQLQueries.SELECT_PAID)
            paid_records = cursor.fetchall()
            
            updated_count = 0
            inserted_count = 0
        
            for record in paid_records:
                detalle_id, num_doc, num_pag, fec_pag = record
                
                # Ensure fec_pag is valid, default to today if not
                try:
                    valid_fec_pag = pd.to_datetime(fec_pag).strftime('%Y-%m-%d') if fec_pag else datetime.now().strftime('%Y-%m-%d')
                except ValueError: # Handle cases where fec_pag might be an invalid date string
                    valid_fec_pag = datetime.now().strftime('%Y-%m-%d')

                cursor.execute(SQLQueries.SELECT_BY_ID, (detalle_id,))
                existing_seguimiento = cursor.fetchone()

                if existing_seguimiento:
                    seguimiento_id = existing_seguimiento[0]
                    cursor.execute(SQLQueries.SELECT_CURRENT_STATUS, (seguimiento_id,)) # Query was for seguimiento, this is correct
                    current_status_result = cursor.fetchone()
                    
                    if current_status_result and current_status_result[0].strip().lower() == Messages.PAID_STATUS.lower():
                        continue 

                    cursor.execute("""
                        UPDATE seguimiento_facturacion 
                        SET estado_aseguradora = ?,
                            fecha_recepcion = ?,
                            observaciones = CASE 
                                WHEN observaciones = '' OR observaciones IS NULL THEN ?
                                ELSE observaciones || ' | ' || ?
                            END,
                            acciones = CASE 
                                WHEN acciones = '' OR acciones IS NULL THEN ?
                                ELSE acciones 
                            END
                        WHERE id = ?
                    """, (Messages.PAID_STATUS, valid_fec_pag, 
                          Messages.DEFAULT_OBSERVATION, Messages.DEFAULT_OBSERVATION, 
                          Messages.DEFAULT_ACTION, seguimiento_id))
                    updated_count += 1
                else:
                    cursor.execute("""
                        INSERT INTO seguimiento_facturacion 
                        (detalle_atencion_id, estado_aseguradora, fecha_envio, fecha_recepcion, observaciones, acciones)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (detalle_id, Messages.PAID_STATUS, valid_fec_pag, valid_fec_pag, 
                          Messages.DEFAULT_OBSERVATION, Messages.DEFAULT_ACTION))
                    inserted_count += 1 

            conn.commit()
            conn.close()
        
            summary = Messages.SUCCESS_PAYMENT.format(updated_count, inserted_count)
            self.logger.info(summary)
            return True, summary
        
        except Exception as e_payment:
            self.logger.error(Messages.ERROR_PAYMENT.format(str(e_payment)))
            return False, Messages.ERROR_PAYMENT.format(str(e_payment))

