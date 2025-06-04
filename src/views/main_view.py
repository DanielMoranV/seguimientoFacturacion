import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from pathlib import Path
from typing import Callable, Optional, Tuple, Dict, Any, List, TYPE_CHECKING

import os

from src.utils.constants import Messages

if TYPE_CHECKING:
    from src.controllers.excel_controller import ExcelController


class MainView:
    def __init__(self, root: ctk.CTk, controller: 'ExcelController'):
        self.root = root
        self.controller = controller
        self.selected_primary_file = None
        self.selected_seguimiento_file = None

        self.setup_ui()
        self.update_stats_display()
    
    def setup_ui(self):
        """Configurar la interfaz de usuario basada en ModernExcelImporter.setup_ui"""
        # Window Setup
        self.root.title(self.controller.get_app_title())
        self.root.geometry("800x700")
        self.root.minsize(600, 500)

        # Main Frame
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title Label
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Seguimiento de Facturación", # Actualizado para coincidir con el título de la aplicación
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(pady=(30, 10))

        # Subtitle Label
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Importación, seguimiento y exportación de datos de facturación", # Actualizado para reflejar todas las funcionalidades
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.subtitle_label.pack(pady=(0, 30))

        # File Selection Frame
        self.file_frame = ctk.CTkFrame(self.main_frame, height=120)
        self.file_frame.pack(fill="x", padx=30, pady=(0, 20))
        self.file_frame.pack_propagate(False) # Prevent frame from shrinking

        self.select_primary_file_button = ctk.CTkButton(
            self.file_frame,
            text="📁 Seleccionar Archivo Principal",
            font=ctk.CTkFont(size=16, weight="bold"), # Added font for consistency
            height=50, # Added height for consistency
            command=self.select_primary_file_dialog
        )
        self.select_primary_file_button.pack(pady=10) # Adjusted padding

        self.primary_file_label = ctk.CTkLabel(
            self.file_frame,
            text=Messages.LABEL_NO_FILE,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.primary_file_label.pack(pady=(0, 10))

        # Progress Frame
        self.progress_frame = ctk.CTkFrame(self.main_frame, height=120)
        self.progress_frame.pack(fill="x", padx=30, pady=(0, 20))
        self.progress_frame.pack_propagate(False)

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, width=400) # Added width
        self.progress_bar.pack(pady=(20, 10))
        self.progress_bar.set(0)

        self.progress_status_label = ctk.CTkLabel(
            self.progress_frame,
            text=Messages.WAITING_FILE,
            font=ctk.CTkFont(size=12)
        )
        self.progress_status_label.pack(pady=(0, 20))

        # Button Frame
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(fill="x", padx=30, pady=(0, 20))
        self.button_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="a")
        self.button_frame.rowconfigure(0, weight=1)

        self.import_primary_button = ctk.CTkButton(
            self.button_frame,
            text="🚀 Importar Datos",
            font=ctk.CTkFont(size=16, weight="bold"), # Added font
            height=45, # Added height
            state="disabled",
            command=self.start_primary_import
        )
        self.import_primary_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.update_seguimiento_button = ctk.CTkButton(
            self.button_frame,
            text="🔄 Act. Seguimiento",
            font=ctk.CTkFont(size=16, weight="bold"), # Added font
            height=45, # Added height
            fg_color="orange",
            hover_color="darkorange",
            command=self.start_seguimiento_update
        )
        self.update_seguimiento_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.export_data_button = ctk.CTkButton(
            self.button_frame,
            text="📥 Exportar Datos",
            font=ctk.CTkFont(size=16, weight="bold"), # Added font
            height=45, # Added height
            fg_color="green",
            hover_color="darkgreen",
            command=self.export_data
        )
        self.export_data_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.clear_db_button = ctk.CTkButton(
            self.button_frame,
            text="🗑️ Limpiar BD",
            font=ctk.CTkFont(size=16, weight="bold"), # Added font
            height=45, # Added height
            fg_color="red",
            hover_color="darkred",
            command=self.confirm_clear_database
        )
        self.clear_db_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        # Stats Frame
        self.stats_frame = ctk.CTkFrame(self.main_frame, height=80)
        self.stats_frame.pack(fill="x", padx=30, pady=(0, 30))
        self.stats_frame.pack_propagate(False)

        self.stats_label = ctk.CTkLabel(
            self.stats_frame,
            text="📊 Registros en base de datos: 0",
            font=ctk.CTkFont(size=16, weight="bold") # Added font
        )
        self.stats_label.pack(pady=25) # Adjusted padding

    def select_primary_file_dialog(self):
        file_path = filedialog.askopenfilename(
            title=Messages.DIALOG_SELECT_FILE,
            filetypes=[("Archivos Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            self.selected_primary_file = file_path
            self.primary_file_label.configure(text=f"📄 {os.path.basename(file_path)}")
            self.import_primary_button.configure(state="normal")
            self.progress_status_label.configure(text=Messages.LABEL_FILE_SELECTED.format(os.path.basename(file_path)))


    def start_primary_import(self):
        if not self.selected_primary_file:
            messagebox.showerror(Messages.DIALOG_ERROR, Messages.ERROR_FILE_SELECTION)
            return
        
        self._disable_buttons()
        self.progress_status_label.configure(text=Messages.IMPORTING_DATA)
        self._start_task(
            lambda: self.controller.handle_primary_excel_import(Path(self.selected_primary_file), self._ui_progress_callback),
            "import_complete"
        )

    def start_seguimiento_update(self):
        file_path = filedialog.askopenfilename(
            title=Messages.DIALOG_SELECT_SEGUIMIENTO,
            filetypes=[("Archivos Excel", "*.xlsx *.xls"), ("Todos los archivos", "*.*")]
        )
        if not file_path:
            return
        
        self.selected_seguimiento_file = file_path
        self._disable_buttons()
        # Update label to show selected seguimiento file
        self.progress_status_label.configure(text=Messages.UPDATING_DATA.format(os.path.basename(file_path)))
        self._start_task(
            lambda: self.controller.handle_seguimiento_update_from_excel(Path(self.selected_seguimiento_file), self._ui_progress_callback),
            "seguimiento_complete"
        )

    def export_data(self):
        export_path = filedialog.asksaveasfilename(
            title=Messages.DIALOG_SAVE_FILE,
            defaultextension=".xlsx",
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
        )
        if not export_path:
            return
            
        self._disable_buttons()
        self.progress_status_label.configure(text=Messages.EXPORTING_DATA)
        self._start_task(
            lambda: self.controller.handle_excel_export(Path(export_path)),
            "export_complete"
        )

    def confirm_clear_database(self):
        if messagebox.askyesno(Messages.DIALOG_CONFIRM, 
                               Messages.CONFIRM_CLEAR_DB,
                               icon='warning'):
            self._disable_buttons()
            self.progress_status_label.configure(text=Messages.CLEANING_DB)
            self._start_task(
                lambda: self.controller.handle_clear_database(),
                "clear_complete"
            )

    def update_stats_display(self):
        """Actualiza el contador de registros en la interfaz"""
        try:
            count = self.controller.handle_get_stats()
            self.stats_label.configure(text=Messages.LABEL_STATS.format(count))
        except Exception as e:
            self.controller.logger.error(f"Error al obtener estadísticas: {str(e)}")
            self.stats_label.configure(text=Messages.ERROR_STATS)

    def _ui_progress_callback(self, progress_percentage: float, message: str = ""):
        self.progress_bar.set(progress_percentage / 100.0)
        if message: # Only update label if message is provided
            self.progress_status_label.configure(text=message)
        self.root.update_idletasks()

    def _start_task(self, task_callable: Callable, completion_event_type: str):
        """Ejecuta una tarea en un hilo separado para mantener la UI responsiva"""
        # Disable buttons before starting the task
        self._disable_buttons()

        def worker():
            success = False
            message_or_result = "Tarea fallida por defecto"
            try:
                success, message_or_result = task_callable()
            except Exception as e:
                self.controller.logger.error(f"Error en tarea {completion_event_type}: {str(e)}")
                message_or_result = Messages.ERROR_UNEXPECTED.format(str(e))
                success = False
            finally:
                # Schedule _handle_task_completion to run in the main thread
                self.root.after(0, self._handle_task_completion, completion_event_type, success, message_or_result)
        
        # Start the worker thread
        task_thread = threading.Thread(target=worker, daemon=True)
        task_thread.start()

    def _handle_task_completion(self, event_type: str, success: bool, result_message: str):
        self.progress_bar.set(1.0 if success else 0.0) # Ensure float for progress bar
        self.progress_status_label.configure(text=result_message)

        if success:
            messagebox.showinfo(Messages.DIALOG_SUCCESS, f"{event_type.replace('_', ' ').capitalize()}: {result_message}")
        else:
            messagebox.showerror(Messages.DIALOG_ERROR, f"{event_type.replace('_', ' ').capitalize()}: {result_message}")
        
        self._enable_buttons() # Re-enable buttons
        self.update_stats_display()
        
        # Reset UI elements after a delay
        self.root.after(3000, self.reset_progress_ui)

    def reset_progress_ui(self):
        self.progress_bar.set(0)
        self.progress_status_label.configure(text=Messages.WAITING_FILE)
        self.primary_file_label.configure(text=Messages.LABEL_NO_FILE)
        self.selected_primary_file = None
        self.selected_seguimiento_file = None # Reset seguimiento file as well
        self.import_primary_button.configure(state="disabled")
        # Ensure all buttons that could be disabled are re-enabled or set to initial state
        self._enable_buttons() # Call this to ensure consistent state

    def _disable_buttons(self):
        """Helper method to disable all interactive buttons during a task."""
        self.select_primary_file_button.configure(state="disabled")
        self.import_primary_button.configure(state="disabled")
        self.update_seguimiento_button.configure(state="disabled")
        self.export_data_button.configure(state="disabled")
        self.clear_db_button.configure(state="disabled")

    def _enable_buttons(self):
        """Helper method to enable buttons after a task, respecting initial states."""
        self.select_primary_file_button.configure(state="normal")
        # Import button should only be enabled if a primary file is selected
        if self.selected_primary_file:
            self.import_primary_button.configure(state="normal")
        else:
            self.import_primary_button.configure(state="disabled")
        self.update_seguimiento_button.configure(state="normal")
        self.export_data_button.configure(state="normal")
        self.clear_db_button.configure(state="normal")
