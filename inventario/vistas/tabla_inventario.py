import customtkinter as ctk

class TablaInventario(ctk.CTkFrame):
    def __init__(self, parent, productos):
        super().__init__(parent, fg_color="transparent")
        self.productos = productos
        self.producto_seleccionado = None
        self.fila_seleccionada = None
        self.encabezados_columnas = [
            "ID", "Producto", "Descripción", "Presentación", "Categoría",
            "P. Compra", "P. Venta", "P. Blíster", "P. Caja", "Stock",
            "Utilidad", "Stock Mínimo"
        ]
        self.alineaciones_columnas = (
            "e", "w", "w", "w", "w", "e",
            "e", "e", "e", "e", "e", "e"
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.create_widgets()

    def create_widgets(self):
        self.frame_encabezados = ctk.CTkFrame(
            self,
            fg_color="#eaf0f5",
            corner_radius=6
        )
        self.frame_encabezados.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        for column_index, encabezado in enumerate(self.encabezados_columnas):
            self.frame_encabezados.grid_columnconfigure(
                column_index, weight=1, uniform="columnas"
            )
            ctk.CTkLabel(
                self.frame_encabezados,
                text=encabezado,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color="#34495e",
                anchor=self.alineaciones_columnas[column_index]
            ).grid(row=0, column=column_index, sticky="ew", padx=9, pady=11)

        self.frame_filas = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )
        self.frame_filas.grid(row=1, column=0, sticky="nsew")
        self.frame_filas.grid_columnconfigure(0, weight=1)
        self.actualizar(self.productos)

    def actualizar(self, productos):
        self.productos = productos
        self.producto_seleccionado = None
        self.fila_seleccionada = None
        for widget in self.frame_filas.winfo_children():
            widget.destroy()

        if not self.productos:
            ctk.CTkLabel(
                self.frame_filas,
                text="No hay productos para mostrar",
                font=ctk.CTkFont(family="Segoe UI", size=13),
                text_color="#636e72"
            ).grid(row=0, column=0, sticky="ew", pady=28)
            return

        for row_index, producto in enumerate(self.productos):
            stock_bajo = producto.stock <= producto.stock_minimo
            color_fila = (
                "#fff1f0"
                if stock_bajo
                else ("#ffffff" if row_index % 2 == 0 else "#f6f8fa")
            )
            frame_fila = ctk.CTkFrame(
                self.frame_filas,
                fg_color=color_fila,
                corner_radius=5,
                border_width=1,
                border_color="#edf0f2"
            )
            frame_fila.grid(row=row_index, column=0, sticky="ew", pady=2)
            frame_fila.color_normal = color_fila
            frame_fila.bind(
                "<Button-1>",
                lambda event, fila=frame_fila, producto_fila=producto:
                    self.seleccionar_producto(producto_fila, fila)
            )

            for column_index in range(len(self.encabezados_columnas)):
                frame_fila.grid_columnconfigure(
                    column_index, weight=1, uniform="columnas"
                )

            valores = (
                str(producto.id_producto),
                str(producto.nombre),
                str(producto.descripcion),
                str(producto.presentacion),
                str(producto.categoria),
                f"Q{float(producto.precio_compra or 0):.2f}",
                f"Q{float(producto.precio_venta or 0):.2f}",
                f"Q{float(producto.precio_blister or 0):.2f}",
                f"Q{float(producto.precio_caja or 0):.2f}",
                f"­⚠️ {producto.stock}" if stock_bajo else str(producto.stock),
                f"Q{float(producto.utilidad or 0):.2f}",
                str(producto.stock_minimo)
            )

            for column_index, (valor, alineacion) in enumerate(
                zip(valores, self.alineaciones_columnas)
            ):
                alerta_stock = stock_bajo and column_index == 9
                etiqueta = ctk.CTkLabel(
                    frame_fila,
                    text=valor,
                    font=ctk.CTkFont(
                        family="Segoe UI",
                        size=11,
                        weight="bold" if alerta_stock else "normal"
                    ),
                    text_color="#c0392b" if alerta_stock else "#2d3436",
                    anchor=alineacion
                )
                etiqueta.grid(
                    row=0,
                    column=column_index,
                    sticky="ew",
                    padx=9,
                    pady=10
                )
                etiqueta.bind(
                    "<Button-1>",
                    lambda event, fila=frame_fila, producto_fila=producto:
                        self.seleccionar_producto(producto_fila, fila)
                )

    def seleccionar_producto(self, producto, fila):
        if self.fila_seleccionada:
            self.fila_seleccionada.configure(
                fg_color=self.fila_seleccionada.color_normal
            )

        self.producto_seleccionado = producto
        self.fila_seleccionada = fila
        fila.configure(fg_color="#d6eaff")
