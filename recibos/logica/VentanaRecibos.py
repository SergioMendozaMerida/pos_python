import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from pathlib import Path
import recibos.logica.Recibos as R
import recibos.logica.CrearReporteRecibos as CRR
import datetime
import recibos.vistas.FrameDetalleRecibo as FDR
import os

class VentanaRecibos(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f4f6f9")

        self.recibos = R.Recibos()
        self.hoy = datetime.date.today()

        # Configuración de colores
        self.color_fondo = "#f4f6f9"
        self.color_primario = "#2c3e50"
        self.color_secundario = "#0984e3"
        self.color_boton = "#27ae60"
        self.color_cancelar = "#d63031"
        self.color_boton_hover = "#229954"
        self.color_border = "#dfe6e9"

        self.color_btn_filtro = "#0984e3"
        self.color_btn_filtro_seleccionado = "#5dade2"

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 1. Frame Filtros
        self.frame_filtros = ctk.CTkFrame(
            self, 
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color=self.color_border
        )
        self.frame_filtros.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.frame_filtros.grid_columnconfigure(0, weight=1)
        self.frame_filtros.grid_columnconfigure(1, weight=1)
        self.frame_filtros.grid_columnconfigure(2, weight=1)
        self.frame_filtros.grid_columnconfigure(3, weight=0)

        ctk.CTkLabel(
            self.frame_filtros,
            text="Filtros de Recibos",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_primario
        ).grid(row=0, column=0, columnspan=4, sticky="w", padx=15, pady=(10, 5))

        # Labels y Entries para filtros
        ctk.CTkLabel(
            self.frame_filtros, 
            text="No. Recibo:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=1, column=0, sticky="w", padx=15, pady=(0, 2))
        
        self.entry_no_recibo = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="No. Recibo...",
            height=36
        )
        self.entry_no_recibo.grid(row=2, column=0, sticky="ew", padx=(15, 5), pady=(0, 5))

        ctk.CTkLabel(
            self.frame_filtros, 
            text="Cliente:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=1, column=1, sticky="w", padx=5, pady=(0, 2))
        
        self.entry_nombre_cliente = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Nombre cliente...",
            height=36
        )
        self.entry_nombre_cliente.grid(row=2, column=1, sticky="ew", padx=5, pady=(0, 5))

        ctk.CTkLabel(
            self.frame_filtros, 
            text="DPI:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=1, column=2, sticky="w", padx=5, pady=(0, 2))
        
        self.entry_dpi = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="DPI...",
            height=36
        )
        self.entry_dpi.grid(row=2, column=2, sticky="ew", padx=(5, 15), pady=(0, 5))

        ctk.CTkLabel(
            self.frame_filtros, 
            text="NIT:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=3, column=0, sticky="w", padx=15, pady=(0, 2))
        
        self.entry_nit = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="NIT...",
            height=36
        )
        self.entry_nit.grid(row=4, column=0, sticky="ew", padx=(15, 5), pady=(0, 5))

        ctk.CTkLabel(
            self.frame_filtros, 
            text="Fecha inicio:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=3, column=1, sticky="w", padx=5, pady=(0, 2))
        
        self.entry_fecha_inicio = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="YYYY-MM-DD",
            height=36
        )
        self.entry_fecha_inicio.grid(row=4, column=1, sticky="ew", padx=5, pady=(0, 5))

        ctk.CTkLabel(
            self.frame_filtros, 
            text="Fecha fin:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=3, column=2, sticky="w", padx=5, pady=(0, 2))
        
        self.entry_fecha_fin = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="YYYY-MM-DD",
            height=36
        )
        self.entry_fecha_fin.grid(row=4, column=2, sticky="ew", padx=5, pady=(0, 5))

        self.btn_buscar = ctk.CTkButton(
            self.frame_filtros, 
            text="🔍 Buscar", 
            fg_color=self.color_secundario, 
            hover_color="#74b9ff",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            width=100,
            command=self.filtrar_recibos
        )
        self.btn_buscar.grid(row=4, column=3, sticky="ew", padx=(5, 15), pady=(0, 5))

        self.entry_no_recibo.bind("<Return>", lambda event: self.filtrar_recibos())
        self.entry_nombre_cliente.bind("<Return>", lambda event: self.filtrar_recibos())
        self.entry_dpi.bind("<Return>", lambda event: self.filtrar_recibos())
        self.entry_nit.bind("<Return>", lambda event: self.filtrar_recibos())
        self.entry_fecha_inicio.bind("<Return>", lambda event: self.filtrar_recibos())
        self.entry_fecha_fin.bind("<Return>", lambda event: self.filtrar_recibos())
        
        self.frame_filtros_predeterminados = ctk.CTkFrame(self.frame_filtros, fg_color="transparent")
        self.frame_filtros_predeterminados.grid(row=5, column=0, columnspan=4, sticky="ew", padx=15, pady=(5, 10))
        self.frame_filtros_predeterminados.grid_columnconfigure(0, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(1, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(2, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(3, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(4, weight=1)

        self.btn_recibos_hoy = ctk.CTkButton(
            self.frame_filtros_predeterminados, 
            text="📅 Hoy", 
            fg_color=self.color_btn_filtro, 
            hover_color="#5dade2",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            command=self.filtrar_recibos_hoy
        )
        self.btn_recibos_hoy.grid(row=0, column=0, sticky="ew", padx=3, pady=2)
        
        self.btn_recibos_semana = ctk.CTkButton(
            self.frame_filtros_predeterminados, 
            text="📊 Semana", 
            fg_color=self.color_btn_filtro, 
            hover_color="#5dade2",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            command=self.filtrar_recibos_semana
        )
        self.btn_recibos_semana.grid(row=0, column=1, sticky="ew", padx=3, pady=2)
        
        self.btn_recibios_mes = ctk.CTkButton(
            self.frame_filtros_predeterminados, 
            text="📈 Mes", 
            fg_color=self.color_btn_filtro, 
            hover_color="#5dade2",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            command=self.filtrar_recibos_mes
        )
        self.btn_recibios_mes.grid(row=0, column=2, sticky="ew", padx=3, pady=2)
        
        self.btn_recibos_anio = ctk.CTkButton(
            self.frame_filtros_predeterminados, 
            text="📑 Año", 
            fg_color=self.color_btn_filtro, 
            hover_color="#5dade2",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            command=self.filtrar_recibos_anio
        )
        self.btn_recibos_anio.grid(row=0, column=3, sticky="ew", padx=3, pady=2)
        
        self.btn_limpiar_filtros = ctk.CTkButton(
            self.frame_filtros_predeterminados, 
            text="🗑️ Limpiar", 
            fg_color=self.color_cancelar, 
            hover_color="#c0392b",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            command=self.limpiar_filtros
        )
        self.btn_limpiar_filtros.grid(row=0, column=4, sticky="ew", padx=3, pady=2)

        self.btns_filtros = [self.btn_recibos_hoy, self.btn_recibos_semana, self.btn_recibios_mes, self.btn_recibos_anio]

        # 2. Frame Tabla Recibos
        self.frame_tabla_recibos = ctk.CTkFrame(
            self,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color=self.color_border
        )
        self.frame_tabla_recibos.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.frame_tabla_recibos.grid_rowconfigure(1, weight=1)
        self.frame_tabla_recibos.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.frame_tabla_recibos,
            text="Recibos",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_primario
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(10, 5))

        tabla_inner_frame = ctk.CTkFrame(self.frame_tabla_recibos, fg_color="transparent")
        tabla_inner_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        tabla_inner_frame.grid_rowconfigure(0, weight=1)
        tabla_inner_frame.grid_columnconfigure(0, weight=1)

        columnas = ("No. Recibo", "Fecha", "Cliente", "Total", "utilidad", "Usuario")
        self.tabla_recibos = ttk.Treeview(tabla_inner_frame, columns=columnas, show="headings", height=10)

        self.tabla_recibos.heading("No. Recibo", text="No. Recibo")
        self.tabla_recibos.heading("Fecha", text="Fecha")
        self.tabla_recibos.heading("Cliente", text="Cliente")
        self.tabla_recibos.heading("Total", text="Total")
        self.tabla_recibos.heading("utilidad", text="Utilidad")
        self.tabla_recibos.heading("Usuario", text="Usuario")

        self.tabla_recibos.column("No. Recibo", width=100, anchor="center")
        self.tabla_recibos.column("Fecha", width=120, anchor="center")
        self.tabla_recibos.column("Cliente", width=250, anchor="w")
        self.tabla_recibos.column("Total", width=100, anchor="e")
        self.tabla_recibos.column("utilidad", width=100, anchor="e")
        self.tabla_recibos.column("Usuario", width=100, anchor="e")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#2d3436",
                        rowheight=34,
                        fieldbackground="#ffffff",
                        borderwidth=0,
                        font=("Segoe UI", 12))

        style.configure("Treeview.Heading",
                        background="#f1f2f6",
                        foreground="#2d3436",
                        relief="flat",
                        font=("Segoe UI", 12, "bold"))

        style.map("Treeview", 
                background=[('selected', "#74b9ff")],
                foreground=[('selected', "white")])

        self.scroll_y = ttk.Scrollbar(tabla_inner_frame, orient="vertical", command=self.tabla_recibos.yview)
        self.scroll_x = ttk.Scrollbar(tabla_inner_frame, orient="horizontal", command=self.tabla_recibos.xview)
        self.tabla_recibos.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.tabla_recibos.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        # 3. Frame Botones Opciones
        self.frame_botones_opciones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones_opciones.grid(row=2, column=0, sticky="ew", padx=10, pady=(2, 10))
        self.frame_botones_opciones.grid_rowconfigure(0, weight=1)
        self.frame_botones_opciones.grid_columnconfigure(0, weight=1, uniform="btns")
        self.frame_botones_opciones.grid_columnconfigure(1, weight=1, uniform="btns")
        self.frame_botones_opciones.grid_columnconfigure(2, weight=1, uniform="btns")

        self.btn_ver_ventas = ctk.CTkButton(
            self.frame_botones_opciones, 
            text="👁️ Ver Ventas del Recibo", 
            fg_color=self.color_secundario, 
            hover_color="#74b9ff",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=40,
            command=self.ver_detalle
        )
        self.btn_ver_ventas.grid(row=0, column=0, padx=(0, 3), sticky="nsew")
        
        self.btn_ver_recibo_pdf = ctk.CTkButton(
            self.frame_botones_opciones, 
            text="📄 Ver Recibo PDF", 
            fg_color=self.color_boton, 
            hover_color="#229954",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=40,
            command=self.ver_recibo_pdf
        )
        self.btn_ver_recibo_pdf.grid(row=0, column=1, padx=3, sticky="nsew")

        self.btn_exportar_recibos_excel = ctk.CTkButton(
            self.frame_botones_opciones,
            text="📤 Exportar Recibos a Excel",
            fg_color="#16a085",
            hover_color="#117864",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=40,
            command=self.exportar_recibos_excel
        )
        self.btn_exportar_recibos_excel.grid(row=0, column=2, padx=(3, 0), sticky="nsew")

        self.mostrar_recibos()

    def mostrar_recibos(self):
        for item in self.tabla_recibos.get_children():
            self.tabla_recibos.delete(item)

        recibos = self.recibos.recibos

        for recibo in recibos:
            self.tabla_recibos.insert("", "end", iid=recibo.no_recibo, values=(
                recibo.no_recibo,
                recibo.fecha,
                recibo.nombre_cliente,
                f"Q {recibo.total:,.2f}",
                f"Q {recibo.utilidad:,.2f}",
                recibo.usuario
            ))

    def actualizar_recibos(self):
        for item in self.tabla_recibos.get_children():
            self.tabla_recibos.delete(item)

        self.recibos.obtener_recibos()
        self.mostrar_recibos()

    def filtrar_recibos(self):
        no_recibo = self.entry_no_recibo.get()
        nombre_cliente = self.entry_nombre_cliente.get()
        dpi = self.entry_dpi.get()
        nit = self.entry_nit.get()
        fecha_inicio = self.entry_fecha_inicio.get()
        fecha_fin = self.entry_fecha_fin.get()

        self.recibos.filtrar_recibos(no_recibo, nombre_cliente, dpi, nit, fecha_inicio, fecha_fin)

        self.mostrar_recibos()
        self.limpiar_botones_filtros()

    def filtrar_recibos_hoy(self):
        self.limpiar_botones_filtros()
        self.btn_recibos_hoy.configure(fg_color=self.color_btn_filtro_seleccionado)
        
        self.limpiar_filtros()
        fecha_inicio = datetime.date.today().strftime("%Y-%m-%d")
        fecha_fin = datetime.date.today().strftime("%Y-%m-%d")

        self.recibos.filtrar_recibos("", "", "", "", fecha_inicio, fecha_fin)
        self.mostrar_recibos()

    def filtrar_recibos_semana(self):
        self.limpiar_botones_filtros()
        self.btn_recibos_semana.configure(fg_color=self.color_btn_filtro_seleccionado)
        
        self.limpiar_filtros()

        hoy = datetime.date.today()
        fecha_inicio = hoy - datetime.timedelta(days=hoy.weekday())
        fecha_fin = fecha_inicio + datetime.timedelta(days=6)

        self.recibos.filtrar_recibos("", "", "", "", fecha_inicio, fecha_fin)
        self.mostrar_recibos()

    def filtrar_recibos_mes(self):
        self.limpiar_botones_filtros()
        self.btn_recibios_mes.configure(fg_color=self.color_btn_filtro_seleccionado)

        self.limpiar_filtros()
        
        hoy = datetime.date.today()
        fecha_inicio = hoy.replace(day=1)
        if hoy.month == 12:
            fecha_fin = fecha_inicio.replace(year=hoy.year + 1, month=1) - datetime.timedelta(days=1)
        else:
            fecha_fin = fecha_inicio.replace(month=hoy.month + 1) - datetime.timedelta(days=1)

        self.recibos.filtrar_recibos("", "", "", "", fecha_inicio, fecha_fin)
        self.mostrar_recibos()

    def filtrar_recibos_anio(self):
        self.limpiar_botones_filtros()
        self.btn_recibos_anio.configure(fg_color=self.color_btn_filtro_seleccionado)
        
        self.limpiar_filtros()

        fecha_inicio = datetime.date(datetime.date.today().year, 1, 1)
        fecha_fin = datetime.date(datetime.date.today().year, 12, 31)

        self.recibos.filtrar_recibos("", "", "", "", fecha_inicio, fecha_fin)
        self.mostrar_recibos()

    def limpiar_filtros(self):
        self.entry_no_recibo.delete(0, tk.END)
        self.entry_nombre_cliente.delete(0, tk.END)
        self.entry_dpi.delete(0, tk.END)
        self.entry_nit.delete(0, tk.END)
        self.entry_fecha_inicio.delete(0, tk.END)
        self.entry_fecha_fin.delete(0, tk.END)
        self.limpiar_botones_filtros()
        self.recibos.obtener_recibos()
        self.mostrar_recibos()

    def limpiar_botones_filtros(self):
        for btn in self.btns_filtros:
            btn.configure(fg_color=self.color_btn_filtro, text_color="white")
        self.mostrar_recibos()

    def ver_detalle(self):
        selection = self.tabla_recibos.selection()

        if not selection:
            messagebox.showwarning("Seleccionar Recibo", "Por favor, seleccione un recibo para ver su detalle.")
            return

        item = selection[0]

        for v in self.recibos.recibos:
            if int(item) == int(v.no_recibo):
                detalle = FDR.FrameDetalleRecibo(self, v)
                break
                
    def ver_recibo_pdf(self):
        selection = self.tabla_recibos.selection()

        if not selection:
            messagebox.showwarning("Seleccionar Recibo", "Por favor, seleccione un recibo para ver su detalle.")
            return

        item = selection[0]
        self.ruta_documentos = Path.home() / "Documents/recibos_pos"
        os.startfile(f"{self.ruta_documentos}/recibo_{item}.pdf")

    def exportar_recibos_excel(self):
        if not getattr(self.recibos, 'recibos', None):
            messagebox.showwarning("Advertencia", "No hay recibos para exportar.")
            return

        reporte = CRR.CrearReporteRecibos(self.recibos)
        reporte.crear_reporte_excel()
        messagebox.showinfo(
            "Éxito",
            f"Reporte de recibos exportado exitosamente a {reporte.ruta_documentos}/{reporte.nombre}.xlsx"
        )
