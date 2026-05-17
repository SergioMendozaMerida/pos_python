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
        self.entry_codigo_producto = tk.Entry(
            self.main_frame,
            font=("Arial", 10),
            bg=self.color_entrada,
            bd=1,
            relief="solid"
        )
        self.entry_codigo_producto.pack(fill="x", pady=(0, 10))

        # Nombre del producto
        tk.Label(
            self.main_frame,
            text="Nombre del producto",
            font=("Arial", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w", pady=(0, 5))
        self.entry_nombre_producto = tk.Entry(
            self.main_frame,
            font=("Arial", 10),
            bg=self.color_entrada,
            bd=1,
            relief="solid"
        )
        self.entry_nombre_producto.pack(fill="x", pady=(0, 10))

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
            padx=10,
            pady=10
        )
        result_frame.pack(fill="both", expand=True, pady=(10, 0))

        self.lbl_producto_encontrado = tk.Label(
            result_frame,
            text="Ingrese código o nombre y presione Buscar.",
            font=("Arial", 10),
            bg=self.color_fondo,
            fg="#2c3e50",
            justify="left",
            anchor="nw"
        )
        self.lbl_producto_encontrado.pack(fill="both", expand=True)

        # Frame para botones con mejor diseño
        button_frame = tk.Frame(self.main_frame, bg=self.color_fondo)
        button_frame.pack(fill="x", pady=(20, 0))

        # Primera fila: Botón Buscar centrado
        search_frame = tk.Frame(button_frame, bg=self.color_fondo)
        search_frame.pack(fill="x", pady=(0, 10))

        self.btn_buscar = tk.Button(
            search_frame,
            text="🔍 Buscar",
            bg=self.color_primario,
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.buscar_producto_codigo
        )
        self.btn_buscar.pack(anchor="center")

        # Segunda fila: Botones Guardar y Cancelar
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
        self.entry_codigo_producto.focus()

    def buscar_producto_codigo(self):
        codigo = self.entry_codigo_producto.get()
        if codigo:
            self.producto_encontrado = self.inventario.buscar_ingresar_stock_por_codigo(codigo)
            if self.producto_encontrado:
                self.lbl_producto_encontrado.config(text=f"Producto encontrado: {self.producto_encontrado.nombre}")
            else:
                self.lbl_producto_encontrado.config(text="Producto no encontrado.")

    def guardar_stock(self):
        # TODO: Implementar lógica de ingreso de stock
        pass

    def cerrar(self):
        self.destroy()
