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
    ERROR_FILE_SELECTION = "Por favor, seleccione un archivo principal primero."
    ERROR_STATS = "Error al obtener estadísticas"
    ERROR_UNEXPECTED = "Error inesperado: {}"
    
    # Mensajes de éxito
    SUCCESS_EXPORT = "Archivo exportado con éxito: {}"
    SUCCESS_UPDATE = "Seguimientos actualizados: {}, Nuevos seguimientos: {}, Errores: {}"
    SUCCESS_PAYMENT = "Estados actualizados: {}, Nuevos registros: {}"
    
    # Mensajes de validación
    MISSING_COLUMNS = "Columnas faltantes: {}"
    NO_DATA = "No hay datos válidos para procesar"
    
    # Mensajes de progreso
    PROCESSING_DOC = "Procesando seguimiento: {}"
    WAITING_FILE = "Esperando archivo..."
    EXPORTING_DATA = "Exportando datos..."
    CLEANING_DB = "Limpiando base de datos..."
    IMPORTING_DATA = "Iniciando importación de datos principales..."
    UPDATING_DATA = "Actualizando con: {}"
    
    # Mensajes de confirmación
    CONFIRM_CLEAR_DB = "¿Está seguro de eliminar todos los datos de la base de datos?\nEsta acción no se puede deshacer."
    
    # Títulos de diálogos
    DIALOG_CONFIRM = "Confirmar"
    DIALOG_SUCCESS = "Éxito"
    DIALOG_ERROR = "Error"
    DIALOG_SELECT_FILE = "Seleccionar Archivo Excel Principal"
    DIALOG_SELECT_SEGUIMIENTO = "Seleccionar archivo Excel de seguimiento"
    DIALOG_SAVE_FILE = "Guardar archivo Excel"
    
    # Etiquetas de UI
    LABEL_NO_FILE = "Ningún archivo principal seleccionado"
    LABEL_FILE_SELECTED = "Archivo seleccionado: {}"
    LABEL_STATS = "📊 Registros en base de datos: {}"
    
    # Estados
    PAID_STATUS = "Pagado"
    ZERO_NEGATIVE_STATUS = "Cero o Negativo"
    
    # Observaciones y acciones por defecto
    DEFAULT_OBSERVATION = "Estado actualizado automáticamente - Factura pagada"
    DEFAULT_ACTION = "Pago procesado"
    ZERO_NEGATIVE_OBSERVATION = "Estado actualizado automáticamente - Monto cero o negativo"
    ZERO_NEGATIVE_ACTION = "Verificar monto"

@dataclass
class SQLQueries:
    # Consultas para detalle_atenciones
    SELECT_ALL = """
        SELECT 
            d.num_doc, d.fec_doc, d.nh_pac, d.nom_pac, d.nom_emp, d.nom_cia,
            d.tot_doc, d.num_fac, d.fec_fac, d.num_pag, d.fec_pag, d.facturador,
            s.estado_aseguradora, s.fecha_envio, s.fecha_recepcion, s.observaciones, s.acciones
        FROM detalle_atenciones d
        LEFT JOIN seguimiento_facturacion s ON d.id = s.detalle_atencion_id
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
    
    # Consulta para montos cero o negativos
    SELECT_ZERO_NEGATIVE = """
        SELECT id, num_doc, tot_doc 
        FROM detalle_atenciones 
        WHERE tot_doc <= 0
    """
    
    # Consulta para exportar pendientes (sin num_pag y tot_doc > 0)
    SELECT_PENDING = """
        SELECT 
            d.num_doc, d.fec_doc, d.nh_pac, d.nom_pac, d.nom_emp, d.nom_cia,
            d.tot_doc, d.num_fac, d.fec_fac, d.num_pag, d.fec_pag, d.facturador,
            s.estado_aseguradora, s.fecha_envio, s.fecha_recepcion, s.observaciones, s.acciones
        FROM detalle_atenciones d
        LEFT JOIN seguimiento_facturacion s ON d.id = s.detalle_atencion_id
        WHERE d.nom_pac != 'No existe...'
        AND (d.num_pag IS NULL OR d.num_pag = '' OR d.num_pag = 'nan')
        AND d.tot_doc > 0
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
