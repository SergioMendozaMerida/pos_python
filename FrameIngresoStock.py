import tkinter as tk
from tkinter import ttk


class FrameIngresoStock(tk.Toplevel):
    def __init__(self, parent, inventario=None, actualizar_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.inventario = inventario
        self.actualizar_callback = actualizar_callback

        self.producto_encontrado = None

        self.color_fondo = "#f0f0f0"
        self.color_header = "#2c3e50"
        self.color_primario = "#3498db"
        self.color_texto = "#2c3e50"
        self.color_entrada = "#ffffff"
        self.color_boton = "#27ae60"
        self.color_cancelar = "#e74c3c"

        self.title("Ingreso de Stock")
        self.geometry("650x550")
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
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        self.main_frame = tk.Frame(self, bg=self.color_fondo)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Código de producto
        tk.Label(
            self.main_frame,
            text="Código de producto",
            font=("Arial", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w", pady=(0, 5))
        codigo_frame = tk.Frame(self.main_frame, bg=self.color_fondo)
        codigo_frame.pack(fill="x", pady=(0, 10))
        self.entry_codigo_producto = tk.Entry(
            codigo_frame,
            font=("Arial", 10),
            bg=self.color_entrada,
            bd=1,
            relief="solid"
        )
        self.entry_codigo_producto.pack(side="left", fill="x", expand=True)
        self.entry_codigo_producto.bind("<Return>", lambda event: self.buscar_producto_codigo())
        self.btn_buscar_codigo = tk.Button(
            codigo_frame,
            text="Buscar por código",
            bg=self.color_primario,
            fg="white",
            font=("Arial", 10, "bold"),
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            command=self.buscar_producto_codigo
        )
        self.btn_buscar_codigo.pack(side="left", padx=(10, 0))

        # Nombre del producto
        tk.Label(
            self.main_frame,
            text="Nombre del producto",
            font=("Arial", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w", pady=(0, 5))
        nombre_frame = tk.Frame(self.main_frame, bg=self.color_fondo)
        nombre_frame.pack(fill="x", pady=(0, 10))
        self.entry_nombre_producto = tk.Entry(
            nombre_frame,
            font=("Arial", 10),
            bg=self.color_entrada,
            bd=1,
            relief="solid"
        )
        self.entry_nombre_producto.pack(side="left", fill="x", expand=True)
        self.entry_nombre_producto.bind("<Return>", lambda event: self.buscar_producto_nombre())
        self.btn_buscar_nombre = tk.Button(
            nombre_frame,
            text="Buscar por nombre",
            bg=self.color_primario,
            fg="white",
            font=("Arial", 10, "bold"),
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            command=self.buscar_producto_nombre
        )
        self.btn_buscar_nombre.pack(side="left", padx=(10, 0))

        # Cantidad a ingresar
        tk.Label(
            self.main_frame,
            text="Cantidad a ingresar",
            font=("Arial", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w", pady=(0, 5))
        self.entry_cantidad = tk.Entry(
            self.main_frame,
            font=("Arial", 10),
            bg=self.color_entrada,
            bd=1,
            relief="solid"
        )
        self.entry_cantidad.pack(fill="x", pady=(0, 10))

        # Resultados de búsqueda
        result_frame = tk.LabelFrame(
            self.main_frame,
            text="Resultado de búsqueda",
            font=("Arial", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto,
            padx=15,
            pady=15,
            bd=2,
            relief="groove",
            labelanchor="n"
        )
        result_frame.pack(fill="both", expand=True, pady=(10, 0))

        self.lbl_nombre_producto_encontrado = tk.Label(
            result_frame,
            text="Ingrese código o nombre y presione Buscar.",
            font=("Arial", 14, "bold"),
            bg=self.color_fondo,
            fg=self.color_primario,
            justify="left",
            anchor="nw"
        )
        self.lbl_nombre_producto_encontrado.pack(fill="x", pady=(0, 10))

        self.lbl_descripcion_producto = tk.Label(
            result_frame,
            text="Descripción: -",
            font=("Arial", 11),
            bg=self.color_fondo,
            fg=self.color_texto,
            justify="left",
            anchor="nw",
            wraplength=600
        )
        self.lbl_descripcion_producto.pack(fill="x", pady=(0, 8))

        self.lbl_stock_actual = tk.Label(
            result_frame,
            text="Stock actual: -",
            font=("Arial", 11, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto,
            justify="left",
            anchor="nw"
        )
        self.lbl_stock_actual.pack(fill="x")

        # Frame para botones con mejor diseño
        button_frame = tk.Frame(self.main_frame, bg=self.color_fondo)
        button_frame.pack(fill="x", pady=(20, 0))

        # Botones Guardar y Cancelar
        action_frame = tk.Frame(button_frame, bg=self.color_fondo)
        action_frame.pack(fill="x")

        self.btn_guardar = tk.Button(
            action_frame,
            text="✓ Guardar",
            bg=self.color_boton,
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.guardar_stock
        )
        self.btn_guardar.pack(side="left", padx=(0, 10))

        self.btn_cerrar = tk.Button(
            action_frame,
            text="✕ Cancelar",
            bg=self.color_cancelar,
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.cerrar
        )
        self.btn_cerrar.pack(side="left")

        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.grab_set()
        self.after(0, self.entry_codigo_producto.focus_set)#para que el focus aplicque despues de que se muestre la ventana

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
            else:
                self.lbl_nombre_producto_encontrado.config(
                    text="Producto no encontrado.",
                    fg="#e74c3c"
                )
                self.lbl_descripcion_producto.config(text="Descripción: -")
                self.lbl_stock_actual.config(text="Stock actual: -")

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
            else:
                self.lbl_nombre_producto_encontrado.config(
                    text="Producto no encontrado.",
                    fg="#e74c3c"
                )
                self.lbl_descripcion_producto.config(text="Descripción: -")
                self.lbl_stock_actual.config(text="Stock actual: -")

    def guardar_stock(self):
        cantidad = self.entry_cantidad.get()
        if cantidad is None or cantidad == "":
            tk.messagebox.showerror("Error", "Ingrese una cantidad válida.")
            return
        self.inventario.aumentar_stock(self.producto_encontrado.id_producto, int(cantidad))
        tk.messagebox.showinfo("Éxito", "Stock actualizado correctamente.")
        self.actualizar_callback()
        self.cerrar()

    def cerrar(self):
        self.destroy()
