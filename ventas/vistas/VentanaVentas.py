from collections.abc import Callable
import tkinter as tk
import ventas.logica.CarritoVenta as CV
from tkinter import messagebox, simpledialog, ttk
import ventas.vistas.FrameTerminarVenta as FTV
import caja.FrameAbrirCerrarCaja as FAC
import caja.FrameDetalleCaja as FDC
import ventas.vistas.FrameModificar as FM

class VentanaVentas(tk.Frame):

    def __init__(self, inventario, reporte_ventas, actualizar_recibos, actualizar_ventas, usuario, caja):
        super().__init__(bg="#f5f6fa")

        self.inventario = inventario
        self.reporte_ventas = reporte_ventas
        self.actualizar_recibos = actualizar_recibos
        self.actualizar_ventas = actualizar_ventas
        self.usuario = usuario
        self.caja = caja
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

        # Configuración de grid para el frame principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.frame_buscar = tk.Frame(self, bg=self.app_bg)
        self.frame_buscar.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        self.frame_buscar.grid_columnconfigure(0, weight=1)

        tk.Label(
            self.frame_buscar,
            text="Buscar productos",
            bg=self.app_bg,
            fg=self.text_color,
            font=("Segoe UI", 13, "bold")
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        # Contenedor para inputs y botón buscar
        search_controls_frame = tk.Frame(self.frame_buscar, bg=self.app_bg)
        search_controls_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        search_controls_frame.grid_columnconfigure(0, weight=1) # search_panel
        search_controls_frame.grid_columnconfigure(1, weight=0) # btn_buscar

        search_panel = tk.Frame(search_controls_frame, bg=self.panel_bg, bd=1, relief="solid")
        search_panel.grid(row=0, column=0, sticky="ew")
        # Configurar columnas para que los Entry se expandan
        search_panel.grid_columnconfigure(1, weight=1)
        search_panel.grid_columnconfigure(3, weight=1)
        search_panel.grid_columnconfigure(5, weight=1)

        tk.Label(search_panel, text="Código:", font=("Segoe UI", 10), bg=self.panel_bg, fg=self.sub_text).grid(row=0, column=0, padx=(10, 5), pady=8, sticky="w")
        self.entry_codigo = tk.Entry(
            search_panel, 
            font=("Segoe UI", 10), 
            bd=0, 
            bg="#ffffff", 
            fg=self.text_color, 
            highlightthickness=1, 
            highlightcolor=self.primary_color, 
            highlightbackground="#b2bec3",
            insertbackground=self.primary_color
        )
        self.entry_codigo.grid(row=0, column=1, sticky="ew", padx=5, pady=8)

        tk.Label(search_panel, text="Nombre:", font=("Segoe UI", 10), bg=self.panel_bg, fg=self.sub_text).grid(row=0, column=2, padx=(10, 5), pady=8, sticky="w")
        self.entry_nombre = tk.Entry(
            search_panel, 
            font=("Segoe UI", 10), 
            bd=0, 
            bg="#ffffff", 
            fg=self.text_color, 
            highlightthickness=1, 
            highlightcolor=self.primary_color, 
            highlightbackground="#b2bec3",
            insertbackground=self.primary_color
        )
        self.entry_nombre.grid(row=0, column=3, sticky="ew", padx=5, pady=8)

        tk.Label(search_panel, text="Descripción:", font=("Segoe UI", 10), bg=self.panel_bg, fg=self.sub_text).grid(row=0, column=4, padx=(10, 5), pady=8, sticky="w")
        self.entry_descripcion = tk.Entry(
            search_panel, 
            font=("Segoe UI", 10), 
            bd=0, 
            bg="#ffffff", 
            fg=self.text_color, 
            highlightthickness=1, 
            highlightcolor=self.primary_color, 
            highlightbackground="#b2bec3",
            insertbackground=self.primary_color
        )
        self.entry_descripcion.grid(row=0, column=5, sticky="ew", padx=(5, 10), pady=8)

        btn_buscar = tk.Button(
            search_controls_frame,
            text="Buscar",
            bg=self.primary_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            activebackground=self.primary_hover,
            cursor="hand2",
            command=lambda: self.buscar(self.entry_nombre.get(), self.entry_descripcion.get())
        )
        btn_buscar.grid(row=0, column=1, padx=(10, 0), sticky="ns", ipadx=15)

        self.entry_codigo.bind("<Return>", lambda e: self.buscar_por_codigo(self.entry_codigo.get()))
        self.entry_nombre.bind("<Return>", lambda e: self.buscar(self.entry_nombre.get(), self.entry_descripcion.get()))
        self.entry_descripcion.bind("<Return>", lambda e: self.buscar(self.entry_nombre.get(), self.entry_descripcion.get()))

        # Contenedor central para las 3 columnas
        self.main_container = tk.Frame(self, bg=self.app_bg)
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.main_container.grid_columnconfigure(0, weight=1, minsize=380) # Productos
        self.main_container.grid_columnconfigure(1, weight=2, minsize=450) # Carrito
        self.main_container.grid_columnconfigure(2, weight=1, minsize=250) # Resumen
        self.main_container.grid_rowconfigure(0, weight=1)

        # 1. Columna Productos
        self.canvas_productos = tk.Canvas(self.main_container, bg=self.card_bg, highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(self.canvas_productos, orient="vertical", command=self.canvas_productos.yview)
        self.canvas_productos.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas_productos.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        self.frame_item_productos = tk.Frame(self.canvas_productos, bg=self.card_bg)

        self.product_window = self.canvas_productos.create_window(
            (0, 0),
            window=self.frame_item_productos,
            anchor="nw"
        )

        # Ajustar ancho de tarjetas al redimensionar canvas
        self.canvas_productos.bind("<Configure>", lambda e: self.canvas_productos.itemconfig(self.product_window, width=e.width))

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

        # 2. Columna Carrito
        self.frame_item_carritos = tk.Frame(self.main_container, bg=self.app_bg)
        self.frame_item_carritos.grid(row=0, column=1, sticky="nsew", padx=5)

        self.frame_cliente = tk.Frame(self.frame_item_carritos, bg=self.panel_bg, bd=1, relief="solid")
        self.frame_cliente.pack(fill="x", pady=(0, 10))

        tk.Label(
            self.frame_cliente,
            text="Datos del cliente",
            bg=self.panel_bg,
            fg=self.text_color,
            font=("Segoe UI", 11, "bold")
        ).grid(row=0, column=0, columnspan=6, sticky="w", padx=10, pady=10)

        # Configurar columnas internas del frame_cliente para que los Entry se expandan
        self.frame_cliente.grid_columnconfigure((1, 3, 5), weight=1)

        self.entry_nombre_cliente = tk.Entry(
            self.frame_cliente,
            font=("Segoe UI", 10),
            bd=0,
            bg="#ffffff",
            fg=self.text_color,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground="#b2bec3",
            insertbackground=self.primary_color
        )
        self.entry_direccion = tk.Entry(
            self.frame_cliente,
            font=("Segoe UI", 10),
            bd=0,
            bg="#ffffff",
            fg=self.text_color,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground="#b2bec3",
            insertbackground=self.primary_color
        )
        self.entry_telefono = tk.Entry(
            self.frame_cliente,
            font=("Segoe UI", 10),
            bd=0,
            bg="#ffffff",
            fg=self.text_color,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground="#b2bec3",
            insertbackground=self.primary_color
        )
        self.entry_dpi = tk.Entry(
            self.frame_cliente,
            font=("Segoe UI", 10),
            bd=0,
            bg="#ffffff",
            fg=self.text_color,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground="#b2bec3",
            insertbackground=self.primary_color
        )
        self.entry_nit = tk.Entry(
            self.frame_cliente,
            font=("Segoe UI", 10),
            bd=0,
            bg="#ffffff",
            fg=self.text_color,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            highlightbackground="#b2bec3",
            insertbackground=self.primary_color
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

        lbl_nombre_cliente.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")
        self.entry_nombre_cliente.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        lbl_direccion.grid(row=1, column=2, padx=(10, 5), pady=5, sticky="w")
        self.entry_direccion.grid(row=1, column=3, columnspan=3, padx=(5, 10), pady=5, sticky="ew")

        lbl_dpi.grid(row=2, column=0, padx=(10, 5), pady=5, sticky="w")
        self.entry_dpi.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        lbl_nit.grid(row=2, column=2, padx=(10, 5), pady=5, sticky="w")
        self.entry_nit.grid(row=2, column=3, padx=5, pady=5, sticky="ew")
        lbl_telefono.grid(row=2, column=4, padx=(10, 5), pady=5, sticky="w")
        self.entry_telefono.grid(row=2, column=5, padx=(5, 10), pady=5, sticky="ew")

        columnas = ['producto', 'precio', 'cantidad', 'sub_total']
        self.tabla_carrito = ttk.Treeview(self.frame_item_carritos, columns=columnas, show="headings")
        self.tabla_carrito.heading('producto', text="Producto")
        self.tabla_carrito.heading('precio', text="Precio")
        self.tabla_carrito.heading('cantidad', text="Cantidad")
        self.tabla_carrito.heading('sub_total', text="SubTotal")
        self.tabla_carrito.column('producto', width=150) # Ajustado para mejor responsividad
        self.tabla_carrito.column('precio', width=80)    # Ajustado
        self.tabla_carrito.column('cantidad', width=60)  # Ajustado
        self.tabla_carrito.column('sub_total', width=100) # Ajustado
        style = ttk.Style()
        style.theme_use("clam") # El tema 'clam' es el más personalizable

        self.scrollbar_table = ttk.Scrollbar(self.tabla_carrito, orient="vertical", command=self.tabla_carrito.yview)
        self.tabla_carrito.configure(yscrollcommand=self.scrollbar_table.set)
        self.scrollbar_table.pack(side="right", fill="y")

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
        self.tabla_carrito.pack(fill="both", expand=True, padx=0, pady=0)

        # 3. Columna Resumen y Botones
        self.frame_concretar_venta = tk.Frame(self.main_container, bg=self.panel_bg, bd=1, relief="solid")
        self.frame_concretar_venta.grid(row=0, column=2, sticky="nsew", padx=(5, 0))

        # Cabecera distintiva para el control de Caja (Estado de la Jornada)
        self.caja_header = tk.Frame(self.frame_concretar_venta, bg="#f8f9fb")
        self.caja_header.pack(fill="x", side="top", pady=(1, 15))

        self.btn_abrir_cerrar_caja = tk.Button(self.caja_header, command=self.cambiar_estado_caja)
        self.btn_ver_estado_caja = tk.Button(self.caja_header, command=self.mostrar_detalle_caja)
        self.actualizar_ui_caja()
        

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

        btn_quitar_producto = tk.Button(
            self.frame_concretar_venta,
            text="Quitar producto",
            bg=self.danger_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            activebackground="#ff7675",
            cursor='hand2',
            command=self.quitar_producto
        )
        btn_quitar_producto.pack(fill="x", padx=10, pady=(0, 10), ipady=8)

        btn_Cantidad = tk.Button(
            self.frame_concretar_venta,
            text="Modificar",
            bg=self.danger_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            activebackground="#ff7675",
            cursor='hand2',
            command=self.cambiar_cantidad
        )
        btn_Cantidad.pack(fill="x", padx=10, pady=(0, 10), ipady=8)

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

        self.carrito = CV.CarrtioVenta(self.usuario)
        self.timer_id = None

        self.show_productos()
        self.show_carrito()

        self.entry_codigo.focus()
        self.entry_nombre.bind("<KeyRelease>", self.iniciar_espera)
        self.entry_descripcion.bind("<KeyRelease>", self.iniciar_espera)

    def actualizar_ui_caja(self):
        """Actualiza el diseño, color e icono del botón según el estado de la caja"""
        if not self.caja.estado:
            # Caso: Caja Cerrada -> Sugerir Apertura
            self.btn_abrir_cerrar_caja.config(
                text="🔓 ABRIR CAJA",
                bg=self.success_color,
                activebackground="#009476",
                fg="white",
                font=("Segoe UI", 11, "bold"),
                bd=0,
                cursor="hand2"
            )
        else:
            # Caso: Caja Abierta -> Sugerir Cierre
            self.btn_abrir_cerrar_caja.config(
                text="🔒 CERRAR JORNADA",
                bg=self.danger_color,
                activebackground="#b32626",
                fg="white",
                font=("Segoe UI", 11, "bold"),
                bd=0,
                cursor="hand2"
            )

        # Botón principal siempre arriba
        self.btn_abrir_cerrar_caja.pack(fill="x", padx=15, pady=(15, 5), ipady=10)

        # Diseño distintivo para el botón de ver detalle (estilo secundario elegante)
        self.btn_ver_estado_caja.config(
            text="📋 VER RESUMEN DE SESIÓN",
            bg="#2c3e50", 
            activebackground="#34495e",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            cursor="hand2"
        )

        # Mostrar detalle solo si la caja está abierta, ubicado debajo
        if self.caja.estado:
            self.btn_ver_estado_caja.pack(fill="x", padx=15, pady=(5, 15), ipady=5)
        else:
            self.btn_ver_estado_caja.pack_forget()

    def cambiar_estado_caja(self):
        if self.caja.estado == True:
            FAC.FrameCerrarCaja(self, self.caja, self.actualizar_ui_caja, self.show_productos)
        else:
            FAC.FrameAbrirCaja(self, self.caja, self.actualizar_ui_caja, self.show_productos)

    def mostrar_detalle_caja(self):
        FDC.FrameDetalleCaja(self, self.caja)

    def buscar_por_codigo(self, codigo):
        if not codigo:
            return

        producto = self.inventario.buscar_producto_por_codigo(codigo)
        if producto is None:
            self.entry_codigo.delete(0, tk.END)
            messagebox.showerror("Error", "Código no encontrado.")
            return
        
        if self.caja.estado == False:
            self.entry_codigo.delete(0, tk.END)
            messagebox.showerror("Error", "La caja se encuentra cerrada. Debe aperturar caja para registrar una venta.")
            return

        self.carrito.agregar_producto(producto.id_producto, 1)
        self.show_carrito()
        self.show_productos()
        self.entry_codigo.delete(0, tk.END)
        self.calcular_total()

    def iniciar_espera(self, event):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.timer_id = self.after(750, lambda: self.buscar(self.entry_nombre.get(), self.entry_descripcion.get()))

    def buscar(self, nombre, descripcion):
        self.inventario.buscar_producto(nombre, descripcion)
        self.show_productos()

    def show_productos(self):
        for item in self.frame_item_productos.winfo_children():
            item.destroy()
            
        for producto in self.inventario.productos:
            # Contenedor principal de la Card
            card = tk.Frame(
                self.frame_item_productos,
                bg="white",
                height=115,
                highlightthickness=1,
                highlightbackground=self.border_color,
                padx=15,
                pady=10
            )
            card.pack_propagate(False)
            card.pack(fill="x", padx=15, pady=8)

            # Panel Izquierdo: Información textual
            info_frame = tk.Frame(card, bg="white")
            info_frame.pack(side="left", fill="both", expand=True)

            tk.Label(
                info_frame, 
                text=producto.nombre, 
                bg="white", 
                fg=self.text_color, 
                font=("Segoe UI", 12, "bold"), 
                anchor="w"
            ).pack(fill="x")

            # Cálculo de stock disponible en tiempo real
            stock_actual = producto.stock
            for pc in self.carrito.productos:
                if pc["id_producto"] == producto.id_producto:
                    stock_actual -= pc["cantidad"]

            # Badge de Stock con color condicional
            color_stock = self.success_color if stock_actual > 5 else self.danger_color
            stock_label = tk.Label(
                info_frame, 
                text=f"Disponible: {stock_actual} unidades", 
                bg="white", 
                fg=color_stock, 
                font=("Segoe UI", 9, "bold"), 
                anchor="w"
            )
            stock_label.pack(fill="x", pady=(2, 0))

            # Pequeña descripción o presentación
            presentacion = producto.presentacion if producto.presentacion else "Sin presentación"
            tk.Label(
                info_frame, 
                text=f"Presentación: {presentacion}", 
                bg="white", 
                fg=self.sub_text, 
                font=("Segoe UI", 9), 
                anchor="w"
            ).pack(fill="x", pady=(2, 0))

            # Panel Derecho: Precio y Acción
            action_frame = tk.Frame(card, bg="white")
            action_frame.pack(side="right", fill="y", padx=(10, 0))

            tk.Label(
                action_frame, 
                text=f"Q{producto.precio_venta:,.2f}", 
                bg="white", 
                fg=self.primary_color, 
                font=("Segoe UI", 15, "bold"), 
                anchor="e"
            ).pack(fill="x", pady=(0, 5))

            btn_agregar = tk.Button(
                action_frame,
                text="+ Agregar",
                bg=self.primary_color,
                fg="white",
                font=("Segoe UI", 9, "bold"),
                relief="flat",
                bd=0,
                padx=15,
                pady=6,
                cursor="hand2",
                activebackground=self.primary_hover,
                command=lambda p=producto: self.agregar(p),
            )
            btn_agregar.pack(side="bottom", anchor="e")

    def agregar(self, producto):

        if self.caja.estado == False:
            messagebox.showerror("Error", "La caja se encuentra cerrada. Debe aperturar caja para registrar una venta.")
            return

        cantidad = simpledialog.askinteger("Cantidad", "Ingrese la Cantidad")
        
        if cantidad is None:
            return
        
        res = self.carrito.agregar_producto(producto.id_producto, cantidad)
        if res == False:
            messagebox.showerror("Error", "Cantidad No disponible.")
            return
        self.show_carrito()
        self.show_productos()
        self.entry_codigo.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.calcular_total()

    def calcular_total(self):
        self.carrito.calcular_total()
        self.lbl_total.configure(text=f"Q   {self.carrito.total:,.2f}")

    def cancelar(self):
        respuesta = messagebox.askyesno("Cancelar", "¿Está seguro que desea cancelar la venta? Los productos y la información del cliente se borraran.")
        if respuesta == False:
            return
        
        self.entry_nombre_cliente.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)
        self.entry_dpi.delete(0, tk.END)
        self.entry_nit.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.carrito.cancelar_venta()
        self.show_carrito()
        self.show_productos()
        messagebox.showinfo("Canelado", "La venta se ha cancelado")

    def quitar_producto(self):
        selection = self.tabla_carrito.selection()
        
        if not selection:
            messagebox.showerror("Error", "Por Favor seleccione un producto.")
            return

        item = int(selection[0])

        respuesta = messagebox.askyesno("Quitar Producto", "¿Está seguro que desea quitar este producto de la venta?")
        if respuesta:
            self.carrito.quitar_producto(item)
            messagebox.showinfo("Exito", "El producto ha sido removido.")
            self.show_carrito()
            self.show_productos()

    def cambiar_cantidad(self):

        selection = self.tabla_carrito.selection()

        if not selection:
            messagebox.showerror("Error", "Por Favor seleccione un producto.")
            return

        item = int(selection[0])
        for pr in self.carrito.productos:
            if pr["id_producto"] == item:
                frame_modificar = FM.FrameModificarVenta(self, self.carrito, item, pr, self.calcular_total, self.show_carrito, self.show_productos)
        #cantidad = simpledialog.askinteger("Remover", "Escriba la cantidad final")

        """if cantidad is not None:
            
            respuesta = self.carrito.cambiar_cantidad(cantidad,item)
            if respuesta == False:
                messagebox.showerror("Error", "Cantidad no disponible.")
            self.show_productos()
            self.show_carrito()"""

    def show_carrito(self):
        for item in self.tabla_carrito.get_children():
            self.tabla_carrito.delete(item)

        for producto in self.carrito.productos:
            self.tabla_carrito.insert("",tk.END, iid=producto["id_producto"], values=(producto["nombre"], f"Q    {producto["precio_venta"]:,.2f}", 
                                                         producto["cantidad"], f"Q  {producto["sub_total"]:.2f}"))

    def concretar_venta(self):

        if self.carrito.productos == []:
            messagebox.showwarning("Carrito vacío", "No hay productos agregados al carrito")
            return

        nombre = self.entry_nombre_cliente.get()
        direccion = self.entry_direccion.get()
        dpi = self.entry_dpi.get()
        nit = self.entry_nit.get()
        telefono = self.entry_telefono.get()

        self.carrito.set_datos_cliente(nombre, direccion, dpi, nit, telefono)

        frm_ter_venta = FTV.FrameTerminarVenta(self, self.carrito, self.limpiar_carrito, self.actualizar_recibos, 
                                               self.actualizar_ventas, self.usuario, self.calcular_total)

        self.show_carrito()
        
    def limpiar_carrito(self):
        for item in self.tabla_carrito.get_children():
            self.tabla_carrito.delete(item)

        self.entry_nombre_cliente.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)
        self.entry_nit.delete(0, tk.END)
        self.entry_dpi.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
    
        self.show_carrito()