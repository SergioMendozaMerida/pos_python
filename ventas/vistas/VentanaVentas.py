from collections.abc import Callable
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import customtkinter as ctk
import ventas.logica.CarritoVenta as CV
import ventas.vistas.FrameTerminarVenta as FTV
import caja.FrameAbrirCerrarCaja as FAC
import caja.FrameDetalleCaja as FDC
import ventas.vistas.FrameModificar as FM

class VentanaVentas(ctk.CTkFrame):

    def __init__(self, master, inventario, reporte_ventas, actualizar_recibos, actualizar_ventas, usuario, caja):
        super().__init__(master, fg_color="#f5f6fa")

        self.inventario = inventario
        self.reporte_ventas = reporte_ventas
        self.actualizar_recibos = actualizar_recibos
        self.actualizar_ventas = actualizar_ventas
        self.usuario = usuario
        self.caja = caja
        self.app_bg = "#f5f6fa"
        self.panel_bg = "#ffffff"
        self.card_bg = "#ffffff"
        self.text_color = "#2d3436"
        self.sub_text = "#636e72"
        self.border_color = "#dfe6e9"
        self.primary_color = "#0984e3"
        self.primary_hover = "#74b9ff"
        self.success_color = "#00b894"
        self.danger_color = "#d63031"

        # Configuración de grid para el frame principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. Contenedor de Búsqueda
        self.frame_buscar = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_buscar.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        self.frame_buscar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.frame_buscar,
            text="Buscar productos",
            text_color=self.text_color,
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        search_controls_frame = ctk.CTkFrame(self.frame_buscar, fg_color="transparent")
        search_controls_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        search_controls_frame.grid_columnconfigure(0, weight=1)
        search_controls_frame.grid_columnconfigure(1, weight=0)

        search_panel = ctk.CTkFrame(
            search_controls_frame, 
            fg_color=self.panel_bg, 
            corner_radius=8,
            border_width=1,
            border_color=self.border_color
        )
        search_panel.grid(row=0, column=0, sticky="ew")
        search_panel.grid_columnconfigure(1, weight=1)
        search_panel.grid_columnconfigure(3, weight=1)
        search_panel.grid_columnconfigure(5, weight=1)

        ctk.CTkLabel(
            search_panel, 
            text="Código:", 
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), 
            text_color=self.sub_text
        ).grid(row=0, column=0, padx=(10, 5), pady=8, sticky="w")

        self.entry_codigo = ctk.CTkEntry(
            search_panel,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            placeholder_text="Código...",
            height=38
        )
        self.entry_codigo.grid(row=0, column=1, sticky="ew", padx=5, pady=8)

        ctk.CTkLabel(
            search_panel, 
            text="Nombre:", 
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), 
            text_color=self.sub_text
        ).grid(row=0, column=2, padx=(10, 5), pady=8, sticky="w")

        self.entry_nombre = ctk.CTkEntry(
            search_panel,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            placeholder_text="Nombre...",
            height=38
        )
        self.entry_nombre.grid(row=0, column=3, sticky="ew", padx=5, pady=8)

        ctk.CTkLabel(
            search_panel, 
            text="Descripción:", 
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), 
            text_color=self.sub_text
        ).grid(row=0, column=4, padx=(10, 5), pady=8, sticky="w")

        self.entry_descripcion = ctk.CTkEntry(
            search_panel,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            placeholder_text="Descripción...",
            height=38
        )
        self.entry_descripcion.grid(row=0, column=5, sticky="ew", padx=(5, 10), pady=8)

        btn_buscar = ctk.CTkButton(
            search_controls_frame,
            text="Buscar",
            fg_color=self.primary_color,
            hover_color=self.primary_hover,
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=38,
            width=110,
            command=lambda: self.buscar(self.entry_nombre.get(), self.entry_descripcion.get())
        )
        btn_buscar.grid(row=0, column=1, padx=(10, 0), sticky="ns")

        self.entry_codigo.bind("<Return>", lambda e: self.buscar_por_codigo(self.entry_codigo.get()))
        self.entry_nombre.bind("<Return>", lambda e: self.buscar(self.entry_nombre.get(), self.entry_descripcion.get()))
        self.entry_descripcion.bind("<Return>", lambda e: self.buscar(self.entry_nombre.get(), self.entry_descripcion.get()))

        # Contenedor central para las 3 columnas
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.main_container.grid_columnconfigure(0, weight=1, minsize=380) # Productos
        self.main_container.grid_columnconfigure(1, weight=2, minsize=450) # Carrito
        self.main_container.grid_columnconfigure(2, weight=1, minsize=250) # Resumen
        self.main_container.grid_rowconfigure(0, weight=1)

        # 1. Columna Productos (Scrollable Frame de CustomTkinter)
        self.frame_item_productos = ctk.CTkScrollableFrame(
            self.main_container,
            fg_color=self.card_bg,
            corner_radius=8,
            border_width=1,
            border_color=self.border_color
        )
        self.frame_item_productos.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # 2. Columna Carrito
        self.frame_item_carritos = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frame_item_carritos.grid(row=0, column=1, sticky="nsew", padx=5)

        self.frame_cliente = ctk.CTkFrame(
            self.frame_item_carritos, 
            fg_color=self.panel_bg, 
            corner_radius=8,
            border_width=1,
            border_color=self.border_color
        )
        self.frame_cliente.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            self.frame_cliente,
            text="Datos del cliente",
            text_color=self.text_color,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        ).grid(row=0, column=0, columnspan=6, sticky="w", padx=10, pady=8)

        self.frame_cliente.grid_columnconfigure((1, 3, 5), weight=1)

        self.entry_nombre_cliente = ctk.CTkEntry(
            self.frame_cliente,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Nombre del cliente...",
            height=34
        )
        self.entry_direccion = ctk.CTkEntry(
            self.frame_cliente,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Dirección...",
            height=34
        )
        self.entry_telefono = ctk.CTkEntry(
            self.frame_cliente,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Teléfono...",
            height=34
        )
        self.entry_dpi = ctk.CTkEntry(
            self.frame_cliente,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="DPI...",
            height=34
        )
        self.entry_nit = ctk.CTkEntry(
            self.frame_cliente,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="NIT...",
            height=34
        )

        ctk.CTkLabel(
            self.frame_cliente,
            text='Cliente:',
            text_color=self.sub_text,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")
        self.entry_nombre_cliente.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(
            self.frame_cliente,
            text='Dirección:',
            text_color=self.sub_text,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=1, column=2, padx=(10, 5), pady=5, sticky="w")
        self.entry_direccion.grid(row=1, column=3, columnspan=3, padx=(5, 10), pady=5, sticky="ew")

        ctk.CTkLabel(
            self.frame_cliente,
            text='DPI:',
            text_color=self.sub_text,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=2, column=0, padx=(10, 5), pady=5, sticky="w")
        self.entry_dpi.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(
            self.frame_cliente,
            text='NIT:',
            text_color=self.sub_text,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=2, column=2, padx=(10, 5), pady=5, sticky="w")
        self.entry_nit.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(
            self.frame_cliente,
            text='Teléfono:',
            text_color=self.sub_text,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=2, column=4, padx=(10, 5), pady=5, sticky="w")
        self.entry_telefono.grid(row=2, column=5, padx=(5, 10), pady=5, sticky="ew")

        columnas = ['producto', 'precio', 'cantidad', 'sub_total']
        self.tabla_carrito = ttk.Treeview(self.frame_item_carritos, columns=columnas, show="headings")
        self.tabla_carrito.heading('producto', text="Producto")
        self.tabla_carrito.heading('precio', text="Precio")
        self.tabla_carrito.heading('cantidad', text="Cantidad")
        self.tabla_carrito.heading('sub_total', text="SubTotal")
        self.tabla_carrito.column('producto', width=150)
        self.tabla_carrito.column('precio', width=80)
        self.tabla_carrito.column('cantidad', width=60)
        self.tabla_carrito.column('sub_total', width=100)
        
        style = ttk.Style()
        style.theme_use("clam")

        self.scrollbar_table = ttk.Scrollbar(self.tabla_carrito, orient="vertical", command=self.tabla_carrito.yview)
        self.tabla_carrito.configure(yscrollcommand=self.scrollbar_table.set)
        self.scrollbar_table.pack(side="right", fill="y")

        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#2d3436",
                        rowheight=34,
                        fieldbackground="#ffffff",
                        borderwidth=0,
                        font=("Segoe UI", 12))

        style.configure("Treeview.Heading",
                        background="#f1f2f6",
                        foreground="#2d3436",
                        relief="flat",
                        font=("Segoe UI", 12, "bold"))

        style.map("Treeview", 
                background=[('selected', "#74b9ff")],
                foreground=[('selected', "white")])
        self.tabla_carrito.pack(fill="both", expand=True, padx=0, pady=0)

        # 3. Columna Resumen y Botones
        self.frame_concretar_venta = ctk.CTkFrame(
            self.main_container, 
            fg_color=self.panel_bg, 
            corner_radius=8,
            border_width=1,
            border_color=self.border_color
        )
        self.frame_concretar_venta.grid(row=0, column=2, sticky="nsew", padx=(5, 0))

        self.caja_header = ctk.CTkFrame(self.frame_concretar_venta, fg_color="#f8f9fb", corner_radius=6)
        self.caja_header.pack(fill="x", side="top", pady=(5, 15), padx=5)

        self.btn_abrir_cerrar_caja = ctk.CTkButton(self.caja_header, command=self.cambiar_estado_caja)
        self.btn_ver_estado_caja = ctk.CTkButton(self.caja_header, command=self.mostrar_detalle_caja)
        self.actualizar_ui_caja()

        ctk.CTkLabel(
            self.frame_concretar_venta,
            text="Resumen",
            text_color=self.text_color,
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold")
        ).pack(pady=(15, 5))

        self.lbl_total = ctk.CTkLabel(
            self.frame_concretar_venta,
            text=f"Q  {0:,.2f}",
            text_color=self.primary_color,
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        )
        self.lbl_total.pack(pady=(0, 20))

        btn_finalizar = ctk.CTkButton(
            self.frame_concretar_venta,
            text="Finalizar",
            fg_color=self.success_color,
            hover_color="#009476",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=42,
            command=self.concretar_venta
        )
        btn_finalizar.pack(fill="x", padx=15, pady=(0, 8))

        btn_quitar_producto = ctk.CTkButton(
            self.frame_concretar_venta,
            text="Quitar producto",
            fg_color=self.danger_color,
            hover_color="#b32626",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=42,
            command=self.quitar_producto
        )
        btn_quitar_producto.pack(fill="x", padx=15, pady=(0, 8))

        btn_Cantidad = ctk.CTkButton(
            self.frame_concretar_venta,
            text="Modificar",
            fg_color="#e67e22",
            hover_color="#d35400",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=42,
            command=self.cambiar_cantidad
        )
        btn_Cantidad.pack(fill="x", padx=15, pady=(0, 8))

        btn_cancelar = ctk.CTkButton(
            self.frame_concretar_venta,
            text="Cancelar",
            fg_color="#636e72",
            hover_color="#4b6584",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=42,
            command=self.cancelar
        )
        btn_cancelar.pack(fill="x", padx=15, pady=(0, 8))

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
            self.btn_abrir_cerrar_caja.configure(
                text="🔓 ABRIR CAJA",
                fg_color=self.success_color,
                hover_color="#009476",
                text_color="white",
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                height=42
            )
        else:
            # Caso: Caja Abierta -> Sugerir Cierre
            self.btn_abrir_cerrar_caja.configure(
                text="🔒 CERRAR JORNADA",
                fg_color=self.danger_color,
                hover_color="#b32626",
                text_color="white",
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                height=42
            )

        self.btn_abrir_cerrar_caja.pack(fill="x", padx=10, pady=(10, 5))

        self.btn_ver_estado_caja.configure(
            text="📋 VER RESUMEN DE SESIÓN",
            fg_color="#2c3e50", 
            hover_color="#34495e",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36
        )

        if self.caja.estado:
            self.btn_ver_estado_caja.pack(fill="x", padx=10, pady=(5, 10))
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
            card = ctk.CTkFrame(
                self.frame_item_productos,
                fg_color="#ffffff",
                border_width=1,
                border_color=self.border_color,
                corner_radius=8,
                height=125
            )
            card.pack_propagate(False)
            card.pack(fill="x", padx=5, pady=5)

            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=12, pady=10)

            nombre = producto.nombre
            if len(nombre) > 25:
                nombre = nombre[:25] + "..."

            ctk.CTkLabel(
                info_frame, 
                text=nombre, 
                text_color=self.text_color, 
                font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), 
                anchor="w",
                justify="left"
            ).pack(fill="x")

            stock_actual = producto.stock
            for pc in self.carrito.productos:
                if pc["id_producto"] == producto.id_producto:
                    stock_actual -= pc["cantidad"]

            color_stock = self.success_color if stock_actual > 5 else self.danger_color
            stock_label = ctk.CTkLabel(
                info_frame, 
                text=f"Disponible: {stock_actual} unidades", 
                text_color=color_stock, 
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), 
                anchor="w"
            )
            stock_label.pack(fill="x", pady=(2, 0))

            presentacion = producto.presentacion if producto.presentacion else "Sin presentación"
            if len(presentacion) > 25:
                presentacion = presentacion[:22] + "..."
            ctk.CTkLabel(
                info_frame, 
                text=f"Presentación: {presentacion}", 
                text_color=self.sub_text, 
                font=ctk.CTkFont(family="Segoe UI", size=11), 
                anchor="w"
            ).pack(fill="x", pady=(2, 0))

            action_frame = ctk.CTkFrame(card, fg_color="transparent")
            action_frame.pack(side="right", fill="y", padx=12, pady=10)

            ctk.CTkLabel(
                action_frame, 
                text=f"Q{producto.precio_venta:,.2f}", 
                text_color=self.primary_color, 
                font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), 
                anchor="e"
            ).pack(fill="x", pady=(0, 5))

            btn_agregar = ctk.CTkButton(
                action_frame,
                text="+ Agregar",
                fg_color=self.primary_color,
                hover_color=self.primary_hover,
                text_color="white",
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                height=32,
                width=90,
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

    def show_carrito(self):
        for item in self.tabla_carrito.get_children():
            self.tabla_carrito.delete(item)

        for producto in self.carrito.productos:
            self.tabla_carrito.insert("", tk.END, iid=producto["id_producto"], values=(producto["nombre"], f"Q    {producto['precio_venta']:,.2f}", 
                                                         producto["cantidad"], f"Q  {producto['sub_total']:.2f}"))

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