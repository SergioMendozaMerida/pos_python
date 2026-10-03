import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import caja.SesionesCaja as SC
import caja.TablaSesionesCaja as TSC
import datetime
import caja.CrearReporteSesionCaja as CRSC
from assets.icons.AnabellIcons import AnabellIcons

class VentanaSesionesCaja(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f4f6f9")

        self.logica = SC.SesionesCaja()
        
        # Configuración de colores
        self.color_fondo = "#f4f6f9"
        self.color_primario = "#2c3e50"
        self.color_secundario = "#0984e3"
        self.color_boton = "#27ae60"
        self.color_cancelar = "#d63031"
        self.color_border = "#dfe6e9"

        self.color_btn_filtro = "#0984e3"
        self.color_btn_filtro_seleccionado = "#5dade2"

        self.icono_buscar = AnabellIcons.obtener_imagen("search_inventory")
        self.icono_limpiar = AnabellIcons.obtener_imagen("clean")
        self.icono_exportar = AnabellIcons.obtener_imagen("export")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 1. FRAME DE FILTROS
        self.frame_contenedor_filtros = ctk.CTkFrame(
            self, 
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color=self.color_border
        )
        self.frame_contenedor_filtros.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.frame_contenedor_filtros.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.frame_contenedor_filtros,
            text="Filtros de Sesiones de Caja",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_primario
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(10, 8))

        # Fila horizontal única para los campos y botón buscar
        self.frame_filtros = ctk.CTkFrame(self.frame_contenedor_filtros, fg_color="transparent")
        self.frame_filtros.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 5))
        self.frame_filtros.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.frame_filtros.grid_columnconfigure(4, weight=0)
        self.frame_filtros.grid_columnconfigure(5, weight=0)

        # 1. Usuario
        ctk.CTkLabel(
            self.frame_filtros, 
            text="Usuario:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(0, 2))
        
        self.entry_usuario = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Usuario...",
            height=36
        )
        self.entry_usuario.grid(row=1, column=0, sticky="ew", padx=(0, 10))

        # 2. Fecha Inicio
        ctk.CTkLabel(
            self.frame_filtros, 
            text="Fecha inicio:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=0, column=1, sticky="w", padx=(0, 5), pady=(0, 2))
        
        self.entry_fecha_inicio = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="YYYY-MM-DD",
            height=36
        )
        self.entry_fecha_inicio.grid(row=1, column=1, sticky="ew", padx=(0, 10))

        # 3. Fecha Fin
        ctk.CTkLabel(
            self.frame_filtros, 
            text="Fecha fin:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=0, column=2, sticky="w", padx=(0, 5), pady=(0, 2))
        
        self.entry_fecha_fin = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="YYYY-MM-DD",
            height=36
        )
        self.entry_fecha_fin.grid(row=1, column=2, sticky="ew", padx=(0, 10))

        # 4. Botón Buscar
        self.btn_buscar = ctk.CTkButton(
            self.frame_filtros,
            text="Buscar",
            image=self.icono_buscar,
            fg_color=self.color_secundario,
            hover_color="#74b9ff",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            width=100,
            command=self.filtrar_sesiones
        )
        self.btn_buscar.grid(row=1, column=4, sticky="ew", padx=3)

        # Eventos
        self.entry_usuario.bind("<Return>", lambda e: self.filtrar_sesiones())
        self.entry_fecha_inicio.bind("<Return>", lambda e: self.filtrar_sesiones())
        self.entry_fecha_fin.bind("<Return>", lambda e: self.filtrar_sesiones())

        self.lbl_filtros_pre = ctk.CTkLabel(
            self.frame_filtros,
            text="Filtros predeterminados:",
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        self.lbl_filtros_pre.grid(row=0, column=3, sticky="w", padx=3, pady=(0, 2))

        self.filtros_pre = ctk.CTkComboBox(
            self.frame_filtros,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            values=["Todo", "Hoy", "Semana", "Mes", "Año"],
            height=36,
            state="readonly",
            command=lambda valor: {
                "Todo": self.limpiar_filtros,
                "Hoy": self.filtrar_hoy,
                "Semana": self.filtrar_semana,
                "Mes": self.filtrar_mes,
                "Año": self.filtrar_anio
            }[valor]()
        )
        self.filtros_pre.set("Todo")
        self.filtros_pre.grid(row=1, column=3, sticky="ew", padx=3)

        self.btn_limpiar = ctk.CTkButton(
            self.frame_filtros,
            text="Limpiar",
            image=self.icono_limpiar,
            fg_color=self.color_cancelar,
            hover_color="#c0392b",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            command=self.limpiar_filtros
        )
        self.btn_limpiar.grid(row=1, column=5, sticky="ew", padx=3)

        # 2. FRAME TABLA
        self.frame_tabla = ctk.CTkFrame(
            self,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color=self.color_border
        )
        self.frame_tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.frame_tabla.grid_rowconfigure(1, weight=1)
        self.frame_tabla.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.frame_tabla,
            text="Historial de Sesiones de Caja",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_primario
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(10, 5))

        self.tabla_sesiones = TSC.TablaSesionesCaja(self.frame_tabla, self.logica.sesiones)
        self.tabla_sesiones.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # 3. FRAME BOTÓN EXPORTAR
        self.frame_botones_opciones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones_opciones.grid(row=2, column=0, sticky="ew", padx=10, pady=(2, 10))
        self.frame_botones_opciones.grid_columnconfigure(0, weight=1)
        self.frame_botones_opciones.grid_columnconfigure(1, weight=0)

        self.btn_exportar_sesiones_excel = ctk.CTkButton(
            self.frame_botones_opciones,
            text="Exportar Sesiones a Excel",
            image=self.icono_exportar,
            fg_color="#27ae60",
            hover_color="#229954",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=40,
            width=180,
            command=self.exportar_sesiones_excel
        )
        self.btn_exportar_sesiones_excel.grid(row=0, column=1, sticky="e")

        self.actualizar_tabla()

    def actualizar_tabla(self):
        self.logica.obtener_sesiones()
        self.mostrar_sesiones()

    def mostrar_sesiones(self):
        self.tabla_sesiones.actualizar(self.logica.sesiones)

    def filtrar_sesiones(self):
        self.logica.filtrar_sesiones(self.entry_fecha_inicio.get(), self.entry_fecha_fin.get(), self.entry_usuario.get())
        self.mostrar_sesiones()

    def filtrar_hoy(self):
        hoy = datetime.date.today().strftime("%Y-%m-%d")
        self.logica.filtrar_sesiones(hoy, hoy, "")
        self.mostrar_sesiones()

    def filtrar_semana(self):
        hoy = datetime.date.today()
        inicio = (hoy - datetime.timedelta(days=hoy.weekday())).strftime("%Y-%m-%d")
        fin = hoy.strftime("%Y-%m-%d")
        self.logica.filtrar_sesiones(inicio, fin, "")
        self.mostrar_sesiones()

    def filtrar_mes(self):
        hoy = datetime.date.today()
        inicio = hoy.replace(day=1).strftime("%Y-%m-%d")
        self.logica.filtrar_sesiones(inicio, "", "")
        self.mostrar_sesiones()

    def filtrar_anio(self):
        inicio = datetime.date(datetime.date.today().year, 1, 1).strftime("%Y-%m-%d")
        self.logica.filtrar_sesiones(inicio, "", "")
        self.mostrar_sesiones()

    def limpiar_filtros_entries(self):
        self.entry_usuario.delete(0, tk.END)
        self.entry_fecha_inicio.delete(0, tk.END)
        self.entry_fecha_fin.delete(0, tk.END)

    def limpiar_filtros(self):
        self.limpiar_filtros_entries()
        self.actualizar_tabla()

    def exportar_sesiones_excel(self):
        if not self.logica.sesiones:
            messagebox.showwarning("Advertencia", "No hay sesiones de caja para exportar.")
            return

        reporte = CRSC.ReporteSesionesCaja(self.logica)
        reporte.crear_reporte_excel()
        messagebox.showinfo("Éxito", f"Reporte de sesiones de caja exportado exitosamente a {reporte.ruta_documentos}/{reporte.nombre}.xlsx")