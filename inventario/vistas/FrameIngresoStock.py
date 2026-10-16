from tkinter import messagebox

import customtkinter as ctk


class FrameIngresoStock(ctk.CTkToplevel):
    def __init__(self, parent, inventario=None, actualizar_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.inventario = inventario
        self.actualizar_callback = actualizar_callback

        self.estado_chek_codigo = ctk.BooleanVar(master=self, value=True)
        self.estado_chek_nombre = ctk.BooleanVar(master=self, value=False)
        self.producto_encontrado = None

        self.color_fondo = "#f8f9fa"
        self.color_header = "#2c3e50"
        self.color_primario = "#0984e3"
        self.color_texto = "#2d3436"
        self.color_subtexto = "#636e72"
        self.color_entrada = "#ffffff"
        self.color_boton = "#00b894"
        self.color_cancelar = "#d63031"
        self.color_borde = "#dfe6e9"

        self.title("Ingreso de Stock")
        window_width = 650
        window_height = 620
        x = max(0, (self.winfo_screenwidth() - window_width) // 2)
        y = max(0, (self.winfo_screenheight() - window_height) // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        self.configure(fg_color=self.color_fondo)
        self.transient(parent)
        self.grab_set()

        header_frame = ctk.CTkFrame(
            self,
            fg_color=self.color_header,
            height=52,
            corner_radius=0,
        )
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        ctk.CTkLabel(
            header_frame,
            text="Ingreso de Stock",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
        ).pack(pady=12)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=18, pady=12)

        options_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        options_frame.pack(fill="x", pady=(0, 8))

        estilo_check = {
            "font": ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            "text_color": self.color_texto,
            "fg_color": self.color_primario,
            "hover_color": "#74b9ff",
            "border_color": self.color_borde,
            "checkbox_width": 18,
            "checkbox_height": 18,
        }
        self.chk_buscar_por_codigo = ctk.CTkCheckBox(
            options_frame,
            text="Buscar por Código",
            variable=self.estado_chek_codigo,
            onvalue=True,
            offvalue=False,
            command=self.desactivar_busqueda_nombre,
            **estilo_check,
        )
        self.chk_buscar_por_codigo.pack(side="left", padx=(0, 15))

        self.chk_buscar_por_nombre = ctk.CTkCheckBox(
            options_frame,
            text="Buscar por Nombre",
            variable=self.estado_chek_nombre,
            onvalue=True,
            offvalue=False,
            command=self.desactivar_busqueda_codigo,
            **estilo_check,
        )
        self.chk_buscar_por_nombre.pack(side="left")

        search_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 8))
        codigo_columna = ctk.CTkFrame(search_frame, fg_color="transparent")
        codigo_columna.pack(side="left", fill="x", expand=True, padx=(0, 8))
        nombre_columna = ctk.CTkFrame(search_frame, fg_color="transparent")
        nombre_columna.pack(side="left", fill="x", expand=True, padx=(8, 0))

        self._crear_label(codigo_columna, "Código de producto")
        codigo_frame = ctk.CTkFrame(codigo_columna, fg_color="transparent")
        codigo_frame.pack(fill="x")
        self.entry_codigo_producto = self._crear_entrada(
            codigo_frame, height=36
        )
        self.entry_codigo_producto.pack(side="left", fill="x", expand=True)
        self.entry_codigo_producto.bind(
            "<Return>", lambda event: self.buscar_producto_codigo()
        )
        self.btn_buscar_codigo = self._crear_boton_buscar(
            codigo_frame, self.buscar_producto_codigo, height=36
        )
        self.btn_buscar_codigo.pack(side="left", padx=(6, 0))

        self._crear_label(nombre_columna, "Nombre del producto")
        nombre_frame = ctk.CTkFrame(nombre_columna, fg_color="transparent")
        nombre_frame.pack(fill="x")
        self.entry_nombre_producto = self._crear_entrada(
            nombre_frame, state="disabled", height=36
        )
        self.entry_nombre_producto.pack(side="left", fill="x", expand=True)
        self.entry_nombre_producto.bind(
            "<Return>", lambda event: self.buscar_producto_nombre()
        )
        self.btn_buscar_nombre = self._crear_boton_buscar(
            nombre_frame,
            self.buscar_producto_nombre,
            state="disabled",
            height=36,
        )
        self.btn_buscar_nombre.pack(side="left", padx=(6, 0))

        amounts_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        amounts_frame.pack(fill="x", pady=(0, 8))
        cantidad_columna = ctk.CTkFrame(amounts_frame, fg_color="transparent")
        cantidad_columna.pack(side="left", fill="x", expand=True, padx=(0, 8))
        compra_columna = ctk.CTkFrame(amounts_frame, fg_color="transparent")
        compra_columna.pack(side="left", fill="x", expand=True, padx=(8, 0))

        self._crear_label(cantidad_columna, "Cantidad a ingresar")
        self.entry_cantidad = self._crear_entrada(
            cantidad_columna, height=36
        )
        self.entry_cantidad.pack(fill="x")
        self.entry_cantidad.bind("<Return>", lambda event: self.guardar_stock())

        self._crear_label(compra_columna, "Precio de compra")
        self.entry_precio_compra = self._crear_entrada(
            compra_columna, state="disabled", height=36
        )
        self.entry_precio_compra.pack(fill="x")

        details_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        details_frame.pack(fill="x", pady=(0, 8))
        venta_columna = ctk.CTkFrame(details_frame, fg_color="transparent")
        venta_columna.pack(side="left", fill="x", expand=True, padx=(0, 8))
        proveedor_columna = ctk.CTkFrame(details_frame, fg_color="transparent")
        proveedor_columna.pack(side="left", fill="x", expand=True, padx=(8, 0))

        self._crear_label(venta_columna, "Precio de venta")
        self.entry_precio_venta = self._crear_entrada(
            venta_columna, state="disabled", height=36
        )
        self.entry_precio_venta.pack(fill="x")

        self._crear_label(proveedor_columna, "Proveedor")
        self.entry_proveedor = self._crear_entrada(
            proveedor_columna, height=36
        )
        self.entry_proveedor.pack(fill="x")

        result_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="white",
            corner_radius=8,
            border_width=1,
            border_color=self.color_borde,
        )
        result_frame.pack(fill="both", expand=True, pady=(2, 8))

        inner_result = ctk.CTkFrame(result_frame, fg_color="transparent")
        inner_result.pack(fill="both", expand=True, padx=14, pady=10)

        self.lbl_nombre_producto_encontrado = ctk.CTkLabel(
            inner_result,
            text="Ingrese código o nombre y presione Buscar.",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=self.color_primario,
            justify="left",
            anchor="w",
            wraplength=550,
        )
        self.lbl_nombre_producto_encontrado.pack(fill="x", pady=(0, 4))

        self.lbl_descripcion_producto = ctk.CTkLabel(
            inner_result,
            text="Descripción: -",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=self.color_subtexto,
            justify="left",
            anchor="w",
            wraplength=550,
        )
        self.lbl_descripcion_producto.pack(fill="x", pady=(0, 4))

        self.lbl_stock_actual = ctk.CTkLabel(
            inner_result,
            text="Stock actual: -",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=self.color_texto,
            justify="left",
            anchor="w",
        )
        self.lbl_stock_actual.pack(fill="x")

        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(fill="x")
        action_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        action_frame.pack(anchor="center")

        self.btn_guardar = ctk.CTkButton(
            action_frame,
            text="✓ Guardar Stock",
            fg_color=self.color_boton,
            hover_color="#009f7f",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            height=38,
            command=self.guardar_stock,
        )
        self.btn_guardar.pack(side="left", padx=(0, 10))

        self.btn_cerrar = ctk.CTkButton(
            action_frame,
            text="✕ Cancelar",
            fg_color=self.color_cancelar,
            hover_color="#b92525",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            height=38,
            command=self.cerrar,
        )
        self.btn_cerrar.pack(side="left")

        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.grab_set()
        self.after(0, self.entry_codigo_producto.focus_set)

    def _crear_label(self, parent, text):
        ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=self.color_texto,
        ).pack(anchor="w", pady=(0, 5))

    def _crear_entrada(self, parent, state="normal", height=38):
        return ctk.CTkEntry(
            parent,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=height,
            corner_radius=6,
            border_width=1,
            border_color=self.color_borde,
            fg_color=self.color_entrada,
            text_color=self.color_texto,
            state=state,
        )

    def _crear_boton_buscar(self, parent, command, state="normal", height=38):
        return ctk.CTkButton(
            parent,
            text="🔍 Buscar",
            fg_color=self.color_primario,
            hover_color="#74b9ff",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            height=height,
            width=96,
            command=command,
            state=state,
        )

    def desactivar_busqueda_codigo(self):
        self.chk_buscar_por_codigo.deselect()
        self.estado_chek_codigo.set(False)
        self.entry_codigo_producto.configure(state="disabled")
        self.btn_buscar_codigo.configure(state="disabled")
        self.entry_nombre_producto.configure(state="normal")
        self.btn_buscar_nombre.configure(state="normal")
        self.entry_nombre_producto.focus_set()

    def desactivar_busqueda_nombre(self):
        self.chk_buscar_por_nombre.deselect()
        self.estado_chek_nombre.set(False)
        self.entry_nombre_producto.configure(state="disabled")
        self.btn_buscar_nombre.configure(state="disabled")
        self.entry_codigo_producto.configure(state="normal")
        self.btn_buscar_codigo.configure(state="normal")
        self.entry_codigo_producto.focus_set()

    def buscar_producto_codigo(self):
        codigo = self.entry_codigo_producto.get()
        if codigo:
            self.producto_encontrado = (
                self.inventario.buscar_ingresar_stock_por_codigo(codigo)
            )
            self._mostrar_producto_encontrado()

    def buscar_producto_nombre(self):
        nombre = self.entry_nombre_producto.get()
        if nombre:
            self.producto_encontrado = (
                self.inventario.buscar_ingresar_stock_por_nombre(nombre)
            )
            self._mostrar_producto_encontrado()

    def _mostrar_producto_encontrado(self):
        if self.producto_encontrado:
            self.lbl_nombre_producto_encontrado.configure(
                text=self.producto_encontrado.nombre,
                text_color=self.color_primario,
            )
            self.lbl_descripcion_producto.configure(
                text=f"Descripción: {self.producto_encontrado.descripcion}"
            )
            self.lbl_stock_actual.configure(
                text=f"Stock actual: {self.producto_encontrado.stock}"
            )
            self.entry_precio_compra.configure(state="normal")
            self.entry_precio_venta.configure(state="normal")
            self.entry_precio_compra.delete(0, "end")
            self.entry_precio_compra.insert(
                0, str(self.producto_encontrado.precio_compra)
            )
            self.entry_precio_venta.delete(0, "end")
            self.entry_precio_venta.insert(
                0, str(self.producto_encontrado.precio_venta)
            )
            self.entry_cantidad.focus_set()
        else:
            self.lbl_nombre_producto_encontrado.configure(
                text="Producto no encontrado.",
                text_color="#e74c3c",
            )
            self.lbl_descripcion_producto.configure(text="Descripción: -")
            self.lbl_stock_actual.configure(text="Stock actual: -")
            self.entry_precio_compra.configure(state="normal")
            self.entry_precio_venta.configure(state="normal")
            self.entry_precio_compra.delete(0, "end")
            self.entry_precio_venta.delete(0, "end")
            self.entry_precio_compra.configure(state="disabled")
            self.entry_precio_venta.configure(state="disabled")

    def guardar_stock(self):
        if not self.producto_encontrado:
            messagebox.showerror(
                "Error", "Busque un producto antes de ingresar stock.", parent=self
            )
            return

        cantidad = self.entry_cantidad.get().strip()
        if not cantidad:
            messagebox.showerror("Error", "Ingrese una cantidad válida.", parent=self)
            return

        precio_compra = self.entry_precio_compra.get().strip()
        precio_venta = self.entry_precio_venta.get().strip()
        proveedor = self.entry_proveedor.get().strip()
        if not precio_compra or not precio_venta:
            messagebox.showerror(
                "Error",
                "Ingrese precio de compra y precio de venta.",
                parent=self,
            )
            return

        try:
            cantidad_val = int(cantidad)
            precio_compra_val = float(precio_compra)
            precio_venta_val = float(precio_venta)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Cantidad y precios deben ser valores numéricos válidos.",
                parent=self,
            )
            return

        self.inventario.aumentar_stock(
            self.producto_encontrado.id_producto,
            self.producto_encontrado.nombre,
            cantidad_val,
            precio_compra_val,
            precio_venta_val,
            proveedor,
        )
        messagebox.showinfo(
            "Éxito", "Stock actualizado correctamente.", parent=self
        )
        if self.actualizar_callback:
            self.actualizar_callback()
        self.vaciar_campos()
        if self.estado_chek_codigo.get():
            self.entry_codigo_producto.focus_set()
        else:
            self.entry_nombre_producto.focus_set()

    def cerrar(self):
        self.destroy()

    def vaciar_campos(self):
        self.entry_codigo_producto.delete(0, "end")
        self.entry_nombre_producto.configure(state="normal")
        self.entry_nombre_producto.delete(0, "end")
        if not self.estado_chek_nombre.get():
            self.entry_nombre_producto.configure(state="disabled")
        self.entry_cantidad.delete(0, "end")
        self.entry_precio_compra.configure(state="normal")
        self.entry_precio_compra.delete(0, "end")
        self.entry_precio_compra.configure(state="disabled")
        self.entry_precio_venta.configure(state="normal")
        self.entry_precio_venta.delete(0, "end")
        self.entry_precio_venta.configure(state="disabled")
        self.entry_proveedor.delete(0, "end")
        self.producto_encontrado = None
        self.lbl_nombre_producto_encontrado.configure(
            text="Ingrese código o nombre y presione Buscar.",
            text_color=self.color_primario,
        )
        self.lbl_descripcion_producto.configure(text="Descripción: -")
        self.lbl_stock_actual.configure(text="Stock actual: -")
