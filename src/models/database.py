import sqlite3
import logging
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

from src.utils.constants import Messages

logger = logging.getLogger('facturacion')

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, db_path: Path):
        """Iniciar DatabaseManager"""
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.db_path = db_path
            self._setup_database()
            logger.info("DatabaseManager inicializado correctamente")
    
    def _setup_database(self):
        """Configurar la base de datos"""
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
                estado_aseguradora VARCHAR(50) NOT NULL,
                fecha_envio DATE,
                fecha_recepcion DATE,
                observaciones TEXT,
                acciones TEXT,
                FOREIGN KEY (detalle_atencion_id) REFERENCES detalle_atenciones (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
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
            df = pd.read_sql_query("""
                SELECT 
                    d.num_doc, d.fec_doc, d.nh_pac, d.nom_pac, d.nom_emp, d.nom_cia,
                    d.tot_doc, d.num_fac, d.fec_fac, d.num_pag, d.fec_pag, d.facturador,
                    s.estado_aseguradora, s.fecha_envio, s.fecha_recepcion, s.observaciones, s.acciones
                FROM detalle_atenciones d
                LEFT JOIN seguimiento_facturacion s ON d.id = s.detalle_atencion_id
                WHERE d.nom_pac != 'No existe...'
            """, conn)
            
            conn.close()

            # Mostrar la consulta
            logger.info("Consulta SQL ejecutada correctamente")
            logger.info(df)
            

            #Cantidad de registros
            total_rows = len(df)
            logger.info(f"Total de registros: {total_rows}")
            
            return self._format_excel(df, export_path)
            
        except Exception as e:
            logger.error(f"Error en export_seguimiento_to_excel: {str(e)}")
            return False, Messages.ERROR_EXPORT.format(str(e))
    
    def _format_excel(self, df: pd.DataFrame, export_path: Path) -> Tuple[bool, str]:
        """Aplicar formato al Excel"""
        try:
            # Renombrar columnas usando mapeo de configuración
            column_mapping = {
                'num_doc': 'Número de Documento',
                'fec_doc': 'Fecha de Documento',
                'nh_pac': 'Historia Clínica',
                'nom_pac': 'Nombre del Paciente',
                'nom_emp': 'Empresa',
                'nom_cia': 'Compañía',
                'tot_doc': 'Total Documento',
                'num_fac': 'Número de Factura',
                'fec_fac': 'Fecha de Factura',
                'num_pag': 'Número de Pago',
                'fec_pag': 'Fecha de Pago',
                'facturador': 'Facturador',
                'estado_aseguradora': 'Estado Aseguradora',
                'fecha_envio': 'Fecha de Envío',
                'fecha_recepcion': 'Fecha de Recepción',
                'observaciones': 'Observaciones',
                'acciones': 'Acciones'
            }
            
            df = df.rename(columns=column_mapping)
            
            # Convertir campos de fecha
            date_columns = ['Fecha de Documento', 'Fecha de Factura', 'Fecha de Pago', 'Fecha de Envío', 'Fecha de Recepción']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            
            # Convertir campos monetarios
            money_columns = ['Total Documento']
            for col in money_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            return True, Messages.SUCCESS_EXPORT.format(str(export_path))
            
        except Exception as e:
            logger.error(f"Error en _format_excel: {str(e)}")
            return False, Messages.ERROR_EXPORT.format(str(e))
