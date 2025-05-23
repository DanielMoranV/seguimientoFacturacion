import sqlite3
from datetime import datetime

def create_database():
    """Crear la base de datos SQLite con las tablas necesarias"""
    conn = sqlite3.connect('facturacion.db')
    cursor = conn.cursor()
    
    # Crear tabla detalle_atenciones
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
    
    # Crear tabla seguimiento_facturacion
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
    print("Base de datos creada exitosamente")

if __name__ == "__main__":
    create_database()