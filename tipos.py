from typing import TypedDict, List, Dict, Optional, Any
from datetime import datetime

class DatabaseConfig(TypedDict):
    name: str
    required_columns: List[str]
    seguimiento_columns: Dict[str, str]

class UIConfig(TypedDict):
    window: Dict[str, str]
    progress_check_interval: int
    export_sheet_name: str

class ExcelConfig(TypedDict):
    date_columns: List[str]
    money_columns: List[str]
    styles: Dict[str, Dict[str, Any]]

class ExportColumnMapping(TypedDict):
    num_doc: str
    fec_doc: str
    nh_pac: str
    nom_pac: str
    nom_emp: str
    nom_cia: str
    tot_doc: str
    num_fac: str
    fec_fac: str
    num_pag: str
    fec_pag: str
    facturador: str
    estado_aseguradora: str
    fecha_envio: str
    fecha_recepcion: str
    observaciones: str
    acciones: str

class ProgressCallback(TypedDict):
    progress: float
    message: str

class ExcelRow(TypedDict):
    num_doc: str
    fec_doc: datetime
    nh_pac: str
    nom_pac: str
    nom_emp: str
    nom_cia: str
    tot_doc: float
    num_fac: str
    fec_fac: datetime
    num_pag: Optional[str]
    fec_pag: Optional[datetime]
    facturador: str
    estado_aseguradora: str
    fecha_envio: Optional[datetime]
    fecha_recepcion: Optional[datetime]
    observaciones: str
    acciones: str
