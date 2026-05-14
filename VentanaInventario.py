import tkinter as tk
from tkinter import ttk, messagebox
import Inventario as inv
import FormProductos as FP
import EditarProducto as EP


class VentanaInventario(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configuración de colores
        self.color_fondo = "#f0f0f0"
        self.color_primario = "#2c3e50"
        self.color_secundario = "#3498db"
        self.color_boton = "#27ae60"
        self.color_cancelar = "#e74c3c"
        self.color_boton_hover = "#229954"
        
        self.configure(bg=self.color_fondo)
        self.inventario = inv.Inventario()

        # Frame principal con padding
        self.main_frame = tk.Frame(self, bg=self.color_fondo)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame búsqueda
        self.frame_buscar = tk.LabelFrame(
            self.main_frame, 
            text="Buscar Productos", 
            font=("Arial", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_primario,
            padx=15,
            pady=15
        )
        self.frame_buscar.pack(fill="x", pady=(0, 15))

        # Labels y entries búsqueda - con mejor layout
        label_frame = tk.Frame(self.frame_buscar, bg=self.color_fondo)
        label_frame.pack(fill="x")

        tk.Label(label_frame, text="Nombre:", bg=self.color_fondo, fg=self.color_primario, font=("Arial", 9)).pack(side="left", padx=(0, 5))
        self.entry_nombre = tk.Entry(label_frame, width=20, font=("Arial", 9))
        self.entry_nombre.pack(side="left", padx=(0, 20))
        self.entry_nombre.bind("<Return>", lambda e:self.buscar_producto(self.entry_nombre.get(), self.entry_descripcion.get()))
        self.entry_nombre.bind("<KeyRelease>", self.iniciar_espera)

        tk.Label(label_frame, text="Descripción:", bg=self.color_fondo, fg=self.color_primario, font=("Arial", 9)).pack(side="left", padx=(0, 5))
        self.entry_descripcion = tk.Entry(label_frame, width=20, font=("Arial", 9))
        self.entry_descripcion.pack(side="left", padx=(0, 20))
        self.entry_descripcion.bind("<Return>", lambda e:self.buscar_producto(self.entry_nombre.get(), self.entry_descripcion.get()))
        self.entry_descripcion.bind("<KeyRelease>", self.iniciar_espera)

        btn_buscar = tk.Button(
            label_frame, 
            text="Buscar",
            bg=self.color_secundario,
            fg="white",
            font=("Arial", 9, "bold"),
            padx=15,
            command=lambda: self.buscar_producto(self.entry_nombre.get(), self.entry_descripcion.get())
        )
        btn_buscar.pack(side="left")

        # Frame para tabla y scrollbars
        self.frame_tabla = tk.LabelFrame(
            self.main_frame,
            text="Inventario de Productos",
            font=("Arial", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_primario,
            padx=5,
            pady=5
        )
        self.frame_tabla.pack(fill="both", expand=True, pady=(0, 15))

        # Frame para tabla y scrollbars
        tabla_scroll_frame = tk.Frame(self.frame_tabla, bg=self.color_fondo)
        tabla_scroll_frame.pack(fill="both", expand=True)

        self.columnas = ("id", "nombre", "descripcion", "presentacion", "categoria", "precio_compra", "precio_venta", "stock")
        self.tabla_productos = ttk.Treeview(tabla_scroll_frame, columns=self.columnas, show="headings", height=10)

        # Configurar headings
        self.tabla_productos.heading("id", text="ID")
        self.tabla_productos.heading("nombre", text="Producto")
        self.tabla_productos.heading("descripcion", text="Descripción")
        self.tabla_productos.heading("presentacion", text="Presentación")
        self.tabla_productos.heading("categoria", text="Categoría")
        self.tabla_productos.heading("precio_compra", text="P. Compra")
        self.tabla_productos.heading("precio_venta", text="P. Venta")
        self.tabla_productos.heading("stock", text="Stock")

        # Configurar ancho de columnas
        self.tabla_productos.column("id", width=0, stretch=False)  # Columna oculta
        self.tabla_productos.column("nombre", width=120, anchor="w")
        self.tabla_productos.column("descripcion", width=150, anchor="w")
        self.tabla_productos.column("presentacion", width=100, anchor="center")
        self.tabla_productos.column("categoria", width=100, anchor="center")
        self.tabla_productos.column("precio_compra", width=90, anchor="center")
        self.tabla_productos.column("precio_venta", width=90, anchor="center")
        self.tabla_productos.column("stock", width=70, anchor="center")

        # Scrollbars
        self.scroll_bar = tk.Scrollbar(tabla_scroll_frame, orient="vertical", command=self.tabla_productos.yview)
        self.tabla_productos.configure(yscrollcommand=self.scroll_bar.set)
        
        self.scroll_barx = tk.Scrollbar(tabla_scroll_frame, orient="horizontal", command=self.tabla_productos.xview)
        self.tabla_productos.configure(xscrollcommand=self.scroll_barx.set)

        # Empacar tabla y scrollbars
        self.tabla_productos.grid(row=0, column=0, sticky="nsew")
        self.scroll_bar.grid(row=0, column=1, sticky="ns")
        self.scroll_barx.grid(row=1, column=0, sticky="ew")
        
        tabla_scroll_frame.grid_rowconfigure(0, weight=1)
        tabla_scroll_frame.grid_columnconfigure(0, weight=1)

        # Frame de botones
        self.frame_botones = tk.Frame(self.main_frame, bg=self.color_fondo)
        self.frame_botones.pack(fill="x")

        self.btn_ingresar = tk.Button(
            self.frame_botones,
            text="➕ Ingresar Nuevo Producto",
            bg=self.color_boton,
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=12,
            cursor="hand2",
            command=self.abrir_formulario
        )
        self.btn_ingresar.pack(side="left", padx=(0, 10), pady=10)

        self.btn_editar = tk.Button(
            self.frame_botones,
            text="✏️ Editar Producto",
            bg=self.color_secundario,
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=12,
            cursor="hand2",
            command=self.abrir_editar_formulario
        )
        self.btn_editar.pack(side="left", padx=(0, 10), pady=10)

        self.btn_eliminar = tk.Button(
            self.frame_botones,
            text="🗑️ Eliminar Producto",
            bg=self.color_cancelar,
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=12,
            cursor="hand2",
            command=self.eliminar_producto_seleccionado
        )
        self.btn_eliminar.pack(side="left", padx=(0, 10), pady=10)

        self.cargar_productos()

        self.timer_id = None

    def iniciar_espera(self, event):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.timer_id = self.after(700, lambda: self.buscar_producto(self.entry_nombre.get(), self.entry_descripcion.get()))

    def abrir_formulario(self):
        formulario = FP.FormProductos(self, self.inventario, self.actualizar_tabla)

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
                producto.precio_compra,
                producto.precio_venta,
                producto.stock
            ))

    def buscar_producto(self, nombre="", descripcion=""):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        self.inventario.buscar_producto(nombre, descripcion)
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        for producto in self.inventario.productos:
            self.tabla_productos.insert("", tk.END, values=(
                producto.id_producto,
                producto.nombre,
                producto.descripcion,
                producto.presentacion,
                producto.categoria,
                producto.precio_compra,
                producto.precio_venta,
                producto.stock
            ))

    def abrir_editar_formulario(self):
        seleccion = self.tabla_productos.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione un producto de la tabla para editar.")
            return

        # Obtener el ID del producto seleccionado
        item = self.tabla_productos.item(seleccion[0])
        id_producto = item['values'][0]

        # Buscar el producto en la lista de productos
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

        # Obtener el ID del producto seleccionado
        item = self.tabla_productos.item(seleccion[0])
        id_producto = item['values'][0]
        nombre_producto = item['values'][1]  # Nombre del producto para el mensaje

        # Confirmar eliminación
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
