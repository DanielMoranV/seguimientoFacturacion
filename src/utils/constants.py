from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

@dataclass
class Messages:
    # Mensajes de error
    ERROR_DB_INIT = "Error al inicializar DatabaseManager: {}"
    ERROR_EXPORT = "Error al exportar: {}"
    ERROR_UPDATE = "Error general: {}"
    ERROR_PAYMENT = "Error al actualizar estados de pago: {}"
    ERROR_OPENPYXL = "openpyxl no está instalado. El formato Excel estará limitado."
    
    # Mensajes de éxito
    SUCCESS_EXPORT = "Archivo exportado con éxito: {}"
    SUCCESS_UPDATE = "Seguimientos actualizados: {}, Nuevos seguimientos: {}, Errores: {}"
    SUCCESS_PAYMENT = "Estados actualizados: {}, Nuevos registros: {}"
    
    # Mensajes de validación
    MISSING_COLUMNS = "Columnas faltantes: {}"
    NO_DATA = "No hay datos válidos para procesar"
    
    # Mensajes de progreso
    PROCESSING_DOC = "Procesando seguimiento: {}"
    
    # Estado de pago
    PAID_STATUS = "Pagado"
    
    # Observaciones y acciones por defecto
    DEFAULT_OBSERVATION = "Estado actualizado automáticamente - Factura pagada"
    DEFAULT_ACTION = "Pago procesado"

@dataclass
class SQLQueries:
    # Consultas para detalle_atenciones
    SELECT_ALL = """
        SELECT 
            d.num_doc, d.fec_doc, d.nh_pac, d.nom_pac, d.nom_emp, d.nom_cia,
            d.tot_doc, d.num_fac, d.fec_fac, d.num_pag, d.fec_pag, d.facturador,
            s.estado_aseguradora, s.fecha_envio, s.fecha_recepcion, s.observaciones, s.acciones
        FROM detalle_atenciones d
        JOIN seguimiento_facturacion s ON d.id = s.detalle_atencion_id
        WHERE d.nom_pac != 'No existe...'
    """
    
    # Consultas para seguimiento_facturacion
    SELECT_BY_DOC = "SELECT id FROM detalle_atenciones WHERE num_doc = ?"
    SELECT_BY_ID = "SELECT id FROM seguimiento_facturacion WHERE detalle_atencion_id = ?"
    SELECT_CURRENT_STATUS = "SELECT estado_aseguradora FROM seguimiento_facturacion WHERE id = ?"
    
    # Consultas para pagos
    SELECT_PAID = """
        SELECT id, num_doc, num_pag, fec_pag 
        FROM detalle_atenciones 
        WHERE num_pag IS NOT NULL 
        AND num_pag != '' 
        AND num_pag != 'nan'
    """

@dataclass
class ExcelStyles:
    HEADER_FONT = {
        'bold': True,
        'color': 'FFFFFF',
        'size': 12
    }
    HEADER_FILL = {
        'start_color': '366092',
        'end_color': '366092',
        'fill_type': 'solid'
    }
    HEADER_ALIGNMENT = {
        'horizontal': 'center',
        'vertical': 'center'
    }
    DATE_FORMAT = 'DD/MM/YYYY'
    CURRENCY_FORMAT = 'S/ #,##0.00'
