import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import inventario.logica.Inventario as inv
import inventario.vistas.FormProductos as FP
import inventario.vistas.EditarProducto as EP
import inventario.vistas.FrameIngresoStock as FIS
import categoria.FrameCategoria as FCAT
import inventario.logica.crearReporteInventario as CRI

class VentanaInventario(ctk.CTkFrame):
    def __init__(self, parent, usuario, actualizar_tabla_ingresos):
        super().__init__(parent, fg_color="#f4f6f9")
        
        # Configuración de colores
        self.color_fondo = "#f4f6f9"
        self.color_primario = "#2c3e50"
        self.color_secundario = "#0984e3"
        self.color_boton = "#27ae60"
        self.color_cancelar = "#d63031"
        self.color_border = "#dfe6e9"
        
        self.usuario = usuario
        self.actualizar_tabla_ingresos = actualizar_tabla_ingresos
        self.inventario = inv.Inventario(usuario)

        # Frame principal con padding
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Frame búsqueda
        self.frame_buscar = ctk.CTkFrame(
            self.main_frame, 
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color=self.color_border
        )
        self.frame_buscar.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            self.frame_buscar,
            text="Buscar Productos",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_primario
        ).pack(anchor="w", padx=15, pady=(12, 5))

        # Inputs y botón búsqueda
        label_frame = ctk.CTkFrame(self.frame_buscar, fg_color="transparent")
        label_frame.pack(fill="x", padx=15, pady=(0, 12))

        ctk.CTkLabel(
            label_frame, 
            text="Nombre:", 
            text_color=self.color_primario, 
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).pack(side="left", padx=(0, 5))

        self.entry_nombre = ctk.CTkEntry(
            label_frame, 
            width=200, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Nombre...",
            height=36
        )
        self.entry_nombre.pack(side="left", padx=(0, 15))
        self.entry_nombre.bind("<Return>", lambda e: self.buscar_producto(self.entry_nombre.get(), self.entry_descripcion.get(), self.entry_codigo.get()))
        self.entry_nombre.bind("<KeyRelease>", self.iniciar_espera)

        ctk.CTkLabel(
            label_frame, 
            text="Descripción:", 
            text_color=self.color_primario, 
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).pack(side="left", padx=(0, 5))

        self.entry_descripcion = ctk.CTkEntry(
            label_frame, 
            width=200, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Descripción...",
            height=36
        )
        self.entry_descripcion.pack(side="left", padx=(0, 15))
        self.entry_descripcion.bind("<Return>", lambda e: self.buscar_producto(self.entry_nombre.get(), self.entry_descripcion.get(), self.entry_codigo.get()))
        self.entry_descripcion.bind("<KeyRelease>", self.iniciar_espera)

        ctk.CTkLabel(
            label_frame, 
            text="Código:", 
            text_color=self.color_cancelar, 
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).pack(side="left", padx=(0, 5))

        self.entry_codigo = ctk.CTkEntry(
            label_frame, 
            width=200, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Código...",
            height=36
        )
        self.entry_codigo.pack(side="left", padx=(0, 15))
        self.entry_codigo.bind("<Return>", lambda e: self.buscar_producto(self.entry_nombre.get(), self.entry_descripcion.get(), self.entry_codigo.get()))
        self.entry_codigo.bind("<KeyRelease>", self.iniciar_espera)
        self.entry_codigo.focus()

        btn_buscar = ctk.CTkButton(
            label_frame, 
            text="🔍 Buscar",
            fg_color=self.color_secundario,
            hover_color="#74b9ff",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            width=100,
            command=lambda: self.buscar_producto(self.entry_nombre.get(), self.entry_descripcion.get(), self.entry_codigo.get())
        )
        btn_buscar.pack(side="left")

        # Frame para tabla y scrollbars
        self.frame_tabla = ctk.CTkFrame(
            self.main_frame,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color=self.color_border
        )
        self.frame_tabla.pack(fill="both", expand=True, pady=(0, 12))

        ctk.CTkLabel(
            self.frame_tabla,
            text="Inventario de Productos",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_primario
        ).pack(anchor="w", padx=15, pady=(10, 5))

        tabla_scroll_frame = ctk.CTkFrame(self.frame_tabla, fg_color="transparent")
        tabla_scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.columnas = ("id", "nombre", "descripcion", "presentacion", "categoria", "precio_compra", "precio_venta", "precio_blister", "precio_caja", 
                        "stock", "utilidad")
        self.tabla_productos = ttk.Treeview(tabla_scroll_frame, columns=self.columnas, show="headings", height=10)

        # Configurar headings
        self.tabla_productos.heading("id", text="ID")
        self.tabla_productos.heading("nombre", text="Producto")
        self.tabla_productos.heading("descripcion", text="Descripción")
        self.tabla_productos.heading("presentacion", text="Presentación")
        self.tabla_productos.heading("categoria", text="Categoría")
        self.tabla_productos.heading("precio_compra", text="P. Compra")
        self.tabla_productos.heading("precio_venta", text="P. Venta")
        self.tabla_productos.heading("precio_blister", text="P. Blíster")
        self.tabla_productos.heading("precio_caja", text="P. Caja")
        self.tabla_productos.heading("stock", text="Stock")
        self.tabla_productos.heading("utilidad", text="Utilidad")

        # Configurar ancho de columnas
        self.tabla_productos.column("id", width=0, stretch=False)
        self.tabla_productos.column("nombre", width=130, anchor="w")
        self.tabla_productos.column("descripcion", width=160, anchor="w")
        self.tabla_productos.column("presentacion", width=100, anchor="center")
        self.tabla_productos.column("categoria", width=100, anchor="center")
        self.tabla_productos.column("precio_compra", width=90, anchor="center")
        self.tabla_productos.column("precio_venta", width=90, anchor="center")
        self.tabla_productos.column("precio_blister", width=90, anchor="center")
        self.tabla_productos.column("precio_caja", width=90, anchor="center")
        self.tabla_productos.column("stock", width=70, anchor="center")
        self.tabla_productos.column("utilidad", width=80, anchor="center")

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

        # Scrollbars
        self.scroll_bar = ttk.Scrollbar(tabla_scroll_frame, orient="vertical", command=self.tabla_productos.yview)
        self.tabla_productos.configure(yscrollcommand=self.scroll_bar.set)
        
        self.scroll_barx = ttk.Scrollbar(tabla_scroll_frame, orient="horizontal", command=self.tabla_productos.xview)
        self.tabla_productos.configure(xscrollcommand=self.scroll_barx.set)

        self.tabla_productos.grid(row=0, column=0, sticky="nsew")
        self.scroll_bar.grid(row=0, column=1, sticky="ns")
        self.scroll_barx.grid(row=1, column=0, sticky="ew")
        
        tabla_scroll_frame.grid_rowconfigure(0, weight=1)
        tabla_scroll_frame.grid_columnconfigure(0, weight=1)

        # Frame de botones
        self.frame_botones = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_botones.pack(fill="x")

        self.btn_ingresar = ctk.CTkButton(
            self.frame_botones,
            text="➕ Nuevo",
            fg_color=self.color_boton,
            hover_color="#229954",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=40,
            command=self.abrir_formulario
        )
        self.btn_ingresar.pack(side="left", padx=(0, 10), pady=5)

        self.btn_editar = ctk.CTkButton(
            self.frame_botones,
            text="✏️ Editar",
            fg_color=self.color_secundario,
            hover_color="#74b9ff",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=40,
            command=self.abrir_editar_formulario
        )
        self.btn_editar.pack(side="left", padx=(0, 10), pady=5)

        self.btn_eliminar = ctk.CTkButton(
            self.frame_botones,
            text="🗑️ Eliminar",
            fg_color=self.color_cancelar,
            hover_color="#c0392b",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=40,
            command=self.eliminar_producto_seleccionado
        )
        self.btn_eliminar.pack(side="left", padx=(0, 10), pady=5)

        self.btn_categorias = ctk.CTkButton(
            self.frame_botones,
            text="🏷️ Categorías",
            fg_color="#e67e22",
            hover_color="#d35400",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=40,
            command=self.abrir_frame_categorias
        )
        self.btn_categorias.pack(side="left", padx=(0, 10), pady=5)

        self.btn_ingreso_stock = ctk.CTkButton(
            self.frame_botones,
            text="📦 Ingreso Stock",
            fg_color="#8e44ad",
            hover_color="#71368a",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=40,
            command=self.abrir_ingreso_stock
        )
        self.btn_ingreso_stock.pack(side="left", padx=(0, 10), pady=5)

        self.btn_exportar_excel = ctk.CTkButton(
            self.frame_botones,
            text="📊 Exportar",
            fg_color="#16a085",
            hover_color="#117864",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=40,
            command=self.exportar_a_excel
        )
        self.btn_exportar_excel.pack(side="left", padx=(0, 10), pady=5)

        self.cargar_productos()
        self.timer_id = None

    def exportar_a_excel(self):
        if not self.inventario.productos:
            messagebox.showwarning("Advertencia", "No hay productos para exportar.")
            return

        reporte = CRI.ReporteInventario(self.inventario)
        reporte.crear_reporte_excel()
        messagebox.showinfo("Éxito", f"Reporte de inventario exportado exitosamente a {reporte.ruta_documentos}/{reporte.nombre}.xlsx")
        
    def iniciar_espera(self, event):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.timer_id = self.after(700, lambda: self.buscar_producto(self.entry_nombre.get(), self.entry_descripcion.get(), self.entry_codigo.get()))

    def abrir_frame_categorias(self):
        FCAT.FrameCategoria(self)

    def abrir_formulario(self):
        formulario = FP.FormProductos(self, self.inventario, self.actualizar_tabla)

    def abrir_ingreso_stock(self):
        ingreso_stock = FIS.FrameIngresoStock(self, self.inventario, self.actualizar_tabla, self.actualizar_tabla_ingresos)
        ingreso_stock.focus()

    def cargar_productos(self):
        self.inventario.obtener_productos()
        self.mostrar_productos()

    def actualizar_tabla(self):
        self.cargar_productos()

    def mostrar_productos(self):
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        for producto in self.inventario.productos:
            self.tabla_productos.insert("", tk.END, values=(
                producto.id_producto,
                producto.nombre,
                producto.descripcion,
                producto.presentacion,
                producto.categoria,
                f"Q{producto.precio_compra:.2f}",
                f"Q{producto.precio_venta:.2f}",
                f"Q{producto.precio_blister:.2f}",
                f"Q{producto.precio_caja:.2f}",
                producto.stock,
                f"Q{producto.utilidad:.2f}"
            ))

    def buscar_producto(self, nombre="", descripcion="", codigo=""):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        self.inventario.buscar_producto(nombre, descripcion, codigo)
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        for producto in self.inventario.productos:
            self.tabla_productos.insert("", tk.END, values=(
                producto.id_producto,
                producto.nombre,
                producto.descripcion,
                producto.presentacion,
                producto.categoria,
                f"Q{producto.precio_compra:.2f}",
                f"Q{producto.precio_venta:.2f}",
                f"Q{producto.precio_blister:.2f}",
                f"Q{producto.precio_caja:.2f}",
                producto.stock,
                f"Q{producto.utilidad:.2f}"
            ))

    def abrir_editar_formulario(self):
        seleccion = self.tabla_productos.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione un producto de la tabla para editar.")
            return

        item = self.tabla_productos.item(seleccion[0])
        id_producto = item['values'][0]

        producto_seleccionado = None
        for producto in self.inventario.productos:
            if producto.id_producto == id_producto:
                producto_seleccionado = producto
                break

        if producto_seleccionado:
            formulario = EP.EditarProducto(self, self.inventario, producto_seleccionado, self.actualizar_tabla)

    def eliminar_producto_seleccionado(self):
        seleccion = self.tabla_productos.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione un producto de la tabla para eliminar.")
            return

        item = self.tabla_productos.item(seleccion[0])
        id_producto = item['values'][0]
        nombre_producto = item['values'][1]

        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar el producto '{nombre_producto}'?\n\nEsta acción no se puede deshacer."
        )

        if respuesta:
            try:
                self.inventario.eliminar_producto(id_producto)
                self.actualizar_tabla()
                messagebox.showinfo("Producto eliminado", f"El producto '{nombre_producto}' ha sido eliminado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el producto: {str(e)}")
