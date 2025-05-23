import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import queue
from pathlib import Path
from typing import Callable

from src.utils.constants import Messages

class MainView:
    def __init__(self, root: ctk.CTk, controller: 'ExcelController'):
        self.root = root
        self.controller = controller
        self.setup_ui()
        self.progress_queue = queue.Queue()
        self.progress_thread = None
    
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Configuración de la ventana
        self.root.title("Seguimiento de Facturación")
        self.root.geometry("800x600")
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Botones
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.import_button = ctk.CTkButton(
            button_frame, 
            text="Importar Excel",
            command=self.import_excel
        )
        self.import_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.export_button = ctk.CTkButton(
            button_frame,
            text="Exportar Excel",
            command=self.export_excel
        )
        self.export_button.pack(side=tk.LEFT)
        
        # Barra de progreso
        self.progress_bar = ctk.CTkProgressBar(main_frame)
        self.progress_bar.pack(fill=tk.X, pady=(0, 20))
        self.progress_bar.set(0)
        
        # Etiqueta de estado
        self.status_label = ctk.CTkLabel(main_frame, text="")
        self.status_label.pack(fill=tk.X)
    
    def import_excel(self):
        """Manejar la importación de Excel"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        
        if not file_path:
            return
        
        self._start_progress_thread(
            lambda: self.controller.handle_excel_import(Path(file_path), self.update_progress)
        )
    
    def export_excel(self):
        """Manejar la exportación a Excel"""
        export_path = filedialog.asksaveasfilename(
            title="Guardar archivo Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        
        if not export_path:
            return
        
        self._start_progress_thread(
            lambda: self.controller.handle_excel_export(Path(export_path))
        )
    
    def update_progress(self, progress: float, message: str = ""):
        """Actualizar la barra de progreso y el mensaje de estado"""
        self.progress_bar.set(progress)
        self.status_label.configure(text=message)
        self.root.update()
    
    def show_message(self, title: str, message: str, error: bool = False):
        """Mostrar mensaje al usuario"""
        if error:
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)
    
    def _start_progress_thread(self, task: Callable):
        """Iniciar un hilo para ejecutar una tarea con progreso"""
        def worker():
            try:
                success, message = task()
                if success:
                    self.show_message("Éxito", message)
                else:
                    self.show_message("Error", message, error=True)
            except Exception as e:
                self.show_message("Error", str(e), error=True)
            finally:
                self.progress_bar.set(0)
                self.status_label.configure(text="")
        
        self.progress_thread = threading.Thread(target=worker)
        self.progress_thread.daemon = True
        self.progress_thread.start()
