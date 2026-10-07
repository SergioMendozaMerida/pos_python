import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import inventario.logica.Inventario as inv
import inventario.vistas.FormProductos as FP
import inventario.vistas.EditarProducto as EP
import inventario.vistas.FrameIngresoStock as FIS
import inventario.vistas.tabla_inventario as TI
import categoria.FrameCategoria as FCAT
import inventario.logica.crearReporteInventario as CRI
from assets.icons.AnabellIcons import AnabellIcons

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

        self.icon_buscar = AnabellIcons.obtener_imagen('search_inventory')
        self.icon_add = AnabellIcons.obtener_imagen('add')
        self.icon_editar = AnabellIcons.obtener_imagen('edit')
        self.icon_categoria = AnabellIcons.obtener_imagen('category')
        self.icon_export = AnabellIcons.obtener_imagen('export')
        self.icon_agregar_stock = AnabellIcons.obtener_imagen('add_stock')
        self.icon_borrar = AnabellIcons.obtener_imagen('delete')
        self.vista_actual = "tabla_inventario"

        # Frame búsqueda
        self.frame_contenedor_filtros = ctk.CTkFrame(
            self.main_frame, 
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color=self.color_border
        )
        self.frame_contenedor_filtros.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            self.frame_contenedor_filtros,
            text="Buscar Productos",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_primario
        ).pack(anchor="w", padx=15, pady=(12, 5))

        # Inputs y botón búsqueda
        self.frame_filtros = ctk.CTkFrame(self.frame_contenedor_filtros, fg_color="transparent")
        self.frame_filtros.pack(fill="x", padx=15, pady=(0, 12))

        ctk.CTkLabel(
            self.frame_filtros, 
            text="Nombre:", 
            text_color=self.color_primario, 
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).pack(side="left", padx=(0, 5))

        self.entry_nombre = ctk.CTkEntry(
            self.frame_filtros, 
            width=200, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Nombre...",
            height=36
        )
        self.entry_nombre.pack(side="left", padx=(0, 15))
        self.entry_nombre.bind("<Return>", lambda e: self.buscar_producto(self.entry_nombre.get(), self.entry_descripcion.get(), self.entry_codigo.get()))
        self.entry_nombre.bind("<KeyRelease>", self.iniciar_espera)

        ctk.CTkLabel(
            self.frame_filtros, 
            text="Descripción:", 
            text_color=self.color_primario, 
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).pack(side="left", padx=(0, 5))

        self.entry_descripcion = ctk.CTkEntry(
            self.frame_filtros, 
            width=200, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Descripción...",
            height=36
        )
        self.entry_descripcion.pack(side="left", padx=(0, 15))
        self.entry_descripcion.bind("<Return>", lambda e: self.buscar_producto(self.entry_nombre.get(), self.entry_descripcion.get(), self.entry_codigo.get()))
        self.entry_descripcion.bind("<KeyRelease>", self.iniciar_espera)

        ctk.CTkLabel(
            self.frame_filtros, 
            text="Código:", 
            text_color=self.color_cancelar, 
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).pack(side="left", padx=(0, 5))

        self.entry_codigo = ctk.CTkEntry(
            self.frame_filtros, 
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
            self.frame_filtros, 
            text="Buscar",
            image=self.icon_buscar,
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

        # self.columnas = ("id", "nombre", "descripcion", "presentacion", "categoria", "precio_compra", "precio_venta", "precio_blister", "precio_caja",
        #                 "stock", "utilidad", "stock_minimo")
        # self.tabla_productos = ttk.Treeview(tabla_scroll_frame, columns=self.columnas, show="headings", height=10)
        #
        # # Configurar headings
        # self.tabla_productos.heading("id", text="ID")
        # self.tabla_productos.heading("nombre", text="Producto")
        # self.tabla_productos.heading("descripcion", text="Descripción")
        # self.tabla_productos.heading("presentacion", text="Presentación")
        # self.tabla_productos.heading("categoria", text="Categoría")
        # self.tabla_productos.heading("precio_compra", text="P. Compra")
        # self.tabla_productos.heading("precio_venta", text="P. Venta")
        # self.tabla_productos.heading("precio_blister", text="P. Blíster")
        # self.tabla_productos.heading("precio_caja", text="P. Caja")
        # self.tabla_productos.heading("stock", text="Stock")
        # self.tabla_productos.heading("utilidad", text="Utilidad")
        # self.tabla_productos.heading("stock_minimo", text="Stock Mínimo")
        # # Configurar ancho de columnas
        # self.tabla_productos.column("id", width=0, stretch=False)
        # self.tabla_productos.column("nombre", width=130, anchor="w")
        # self.tabla_productos.column("descripcion", width=160, anchor="w")
        # self.tabla_productos.column("presentacion", width=100, anchor="center")
        # self.tabla_productos.column("categoria", width=100, anchor="center")
        # self.tabla_productos.column("precio_compra", width=90, anchor="center")
        # self.tabla_productos.column("precio_venta", width=90, anchor="center")
        # self.tabla_productos.column("precio_blister", width=90, anchor="center")
        # self.tabla_productos.column("precio_caja", width=90, anchor="center")
        # self.tabla_productos.column("stock", width=70, anchor="center")
        # self.tabla_productos.column("utilidad", width=80, anchor="center")
        # self.tabla_productos.column("stock_minimo", width=90, anchor="center")
        # style = ttk.Style()
        # style.theme_use("clam")
        #
        # style.configure("Treeview",
        #                 background="#ffffff",
        #                 foreground="#2d3436",
        #                 rowheight=34,
        #                 fieldbackground="#ffffff",
        #                 borderwidth=0,
        #                 font=("Segoe UI", 12))
        #
        # style.configure("Treeview.Heading",
        #                 background="#f1f2f6",
        #                 foreground="#2d3436",
        #                 relief="flat",
        #                 font=("Segoe UI", 12, "bold"))
        #
        # style.map("Treeview",
        #         background=[('selected', "#74b9ff")],
        #         foreground=[('selected', "white")])
        #
        # # Scrollbars
        # self.scroll_bar = ttk.Scrollbar(tabla_scroll_frame, orient="vertical", command=self.tabla_productos.yview)
        # self.tabla_productos.configure(yscrollcommand=self.scroll_bar.set)
        #
        # self.scroll_barx = ttk.Scrollbar(tabla_scroll_frame, orient="horizontal", command=self.tabla_productos.xview)
        # self.tabla_productos.configure(xscrollcommand=self.scroll_barx.set)
        #
        # self.tabla_productos.grid(row=0, column=0, sticky="nsew")
        # self.scroll_bar.grid(row=0, column=1, sticky="ns")
        # self.scroll_barx.grid(row=1, column=0, sticky="ew")
        #
        # tabla_scroll_frame.grid_rowconfigure(0, weight=1)
        # tabla_scroll_frame.grid_columnconfigure(0, weight=1)

        self.tabla_inventario = TI.TablaInventario(
            tabla_scroll_frame,
            self.inventario.productos
        )
        self.tabla_inventario.pack(fill="both", expand=True)

        self.frame_treeview = ctk.CTkFrame(
            tabla_scroll_frame,
            fg_color="transparent"
        )
        self.frame_treeview.grid_rowconfigure(0, weight=1)
        self.frame_treeview.grid_columnconfigure(0, weight=1)

        self.columnas = (
            "id", "nombre", "descripcion", "presentacion", "categoria",
            "precio_compra", "precio_venta", "precio_blister", "precio_caja",
            "stock", "utilidad", "stock_minimo"
        )
        self.tabla_productos = ttk.Treeview(
            self.frame_treeview,
            columns=self.columnas,
            show="headings",
            height=10
        )
        encabezados = (
            "ID", "Producto", "Descripción", "Presentación", "Categoría",
            "P. Compra", "P. Venta", "P. Blíster", "P. Caja", "Stock",
            "Utilidad", "Stock Mínimo"
        )
        anchos = (0, 130, 160, 100, 100, 90, 90, 90, 90, 70, 80, 90)
        for columna, encabezado, ancho in zip(
            self.columnas, encabezados, anchos
        ):
            self.tabla_productos.heading(columna, text=encabezado)
            self.tabla_productos.column(
                columna,
                width=ancho,
                minwidth=50 if ancho else 0,
                stretch=bool(ancho),
                anchor="e" if columna in {
                    "id", "precio_compra", "precio_venta", "precio_blister",
                    "precio_caja", "stock", "utilidad", "stock_minimo"
                } else "w"
            )
        self.tabla_productos.tag_configure(
            "stock_bajo",
            background="#fff1f0",
            foreground="#c0392b"
        )

        self.scroll_bar = ttk.Scrollbar(
            self.frame_treeview,
            orient="vertical",
            command=self.tabla_productos.yview
        )
        self.tabla_productos.configure(yscrollcommand=self.scroll_bar.set)
        self.scroll_barx = ttk.Scrollbar(
            self.frame_treeview,
            orient="horizontal",
            command=self.tabla_productos.xview
        )
        self.tabla_productos.configure(xscrollcommand=self.scroll_barx.set)
        self.tabla_productos.grid(row=0, column=0, sticky="nsew")
        self.scroll_bar.grid(row=0, column=1, sticky="ns")
        self.scroll_barx.grid(row=1, column=0, sticky="ew")

        # Frame de botones
        self.frame_botones = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_botones.pack(fill="x")

        self.btn_cambiar_vista = ctk.CTkButton(
            self.frame_botones,
            text="Ver Treeview",
            fg_color="#636e72",
            hover_color="#4b5457",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=40,
            command=self.cambiar_vista
        )
        self.btn_cambiar_vista.pack(side="right", padx=(10, 0), pady=5)

        self.btn_ingresar = ctk.CTkButton(
            self.frame_botones,
            text="Nuevo",
            image=self.icon_add,
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
            text="Editar",
            image=self.icon_editar,
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
            text="Eliminar",
            image=self.icon_borrar,
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
            text="Categorías",
            image=self.icon_categoria,
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
            text="Ingreso Stock",
            image=self.icon_agregar_stock,
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
            text="Exportar",
            image=self.icon_export,
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
        # Código original de carga del Treeview conservado:
        # for item in self.tabla_productos.get_children():
        #     self.tabla_productos.delete(item)
        # for producto in self.inventario.productos:
        #     self.tabla_productos.insert("", tk.END, values=(
        #         producto.id_producto,
        #         producto.nombre,
        #         producto.descripcion,
        #         producto.presentacion,
        #         producto.categoria,
        #         f"Q{producto.precio_compra:.2f}",
        #         f"Q{producto.precio_venta:.2f}",
        #         f"Q{producto.precio_blister:.2f}",
        #         f"Q{producto.precio_caja:.2f}",
        #         producto.stock,
        #         f"Q{producto.utilidad:.2f}",
        #         producto.stock_minimo
        #     ))
        self.tabla_inventario.actualizar(self.inventario.productos)
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        for producto in self.inventario.productos:
            stock_bajo = producto.stock <= producto.stock_minimo
            self.tabla_productos.insert(
                "",
                tk.END,
                iid=str(producto.id_producto),
                values=(
                    producto.id_producto,
                    producto.nombre,
                    producto.descripcion,
                    producto.presentacion,
                    producto.categoria,
                    f"Q{float(producto.precio_compra or 0):.2f}",
                    f"Q{float(producto.precio_venta or 0):.2f}",
                    f"Q{float(producto.precio_blister or 0):.2f}",
                    f"Q{float(producto.precio_caja or 0):.2f}",
                    producto.stock,
                    f"Q{float(producto.utilidad or 0):.2f}",
                    producto.stock_minimo
                ),
                tags=("stock_bajo",) if stock_bajo else ()
            )

    def cambiar_vista(self):
        if self.vista_actual == "tabla_inventario":
            self.tabla_inventario.pack_forget()
            self.frame_treeview.pack(fill="both", expand=True)
            self.vista_actual = "treeview"
            self.btn_cambiar_vista.configure(text="Ver TablaInventario")
        else:
            self.frame_treeview.pack_forget()
            self.tabla_inventario.pack(fill="both", expand=True)
            self.vista_actual = "tabla_inventario"
            self.btn_cambiar_vista.configure(text="Ver Treeview")

    def obtener_producto_seleccionado(self):
        if self.vista_actual == "treeview":
            seleccion = self.tabla_productos.selection()
            if not seleccion:
                return None
            id_producto = self.tabla_productos.item(
                seleccion[0], "values"
            )[0]
            return next(
                (
                    producto for producto in self.inventario.productos
                    if str(producto.id_producto) == str(id_producto)
                ),
                None
            )
        return self.tabla_inventario.producto_seleccionado

    def buscar_producto(self, nombre="", descripcion="", codigo=""):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        self.inventario.buscar_producto(nombre, descripcion, codigo)
        # Código original de búsqueda del Treeview conservado:
        # for item in self.tabla_productos.get_children():
        #     self.tabla_productos.delete(item)
        # for producto in self.inventario.productos:
        #     self.tabla_productos.insert("", tk.END, values=(
        #         producto.id_producto,
        #         producto.nombre,
        #         producto.descripcion,
        #         producto.presentacion,
        #         producto.categoria,
        #         f"Q{producto.precio_compra:.2f}",
        #         f"Q{producto.precio_venta:.2f}",
        #         f"Q{producto.precio_blister:.2f}",
        #         f"Q{producto.precio_caja:.2f}",
        #         producto.stock,
        #         f"Q{producto.utilidad:.2f}",
        #         producto.stock_minimo
        #     ))
        self.mostrar_productos()

    def abrir_editar_formulario(self):
        # seleccion = self.tabla_productos.selection()
        # if not seleccion:
        #     messagebox.showwarning("Selección requerida", "Por favor, seleccione un producto de la tabla para editar.")
        #     return
        # item = self.tabla_productos.item(seleccion[0])
        # id_producto = item['values'][0]
        # producto_seleccionado = None
        # for producto in self.inventario.productos:
        #     if producto.id_producto == id_producto:
        #         producto_seleccionado = producto
        #         break
        producto_seleccionado = self.obtener_producto_seleccionado()
        if not producto_seleccionado:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione un producto de la tabla para editar.")
            return

        formulario = EP.EditarProducto(self, self.inventario, producto_seleccionado, self.actualizar_tabla)

    def eliminar_producto_seleccionado(self):
        # seleccion = self.tabla_productos.selection()
        # if not seleccion:
        #     messagebox.showwarning("Selección requerida", "Por favor, seleccione un producto de la tabla para eliminar.")
        #     return
        # item = self.tabla_productos.item(seleccion[0])
        # id_producto = item['values'][0]
        # nombre_producto = item['values'][1]
        producto_seleccionado = self.obtener_producto_seleccionado()
        if not producto_seleccionado:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione un producto de la tabla para eliminar.")
            return

        # item = self.tabla_productos.item(seleccion[0])
        id_producto = producto_seleccionado.id_producto
        nombre_producto = producto_seleccionado.nombre

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
