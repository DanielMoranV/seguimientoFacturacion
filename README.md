# Excel to SQLite Importer 🚀

Una aplicación moderna con interfaz gráfica para importar datos desde archivos Excel a una base de datos SQLite, con validaciones, animaciones de carga y manejo inteligente de duplicados.

## ✨ Características

- **Interfaz Gráfica Moderna**: Diseño minimalista y elegante con CustomTkinter
- **Validación Inteligente**: Verifica columnas requeridas y estructura de datos
- **Manejo de Duplicados**: Actualiza registros existentes basándose en `num_doc`
- **Animaciones de Carga**: Barra de progreso en tiempo real con feedback visual
- **Control de Estado**: Deshabilitación automática de botones durante el procesamiento
- **Estadísticas en Vivo**: Contador de registros en la base de datos
- **Manejo de Errores**: Validaciones robustas con mensajes informativos
- **Multiplataforma**: Compatible con Windows, macOS y Linux

## 🛠️ Instalación

### Opción 1: Instalación Automática
```bash
# Clonar o descargar los archivos
cd excel_to_sqlite

# Ejecutar script de configuración
python setup.py
```

### Opción 2: Instalación Manual
```bash
# Instalar dependencias
pip install -r requirements.txt

# Crear directorios opcionales
mkdir exports samples
```

## 📋 Dependencias

- `pandas>=1.5.0` - Procesamiento de datos
- `openpyxl>=3.0.0` - Lectura de archivos Excel
- `customtkinter>=5.0.0` - Interfaz gráfica moderna
- `pillow>=9.0.0` - Procesamiento de imágenes para la UI

## 🚀 Uso

### Interfaz Gráfica (Recomendado)
```bash
python src/main.py
```

## 📊 Estructura de Datos

### Tabla: `detalle_atenciones`
Campos requeridos en el Excel:
- `num_doc` - Número de documento (clave única)
- `fec_doc` - Fecha del documento
- `nh_pac` - Número de historia del paciente
- `nom_pac` - Nombre del paciente
- `nom_emp` - Nombre de la empresa
- `nom_cia` - Nombre de la compañía
- `ta_doc` - Tipo de documento (1 carácter)
- `nom_ser` - Nombre del servicio
- `tot_doc` - Total del documento
- `num_fac` - Número de factura
- `fec_fac` - Fecha de factura
- `num_pag` - Número de pago
- `fec_pag` - Fecha de pago
- `usu_sis` - Usuario del sistema
- `cod_dx` - Código de diagnóstico
- `facturador` - Facturador
- `producto` - Producto

### Tabla: `seguimiento_facturacion`
Para futuras implementaciones de seguimiento.

## 🎯 Funcionalidades de la Interfaz

### Panel Principal
- **Selección de Archivo**: Botón intuitivo para elegir archivos Excel
- **Validación Automática**: Verificación en tiempo real de la estructura
- **Barra de Progreso**: Indicador visual del proceso de importación
- **Estadísticas**: Contador en vivo de registros en la base de datos

### Controles Inteligentes
- **Deshabilitación Automática**: Los botones se deshabilitan durante el procesamiento
- **Feedback Visual**: Iconos y colores que indican el estado de las operaciones
- **Mensajes Informativos**: Notificaciones claras sobre el progreso y resultados

### Gestión de Datos
- **Importación Inteligente**: Inserta nuevos registros y actualiza existentes
- **Limpieza de Datos**: Conversión automática de tipos y manejo de valores nulos
- **Limpieza de Base de Datos**: Opción para eliminar todos los registros

## 🔧 Características Técnicas

### Validaciones
- ✅ Verificación de existencia del archivo
- ✅ Validación de formato Excel
- ✅ Comprobación de columnas requeridas
- ✅ Validación de tipos de datos
- ✅ Manejo de valores nulos y vacíos

### Procesamiento
- 🔄 Procesamiento asíncrono (no bloquea la interfaz)
- 📊 Progreso en tiempo real
- 🔍 Detección de duplicados por `num_doc`
- 🔄 Actualización completa de registros existentes
- 📈 Contadores de inserción, actualización y errores

### Rendimiento
- ⚡ Procesamiento por lotes para archivos grandes
- 🧵 Multihilo para no bloquear la interfaz
- 💾 Uso eficiente de memoria
- 🏃‍♂️ Optimización de consultas SQL

## 🐛 Solución de Problemas

### Error: "Columnas faltantes"
- Verificar que el Excel tenga todas las columnas requeridas
- Los nombres deben coincidir exactamente (case-sensitive)
- Pueden estar en cualquier orden, pero deben existir

### Error: "No se puede leer el archivo"
- Verificar que el archivo no esté abierto en Excel
- Comprobar permisos de lectura
- Intentar con un archivo Excel diferente

### Interfaz no responde
- El procesamiento se ejecuta en segundo plano
- Esperar a que termine o reiniciar la aplicación
- Verificar que el archivo no sea demasiado grande

### Base de datos bloqueada
- Cerrar otras conexiones a la base de datos
- Reiniciar la aplicación
- Verificar permisos de escritura en el directorio

## 📁 Estructura del Proyecto

```
excel_to_sqlite/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Aplicación principal con interfaz gráfica
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuración general y de base de datos
│   │   ├── logging_config.py   # Configuración de logging
│   │   └── tipos.py            # Definiciones de tipos (TypedDicts)
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── excel_controller.py # Controlador para la lógica de negocio
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py         # Gestor de base de datos (SQLite)
│   ├── utils/
│   │   ├── __init__.py
│   │   └── constants.py        # Constantes (mensajes, SQL, estilos)
│   └── views/
│       ├── __init__.py
│       └── main_view.py        # Interfaz gráfica de usuario (CustomTkinter)
├── .gitignore
├── README.md                   # Este archivo
├── requirements.txt            # Dependencias del proyecto
├── setup.py                    # Script de instalación y configuración
├── run_app.bat                 # Script para ejecutar en Windows
├── logs/                       # Directorio para archivos de log (creado automáticamente)
├── exports/                    # Directorio para exportaciones (creado por setup.py)
└── samples/                    # Directorio para archivos de muestra (creado por setup.py)
# Nota: facturacion.db se crea dentro de src/core/ por defecto, según config.py
```

## 🎨 Personalización

### Temas
La aplicación soporta temas claro y oscuro automáticamente según la configuración del sistema. Para forzar un tema específico, modificar en `src/main.py`:

```python
ctk.set_appearance_mode("dark")   # Tema oscuro
ctk.set_appearance_mode("light")  # Tema claro
ctk.set_appearance_mode("system") # Automático (por defecto)
```

### Colores
Para cambiar el esquema de colores, modificar en `src/main.py`:

```python
ctk.set_default_color_theme("blue")    # Azul (por defecto)
ctk.set_default_color_theme("green")   # Verde
ctk.set_default_color_theme("dark-blue") # Azul oscuro
```

## 🔄 Flujo de Trabajo

### 1. Preparar Archivo Excel
- Asegurar que contenga todas las columnas requeridas
- Verificar que los datos estén en el formato correcto
- Cerrar el archivo si está abierto en Excel

### 2. Ejecutar Aplicación
```bash
python src/main.py
```

### 3. Importar Datos
1. Hacer clic en "📁 Seleccionar Archivo Excel"
2. Elegir el archivo desde el explorador
3. Esperar la validación automática
4. Hacer clic en "🚀 Importar Datos"
5. Observar el progreso en la barra de carga
6. Revisar el resumen de resultados

### 4. Verificar Resultados
- El contador de registros se actualiza automáticamente
- Revisar mensajes de éxito o error
- Usar las utilidades de base de datos si es necesario

## 🧪 Casos de Uso

### Importación Inicial
```python
# Primera vez importando datos
# - Todos los registros se insertarán como nuevos
# - Se creará la base de datos automáticamente
```

### Actualización de Datos
```python
# Importar archivo con registros existentes
# - Los registros con num_doc existente se actualizarán
# - Los nuevos num_doc se insertarán
# - Se mantiene la integridad de datos
```

### Limpieza de Base de Datos
```python
# Usar el botón "🗑️ Limpiar Base de Datos"
# - Elimina todos los registros
# - Mantiene la estructura de las tablas
# - Requiere confirmación del usuario
```

## 📈 Monitoreo y Logs

### Información en Tiempo Real
- **Progreso Visual**: Barra de progreso con porcentaje
- **Estado Actual**: Mensaje descriptivo de la operación
- **Conteo de Registros**: Estadísticas actualizadas automáticamente

### Resultados Detallados
- **Insertados**: Nuevos registros añadidos
- **Actualizados**: Registros existentes modificados
- **Errores**: Filas que no se pudieron procesar

## 🛡️ Seguridad y Validación

### Validaciones de Entrada
- Verificación de tipos de archivo
- Validación de estructura de datos
- Sanitización de entrada de usuario
- Manejo seguro de rutas de archivo

### Protección de Datos
- Transacciones atómicas en base de datos
- Rollback automático en caso de error
- Backup implícito mediante SQLite
- Confirmación para operaciones destructivas

## 🚀 Rendimiento

### Optimizaciones Implementadas
- **Procesamiento Asíncrono**: No bloquea la interfaz de usuario
- **Carga por Lotes**: Procesa múltiples registros eficientemente
- **Índices de Base de Datos**: Búsquedas rápidas por num_doc
- **Limpieza de Memoria**: Liberación automática de recursos

### Recomendaciones para Archivos Grandes
- **Archivos > 10,000 filas**: El procesamiento puede tomar varios minutos
- **Archivos > 50,000 filas**: Considerar dividir en lotes más pequeños
- **Memoria RAM**: Asegurar al menos 4GB disponibles para archivos muy grandes

## 🔧 Configuración Avanzada

### Base de Datos Personalizada
Para cambiar la ubicación o nombre de la base de datos, modificar las entradas `name` y `DB_PATH` en `src/core/config.py`.

### Timeout de Conexión
```python
# Configurar timeout para archivos muy grandes
conn = sqlite3.connect(self.db_path, timeout=30.0)
```

## 🐛 Debug y Desarrollo

### Modo Desarrollo
```python
# Activar logs detallados
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Testing
```python
# Ejecutar con archivo de prueba
python src/main.py
# Usar archivo en directorio samples/
```

### Logs de Error
Los errores se muestran en:
- Interfaz gráfica (messagebox)
- Consola (para desarrollo)
- Barra de progreso (feedback visual)

## 📞 Soporte y Contribución

### Reportar Problemas
- Incluir versión de Python
- Adjuntar archivo Excel de ejemplo (sin datos sensibles)
- Describir pasos para reproducir el error
- Incluir mensaje de error completo

### Mejoras Futuras
- [ ] Soporte para CSV
- [ ] Exportación a diferentes formatos
- [ ] Configuración de mapeo de columnas
- [ ] Historial de importaciones
- [ ] Validaciones de negocio personalizables
- [ ] Interfaz web opcional
- [ ] Soporte para múltiples bases de datos

## 📝 Licencia

Este proyecto está disponible bajo licencia MIT. Libre para uso personal y comercial.

## 🙏 Agradecimientos

- **CustomTkinter**: Por la librería de interfaz moderna
- **Pandas**: Por el potente procesamiento de datos
- **OpenPyXL**: Por el soporte robusto de Excel
- **SQLite**: Por la base de datos embebida eficiente

---

**¡Listo para usar! 🎉**

Para cualquier duda o sugerencia, no dudes en contactar o crear un issue en el repositorio.