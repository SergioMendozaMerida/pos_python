import tkinter as tk
from tkinter import messagebox, ttk
import categoria.Categoria as Cat

class EditarProducto(tk.Toplevel):
    def __init__(self, parent, inventario, producto, actualizar_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.inventario = inventario
        self.producto = producto
        self.actualizar_callback = actualizar_callback

        self.categorias = Cat.Categorias().lista_categorias

        # Colores coordinados
        self.color_fondo = "#f8f9fa"
        self.color_header = "#2c3e50"
        self.color_primario = "#0984e3"
        self.color_exito = "#00b894"
        self.color_cancelar = "#d63031"
        self.color_entrada = "#ffffff"
        self.color_texto = "#2d3436"
        self.color_borde = "#dfe6e9"

        self.title("Editar Producto")
        self.geometry("520x620")
        self.resizable(False, False)
        self.configure(bg=self.color_fondo)

        # Header
        self.header_frame = tk.Frame(self, bg=self.color_header, height=60)
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)

        tk.Label(
            self.header_frame,
            text="Editar Producto",
            font=("Segoe UI", 16, "bold"),
            bg=self.color_header,
            fg="white"
        ).pack(pady=15)

        # Frame principal con padding
        self.main_frame = tk.Frame(self, bg=self.color_fondo)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Fila 1: Nombre y Categoría
        row1_frame = tk.Frame(self.main_frame, bg=self.color_fondo)
        row1_frame.pack(fill="x", pady=(0, 15))

        col1_frame = tk.Frame(row1_frame, bg=self.color_fondo)
        col1_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(col1_frame, text="Nombre *", font=("Segoe UI", 9, "bold"), bg=self.color_fondo, fg=self.color_texto).pack(anchor="w", pady=(0, 5))
        self.entry_nombre = tk.Entry(
            col1_frame, 
            font=("Segoe UI", 10), 
            bg=self.color_entrada, 
            relief="flat", 
            bd=0, 
            highlightthickness=1, 
            highlightbackground=self.color_borde,
            highlightcolor=self.color_primario
        )
        self.entry_nombre.pack(fill="both", expand=True, ipady=4)

        col2_frame = tk.Frame(row1_frame, bg=self.color_fondo)
        col2_frame.pack(side="left", fill="both", expand=True)

        tk.Label(col2_frame, text="Categoría", font=("Segoe UI", 9, "bold"), bg=self.color_fondo, fg=self.color_texto).pack(anchor="w", pady=(0, 5))
        self.entry_categoria = ttk.Combobox(
            col2_frame,
            font=("Segoe UI", 10),
            values=self.categorias
                )
        self.entry_categoria.pack(fill="both", expand=True, ipady=4)

        # Fila 2: Descripción
        tk.Label(self.main_frame, text="Descripción", font=("Segoe UI", 9, "bold"), bg=self.color_fondo, fg=self.color_texto).pack(anchor="w", pady=(0, 5))
        self.entry_descripcion = tk.Entry(
            self.main_frame, 
            font=("Segoe UI", 10), 
            bg=self.color_entrada, 
            relief="flat", 
            bd=0, 
            highlightthickness=1, 
            highlightbackground=self.color_borde,
            highlightcolor=self.color_primario
        )
        self.entry_descripcion.pack(fill="x", pady=(0, 15), ipady=4)

        # Fila 3: Presentación
        tk.Label(self.main_frame, text="Presentación", font=("Segoe UI", 9, "bold"), bg=self.color_fondo, fg=self.color_texto).pack(anchor="w", pady=(0, 5))
        self.entry_presentacion = tk.Entry(
            self.main_frame, 
            font=("Segoe UI", 10), 
            bg=self.color_entrada, 
            relief="flat", 
            bd=0, 
            highlightthickness=1, 
            highlightbackground=self.color_borde,
            highlightcolor=self.color_primario
        )
        self.entry_presentacion.pack(fill="x", pady=(0, 15), ipady=4)

        # Fila 4: Precios (Compra y Venta)
        row_precios = tk.Frame(self.main_frame, bg=self.color_fondo)
        row_precios.pack(fill="x", pady=(0, 15))

        col_compra = tk.Frame(row_precios, bg=self.color_fondo)
        col_compra.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(col_compra, text="Precio Compra Q", font=("Segoe UI", 9, "bold"), bg=self.color_fondo, fg=self.color_texto).pack(anchor="w", pady=(0, 5))
        self.entry_precio_compra = tk.Entry(
            col_compra, 
            font=("Segoe UI", 10), 
            bg=self.color_entrada, 
            relief="flat", 
            bd=0, 
            highlightthickness=1, 
            highlightbackground=self.color_borde,
            highlightcolor=self.color_primario
        )
        self.entry_precio_compra.pack(fill="both", expand=True, ipady=4)

        col_venta = tk.Frame(row_precios, bg=self.color_fondo)
        col_venta.pack(side="left", fill="both", expand=True)

        tk.Label(col_venta, text="Precio Venta Q", font=("Segoe UI", 9, "bold"), bg=self.color_fondo, fg=self.color_texto).pack(anchor="w", pady=(0, 5))
        self.entry_precio_venta = tk.Entry(
            col_venta, 
            font=("Segoe UI", 10), 
            bg=self.color_entrada, 
            relief="flat", 
            bd=0, 
            highlightthickness=1, 
            highlightbackground=self.color_borde,
            highlightcolor=self.color_primario
        )
        self.entry_precio_venta.pack(fill="both", expand=True, ipady=4)

        # Cargar datos del producto
        self.cargar_datos_producto()

        # Frame de botones
        btn_frame = tk.Frame(self.main_frame, bg=self.color_fondo)
        btn_frame.pack(fill="x", side="bottom")

        self.btn_guardar = tk.Button(
            btn_frame,
            text="✓ Actualizar",
            font=("Segoe UI", 11, "bold"),
            bg=self.color_exito,
            fg="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2",
            command=self.actualizar_producto
        )
        self.btn_guardar.pack(side="left", padx=(0, 10))

        self.btn_cancelar = tk.Button(
            btn_frame,
            text="✕ Cancelar",
            font=("Segoe UI", 11, "bold"),
            bg=self.color_cancelar,
            fg="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2",
            command=self.cerrar
        )
        self.btn_cancelar.pack(side="left")

        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.entry_nombre.focus()
        self.grab_set()

    def cargar_datos_producto(self):
        """Carga los datos del producto en los campos del formulario"""
        self.entry_nombre.insert(0, self.producto.nombre)
        self.entry_descripcion.insert(0, self.producto.descripcion)
        self.entry_presentacion.insert(0, self.producto.presentacion)
        self.entry_categoria.insert(0, self.producto.categoria)
        self.entry_precio_compra.insert(0, str(self.producto.precio_compra))
        self.entry_precio_venta.insert(0, str(self.producto.precio_venta))

    def actualizar_producto(self):
        nombre = self.entry_nombre.get().strip()
        descripcion = self.entry_descripcion.get().strip()
        presentacion = self.entry_presentacion.get().strip()
        categoria = self.entry_categoria.get().strip()
        precio_compra = self.entry_precio_compra.get().strip()
        precio_venta = self.entry_precio_venta.get().strip()

        if not nombre:
            messagebox.showwarning("Validación", "Debe ingresar el nombre del producto.")
            return

        try:
            precio_compra_val = float(precio_compra) if precio_compra else 0.0
            precio_venta_val = float(precio_venta) if precio_venta else 0.0
        except ValueError:
            messagebox.showwarning("Validación", "Precio y stock deben ser numéricos.")
            return

        self.inventario.editar_producto(
            self.producto.id_producto,
            nombre,
            descripcion,
            presentacion,
            categoria,
            precio_compra_val,
            precio_venta_val
        )

        if self.actualizar_callback:
            self.actualizar_callback()

        messagebox.showinfo("Éxito", "El producto se ha actualizado correctamente.")
        self.destroy()

    def cerrar(self):
        self.destroy()