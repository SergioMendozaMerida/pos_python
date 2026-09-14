import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import reportes.CrearReportes as CR

class VentanaReporteVentas(ctk.CTkFrame):
    def __init__(self, parent, reporte_ventas):
        super().__init__(parent, fg_color="#f4f6f9")
        self.parent = parent
        self.reporte_ventas = reporte_ventas
        self.tres_productos_mas_vendidos = reporte_ventas.tres_productos_mas_vendidos
        self.crear_reporte_ventas = CR.CrearReportes(reporte_ventas)
        self.hoy = datetime.date.today()
        self.nombre_reporte = f"{self.hoy} - reporte ventas"
        
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
            text="Filtros de Ventas",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_primario
        ).grid(row=0, column=0, columnspan=5, sticky="w", padx=15, pady=(10, 5))

        self.lbl_nombre_producto = ctk.CTkLabel(
            self.frame_filtros, 
            text="Producto:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        self.lbl_fecha_inicio = ctk.CTkLabel(
            self.frame_filtros, 
            text="Fecha inicio:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        self.lbl_fecha_fin = ctk.CTkLabel(
            self.frame_filtros, 
            text="Fecha fin:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        
        self.entry_nombre_producto = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Nombre producto...",
            height=36
        )
        self.entry_fecha_inicio = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="YYYY-MM-DD",
            height=36
        )
        self.entry_fecha_fin = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="YYYY-MM-DD",
            height=36
        )
        
        self.bton_buscar = ctk.CTkButton(
            self.frame_filtros, 
            text="🔍 Buscar", 
            fg_color=self.color_secundario, 
            hover_color="#74b9ff",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            width=95,
            command=self.filtrar_ventas
        )
        self.bton_ordenar_desc = ctk.CTkButton(
            self.frame_filtros, 
            text="⬇️ Desc", 
            fg_color=self.color_secundario, 
            hover_color="#74b9ff",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            width=90,
            command=self.mostrar_ventas_desc
        )

        self.lbl_nombre_producto.grid(row=1, column=0, sticky="w", padx=15, pady=(0, 2))
        self.entry_nombre_producto.grid(row=2, column=0, sticky="ew", padx=(15, 5), pady=(0, 5))
        self.lbl_fecha_inicio.grid(row=1, column=1, sticky="w", padx=5, pady=(0, 2))
        self.entry_fecha_inicio.grid(row=2, column=1, sticky="ew", padx=5, pady=(0, 5))
        self.lbl_fecha_fin.grid(row=1, column=2, sticky="w", padx=5, pady=(0, 2))
        self.entry_fecha_fin.grid(row=2, column=2, sticky="ew", padx=5, pady=(0, 5))
        self.bton_buscar.grid(row=2, column=3, sticky="ew", padx=(5, 5), pady=(0, 5))
        self.bton_ordenar_desc.grid(row=2, column=4, sticky="ew", padx=(5, 15), pady=(0, 5))

        self.frame_filtros_predeterminados = ctk.CTkFrame(self.frame_filtros, fg_color="transparent")
        self.frame_filtros_predeterminados.grid(row=3, column=0, columnspan=5, sticky="ew", padx=15, pady=(5, 10))
        self.frame_filtros_predeterminados.grid_columnconfigure(0, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(1, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(2, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(3, weight=1)
        self.frame_filtros_predeterminados.grid_columnconfigure(4, weight=1)

        self.btn_ventas_hoy = ctk.CTkButton(
            self.frame_filtros_predeterminados, 
            text="📅 Hoy", 
            fg_color=self.color_btn_filtro, 
            hover_color="#5dade2",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            command=self.filtrar_ventas_hoy
        )
        self.btn_ventas_semana = ctk.CTkButton(
            self.frame_filtros_predeterminados, 
            text="📊 Semana", 
            fg_color=self.color_btn_filtro, 
            hover_color="#5dade2",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            command=self.filtrar_ventas_semana
        )
        self.btn_ventas_mes = ctk.CTkButton(
            self.frame_filtros_predeterminados, 
            text="📈 Mes", 
            fg_color=self.color_btn_filtro, 
            hover_color="#5dade2",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            command=self.filtrar_ventas_mes
        )
        self.btn_ventas_año = ctk.CTkButton(
            self.frame_filtros_predeterminados, 
            text="📑 Año", 
            fg_color=self.color_btn_filtro, 
            hover_color="#5dade2",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            command=self.filtrar_ventas_año
        )
        self.btn_limpiar_filtros = ctk.CTkButton(
            self.frame_filtros_predeterminados, 
            text="🗑️ Limpiar", 
            fg_color="#d63031", 
            hover_color="#c0392b",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            command=self.limpiar_filtros
        )

        self.btn_ventas_hoy.grid(row=0, column=0, sticky="ew", padx=3, pady=2)
        self.btn_ventas_semana.grid(row=0, column=1, sticky="ew", padx=3, pady=2)
        self.btn_ventas_mes.grid(row=0, column=2, sticky="ew", padx=3, pady=2)
        self.btn_ventas_año.grid(row=0, column=3, sticky="ew", padx=3, pady=2)
        self.btn_limpiar_filtros.grid(row=0, column=4, sticky="ew", padx=3, pady=2)

        self.btns_filtros = [self.btn_ventas_hoy, self.btn_ventas_semana, self.btn_ventas_mes, self.btn_ventas_año]

        # 2. Frame Tabla
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
            text="Reporte de Ventas",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_primario
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(10, 5))

        tabla_inner_frame = ctk.CTkFrame(self.frame_tabla, fg_color="transparent")
        tabla_inner_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        tabla_inner_frame.grid_rowconfigure(0, weight=1)
        tabla_inner_frame.grid_columnconfigure(0, weight=1)

        columnas = ("No. Recibo", "Fecha", "Producto", "Cantidad", "Precio Unitario", "Total", "utilidad", "Descuento")
        self.tabla_ventas = ttk.Treeview(tabla_inner_frame, columns=columnas, show="headings", height=10)

        self.tabla_ventas.heading("No. Recibo", text="No. Recibo")
        self.tabla_ventas.heading("Fecha", text="Fecha")
        self.tabla_ventas.heading("Producto", text="Producto")
        self.tabla_ventas.heading("Cantidad", text="Cantidad")
        self.tabla_ventas.heading("Precio Unitario", text="Precio Unitario")
        self.tabla_ventas.heading("Total", text="Total")
        self.tabla_ventas.heading("utilidad", text="Utilidad")
        self.tabla_ventas.heading("Descuento", text="Descuento")

        self.tabla_ventas.column("No. Recibo", width=100, anchor="center")
        self.tabla_ventas.column("Fecha", width=100, anchor="center")
        self.tabla_ventas.column("Producto", width=140, anchor="w")
        self.tabla_ventas.column("Cantidad", width=80, anchor="center")
        self.tabla_ventas.column("Precio Unitario", width=100, anchor="center")
        self.tabla_ventas.column("Total", width=100, anchor="center")
        self.tabla_ventas.column("utilidad", width=100, anchor="center")
        self.tabla_ventas.column("Descuento", width=100, anchor="center")

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

        self.scroll_y = ttk.Scrollbar(tabla_inner_frame, orient="vertical", command=self.tabla_ventas.yview)
        self.scroll_x = ttk.Scrollbar(tabla_inner_frame, orient="horizontal", command=self.tabla_ventas.xview)
        self.tabla_ventas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.tabla_ventas.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        # 3. Frame Resumen
        self.frame_resumen_tabla = ctk.CTkFrame(
            self, 
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color=self.color_border
        )
        self.frame_resumen_tabla.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.frame_resumen_tabla.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.frame_resumen_tabla,
            text="Resumen",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_primario
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(8, 2))

        resumen_labels_frame = ctk.CTkFrame(self.frame_resumen_tabla, fg_color="transparent")
        resumen_labels_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 10))

        self.lbl_total_ventas = ctk.CTkLabel(
            resumen_labels_frame, 
            text="Total Ventas: Q 0.00", 
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), 
            text_color=self.color_primario
        )
        self.lbl_total_utilidades = ctk.CTkLabel(
            resumen_labels_frame, 
            text="Total Utilidades: Q 0.00", 
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), 
            text_color=self.color_primario
        )

        self.lbl_total_ventas.grid(row=0, column=0, sticky="w", pady=(0, 2))
        self.lbl_total_utilidades.grid(row=1, column=0, sticky="w", pady=(0, 2))

        # 4. Frame Botón Exportar
        self.frame_botones_exportar = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones_exportar.grid(row=3, column=0, sticky="ew", padx=10, pady=(2, 10))
        self.frame_botones_exportar.grid_columnconfigure(0, weight=1)

        self.btn_exportar_excel = ctk.CTkButton(
            self.frame_botones_exportar, 
            text="📊 Exportar a Excel", 
            fg_color=self.color_boton, 
            hover_color="#229954",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=40,
            command=self.generar_reporte_excel
        )

        self.btn_exportar_excel.grid(row=0, column=0, sticky="ew")

        self.mostrar_ventas(self.reporte_ventas.ventas)

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
                f"Q {float(venta.utilidad):,.2f}",
                f"Q {float(venta.descuento):,.2f}"
            ))

        self.lbl_total_ventas.configure(text=f"Total Ventas: Q {self.reporte_ventas.total_ventas:,.2f}")

        total_utilidades = sum(float(v.utilidad) for v in ventas)
        self.lbl_total_utilidades.configure(text=f"Total Utilidades: Q {total_utilidades:,.2f}")

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
                f"Q {float(venta.utilidad):,.2f}",
                f"Q {float(venta.descuento):,.2f}"
            ))

        self.lbl_total_ventas.configure(text=f"Total Ventas: Q {self.reporte_ventas.total_ventas:,.2f}")

        total_utilidades = sum(float(v.utilidad) for v in self.reporte_ventas.ventas)
        self.lbl_total_utilidades.configure(text=f"Total Utilidades: Q {total_utilidades:,.2f}")

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
                f"Q {float(venta.utilidad):,.2f}",
                f"Q {float(venta.descuento):,.2f}"
            ))

        self.lbl_total_ventas.configure(text=f"Total Ventas: Q {self.reporte_ventas.total_ventas:,.2f}")

        total_utilidades = sum(float(v.utilidad) for v in self.reporte_ventas.ventas)
        self.lbl_total_utilidades.configure(text=f"Total Utilidades: Q {total_utilidades:,.2f}")

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
        self.btn_ventas_hoy.configure(fg_color=self.color_btn_filtro_seleccionado)

        self.reporte_ventas.filtrar_ventas(datetime.date.today(), datetime.date.today(), "")

        self.mostrar_ventas(self.reporte_ventas.ventas)
        self.crear_reporte_ventas.set_nombre(f"{self.hoy} - Reporte Diario")

    def filtrar_ventas_semana(self):
        self.limpiar_botones_filtros()
        self.btn_ventas_semana.configure(fg_color=self.color_btn_filtro_seleccionado)

        hoy = datetime.date.today()
        inicio_semana = hoy - datetime.timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + datetime.timedelta(days=6)
        self.reporte_ventas.filtrar_ventas(inicio_semana, fin_semana, "")
        self.mostrar_ventas(self.reporte_ventas.ventas)
        self.crear_reporte_ventas.set_nombre(f"{inicio_semana} a {fin_semana} - Reporte Semanal")

    def filtrar_ventas_mes(self):
        self.limpiar_botones_filtros()
        self.btn_ventas_mes.configure(fg_color=self.color_btn_filtro_seleccionado)

        hoy = datetime.date.today()
        inicio_mes = hoy.replace(day=1)
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
        self.btn_ventas_año.configure(fg_color=self.color_btn_filtro_seleccionado)

        incio_año = datetime.date(datetime.date.today().year, 1, 1)
        fin_año = datetime.date(datetime.date.today().year, 12, 31)
        self.reporte_ventas.filtrar_ventas(incio_año, fin_año, "")
        self.mostrar_ventas(self.reporte_ventas.ventas)

        año = datetime.date.today().year

        self.crear_reporte_ventas.set_nombre(f"{año} Reporte Anual")

    def limpiar_botones_filtros(self):
        for btn in self.btns_filtros:
            btn.configure(fg_color=self.color_btn_filtro, text_color="white")

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