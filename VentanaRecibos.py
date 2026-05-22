import tkinter as tk
from tkinter import ttk
import Recibos as R
import datetime


class VentanaRecibos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.recibos = R.Recibos()
        self.hoy = datetime.date.today()

        self.configure(bg="#f0f0f0")

        self.color_btn_filtro = "#0984e3"
        self.color_btn_filtro_seleccionado = "#b6d1e6"

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame_filtros = tk.Frame(self, bg="#f0f0f0", padx=10, pady=10)
        self.frame_filtros.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.frame_filtros.grid_columnconfigure(0, weight=1)
        self.frame_filtros.grid_columnconfigure(1, weight=1)
        self.frame_filtros.grid_columnconfigure(2, weight=1)
        self.frame_filtros.grid_columnconfigure(3, weight=0) # Para el botón buscar

        # Labels y Entries para filtros
        tk.Label(self.frame_filtros, text="No. Recibo:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(0, 5))
        self.entry_no_recibo = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_no_recibo.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=(0, 10))

        tk.Label(self.frame_filtros, text="Cliente:", bg="#f0f0f0").grid(row=0, column=1, sticky="w", padx=(0, 5), pady=(0, 5))
        self.entry_nombre_cliente = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_nombre_cliente.grid(row=1, column=1, sticky="ew", padx=(0, 5), pady=(0, 10))

        tk.Label(self.frame_filtros, text="DPI:", bg="#f0f0f0").grid(row=0, column=2, sticky="w", padx=(0, 5), pady=(0, 5))
        self.entry_dpi = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_dpi.grid(row=1, column=2, sticky="ew", padx=(0, 5), pady=(0, 10))

        tk.Label(self.frame_filtros, text="NIT:", bg="#f0f0f0").grid(row=2, column=0, sticky="w", padx=(0, 5), pady=(0, 5))
        self.entry_nit = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_nit.grid(row=3, column=0, sticky="ew", padx=(0, 5), pady=(0, 10))

        tk.Label(self.frame_filtros, text="Fecha inicio:", bg="#f0f0f0").grid(row=2, column=1, sticky="w", padx=(0, 5), pady=(0, 5))
        self.entry_fecha_inicio = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_fecha_inicio.grid(row=3, column=1, sticky="ew", padx=(0, 5), pady=(0, 10))

        tk.Label(self.frame_filtros, text="Fecha fin:", bg="#f0f0f0").grid(row=2, column=2, sticky="w", padx=(0, 5), pady=(0, 5))
        self.entry_fecha_fin = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_fecha_fin.grid(row=3, column=2, sticky="ew", padx=(0, 5), pady=(0, 10))

        self.btn_buscar = tk.Button(self.frame_filtros, text="Buscar", bg="#0984e3", fg="white", relief="flat", cursor="hand2", command=self.filtrar_recibos)
        self.btn_buscar.grid(row=3, column=3, sticky="ew", padx=(5, 0), pady=(0, 10))
        
        self.frame_filtros_predeterminados = tk.Frame(self.frame_filtros, bg="#f0f0f0")
        self.frame_filtros_predeterminados.grid(row=4, column=0, columnspan=4, sticky="ew", pady=(5,0))
        self.frame_filtros_predeterminados.grid_columnconfigure(0, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(1, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(2, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(3, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(4, weight=1) # Para el botón limpiar

        self.btn_recibos_hoy = tk.Button(self.frame_filtros_predeterminados, text="Recibos de Hoy", bg=self.color_btn_filtro, fg="white", relief="flat", cursor="hand2", command=self.filtrar_recibos_hoy)
        self.btn_recibos_hoy.grid(row=0, column=0, sticky="ew", padx=3, pady=3)
        self.btn_recibos_semana = tk.Button(self.frame_filtros_predeterminados, text="Recibos de la Semana", bg=self.color_btn_filtro, fg="white", relief="flat", cursor="hand2", command=self.filtrar_recibos_semana)
        self.btn_recibos_semana.grid(row=0, column=1, sticky="ew", padx=3, pady=3)
        self.btn_recibios_mes = tk.Button(self.frame_filtros_predeterminados, text="Recibos del Mes", bg=self.color_btn_filtro, fg="white", relief="flat", cursor="hand2", command=self.filtrar_recibos_mes)
        self.btn_recibios_mes.grid(row=0, column=2, sticky="ew", padx=3, pady=3)
        self.btn_recibos_anio = tk.Button(self.frame_filtros_predeterminados, text="Recibos del Año", bg=self.color_btn_filtro, fg="white", relief="flat", cursor="hand2", command=self.filtrar_recibos_anio)
        self.btn_recibos_anio.grid(row=0, column=3, sticky="ew", padx=3, pady=3)
        self.btn_limpiar_filtros = tk.Button(self.frame_filtros_predeterminados, text="Limpiar Filtros", bg="#636e72", fg="white", relief="flat", cursor="hand2", command=self.limpiar_filtros)
        self.btn_limpiar_filtros.grid(row=0, column=4, sticky="ew", padx=3, pady=3)

        self.btns_filtros = [self.btn_recibos_hoy, self.btn_recibos_semana, self.btn_recibios_mes, self.btn_recibos_anio]

        self.frame_tabla_recibos = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
        self.frame_tabla_recibos.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.frame_tabla_recibos.grid_rowconfigure(0, weight=1)
        self.frame_tabla_recibos.grid_columnconfigure(0, weight=1)

        columnas = ("No. Recibo", "Fecha", "Cliente", "Total")
        self.tabla_recibos = ttk.Treeview(self.frame_tabla_recibos, columns=columnas, show="headings", height=10)

        self.tabla_recibos.heading("No. Recibo", text="No. Recibo")
        self.tabla_recibos.heading("Fecha", text="Fecha")
        self.tabla_recibos.heading("Cliente", text="Cliente")
        self.tabla_recibos.heading("Total", text="Total")

        self.tabla_recibos.column("No. Recibo", width=100, anchor="center")
        self.tabla_recibos.column("Fecha", width=120, anchor="center")
        self.tabla_recibos.column("Cliente", width=250, anchor="w")
        self.tabla_recibos.column("Total", width=100, anchor="e")

        self.scroll_y = tk.Scrollbar(self.frame_tabla_recibos, orient="vertical", command=self.tabla_recibos.yview)
        self.scroll_x = tk.Scrollbar(self.frame_tabla_recibos, orient="horizontal", command=self.tabla_recibos.xview)
        self.tabla_recibos.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.tabla_recibos.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.frame_botones_opciones = tk.Frame(self, bg="#f0f0f0", padx=10, pady=10)
        self.frame_botones_opciones.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
        self.frame_botones_opciones.grid_columnconfigure(0, weight=1)
        self.frame_botones_opciones.grid_columnconfigure(1, weight=1)

        self.btn_ver_ventas = tk.Button(self.frame_botones_opciones, text="Ver Ventas del Recibo", bg="#0984e3", fg="white", relief="flat", cursor="hand2")
        self.btn_ver_ventas.pack(side="left", padx=(0, 5), fill="x", expand=True)
        self.btn_ver_recibo_pdf = tk.Button(self.frame_botones_opciones, text="Ver Recibo PDF", bg="#00b894", fg="white", relief="flat", cursor="hand2")
        self.btn_ver_recibo_pdf.pack(side="left", padx=(5, 0), fill="x", expand=True)

        self.mostrar_recibos(self.recibos.recibos)

    def mostrar_recibos(self, recibos):
        for item in self.tabla_recibos.get_children():
            self.tabla_recibos.delete(item)

        for recibo in recibos:
            self.tabla_recibos.insert("", "end", values=(
                recibo.no_recibo,
                recibo.fecha,
                recibo.nombre_cliente,
                f"Q {recibo.total:,.2f}"
            ))

    def filtrar_recibos(self):
        # Lógica de filtrado de recibos
        # Aquí deberías llamar a un método en self.recibos para filtrar
        # y luego actualizar la tabla con self.mostrar_recibos()
        self.limpiar_botones_filtros()
        print("Filtrando recibos...")

    def filtrar_recibos_hoy(self):
        self.limpiar_botones_filtros()
        self.btn_recibos_hoy.config(bg=self.color_btn_filtro_seleccionado)
        # Lógica para filtrar recibos de hoy
        print("Filtrando recibos de hoy...")

    def filtrar_recibos_semana(self):
        self.limpiar_botones_filtros()
        self.btn_recibos_semana.config(bg=self.color_btn_filtro_seleccionado)
        # Lógica para filtrar recibos de la semana
        print("Filtrando recibos de la semana...")

    def filtrar_recibos_mes(self):
        self.limpiar_botones_filtros()
        self.btn_recibios_mes.config(bg=self.color_btn_filtro_seleccionado)
        # Lógica para filtrar recibos del mes
        print("Filtrando recibos del mes...")

    def filtrar_recibos_anio(self):
        self.limpiar_botones_filtros()
        self.btn_recibos_anio.config(bg=self.color_btn_filtro_seleccionado)
        # Lógica para filtrar recibos del año
        print("Filtrando recibos del año...")

    def limpiar_filtros(self):
        self.entry_no_recibo.delete(0, tk.END)
        self.entry_nombre_cliente.delete(0, tk.END)
        self.entry_dpi.delete(0, tk.END)
        self.entry_nit.delete(0, tk.END)
        self.entry_fecha_inicio.delete(0, tk.END)
        self.entry_fecha_fin.delete(0, tk.END)
        self.limpiar_botones_filtros()
        self.recibos.obtener_recibos() # Recargar todos los recibos
        self.mostrar_recibos(self.recibos.recibos)
        print("Filtros limpiados.")

    def limpiar_botones_filtros(self):
        for btn in self.btns_filtros:
            btn.config(bg=self.color_btn_filtro)
