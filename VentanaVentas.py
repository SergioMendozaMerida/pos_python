from collections.abc import Callable
import tkinter as tk
import CarritoVenta as CV
from tkinter import messagebox, simpledialog, ttk
import FrameTerminarVenta as FTV

class VentanaVentas(tk.Frame):

    def __init__(self, inventario):
        super().__init__(bg="#f5f6fa")

        self.inventario = inventario

        self.app_bg = "#ecf0f3"
        self.panel_bg = "#ffffff"
        self.card_bg = "#ffffff"
        self.text_color = "#2d3436"
        self.sub_text = "#636e72"
        self.border_color = "#dfe6e9"
        self.primary_color = "#0984e3"
        self.primary_hover = "#74b9ff"
        self.success_color = "#00b894"
        self.danger_color = "#d63031"

        self.configure(bg=self.app_bg)

        self.frame_buscar = tk.Frame(self, bg=self.app_bg)
        self.frame_buscar.place(x=10, y=5, width=1180, height=95)

        tk.Label(
            self.frame_buscar,
            text="Buscar productos",
            bg=self.app_bg,
            fg=self.text_color,
            font=("Segoe UI", 13, "bold")
        ).place(x=10, y=10)

        search_panel = tk.Frame(self.frame_buscar, bg=self.panel_bg, bd=1, relief="solid")
        search_panel.place(x=10, y=45, width=600, height=42)

        tk.Label(
            search_panel,
            text="Nombre:",
            font=("Segoe UI", 10),
            bg=self.panel_bg,
            fg=self.sub_text
        ).place(x=10, y=10)
        self.entry_nombre = tk.Entry(
            search_panel,
            font=("Segoe UI", 10),
            bd=0,
            bg="#f8f9fb",
            fg=self.text_color,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground=self.border_color
        )
        self.entry_nombre.place(x=75, y=8, width=190, height=26)

        tk.Label(
            search_panel,
            text="Descripción:",
            font=("Segoe UI", 10),
            bg=self.panel_bg,
            fg=self.sub_text
        ).place(x=280, y=10)
        self.entry_descripcion = tk.Entry(
            search_panel,
            font=("Segoe UI", 10),
            bd=0,
            bg="#f8f9fb",
            fg=self.text_color,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground=self.border_color
        )
        self.entry_descripcion.place(x=365, y=8, width=190, height=26)

        btn_buscar = tk.Button(
            self.frame_buscar,
            text="Buscar",
            bg=self.primary_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            activebackground=self.primary_hover,
            cursor="hand2",
            command=lambda: self.buscar(self.entry_nombre.get(), self.entry_descripcion.get())
        )
        btn_buscar.place(x=630, y=50, width=100, height=30)

        self.entry_nombre.bind("<Return>", lambda e: self.buscar(self.entry_nombre.get(), self.entry_descripcion.get()))
        self.entry_descripcion.bind("<Return>", lambda e: self.buscar(self.entry_nombre.get(), self.entry_descripcion.get()))

        self.canvas_productos = tk.Canvas(self, bg=self.card_bg, highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(self.canvas_productos, orient="vertical", command=self.canvas_productos.yview)
        self.canvas_productos.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas_productos.place(x=10, y=110, width=400, height=520)

        self.frame_item_productos = tk.Frame(self.canvas_productos, bg=self.card_bg)
        self.frame_item_productos.place(x=5, y=5)

        self.canvas_productos.create_window(
            (0, 0),
            window=self.frame_item_productos,
            anchor="nw",
            width=380
        )

        self.frame_item_productos.bind(
            "<Configure>",
            lambda e: self.canvas_productos.configure(
                scrollregion=self.canvas_productos.bbox("all")
            )
        )

        self.canvas_productos.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas_productos.yview_scroll(
                int(-1 * (e.delta / 120)),
                "units"
            )
        )

        self.frame_item_carritos = tk.Frame(self, bg=self.app_bg)
        self.frame_item_carritos.place(x=420, y=110, width=600, height=520)

        self.frame_cliente = tk.Frame(self.frame_item_carritos, bg=self.panel_bg, bd=1, relief="solid")
        self.frame_cliente.place(x=10, y=10, width=580, height=130)

        tk.Label(
            self.frame_cliente,
            text="Datos del cliente",
            bg=self.panel_bg,
            fg=self.text_color,
            font=("Segoe UI", 11, "bold")
        ).place(x=10, y=10)

        self.entry_nombre_cliente = tk.Entry(
            self.frame_cliente,
            font=("Segoe UI", 10),
            bd=0,
            bg="#f8f9fb",
            fg=self.text_color,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground=self.border_color
        )
        self.entry_direccion = tk.Entry(
            self.frame_cliente,
            font=("Segoe UI", 10),
            bd=0,
            bg="#f8f9fb",
            fg=self.text_color,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground=self.border_color
        )
        self.entry_telefono = tk.Entry(
            self.frame_cliente,
            font=("Segoe UI", 10),
            bd=0,
            bg="#f8f9fb",
            fg=self.text_color,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground=self.border_color
        )
        self.entry_dpi = tk.Entry(
            self.frame_cliente,
            font=("Segoe UI", 10),
            bd=0,
            bg="#f8f9fb",
            fg=self.text_color,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground=self.border_color
        )
        self.entry_nit = tk.Entry(
            self.frame_cliente,
            font=("Segoe UI", 10),
            bd=0,
            bg="#f8f9fb",
            fg=self.text_color,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground=self.border_color
        )

        lbl_nombre_cliente = tk.Label(
            self.frame_cliente,
            text='Cliente:',
            bg=self.panel_bg,
            fg=self.sub_text,
            font=("Segoe UI", 10, "bold")
        )
        lbl_direccion = tk.Label(
            self.frame_cliente,
            text='Dirección:',
            bg=self.panel_bg,
            fg=self.sub_text,
            font=("Segoe UI", 10, "bold")
        )
        lbl_dpi = tk.Label(
            self.frame_cliente,
            text='DPI:',
            bg=self.panel_bg,
            fg=self.sub_text,
            font=("Segoe UI", 10, "bold")
        )
        lbl_nit = tk.Label(
            self.frame_cliente,
            text='NIT:',
            bg=self.panel_bg,
            fg=self.sub_text,
            font=("Segoe UI", 10, "bold")
        )
        lbl_telefono = tk.Label(
            self.frame_cliente,
            text='Teléfono:',
            bg=self.panel_bg,
            fg=self.sub_text,
            font=("Segoe UI", 10, "bold")
        )

        lbl_nombre_cliente.place(x=10, y=40, width=70)
        self.entry_nombre_cliente.place(x=90, y=40, width=190, height=26)
        lbl_direccion.place(x=300, y=40, width=70)
        self.entry_direccion.place(x=380, y=40, width=190, height=26)

        lbl_dpi.place(x=10, y=76, width=40)
        self.entry_dpi.place(x=55, y=76, width=120, height=26)
        lbl_nit.place(x=190, y=76, width=40)
        self.entry_nit.place(x=235, y=76, width=120, height=26)
        lbl_telefono.place(x=370, y=76, width=70)
        self.entry_telefono.place(x=445, y=76, width=130, height=26)

        columnas = ['producto', 'precio', 'cantidad', 'sub_total']
        self.tabla_carrito = ttk.Treeview(self.frame_item_carritos, columns=columnas, show="headings")
        self.tabla_carrito.heading('producto', text="Producto")
        self.tabla_carrito.heading('precio', text="Precio")
        self.tabla_carrito.heading('cantidad', text="Cantidad")
        self.tabla_carrito.heading('sub_total', text="SubTotal")
        self.tabla_carrito.column('producto', width=300)
        self.tabla_carrito.column('precio', width=100)
        self.tabla_carrito.column('cantidad', width=100)
        self.tabla_carrito.column('sub_total', width=90)
        style = ttk.Style()
        style.theme_use("clam") # El tema 'clam' es el más personalizable

        # Configurar el estilo general de la Tabla (Treeview)
        style.configure("Treeview",
                        background="#ffffff",       # Fondo de las celdas
                        foreground="#2d3436",       # Color de letra
                        rowheight=30,               # Filas más altas para que respiren
                        fieldbackground="#ffffff",
                        borderwidth=0,
                        font=("Segoe UI", 10))

        # Estilo de las cabeceras (Headers)
        style.configure("Treeview.Heading",
                        background="#f1f2f6",       # Gris muy suave
                        foreground="#2d3436",
                        relief="flat",
                        font=("Segoe UI", 10, "bold"))

        # Efecto al seleccionar una fila
        style.map("Treeview", 
                background=[('selected', "#74b9ff")], # Azul suave al seleccionar
                foreground=[('selected', "white")])
        self.tabla_carrito.place(x=10, y=120, width=580, height=370)

        self.frame_concretar_venta = tk.Frame(self, bg=self.panel_bg, bd=1, relief="solid")
        self.frame_concretar_venta.place(x=1030, y=110, width=160, height=520)

        tk.Label(
            self.frame_concretar_venta,
            text="Resumen",
            bg=self.panel_bg,
            fg=self.text_color,
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(20, 10))

        self.lbl_total = tk.Label(
            self.frame_concretar_venta,
            text=f"Q  {0:,.2f}",
            bg=self.panel_bg,
            fg=self.primary_color,
            font=("Segoe UI", 18, "bold")
        )
        self.lbl_total.pack(pady=(0, 25))

        btn_finalizar = tk.Button(
            self.frame_concretar_venta,
            text="Finalizar",
            bg=self.success_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            activebackground="#55efc4",
            cursor='hand2',
            command=self.concretar_venta
        )
        btn_finalizar.pack(fill="x", padx=10, pady=(0, 10), ipady=8)

        btn_eliminar_producto = tk.Button(
            self.frame_concretar_venta,
            text="Remover",
            bg=self.danger_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            activebackground="#ff7675",
            cursor='hand2',
            command=self.quitar_producto
        )
        btn_eliminar_producto.pack(fill="x", padx=10, pady=(0, 10), ipady=8)

        btn_cancelar = tk.Button(
            self.frame_concretar_venta,
            text="Cancelar",
            bg="#636e72",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            activebackground="#b2bec3",
            cursor='hand2',
            command=self.cancelar
        )
        btn_cancelar.pack(fill="x", padx=10, pady=(0, 10), ipady=8)

        self.carrito = CV.CarrtioVenta()

        self.show_productos()
        self.show_carrito()

    def buscar(self, nombre, descripcion):
        self.inventario.buscar_producto(nombre,descripcion)
        self.show_productos()

    def show_productos(self):
        for item in self.frame_item_productos.winfo_children():
            item.destroy()
            
        for producto in self.inventario.productos:
            frame = tk.Frame(
                self.frame_item_productos,
                bg="white",
                width=360,
                height=96,
                bd=1,
                relief="solid",
                highlightbackground=self.border_color,
                highlightcolor=self.border_color,
                highlightthickness=1
            )
            frame.propagate(False)
            frame.pack(pady=8)

            # Nombre: Esquina superior izquierda
            lbl_nombre = tk.Label(
                frame,
                text=producto.nombre,
                bg="white",
                fg=self.text_color,
                font=("Segoe UI", 11, "bold")
            )
            lbl_nombre.place(x=10, y=10) # 10px de margen desde arriba y la izquierda

            # Stock: Debajo del nombre
            lbl_stock = tk.Label(
                frame,
                text=f"Stock: {producto.stock}", # Añadí la palabra "Stock:" para más claridad
                bg="white",
                fg="#7f8c8d", # Un tono gris para que no compita con el precio
                font=("Segoe UI", 10)
            )
            lbl_stock.place(x=10, y=35) # Ubicado más abajo en el eje Y

            # Precio: Esquina superior derecha (Bastante visible)
            lbl_precio = tk.Label(
                frame,
                text=f"Q{producto.precio_venta:,.2f}",
                bg="white",
                fg="#27ae60",
                font=("Segoe UI", 14, "bold") # Aumenté el tamaño y puse negrita
            )
            # relx=0.95 lo manda casi al borde derecho, anchor="ne" ancla la esquina superior derecha
            lbl_precio.place(relx=0.95, y=10, anchor="ne") 

            # Botón Agregar: Esquina inferior derecha
            btn_agregar = tk.Button(
                frame,
                text="Agregar",
                bg="#0984e3",
                fg="white",
                activebackground="#74b9ff",
                relief="flat",
                cursor="hand2",
                command=lambda p=producto: self.agregar(p)
            )
            # relx=0.95 y rely=0.90 lo mandan abajo a la derecha, anchor="se" ancla la esquina inferior derecha
            btn_agregar.place(relx=0.95, rely=0.90, anchor="se")

    def agregar(self, producto):
        cantidad = simpledialog.askinteger("Cantidad", "Ingrese la Cantidad")
        
        if cantidad is None:
            return
        for pr in self.inventario.productos:
            if producto.id_producto == pr.id_producto:
                if cantidad > pr.stock:
                    messagebox.showerror("Error", f"Cantidad no disponible. Cantidad actual: {pr.stock}")
                    return
                pr.stock -= cantidad
                print(pr.stock)
        res = self.carrito.agregar_producto(producto.id_producto, cantidad)
        if res == False:
            messagebox.showerror("Error", "Cantidad No disponible.")
            return
        self.show_carrito()
        """for p in self.inventario.productos:
            if p.id_producto == producto.id_producto:
                p.stock -= cantidad"""
        #self.inventario.obtener_productos()
        self.show_productos()
        self.entry_nombre.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.calcular_total()

    def calcular_total(self):
        self.carrito.calcular_total()
        self.lbl_total.configure(text=f"Q   {self.carrito.total:,.2f}")

    def cancelar(self):
        respuesta = messagebox.askyesno("Cancelar", """¿Está seguro que desea cancelar la venta?
        Los productos y la información del cliente se borraran.""")
        if respuesta == False:
            return
        
        self.entry_nombre_cliente.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)
        self.entry_dpi.delete(0, tk.END)
        self.entry_nit.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.carrito.cancelar_venta()
        self.show_carrito()
        messagebox.showinfo("Canelado", "La venta se ha cancelado")

    def quitar_producto(self):
        item = int(self.tabla_carrito.selection()[0])
        cantidad = simpledialog.askinteger("Remover", "Escriba la cantidad final")

        for p in self.carrito.productos:
            if p["id_producto"] == item:
                p["cantidad"] = cantidad
                messagebox.showinfo("Cantidad", "Cantidad cambiada exitosamente.")
                self.show_carrito()
                return

    def show_carrito(self):
        for item in self.tabla_carrito.get_children():
            self.tabla_carrito.delete(item)

        for producto in self.carrito.productos:
            self.tabla_carrito.insert("",tk.END, iid=producto["id_producto"], values=(producto["nombre"], f"Q    {producto["precio_venta"]:,.2f}", 
                                                         producto["cantidad"], f"Q  {producto["sub_total"]:.2f}"))

    def concretar_venta(self):
        nombre = self.entry_nombre_cliente.get()
        direccion = self.entry_direccion.get()
        dpi = self.entry_dpi.get()
        nit = self.entry_nit.get()
        telefono = self.entry_telefono.get()

        self.carrito.set_datos_cliente(nombre, direccion, dpi, nit, telefono)

        frm_ter_venta = FTV.FrameTerminarVenta(self, self.carrito.numero_recibo,self.carrito.total,self.entry_nombre_cliente.get())
        #frm_ter_venta

        self.carrito.concretar_venta()

        self.show_carrito()

        messagebox.showinfo("Exito", "Venta registrada exitosamente.")