import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import ingresos.ingresos as I
import datetime
import ingresos.CrearReporteIngresos as CRI
from assets.icons.AnabellIcons import AnabellIcons

class VentanaIngresosStock(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f4f6f9")

        self.registros = I.Ingresos()
        
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
            text="Filtros de Ingresos de Stock",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_primario
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(10, 8))

        # Fila horizontal única para los 4 campos y el botón buscar
        self.frame_filtros = ctk.CTkFrame(self.frame_contenedor_filtros, fg_color="transparent")
        self.frame_filtros.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 5))
        self.frame_filtros.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame_filtros.grid_columnconfigure(5, weight=0)
        self.frame_filtros.grid_columnconfigure(6, weight=0)

        # 1. Producto
        ctk.CTkLabel(
            self.frame_filtros, 
            text="Producto:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(0, 2))
        
        self.entry_producto = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Nombre producto...",
            height=36
        )
        self.entry_producto.grid(row=1, column=0, sticky="ew", padx=(0, 10))

        # 2. Proveedor
        ctk.CTkLabel(
            self.frame_filtros, 
            text="Proveedor:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=0, column=1, sticky="w", padx=(0, 5), pady=(0, 2))
        
        self.entry_proveedor = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Proveedor...",
            height=36
        )
        self.entry_proveedor.grid(row=1, column=1, sticky="ew", padx=(0, 10))

        # 3. Fecha Inicio
        ctk.CTkLabel(
            self.frame_filtros, 
            text="Fecha inicio:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=0, column=2, sticky="w", padx=(0, 5), pady=(0, 2))
        
        self.entry_fecha_inicio = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="YYYY-MM-DD",
            height=36
        )
        self.entry_fecha_inicio.grid(row=1, column=2, sticky="ew", padx=(0, 10))

        # 4. Fecha Fin
        ctk.CTkLabel(
            self.frame_filtros, 
            text="Fecha fin:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=0, column=3, sticky="w", padx=(0, 5), pady=(0, 2))
        
        self.entry_fecha_fin = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="YYYY-MM-DD",
            height=36
        )
        self.entry_fecha_fin.grid(row=1, column=3, sticky="ew", padx=(0, 10))

        # 5. Botón Buscar
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
            command=self.filtrar_ingresos
        )
        self.btn_buscar.grid(row=1, column=5, sticky="ew", padx=3)

        # Eventos Enter para buscar
        self.entry_producto.bind("<Return>", lambda e: self.filtrar_ingresos())
        self.entry_proveedor.bind("<Return>", lambda e: self.filtrar_ingresos())
        self.entry_fecha_inicio.bind("<Return>", lambda e: self.filtrar_ingresos())
        self.entry_fecha_fin.bind("<Return>", lambda e: self.filtrar_ingresos())

        self.lbl_filtros_pre = ctk.CTkLabel(
            self.frame_filtros,
            text="Filtros predeterminados:",
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        self.lbl_filtros_pre.grid(row=0, column=4, sticky="w", padx=3, pady=(0, 2))

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
        self.filtros_pre.grid(row=1, column=4, sticky="ew", padx=3)

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
        self.btn_limpiar.grid(row=1, column=6, sticky="ew", padx=3)

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
            text="Historial de Ingresos de Stock",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_primario
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(10, 5))

        tabla_inner_frame = ctk.CTkFrame(self.frame_tabla, fg_color="transparent")
        tabla_inner_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        tabla_inner_frame.grid_rowconfigure(0, weight=1)
        tabla_inner_frame.grid_columnconfigure(0, weight=1)

        self.tabla_ingresos = ttk.Treeview(
            tabla_inner_frame, 
            columns=("Fecha", "Producto", "Cantidad", "Precio Compra", "Precio Venta", "Proveedor", "Usuario"), 
            show="headings", 
            height=10
        )
        
        self.tabla_ingresos.heading("Fecha", text="Fecha")
        self.tabla_ingresos.heading("Producto", text="Producto")
        self.tabla_ingresos.heading("Cantidad", text="Cantidad")
        self.tabla_ingresos.heading("Precio Compra", text="Precio Compra")
        self.tabla_ingresos.heading("Precio Venta", text="Precio Venta")
        self.tabla_ingresos.heading("Proveedor", text="Proveedor")
        self.tabla_ingresos.heading("Usuario", text="Usuario")

        self.tabla_ingresos.column("Fecha", width=130, anchor="center")
        self.tabla_ingresos.column("Producto", width=180, anchor="w")
        self.tabla_ingresos.column("Cantidad", width=80, anchor="center")
        self.tabla_ingresos.column("Precio Compra", width=100, anchor="e")
        self.tabla_ingresos.column("Precio Venta", width=100, anchor="e")
        self.tabla_ingresos.column("Proveedor", width=130, anchor="w")
        self.tabla_ingresos.column("Usuario", width=100, anchor="center")

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

        self.scroll_y = ttk.Scrollbar(tabla_inner_frame, orient="vertical", command=self.tabla_ingresos.yview)
        self.tabla_ingresos.configure(yscrollcommand=self.scroll_y.set)
        self.tabla_ingresos.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")

        # 3. FRAME BOTÓN EXPORTAR
        self.frame_botones_opciones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones_opciones.grid(row=2, column=0, sticky="ew", padx=10, pady=(2, 10))
        self.frame_botones_opciones.grid_columnconfigure(0, weight=1)
        self.frame_botones_opciones.grid_columnconfigure(1, weight=0)

        self.btn_exportar_ingresos_excel = ctk.CTkButton(
            self.frame_botones_opciones,
            text="Exportar a Excel",
            image=self.icono_exportar,
            fg_color="#27ae60",
            hover_color="#229954",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            width=180,
            command=self.exportar_ingresos_excel
        )
        self.btn_exportar_ingresos_excel.grid(row=0, column=1, sticky="e")

        self.actualizar_tabla()

    def actualizar_tabla(self):
        self.registros.obtener_ingresos()
        self.mostrar_ingresos()

    def mostrar_ingresos(self):
        for item in self.tabla_ingresos.get_children():
            self.tabla_ingresos.delete(item)

        for ingreso in self.registros.ingresos:
            self.tabla_ingresos.insert("", tk.END, values=(
                ingreso.fecha_ingreso,
                ingreso.producto,
                ingreso.cantidad,
                f"Q {float(ingreso.precio_compra):,.2f}",
                f"Q {float(ingreso.precio_venta):,.2f}",
                ingreso.proveedor,
                ingreso.usuario
            ))

    def filtrar_ingresos(self):
        producto = self.entry_producto.get()
        proveedor = self.entry_proveedor.get()
        f_inicio = self.entry_fecha_inicio.get()
        f_fin = self.entry_fecha_fin.get()

        self.registros.filtrar_ingresos(producto, proveedor, f_inicio, f_fin)
        self.mostrar_ingresos()

    def filtrar_hoy(self):
        self.limpiar_filtros_entries()
        hoy = datetime.date.today().strftime("%Y-%m-%d")
        self.registros.filtrar_ingresos("", "", hoy, hoy)
        self.mostrar_ingresos()

    def filtrar_semana(self):
        self.limpiar_filtros_entries()
        hoy = datetime.date.today()
        inicio = (hoy - datetime.timedelta(days=hoy.weekday())).strftime("%Y-%m-%d")
        fin = hoy.strftime("%Y-%m-%d")
        self.registros.filtrar_ingresos("", "", inicio, fin)
        self.mostrar_ingresos()

    def filtrar_mes(self):
        self.limpiar_filtros_entries()
        hoy = datetime.date.today()
        inicio = hoy.replace(day=1).strftime("%Y-%m-%d")
        self.registros.filtrar_ingresos("", "", inicio, "")
        self.mostrar_ingresos()

    def filtrar_anio(self):
        self.limpiar_filtros_entries()
        inicio = datetime.date(datetime.date.today().year, 1, 1).strftime("%Y-%m-%d")
        self.registros.filtrar_ingresos("", "", inicio, "")
        self.mostrar_ingresos()

    def limpiar_filtros(self):
        self.limpiar_filtros_entries()
        self.actualizar_tabla()

    def limpiar_filtros_entries(self):
        self.entry_producto.delete(0, tk.END)
        self.entry_proveedor.delete(0, tk.END)
        self.entry_fecha_inicio.delete(0, tk.END)
        self.entry_fecha_fin.delete(0, tk.END)

    def exportar_ingresos_excel(self):
        if not self.registros.ingresos:
            messagebox.showwarning("Advertencia", "No hay ingresos para exportar.")
            return

        reporte = CRI.ReporteIngresos(self.registros)
        reporte.crear_reporte_excel()
        messagebox.showinfo("Éxito", f"Reporte de ingresos exportado exitosamente a {reporte.ruta_documentos}/{reporte.nombre}.xlsx")