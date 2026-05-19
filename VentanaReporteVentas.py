import tkinter as tk
from tkinter import ttk

class VentanaReporteVentas(tk.Frame):
    def __init__(self, parent, reporte_ventas):
        super().__init__(parent)
        self.parent = parent
        self.reporte_ventas = reporte_ventas

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame_filtros = tk.Frame(self, bg="#f0f0f0", padx=10, pady=10)
        self.frame_filtros.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.frame_filtros.grid_columnconfigure(0, weight=1)
        self.frame_filtros.grid_columnconfigure(1, weight=1)
        self.frame_filtros.grid_columnconfigure(2, weight=1)
        self.frame_filtros.grid_columnconfigure(3, weight=0)

        self.lbl_nombre_producto = tk.Label(self.frame_filtros, text="Producto:", bg="#f0f0f0")
        self.lbl_fecha_inicio = tk.Label(self.frame_filtros, text="Fecha inicio:", bg="#f0f0f0")
        self.lbl_fecha_fin = tk.Label(self.frame_filtros, text="Fecha fin:", bg="#f0f0f0")
        self.entry_nombre_producto = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_fecha_inicio = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_fecha_fin = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.bton_buscar = tk.Button(self.frame_filtros, text="Buscar", bg="#0984e3", fg="white", relief="flat", cursor="hand2")

        self.lbl_nombre_producto.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(0, 5))
        self.entry_nombre_producto.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=(0, 10))
        self.lbl_fecha_inicio.grid(row=0, column=1, sticky="w", padx=(0, 5), pady=(0, 5))
        self.entry_fecha_inicio.grid(row=1, column=1, sticky="ew", padx=(0, 5), pady=(0, 10))
        self.lbl_fecha_fin.grid(row=0, column=2, sticky="w", padx=(0, 5), pady=(0, 5))
        self.entry_fecha_fin.grid(row=1, column=2, sticky="ew", padx=(0, 5), pady=(0, 10))
        self.bton_buscar.grid(row=1, column=3, sticky="ew", padx=(5, 0), pady=(0, 10))

        self.frame_filtros_predeterminados = tk.Frame(self.frame_filtros, bg="#f0f0f0")
        self.frame_filtros_predeterminados.grid(row=2, column=0, columnspan=4, sticky="ew")
        self.frame_filtros_predeterminados.grid_columnconfigure(0, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(1, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(2, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(3, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(4, weight=1)

        self.btn_ventas_hoy = tk.Button(self.frame_filtros_predeterminados, text="Ventas de Hoy", bg="#0984e3", fg="white", relief="flat", cursor="hand2")
        self.btn_ventas_semana = tk.Button(self.frame_filtros_predeterminados, text="Ventas de la Semana", bg="#0984e3", fg="white", relief="flat", cursor="hand2")
        self.btn_ventas_mes = tk.Button(self.frame_filtros_predeterminados, text="Ventas del Mes", bg="#0984e3", fg="white", relief="flat", cursor="hand2")
        self.btn_ventas_año = tk.Button(self.frame_filtros_predeterminados, text="Ventas del Año", bg="#0984e3", fg="white", relief="flat", cursor="hand2")
        self.btn_productos_mas_vendidos = tk.Button(self.frame_filtros_predeterminados, text="Productos Más Vendidos", bg="#0984e3", fg="white", relief="flat", cursor="hand2")

        self.btn_ventas_hoy.grid(row=0, column=0, sticky="ew", padx=3, pady=3)
        self.btn_ventas_semana.grid(row=0, column=1, sticky="ew", padx=3, pady=3)
        self.btn_ventas_mes.grid(row=0, column=2, sticky="ew", padx=3, pady=3)
        self.btn_ventas_año.grid(row=0, column=3, sticky="ew", padx=3, pady=3)
        self.btn_productos_mas_vendidos.grid(row=0, column=4, sticky="ew", padx=3, pady=3)

        self.frame_tabla = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
        self.frame_tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.frame_tabla.grid_rowconfigure(0, weight=1)
        self.frame_tabla.grid_columnconfigure(0, weight=1)

        columnas = ("No. Recibo", "Fecha", "Producto", "Cantidad", "Precio Unitario", "Total")
        self.tabla_ventas = tk.ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=10)

        self.tabla_ventas.heading("No. Recibo", text="No. Recibo")
        self.tabla_ventas.heading("Fecha", text="Fecha")
        self.tabla_ventas.heading("Producto", text="Producto")
        self.tabla_ventas.heading("Cantidad", text="Cantidad")
        self.tabla_ventas.heading("Precio Unitario", text="Precio Unitario")
        self.tabla_ventas.heading("Total", text="Total")

        self.tabla_ventas.column("No. Recibo", width=100, anchor="center")
        self.tabla_ventas.column("Fecha", width=100, anchor="center")
        self.tabla_ventas.column("Producto", width=100, anchor="center")
        self.tabla_ventas.column("Cantidad", width=100, anchor="center")
        self.tabla_ventas.column("Precio Unitario", width=100, anchor="center")
        self.tabla_ventas.column("Total", width=100, anchor="center")

        self.scroll_y = tk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla_ventas.yview)
        self.scroll_x = tk.Scrollbar(self.frame_tabla, orient="horizontal", command=self.tabla_ventas.xview)
        self.tabla_ventas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.tabla_ventas.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.frame_resumen_tabla = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
        self.frame_resumen_tabla.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.frame_resumen_tabla.grid_columnconfigure(0, weight=1)

        self.lbl_total_ventas = tk.Label(self.frame_resumen_tabla, text="Total Ventas: Q 0.00", font=("Arial", 12, "bold"), bg="#ffffff", fg="#333")
        self.lbl_producto_mas_vendido = tk.Label(self.frame_resumen_tabla, text="Producto Más Vendido: N/A", font=("Arial", 12), bg="#ffffff", fg="#333")
        self.lbl_segundo_producto_mas_vendido = tk.Label(self.frame_resumen_tabla, text="Segundo Producto Más Vendido: N/A", font=("Arial", 12), bg="#ffffff", fg="#333")
        self.lbl_tercer_producto_mas_vendido = tk.Label(self.frame_resumen_tabla, text="Tercer Producto Más Vendido: N/A", font=("Arial", 12), bg="#ffffff", fg="#333")

        self.lbl_total_ventas.grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.lbl_producto_mas_vendido.grid(row=1, column=0, sticky="w", pady=(0, 5))
        self.lbl_segundo_producto_mas_vendido.grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.lbl_tercer_producto_mas_vendido.grid(row=3, column=0, sticky="w")

        self.frame_botones_exportar = tk.Frame(self, bg="#f0f0f0", padx=10, pady=10)
        self.frame_botones_exportar.grid(row=3, column=0, sticky="ew", padx=10, pady=(5, 10))
        self.frame_botones_exportar.grid_columnconfigure(0, weight=1)
        self.frame_botones_exportar.grid_columnconfigure(1, weight=1)

        self.btn_exportar_excel = tk.Button(self.frame_botones_exportar, text="Exportar a Excel", bg="#0984e3", fg="white", relief="flat", cursor="hand2")
        self.btn_exportar_csv = tk.Button(self.frame_botones_exportar, text="Exportar a CSV", bg="#0984e3", fg="white", relief="flat", cursor="hand2")

        self.btn_exportar_excel.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.btn_exportar_csv.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        self.mostrar_ventas(self.reporte_ventas.ventas)

    def buscar_ventas(self, nombre_producto, fecha_inicio, fecha_fin):
        # Aquí iría la lógica para buscar las ventas según los filtros ingresados
        pass

        #columnas = ("No. Recibo", "Fecha", "Producto", "Cantidad", "Precio Unitario", "Total")
    def mostrar_ventas(self, ventas):
        for venta in ventas:
            self.tabla_ventas.insert("", "end", values=(
                venta.id_recibo,
                venta.fecha,
                venta.producto,
                venta.cantidad,
                venta.precio,
                venta.sub_total
            ))
