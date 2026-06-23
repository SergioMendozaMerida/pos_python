import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
import recibos.logica.Recibos as R
import recibos.logica.CrearReporteRecibos as CRR
import datetime
import recibos.vistas.FrameDetalleRecibo as FDR
import os

class VentanaRecibos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.recibos = R.Recibos()
        self.hoy = datetime.date.today()

        # Configuración de colores (consistente con VentanaInventario)
        self.color_fondo = "#f0f0f0"
        self.color_primario = "#2c3e50"
        self.color_secundario = "#3498db"
        self.color_boton = "#27ae60"
        self.color_cancelar = "#e74c3c"
        self.color_boton_hover = "#229954"
        
        self.configure(bg=self.color_fondo)

        self.color_btn_filtro = "#0984e3"
        self.color_btn_filtro_seleccionado = "#5dade2"

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame_filtros = tk.LabelFrame(
            self, 
            text="Filtros de Recibos",
            font=("Segoe UI", 9, "bold"),
            bg=self.color_fondo,
            fg=self.color_primario,
            padx=10,
            pady=8
        )
        self.frame_filtros.grid(row=0, column=0, sticky="ew", padx=8, pady=(5, 2))
        self.frame_filtros.grid_columnconfigure(0, weight=1)
        self.frame_filtros.grid_columnconfigure(1, weight=1)
        self.frame_filtros.grid_columnconfigure(2, weight=1)
        self.frame_filtros.grid_columnconfigure(3, weight=0)

        # Labels y Entries para filtros
        tk.Label(
            self.frame_filtros, 
            text="No. Recibo:", 
            bg=self.color_fondo,
            fg=self.color_primario,
            font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(0, 5))
        self.entry_no_recibo = tk.Entry(
            self.frame_filtros, 
            bg="#ffffff", 
            fg="#2d3436",
            relief="flat", 
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=1, 
            highlightbackground="#b2bec3", 
            highlightcolor=self.color_secundario
        )
        self.entry_no_recibo.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=(0, 10), ipady=3)

        tk.Label(
            self.frame_filtros, 
            text="Cliente:", 
            bg=self.color_fondo,
            fg=self.color_primario,
            font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=1, sticky="w", padx=(0, 5), pady=(0, 5))
        self.entry_nombre_cliente = tk.Entry(
            self.frame_filtros, 
            bg="#ffffff", 
            fg="#2d3436",
            relief="flat", 
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=1, 
            highlightbackground="#b2bec3", 
            highlightcolor=self.color_secundario
        )
        self.entry_nombre_cliente.grid(row=1, column=1, sticky="ew", padx=(0, 5), pady=(0, 5), ipady=2)

        tk.Label(
            self.frame_filtros, 
            text="DPI:", 
            bg=self.color_fondo,
            fg=self.color_primario,
            font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=2, sticky="w", padx=(0, 5), pady=(0, 2))
        self.entry_dpi = tk.Entry(
            self.frame_filtros, 
            bg="#ffffff", 
            fg="#2d3436",
            relief="flat", 
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=1, 
            highlightbackground="#b2bec3", 
            highlightcolor=self.color_secundario
        )
        self.entry_dpi.grid(row=1, column=2, sticky="ew", padx=(0, 5), pady=(0, 5), ipady=2)

        tk.Label(
            self.frame_filtros, 
            text="NIT:", 
            bg=self.color_fondo,
            fg=self.color_primario,
            font=("Segoe UI", 9, "bold")
        ).grid(row=2, column=0, sticky="w", padx=(0, 5), pady=(0, 2))
        self.entry_nit = tk.Entry(
            self.frame_filtros, 
            bg="#ffffff", 
            fg="#2d3436",
            relief="flat", 
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=1, 
            highlightbackground="#b2bec3", 
            highlightcolor=self.color_secundario
        )
        self.entry_nit.grid(row=3, column=0, sticky="ew", padx=(0, 5), pady=(0, 5), ipady=2)

        tk.Label(
            self.frame_filtros, 
            text="Fecha inicio:", 
            bg=self.color_fondo,
            fg=self.color_primario,
            font=("Segoe UI", 9, "bold")
        ).grid(row=2, column=1, sticky="w", padx=(0, 5), pady=(0, 2))
        self.entry_fecha_inicio = tk.Entry(
            self.frame_filtros, 
            bg="#ffffff", 
            fg="#2d3436",
            relief="flat", 
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=1, 
            highlightbackground="#b2bec3", 
            highlightcolor=self.color_secundario
        )
        self.entry_fecha_inicio.grid(row=3, column=1, sticky="ew", padx=(0, 5), pady=(0, 5), ipady=2)

        tk.Label(
            self.frame_filtros, 
            text="Fecha fin:", 
            bg=self.color_fondo,
            fg=self.color_primario,
            font=("Segoe UI", 9, "bold")
        ).grid(row=2, column=2, sticky="w", padx=(0, 5), pady=(0, 2))
        self.entry_fecha_fin = tk.Entry(
            self.frame_filtros, 
            bg="#ffffff", 
            fg="#2d3436",
            relief="flat", 
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=1, 
            highlightbackground="#b2bec3", 
            highlightcolor=self.color_secundario
        )
        self.entry_fecha_fin.grid(row=3, column=2, sticky="ew", padx=(0, 5), pady=(0, 5), ipady=2)

        self.btn_buscar = tk.Button(
            self.frame_filtros, 
            text="🔍 Buscar", 
            bg=self.color_secundario, 
            fg="white",
            font=("Arial", 8, "bold"),
            relief="flat", 
            bd=0,
            padx=10,
            cursor="hand2",
            activebackground="#5dade2",
            command=self.filtrar_recibos
        )
        self.btn_buscar.grid(row=3, column=3, sticky="ew", padx=(5, 0), pady=(0, 5), ipady=2)

        self.entry_no_recibo.bind("<Return>", lambda event: self.filtrar_recibos())
        self.entry_nombre_cliente.bind("<Return>", lambda event: self.filtrar_recibos())
        self.entry_dpi.bind("<Return>", lambda event: self.filtrar_recibos())
        self.entry_nit.bind("<Return>", lambda event: self.filtrar_recibos())
        self.entry_fecha_inicio.bind("<Return>", lambda event: self.filtrar_recibos())
        self.entry_fecha_fin.bind("<Return>", lambda event: self.filtrar_recibos())
        
        self.frame_filtros_predeterminados = tk.Frame(self.frame_filtros, bg=self.color_fondo)
        self.frame_filtros_predeterminados.grid(row=4, column=0, columnspan=4, sticky="ew", pady=(5, 0))
        self.frame_filtros_predeterminados.grid_columnconfigure(0, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(1, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(2, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(3, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(4, weight=1)

        self.btn_recibos_hoy = tk.Button(
            self.frame_filtros_predeterminados, 
            text="📅 Hoy", 
            bg=self.color_btn_filtro, 
            fg="white",
            font=("Arial", 8, "bold"),
            relief="flat", 
            bd=0,
            padx=8,
            pady=4,
            cursor="hand2",
            activebackground="#5dade2",
            command=self.filtrar_recibos_hoy
        )
        self.btn_recibos_hoy.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        
        self.btn_recibos_semana = tk.Button(
            self.frame_filtros_predeterminados, 
            text="📊 Semana", 
            bg=self.color_btn_filtro, 
            fg="white",
            font=("Arial", 8, "bold"),
            relief="flat", 
            bd=0,
            padx=8,
            pady=4,
            cursor="hand2",
            activebackground="#5dade2",
            command=self.filtrar_recibos_semana
        )
        self.btn_recibos_semana.grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        
        self.btn_recibios_mes = tk.Button(
            self.frame_filtros_predeterminados, 
            text="📈 Mes", 
            bg=self.color_btn_filtro, 
            fg="white",
            font=("Arial", 8, "bold"),
            relief="flat", 
            bd=0,
            padx=8,
            pady=4,
            cursor="hand2",
            activebackground="#5dade2",
            command=self.filtrar_recibos_mes
        )
        self.btn_recibios_mes.grid(row=0, column=2, sticky="ew", padx=2, pady=2)
        
        self.btn_recibos_anio = tk.Button(
            self.frame_filtros_predeterminados, 
            text="📑 Año", 
            bg=self.color_btn_filtro, 
            fg="white",
            font=("Arial", 8, "bold"),
            relief="flat", 
            bd=0,
            padx=8,
            pady=4,
            cursor="hand2",
            activebackground="#5dade2",
            command=self.filtrar_recibos_anio
        )
        self.btn_recibos_anio.grid(row=0, column=3, sticky="ew", padx=2, pady=2)
        
        self.btn_limpiar_filtros = tk.Button(
            self.frame_filtros_predeterminados, 
            text="🗑️ Limpiar", 
            bg=self.color_cancelar, 
            fg="white",
            font=("Arial", 8, "bold"),
            relief="flat", 
            bd=0,
            padx=8,
            pady=4,
            cursor="hand2",
            activebackground="#c0392b",
            command=self.limpiar_filtros
        )
        self.btn_limpiar_filtros.grid(row=0, column=4, sticky="ew", padx=2, pady=2)

        self.btns_filtros = [self.btn_recibos_hoy, self.btn_recibos_semana, self.btn_recibios_mes, self.btn_recibos_anio]

        self.frame_tabla_recibos = tk.LabelFrame(
            self,
            text="Recibos",
            font=("Segoe UI", 9, "bold"),
            bg="#ffffff",
            fg=self.color_primario,
            padx=3, 
            pady=3
        )
        self.frame_tabla_recibos.grid(row=1, column=0, sticky="nsew", padx=8, pady=2)
        self.frame_tabla_recibos.grid_rowconfigure(0, weight=1)
        self.frame_tabla_recibos.grid_columnconfigure(0, weight=1)

        columnas = ("No. Recibo", "Fecha", "Cliente", "Total","utilidad", "Usuario")
        self.tabla_recibos = ttk.Treeview(self.frame_tabla_recibos, columns=columnas, show="headings", height=10)

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

        self.scroll_y = tk.Scrollbar(self.frame_tabla_recibos, orient="vertical", command=self.tabla_recibos.yview)
        self.scroll_x = tk.Scrollbar(self.frame_tabla_recibos, orient="horizontal", command=self.tabla_recibos.xview)
        self.tabla_recibos.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.tabla_recibos.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.frame_botones_opciones = tk.Frame(self, bg=self.color_fondo, padx=8, pady=6)
        self.frame_botones_opciones.grid(row=2, column=0, sticky="ew", padx=8, pady=(2, 6))
        self.frame_botones_opciones.grid_rowconfigure(0, weight=1)
        self.frame_botones_opciones.grid_columnconfigure(0, weight=1, uniform="btns")
        self.frame_botones_opciones.grid_columnconfigure(1, weight=1, uniform="btns")
        self.frame_botones_opciones.grid_columnconfigure(2, weight=1, uniform="btns")

        self.btn_ver_ventas = tk.Button(
            self.frame_botones_opciones, 
            text="👁️ Ver Ventas del Recibo", 
            bg=self.color_secundario, 
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat", 
            bd=0,
            padx=15,
            pady=6,
            cursor="hand2",
            activebackground="#5dade2",
            command=self.ver_detalle
        )
        self.btn_ver_ventas.grid(row=0, column=0, padx=(0, 3), sticky="nsew")
        
        self.btn_ver_recibo_pdf = tk.Button(
            self.frame_botones_opciones, 
            text="📄 Ver Recibo PDF", 
            bg=self.color_boton, 
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat", 
            bd=0,
            padx=15,
            pady=6,
            cursor="hand2",
            activebackground=self.color_boton_hover,
            command=self.ver_recibo_pdf
        )
        self.btn_ver_recibo_pdf.grid(row=0, column=1, padx=3, sticky="nsew")

        self.btn_exportar_recibos_excel = tk.Button(
            self.frame_botones_opciones,
            text="📤 Exportar Recibos a Excel",
            bg=self.color_boton,
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=6,
            cursor="hand2",
            activebackground=self.color_boton_hover,
            command=self.exportar_recibos_excel
        )
        self.btn_exportar_recibos_excel.grid(row=0, column=2, padx=(3, 0), sticky="nsew")

        self.mostrar_recibos()

    def mostrar_recibos(self):
        for item in self.tabla_recibos.get_children():
            self.tabla_recibos.delete(item)

        #self.recibos.obtener_recibos()
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
        self.btn_recibos_hoy.config(bg=self.color_btn_filtro_seleccionado)
        
        self.limpiar_filtros()
        fecha_inicio = datetime.date.today().strftime("%Y-%m-%d")
        fecha_fin = datetime.date.today().strftime("%Y-%m-%d")

        self.recibos.filtrar_recibos("", "", "", "", fecha_inicio, fecha_fin)

        self.mostrar_recibos()


    def filtrar_recibos_semana(self):
        self.limpiar_botones_filtros()
        self.btn_recibos_semana.config(bg=self.color_btn_filtro_seleccionado)
        
        self.limpiar_filtros()

        hoy = datetime.date.today()
        ayer = hoy - datetime.timedelta(days=1)
        fecha_inicio = hoy - datetime.timedelta(days=hoy.weekday())
        fecha_fin = fecha_inicio + datetime.timedelta(days=6)

        self.recibos.filtrar_recibos("", "", "", "", fecha_inicio, fecha_fin)

        self.mostrar_recibos()

    def filtrar_recibos_mes(self):
        self.limpiar_botones_filtros()
        self.btn_recibios_mes.config(bg=self.color_btn_filtro_seleccionado)

        self.limpiar_filtros()
        
        hoy = datetime.date.today()
        fecha_inicio = hoy.replace(day=1)
        # Para obtener el último día del mes, se puede tomar el primer día del siguiente mes y restarle un día
        if hoy.month == 12:
            fecha_fin = fecha_inicio.replace(year=hoy.year + 1, month=1) - datetime.timedelta(days=1)
        else:
            fecha_fin = fecha_inicio.replace(month=hoy.month + 1) - datetime.timedelta(days=1)

        self.recibos.filtrar_recibos("", "", "", "", fecha_inicio, fecha_fin)
        self.mostrar_recibos()

    def filtrar_recibos_anio(self):
        self.limpiar_botones_filtros()
        self.btn_recibos_anio.config(bg=self.color_btn_filtro_seleccionado)
        
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
        self.recibos.obtener_recibos() # Recargar todos los recibos
        self.mostrar_recibos()

    def limpiar_botones_filtros(self):
        for btn in self.btns_filtros:
            btn.config(bg=self.color_btn_filtro)
        self.mostrar_recibos()
    def ver_detalle(self):
        selection = self.tabla_recibos.selection()

        if not selection:
            messagebox.showwarning("Seleccionar Recibo", "Por favor, seleccione un recibo para ver su detalle.")
            return

        item = selection[0]

        for v in self.recibos.recibos:
            if int(item) == int(v.no_recibo):
                print(v.no_recibo)
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
