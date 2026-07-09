import tkinter as tk
from tkinter import font, messagebox

class FrameModificarVenta(tk.Toplevel):
    def __init__(self, parent, carrito, producto=None, info_producto=None, calcular_total=None, show_carrito=None, actualizar_productos=None):
        super().__init__(parent)
        self.title("Modificar Venta")
        self.geometry("400x430")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.focus_set()

        self.carrito = carrito
        self.producto = producto
        self.calcular_total = calcular_total
        self.show_carrito = show_carrito
        self.info_producto = info_producto
        self.actualizar_productos = actualizar_productos
        
        # --- Paleta de Colores y Fuentes ---
        self.color_fondo = "#f8f9fa"
        self.color_header = "#2c3e50"
        self.color_card = "#ffffff"
        self.color_texto = "#2d3436"
        self.color_primario = "#0984e3"
        self.color_borde = "#dfe6e9"

        fuente_titulo = font.Font(family="Segoe UI", size=14, weight="bold")
        fuente_normal = font.Font(family="Segoe UI", size=10)
        fuente_negrita = font.Font(family="Segoe UI", size=10, weight="bold")

        self.configure(bg=self.color_fondo)

        self.columnconfigure(0, weight=1)

        # Header
        self.header_frame = tk.Frame(self, bg=self.color_header, height=60)
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)

        tk.Label(
            self.header_frame,
            text="Modificar Venta",
            font=fuente_titulo,
            bg=self.color_header,
            fg="white"
        ).pack(pady=15)

        self.main_frame = tk.Frame(self, bg=self.color_fondo)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Sección de cantidad
        lbl_cantidad = tk.Label(
            self.main_frame,
            text="Cantidad:",
            font=fuente_negrita,
            bg=self.color_fondo,
            fg=self.color_texto
        )
        lbl_cantidad.pack(anchor="w", pady=(0, 5))

        self.entry_cantidad = tk.Entry(
            self.main_frame,
            font=("Segoe UI", 12),
            bg=self.color_card,
            fg=self.color_texto,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=self.color_borde,
            highlightcolor=self.color_primario
        )
        self.entry_cantidad.pack(fill="x", pady=(0, 20), ipady=8)
        self.entry_cantidad.insert(0, self.info_producto["cantidad"])

        # --- 3. CONTENEDOR PARA CHECKBOXES (Efecto Tarjeta) ---
        frame_opciones = tk.LabelFrame(
            self.main_frame,
            text="Opciones de Precio",
            font=fuente_negrita,
            bg=self.color_card,
            fg=self.color_texto,
            bd=0,
            relief="flat",
            padx=10,
            pady=10
        )
        frame_opciones.pack(fill="x", pady=(0, 8))

        tk.Label(
            self.main_frame,
            text="Atajos: F1 Unidad • F2 Blíster • F3 Caja",
            font=("Segoe UI", 9, "italic"),
            bg=self.color_fondo,
            fg=self.color_primario
        ).pack(anchor="w", pady=(0, 12))

        frame_opciones.columnconfigure(0, weight=1)
        frame_opciones.columnconfigure(1, weight=1)
        frame_opciones.columnconfigure(2, weight=1)

        self.state_unidad = tk.BooleanVar(value=False)
        self.state_blister = tk.BooleanVar(value=False)
        self.state_caja = tk.BooleanVar(value=False)

        self.chk_box_unidad = tk.Checkbutton(
            frame_opciones,
            text=f"Q{self.info_producto['precio_venta']:,.2f} Unidad",
            variable=self.state_unidad,
            command=lambda: self.desactivar_opciones(self.chk_box_unidad),
            font=fuente_normal,
            bg=self.color_card,
            fg=self.color_texto,
            activebackground=self.color_card,
            highlightthickness=0,
            bd=0,
            anchor="w",
            padx=5
        )
        self.chk_box_blister = tk.Checkbutton(
            frame_opciones,
            text=f"Q{self.info_producto['precio_blister']:,.2f} Blíster",
            variable=self.state_blister,
            command=lambda: self.desactivar_opciones(self.chk_box_blister),
            font=fuente_normal,
            bg=self.color_card,
            fg=self.color_texto,
            activebackground=self.color_card,
            highlightthickness=0,
            bd=0,
            anchor="w",
            padx=5
        )
        self.chk_box_caja = tk.Checkbutton(
            frame_opciones,
            text=f"Q{self.info_producto['precio_caja']:,.2f} Caja",
            variable=self.state_caja,
            command=lambda: self.desactivar_opciones(self.chk_box_caja),
            font=fuente_normal,
            bg=self.color_card,
            fg=self.color_texto,
            activebackground=self.color_card,
            highlightthickness=0,
            bd=0,
            anchor="w",
            padx=5
        )

        self.chk_box_unidad.grid(row=0, column=0, pady=10, padx=5, sticky="w")
        self.chk_box_blister.grid(row=0, column=1, pady=10, padx=5, sticky="w")
        self.chk_box_caja.grid(row=0, column=2, pady=10, padx=5, sticky="w")

        self.entry_descuento = tk.Entry(
            self.main_frame,
            font=("Segoe UI", 12),
            bg=self.color_card,
            fg=self.color_texto,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=self.color_borde,
            highlightcolor=self.color_primario
        )

        self.entry_descuento.pack(fill="x", pady=(0, 20), ipady=8)
        self.entry_descuento.insert(0, f"{self.info_producto['descuento']}")

        self.chk_box_unidad.select()
        self.opciones = [self.chk_box_blister, self.chk_box_caja, self.chk_box_unidad]

        btn_guardar = tk.Button(
            self.main_frame,
            text="Aplicar Cambios",
            font=fuente_negrita,
            bg=self.color_primario,
            fg="white",
            relief="flat",
            bd=0,
            padx=10,
            pady=10,
            cursor="hand2",
            command=self.guardar
        )
        btn_guardar.pack(fill="x", pady=(10, 0))

        self.entry_cantidad.focus_set()
        self.bind("<F1>", lambda event: self.desactivar_opciones(self.chk_box_unidad))
        self.bind("<F2>", lambda event: self.desactivar_opciones(self.chk_box_blister))
        self.bind("<F3>", lambda event: self.desactivar_opciones(self.chk_box_caja))
        self.bind("<Return>", lambda event: self.guardar())


        if info_producto["precio_blister"] <= 0:
            self.chk_box_blister.destroy()
        if info_producto["precio_caja"] <= 0:
            self.chk_box_caja.destroy()

    def desactivar_opciones(self, opcion_seleccionada):

        if opcion_seleccionada.winfo_exists():
            
            # Nota: Al usar BooleanVar, deselect() se maneja mejor cambiando el valor a False,
            # pero si mantienes tu lógica original, este método deselecciona visualmente.
            for opcion in self.opciones:
                if opcion.winfo_exists():
                    opcion.deselect()

            opcion_seleccionada.select()

        else:
            return

    def guardar(self):
        # Validar que la cantidad sea un número entero
        try:
            cantidad_str = self.entry_cantidad.get().strip()
            cantidad = int(cantidad_str)
        except ValueError:
            messagebox.showerror("Validación", "La cantidad debe ser un número entero.")
            self.entry_cantidad.focus()
            return

        # Validar que al menos una opción esté seleccionada
        if not (self.state_unidad.get() or self.state_blister.get() or self.state_caja.get()):
            messagebox.showerror("Validación", "Debe seleccionar al menos una opción: Unidad, Blíster o Caja.")
            return

        descuento = int(self.entry_descuento.get())

        if self.state_unidad.get():
            res = self.carrito.cambiar_cantidad_unidades(cantidad, "unidad", self.producto, descuento)
        elif self.state_blister.get():
            res = self.carrito.cambiar_cantidad_unidades(cantidad, "blister", self.producto, descuento)
        elif self.state_caja.get():
            res = self.carrito.cambiar_cantidad_unidades(cantidad, "caja", self.producto, descuento)

        if res:
            self.show_carrito()
            self.actualizar_productos()
            self.destroy()

        