import os
from pathlib import Path
from typing import Dict, List

# Configuración de la base de datos
DB_CONFIG = {
    'name': 'facturacion.db',
    'required_columns': [
        'num_doc', 'fec_doc', 'nh_pac', 'nom_pac', 'nom_emp', 
        'nom_cia', 'ta_doc', 'nom_ser', 'tot_doc', 'num_fac', 
        'fec_fac', 'num_pag', 'fec_pag', 'usu_sis', 'cod_dx', 
        'facturador', 'producto'
    ],
    'seguimiento_columns': {
        'Número de Documento': 'num_doc',
        'Estado Aseguradora': 'estado_aseguradora', 
        'Fecha de Envío': 'fecha_envio',
        'Fecha de Recepción': 'fecha_recepcion',
        'Observaciones': 'observaciones',
        'Acciones': 'acciones'
    }
}

# Configuración de la interfaz
UI_CONFIG = {
    'window': {
        'title': 'Seguimiento de Facturación',
        'size': '800x700',
        'min_size': '600x500'
    },
    'progress_check_interval': 100,  # ms
    'export_sheet_name': 'Seguimiento_Facturacion'
}

# Configuración de Excel
EXCEL_CONFIG = {
    'date_columns': [
        'Fecha de Documento', 'Fecha de Factura', 
        'Fecha de Pago', 'Fecha de Envío', 'Fecha de Recepción'
    ],
    'money_columns': ['Total Documento'],
    'styles': {
        'header': {
            'font': {'bold': True, 'color': 'FFFFFF', 'size': 12},
            'fill': {'color': '366092'},
            'alignment': {'horizontal': 'center', 'vertical': 'center'}
        },
        'date_format': 'DD/MM/YYYY',
        'currency_format': 'S/ #,##0.00'
    }
}

# Rutas
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / DB_CONFIG['name']

# Columnas para exportación
EXPORT_COLUMN_MAPPING = {
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

def get_config() -> Dict:
    """Obtener configuración completa del sistema"""
    return {
        'db': DB_CONFIG,
        'ui': UI_CONFIG,
        'excel': EXCEL_CONFIG,
        'paths': {
            'base_dir': BASE_DIR,
            'db_path': DB_PATH
        },
        'export_columns': EXPORT_COLUMN_MAPPING
    }
