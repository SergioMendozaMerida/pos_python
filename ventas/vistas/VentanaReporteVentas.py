import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import reportes.CrearReportes as CR

class VentanaReporteVentas(tk.Frame):
    def __init__(self, parent, reporte_ventas):
        super().__init__(parent)
        self.parent = parent
        self.reporte_ventas = reporte_ventas
        self.tres_productos_mas_vendidos = reporte_ventas.tres_productos_mas_vendidos
        self.crear_reporte_ventas = CR.CrearReportes(reporte_ventas)
        self.hoy = datetime.date.today()
        self.nombre_reporte = f"{self.hoy} - reporte ventas"
        
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
            text="Filtros de Ventas",
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

        self.lbl_nombre_producto = tk.Label(
            self.frame_filtros, 
            text="Producto:", 
            bg=self.color_fondo,
            fg=self.color_primario,
            font=("Segoe UI", 9, "bold")
        )
        self.lbl_fecha_inicio = tk.Label(
            self.frame_filtros, 
            text="Fecha inicio:", 
            bg=self.color_fondo,
            fg=self.color_primario,
            font=("Segoe UI", 9, "bold")
        )
        self.lbl_fecha_fin = tk.Label(
            self.frame_filtros, 
            text="Fecha fin:", 
            bg=self.color_fondo,
            fg=self.color_primario,
            font=("Segoe UI", 9, "bold")
        )
        
        self.entry_nombre_producto = tk.Entry(
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
        
        self.bton_buscar = tk.Button(
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
            command=self.filtrar_ventas
        )
        self.bton_ordenar_desc = tk.Button(
            self.frame_filtros, 
            text="⬇️ Desc", 
            bg=self.color_secundario, 
            fg="white",
            font=("Arial", 8, "bold"),
            relief="flat", 
            bd=0,
            padx=10,
            cursor="hand2",
            activebackground="#5dade2",
            command=self.mostrar_ventas_desc
        )

        self.lbl_nombre_producto.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(0, 2))
        self.entry_nombre_producto.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=(0, 5), ipady=2)
        self.lbl_fecha_inicio.grid(row=0, column=1, sticky="w", padx=(0, 5), pady=(0, 2))
        self.entry_fecha_inicio.grid(row=1, column=1, sticky="ew", padx=(0, 5), pady=(0, 5), ipady=2)
        self.lbl_fecha_fin.grid(row=0, column=2, sticky="w", padx=(0, 5), pady=(0, 2))
        self.entry_fecha_fin.grid(row=1, column=2, sticky="ew", padx=(0, 5), pady=(0, 5), ipady=2)
        self.bton_buscar.grid(row=1, column=3, sticky="ew", padx=(5, 0), pady=(0, 5), ipady=2)
        self.bton_ordenar_desc.grid(row=1, column=4, sticky="ew", padx=(5, 0), pady=(0, 5), ipady=2)

        self.frame_filtros_predeterminados = tk.Frame(self.frame_filtros, bg=self.color_fondo)
        self.frame_filtros_predeterminados.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(5, 0))
        self.frame_filtros_predeterminados.grid_columnconfigure(0, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(1, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(2, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(3, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(4, weight=1)

        self.btn_ventas_hoy = tk.Button(
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
            command=self.filtrar_ventas_hoy
        )
        self.btn_ventas_semana = tk.Button(
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
            command=self.filtrar_ventas_semana
        )
        self.btn_ventas_mes = tk.Button(
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
            command=self.filtrar_ventas_mes
        )
        self.btn_ventas_año = tk.Button(
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
            command=self.filtrar_ventas_año
        )
        self.btn_limpiar_filtros = tk.Button(
            self.frame_filtros_predeterminados, 
            text="🗑️ Limpiar", 
            bg="#e74c3c", 
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

        self.btn_ventas_hoy.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        self.btn_ventas_semana.grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        self.btn_ventas_mes.grid(row=0, column=2, sticky="ew", padx=2, pady=2)
        self.btn_ventas_año.grid(row=0, column=3, sticky="ew", padx=2, pady=2)
        self.btn_limpiar_filtros.grid(row=0, column=4, sticky="ew", padx=2, pady=2)

        self.btns_filtros = [self.btn_ventas_hoy, self.btn_ventas_semana, self.btn_ventas_mes, self.btn_ventas_año]


        self.frame_tabla = tk.LabelFrame(
            self,
            text="Reporte de Ventas",
            font=("Segoe UI", 9, "bold"),
            bg="#ffffff",
            fg=self.color_primario,
            padx=3, 
            pady=3
        )
        self.frame_tabla.grid(row=1, column=0, sticky="nsew", padx=8, pady=2)
        self.frame_tabla.grid_rowconfigure(0, weight=1)
        self.frame_tabla.grid_columnconfigure(0, weight=1)

        columnas = ("No. Recibo", "Fecha", "Producto", "Cantidad", "Precio Unitario", "Total","utilidad")
        self.tabla_ventas = tk.ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=10)

        self.tabla_ventas.heading("No. Recibo", text="No. Recibo")
        self.tabla_ventas.heading("Fecha", text="Fecha")
        self.tabla_ventas.heading("Producto", text="Producto")
        self.tabla_ventas.heading("Cantidad", text="Cantidad")
        self.tabla_ventas.heading("Precio Unitario", text="Precio Unitario")
        self.tabla_ventas.heading("Total", text="Total")
        self.tabla_ventas.heading("utilidad", text="Utilidad")
        self.tabla_ventas.column("No. Recibo", width=100, anchor="center")
        self.tabla_ventas.column("Fecha", width=100, anchor="center")
        self.tabla_ventas.column("Producto", width=100, anchor="center")
        self.tabla_ventas.column("Cantidad", width=100, anchor="center")
        self.tabla_ventas.column("Precio Unitario", width=100, anchor="center")
        self.tabla_ventas.column("Total", width=100, anchor="center")
        self.tabla_ventas.column("utilidad", width=100, anchor="center")

        self.scroll_y = tk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla_ventas.yview)
        self.scroll_x = tk.Scrollbar(self.frame_tabla, orient="horizontal", command=self.tabla_ventas.xview)
        self.tabla_ventas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.tabla_ventas.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.frame_resumen_tabla = tk.LabelFrame(
            self, 
            text="Resumen",
            font=("Segoe UI", 9, "bold"),
            bg="#ffffff",
            fg=self.color_primario,
            padx=8, 
            pady=4
        )
        self.frame_resumen_tabla.grid(row=2, column=0, sticky="ew", padx=8, pady=2)
        self.frame_resumen_tabla.grid_columnconfigure(0, weight=1)

        self.lbl_total_ventas = tk.Label(
            self.frame_resumen_tabla, 
            text="Total Ventas: Q 0.00", 
            font=("Arial", 10, "bold"), 
            bg="#ffffff", 
            fg=self.color_primario
        )
        self.lbl_total_utilidades = tk.Label(
            self.frame_resumen_tabla, 
            text="Total Utilidades: Q 0.00", 
            font=("Arial", 10, "bold"), 
            bg="#ffffff", 
            fg=self.color_primario
        )

        self.lbl_total_ventas.grid(row=0, column=0, sticky="w", pady=(0, 2))
        self.lbl_total_utilidades.grid(row=1, column=0, sticky="w", pady=(0, 2))

        self.frame_botones_exportar = tk.Frame(self, bg=self.color_fondo, padx=8, pady=6)
        self.frame_botones_exportar.grid(row=3, column=0, sticky="ew", padx=8, pady=(2, 6))
        self.frame_botones_exportar.grid_columnconfigure(0, weight=1)
        self.frame_botones_exportar.grid_columnconfigure(1, weight=1)

        self.btn_exportar_excel = tk.Button(
            self.frame_botones_exportar, 
            text="📊 Exportar a Excel", 
            bg=self.color_boton, 
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat", 
            bd=0,
            padx=15,
            pady=6,
            cursor="hand2",
            activebackground=self.color_boton_hover,
            command=self.generar_reporte_excel
        )
        self.btn_exportar_csv = tk.Button(
            self.frame_botones_exportar, 
            text="📄 Exportar a CSV", 
            bg=self.color_secundario, 
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat", 
            bd=0,
            padx=15,
            pady=6,
            cursor="hand2",
            activebackground="#5dade2"
        )

        self.btn_exportar_excel.grid(row=0, column=0, sticky="ew", padx=(0, 3))
        self.btn_exportar_csv.grid(row=0, column=1, sticky="ew", padx=(3, 0))

        self.mostrar_ventas(self.reporte_ventas.ventas)

        #columnas = ("No. Recibo", "Fecha", "Producto", "Cantidad", "Precio Unitario", "Total")
    def mostrar_ventas(self, ventas):
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)

        for venta in ventas:
            self.tabla_ventas.insert("", "end", values=(
                venta.id_recibo,
                venta.fecha,
                venta.producto,
                venta.cantidad,
                f"Q {float(venta.precio):,.2f}",
                f"Q {float(venta.sub_total):,.2f}",
                f"Q {float(venta.utilidad):,.2f}"
            ))

        self.lbl_total_ventas.config(text=f"Total Ventas: Q {self.reporte_ventas.total_ventas:,.2f}")

        total_utilidades = sum(float(v.utilidad) for v in ventas)
        self.lbl_total_utilidades.config(text=f"Total Utilidades: Q {total_utilidades:,.2f}")

        self.nombre_reporte = f"{self.hoy} - reporte ventas"

    def mostrar_ventas_desc(self):
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)

        self.reporte_ventas.obtener_ventas_desc()

        for venta in self.reporte_ventas.ventas:
            self.tabla_ventas.insert("", "end", values=(
                venta.id_recibo,
                venta.fecha,
                venta.producto,
                venta.cantidad,
                f"Q {float(venta.precio):,.2f}",
                f"Q {float(venta.sub_total):,.2f}",
                f"Q {float(venta.utilidad):,.2f}"
            ))

        self.lbl_total_ventas.config(text=f"Total Ventas: Q {self.reporte_ventas.total_ventas:,.2f}")

        total_utilidades = sum(float(v.utilidad) for v in self.reporte_ventas.ventas)
        self.lbl_total_utilidades.config(text=f"Total Utilidades: Q {total_utilidades:,.2f}")

        self.nombre_reporte = f"{self.hoy} - reporte ventas"

    def actualizar_ventas(self):
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)

        self.reporte_ventas.obtener_ventas()

        for venta in self.reporte_ventas.ventas:
            self.tabla_ventas.insert("", "end", values=(
                venta.id_recibo,
                venta.fecha,
                venta.producto,
                venta.cantidad,
                f"Q {float(venta.precio):,.2f}",
                f"Q {float(venta.sub_total):,.2f}",
                f"Q {float(venta.utilidad):,.2f}"
            ))

        self.lbl_total_ventas.config(text=f"Total Ventas: Q {self.reporte_ventas.total_ventas:,.2f}")

        total_utilidades = sum(float(v.utilidad) for v in self.reporte_ventas.ventas)
        self.lbl_total_utilidades.config(text=f"Total Utilidades: Q {total_utilidades:,.2f}")

        self.nombre_reporte = f"{self.hoy} - reporte ventas"

    def filtrar_ventas(self):
        nombre_producto = self.entry_nombre_producto.get()
        fecha_inicio = self.entry_fecha_inicio.get()
        fecha_fin = self.entry_fecha_fin.get()
        self.reporte_ventas.filtrar_ventas(fecha_inicio, fecha_fin, nombre_producto)
        self.mostrar_ventas(self.reporte_ventas.ventas)
        self.limpiar_botones_filtros()

        self.crear_reporte_ventas.set_nombre(f"{nombre_producto} - {fecha_inicio} a {fecha_fin} reporte")

    def filtrar_ventas_hoy(self):
        self.limpiar_botones_filtros()
        self.btn_ventas_hoy.config(bg=self.color_btn_filtro_seleccionado)

        self.reporte_ventas.filtrar_ventas(datetime.date.today(), datetime.date.today(), "")

        self.mostrar_ventas(self.reporte_ventas.ventas)
        self.crear_reporte_ventas.set_nombre(f"{self.hoy} - Reporte Diario")

    def filtrar_ventas_semana(self):
        self.limpiar_botones_filtros()
        self.btn_ventas_semana.config(bg=self.color_btn_filtro_seleccionado)

        hoy = datetime.date.today()
        ayer = hoy - datetime.timedelta(days=1)
        inicio_semana = hoy - datetime.timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + datetime.timedelta(days=6)
        self.reporte_ventas.filtrar_ventas(inicio_semana, fin_semana, "")
        self.mostrar_ventas(self.reporte_ventas.ventas)
        self.crear_reporte_ventas.set_nombre(f"{inicio_semana} a {fin_semana} - Reporte Semanal")

    def filtrar_ventas_mes(self):
        self.limpiar_botones_filtros()
        self.btn_ventas_mes.config(bg=self.color_btn_filtro_seleccionado)

        hoy = datetime.date.today()
        inicio_mes = hoy.replace(day=1)
        # Para obtener el último día del mes, se puede tomar el primer día del siguiente mes y restarle un día
        if hoy.month == 12:
            fin_mes = inicio_mes.replace(year=hoy.year + 1, month=1) - datetime.timedelta(days=1)
        else:
            fin_mes = inicio_mes.replace(month=hoy.month + 1) - datetime.timedelta(days=1)

        self.reporte_ventas.filtrar_ventas(inicio_mes, fin_mes, "")
        self.mostrar_ventas(self.reporte_ventas.ventas)

        fecha = datetime.datetime.now()
        nombre_mes = fecha.strftime("%B")
        anio = fecha.strftime("%Y")

        self.crear_reporte_ventas.set_nombre(f"{anio} - {nombre_mes} - Reporte Mensual")

    def filtrar_ventas_año(self):
        self.limpiar_botones_filtros()
        self.btn_ventas_año.config(bg=self.color_btn_filtro_seleccionado)

        incio_año = datetime.date(datetime.date.today().year, 1, 1)
        fin_año = datetime.date(datetime.date.today().year, 12, 31)
        self.reporte_ventas.filtrar_ventas(incio_año, fin_año, "")
        self.mostrar_ventas(self.reporte_ventas.ventas)

        año = datetime.date.today().year

        self.crear_reporte_ventas.set_nombre(f"{año} Reporte Anual")

    def limpiar_botones_filtros(self):
        for btn in self.btns_filtros:
            btn.config(bg=self.color_btn_filtro, fg="white")

    def limpiar_filtros(self):
        self.entry_nombre_producto.delete(0, tk.END)
        self.entry_fecha_inicio.delete(0, tk.END)
        self.entry_fecha_fin.delete(0, tk.END)

        self.limpiar_botones_filtros()

        self.reporte_ventas.obtener_ventas()
        self.mostrar_ventas(self.reporte_ventas.ventas)

    def generar_reporte_excel(self):
        self.crear_reporte_ventas.crear_reporte_excel()
        messagebox.showinfo("Reporte Generado", "Reporte creado exitosamente.")
        