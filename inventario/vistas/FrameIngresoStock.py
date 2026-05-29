import tkinter as tk
from tkinter import ttk, messagebox


class FrameIngresoStock(tk.Toplevel):
    def __init__(self, parent, inventario=None, actualizar_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.inventario = inventario
        self.actualizar_callback = actualizar_callback

        self.estado_chek_codigo = tk.BooleanVar()
        self.estado_chek_nombre = tk.BooleanVar()


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
        self.geometry("650x780")
        self.resizable(False, False)
        self.configure(bg=self.color_fondo)

        header_frame = tk.Frame(self, bg=self.color_header, height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="Ingreso de Stock",
            bg=self.color_header,
            fg="white",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=15)

        self.main_frame = tk.Frame(self, bg=self.color_fondo)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Panel de Opciones de Búsqueda (Debajo del header, antes de los campos)
        options_frame = tk.Frame(self.main_frame, bg=self.color_fondo)
        options_frame.pack(fill="x", pady=(0, 15))

        self.chk_buscar_por_codigo = tk.Checkbutton(
            options_frame, 
            text="Buscar por Código", 
            bg=self.color_fondo, 
            fg=self.color_texto, 
            selectcolor="white",
            activebackground=self.color_fondo,
            font=("Segoe UI", 9, "bold"),
            variable=self.estado_chek_codigo,
            onvalue=1,
            offvalue=0,
            command=self.desactivar_busqueda_nombre
        )
        self.chk_buscar_por_codigo.pack(side="left", padx=(0, 15))
        self.chk_buscar_por_codigo.select()

        self.chk_buscar_por_nombre = tk.Checkbutton(
            options_frame, 
            text="Buscar por Nombre", 
            bg=self.color_fondo, 
            fg=self.color_texto, 
            selectcolor="white",
            activebackground=self.color_fondo,
            font=("Segoe UI", 9, "bold"),
            variable=self.estado_chek_nombre,
            onvalue=True,
            offvalue=False,
            command=self.desactivar_busqueda_codigo
        )
        self.chk_buscar_por_nombre.pack(side="left")
        self.chk_buscar_por_nombre.deselect()

        # Código de producto
        tk.Label(
            self.main_frame,
            text="Código de producto",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w", pady=(0, 5))
        codigo_frame = tk.Frame(self.main_frame, bg=self.color_fondo)
        codigo_frame.pack(fill="x", pady=(0, 10))
        self.entry_codigo_producto = tk.Entry(
            codigo_frame,
            font=("Segoe UI", 11),
            bg=self.color_entrada,
            bd=0,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.color_borde,
            highlightcolor=self.color_primario
        )
        self.entry_codigo_producto.pack(side="left", fill="both", expand=True, ipady=4)
        self.entry_codigo_producto.bind("<Return>", lambda event: self.buscar_producto_codigo())
        self.btn_buscar_codigo = tk.Button(
            codigo_frame,
            text="🔍 Buscar",
            bg=self.color_primario,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=15,
            relief="flat",
            cursor="hand2",
            command=self.buscar_producto_codigo,
        )
        self.btn_buscar_codigo.pack(side="left", padx=(10, 0))

        # Nombre del producto
        tk.Label(
            self.main_frame,
            text="Nombre del producto",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w", pady=(0, 5))
        nombre_frame = tk.Frame(self.main_frame, bg=self.color_fondo)
        nombre_frame.pack(fill="x", pady=(0, 10))
        self.entry_nombre_producto = tk.Entry(
            nombre_frame,
            font=("Segoe UI", 11),
            bg=self.color_entrada,
            bd=0,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.color_borde,
            highlightcolor=self.color_primario,
            state="disabled"
        )
        self.entry_nombre_producto.pack(side="left", fill="both", expand=True, ipady=4)
        self.entry_nombre_producto.bind("<Return>", lambda event: self.buscar_producto_nombre())
        self.btn_buscar_nombre = tk.Button(
            nombre_frame,
            text="🔍 Buscar",
            bg=self.color_primario,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=15,
            relief="flat",
            cursor="hand2",
            command=self.buscar_producto_nombre,
            state="disabled"
        )
        self.btn_buscar_nombre.pack(side="left", padx=(10, 0))

        # Cantidad a ingresar
        tk.Label(
            self.main_frame,
            text="Cantidad a ingresar",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w", pady=(0, 5))
        self.entry_cantidad = tk.Entry(
            self.main_frame,
            font=("Segoe UI", 11),
            bg=self.color_entrada,
            bd=0,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.color_borde,
            highlightcolor=self.color_primario
        )
        self.entry_cantidad.pack(fill="x", pady=(0, 10), ipady=4)
        self.entry_cantidad.bind("<Return>", lambda event: self.guardar_stock())

        # Precio de compra
        tk.Label(
            self.main_frame,
            text="Precio de compra",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w", pady=(0, 5))
        self.entry_precio_compra = tk.Entry(
            self.main_frame,
            font=("Segoe UI", 11),
            bg=self.color_entrada,
            bd=0,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.color_borde,
            highlightcolor=self.color_primario,
            state="disabled"
        )
        self.entry_precio_compra.pack(fill="x", pady=(0, 10), ipady=4)

        # Precio de venta
        tk.Label(
            self.main_frame,
            text="Precio de venta",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w", pady=(0, 5))
        self.entry_precio_venta = tk.Entry(
            self.main_frame,
            font=("Segoe UI", 11),
            bg=self.color_entrada,
            bd=0,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.color_borde,
            highlightcolor=self.color_primario,
            state="disabled"
        )
        self.entry_precio_venta.pack(fill="x", pady=(0, 10), ipady=4)

        # Proveedor
        tk.Label(
            self.main_frame,
            text="Proveedor",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w", pady=(0, 5))
        self.entry_proveedor = tk.Entry(
            self.main_frame,
            font=("Segoe UI", 11),
            bg=self.color_entrada,
            bd=0,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.color_borde,
            highlightcolor=self.color_primario
        )
        self.entry_proveedor.pack(fill="x", pady=(0, 10), ipady=4)

        # Resultados de búsqueda
        result_frame = tk.Frame(
            self.main_frame,
            bg="white",
            bd=1,
            relief="solid",
            highlightbackground=self.color_borde,
            highlightthickness=0
        )
        result_frame.pack(fill="both", expand=True, pady=(15, 0))

        inner_result = tk.Frame(result_frame, bg="white", padx=20, pady=20)
        inner_result.pack(fill="both", expand=True)

        self.lbl_nombre_producto_encontrado = tk.Label(
            inner_result,
            text="Ingrese código o nombre y presione Buscar.",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg=self.color_primario,
            justify="left",
            anchor="nw"
        )
        self.lbl_nombre_producto_encontrado.pack(fill="x", pady=(0, 10))

        self.lbl_descripcion_producto = tk.Label(
            inner_result,
            text="Descripción: -",
            font=("Segoe UI", 11),
            bg="white",
            fg=self.color_subtexto,
            justify="left",
            anchor="nw",
            wraplength=550
        )
        self.lbl_descripcion_producto.pack(fill="x", pady=(0, 8))

        self.lbl_stock_actual = tk.Label(
            inner_result,
            text="Stock actual: -",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg=self.color_texto,
            justify="left",
            anchor="nw"
        )
        self.lbl_stock_actual.pack(fill="x")

        # Frame para botones con mejor diseño
        button_frame = tk.Frame(self.main_frame, bg=self.color_fondo)
        button_frame.pack(fill="x", pady=(25, 0))

        # Botones Guardar y Cancelar
        action_frame = tk.Frame(button_frame, bg=self.color_fondo)
        action_frame.pack(anchor="center")

        self.btn_guardar = tk.Button(
            action_frame,
            text="✓ Guardar Stock",
            bg=self.color_boton,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            bd=0,
            padx=35,
            pady=12,
            relief="flat",
            cursor="hand2",
            command=self.guardar_stock
        )
        self.btn_guardar.pack(side="left", padx=(0, 10))

        self.btn_cerrar = tk.Button(
            action_frame,
            text="✕ Cancelar",
            bg=self.color_cancelar,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            bd=0,
            padx=35,
            pady=12,
            relief="flat",
            cursor="hand2",
            command=self.cerrar
        )
        self.btn_cerrar.pack(side="left")

        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.grab_set()
        self.after(0, self.entry_codigo_producto.focus_set)#para que el focus aplicque despues de que se muestre la ventana
    
    def desactivar_busqueda_codigo(self):
        self.chk_buscar_por_codigo.deselect()
        self.entry_codigo_producto.config(state="disabled")
        self.btn_buscar_codigo.config(state="disabled")
        self.entry_nombre_producto.config(state="normal")
        self.btn_buscar_nombre.config(state="normal")
        self.entry_nombre_producto.focus()


    def desactivar_busqueda_nombre(self):
        self.chk_buscar_por_nombre.deselect()
        self.entry_nombre_producto.config(state="disabled")
        self.btn_buscar_nombre.config(state="disabled")
        self.entry_codigo_producto.config(state="normal")
        self.btn_buscar_codigo.config(state="normal")
        self.entry_codigo_producto.focus()


    def buscar_producto_codigo(self):
        codigo = self.entry_codigo_producto.get()
        if codigo:
            self.producto_encontrado = self.inventario.buscar_ingresar_stock_por_codigo(codigo)
            if self.producto_encontrado:
                self.lbl_nombre_producto_encontrado.config(
                    text=self.producto_encontrado.nombre,
                    fg=self.color_primario
                )
                self.lbl_descripcion_producto.config(
                    text=f"Descripción: {self.producto_encontrado.descripcion}"
                )
                self.lbl_stock_actual.config(
                    text=f"Stock actual: {self.producto_encontrado.stock}"
                )
                self.entry_precio_compra.config(state="normal")
                self.entry_precio_venta.config(state="normal")
                self.entry_precio_compra.delete(0, tk.END)
                self.entry_precio_compra.insert(0, str(self.producto_encontrado.precio_compra))
                self.entry_precio_venta.delete(0, tk.END)
                self.entry_precio_venta.insert(0, str(self.producto_encontrado.precio_venta))
                self.entry_cantidad.focus()
            else:
                self.lbl_nombre_producto_encontrado.config(
                    text="Producto no encontrado.",
                    fg="#e74c3c"
                )
                self.lbl_descripcion_producto.config(text="Descripción: -")
                self.lbl_stock_actual.config(text="Stock actual: -")
                self.entry_precio_compra.config(state="disabled")
                self.entry_precio_venta.config(state="disabled")
                self.entry_precio_compra.delete(0, tk.END)
                self.entry_precio_venta.delete(0, tk.END)

    def buscar_producto_nombre(self):
        nombre = self.entry_nombre_producto.get()
        if nombre:
            self.producto_encontrado = self.inventario.buscar_ingresar_stock_por_nombre(nombre)
            if self.producto_encontrado:
                self.lbl_nombre_producto_encontrado.config(
                    text=self.producto_encontrado.nombre,
                    fg=self.color_primario
                )
                self.lbl_descripcion_producto.config(
                    text=f"Descripción: {self.producto_encontrado.descripcion}"
                )
                self.lbl_stock_actual.config(
                    text=f"Stock actual: {self.producto_encontrado.stock}"
                )
                self.entry_precio_compra.config(state="normal")
                self.entry_precio_venta.config(state="normal")
                self.entry_precio_compra.delete(0, tk.END)
                self.entry_precio_compra.insert(0, str(self.producto_encontrado.precio_compra))
                self.entry_precio_venta.delete(0, tk.END)
                self.entry_precio_venta.insert(0, str(self.producto_encontrado.precio_venta))
                self.entry_cantidad.focus()
            else:
                self.lbl_nombre_producto_encontrado.config(
                    text="Producto no encontrado.",
                    fg="#e74c3c"
                )
                self.lbl_descripcion_producto.config(text="Descripción: -")
                self.lbl_stock_actual.config(text="Stock actual: -")
                self.entry_precio_compra.config(state="disabled")
                self.entry_precio_venta.config(state="disabled")
                self.entry_precio_compra.delete(0, tk.END)
                self.entry_precio_venta.delete(0, tk.END)

    def guardar_stock(self):
        cantidad = self.entry_cantidad.get()
        if cantidad is None or cantidad == "":
            tk.messagebox.showerror("Error", "Ingrese una cantidad válida.")
            return
        precio_compra = self.entry_precio_compra.get()
        precio_venta = self.entry_precio_venta.get()
        proveedor = self.entry_proveedor.get().strip()
        if precio_compra is None or precio_compra == "" or precio_venta is None or precio_venta == "":
            tk.messagebox.showerror("Error", "Ingrese precio de compra y precio de venta.")
            return
        try:
            precio_compra_val = float(precio_compra)
            precio_venta_val = float(precio_venta)
        except ValueError:
            tk.messagebox.showerror("Error", "Los precios deben ser valores numéricos.")
            return
        self.inventario.aumentar_stock(self.producto_encontrado.id_producto, int(cantidad), precio_compra_val, precio_venta_val, proveedor)
        tk.messagebox.showinfo("Éxito", "Stock actualizado correctamente.")
        self.actualizar_callback()
        self.vaciar_campos()
        if self.estado_chek_codigo.get():
            self.entry_codigo_producto.focus()
        else:
            self.entry_nombre_producto.focus()

    def cerrar(self):
        self.destroy()

    def vaciar_campos(self):
        self.entry_codigo_producto.delete(0, tk.END)
        self.entry_nombre_producto.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_precio_compra.delete(0, tk.END)
        self.entry_precio_venta.delete(0, tk.END)
        self.entry_proveedor.delete(0, tk.END)
        self.lbl_nombre_producto_encontrado.config(
            text="Ingrese código o nombre y presione Buscar.",
            fg=self.color_primario
        )
        self.lbl_descripcion_producto.config(text="Descripción: -")
        self.lbl_stock_actual.config(text="Stock actual: -")
