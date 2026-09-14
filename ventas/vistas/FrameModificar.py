import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

class FrameModificarVenta(ctk.CTkToplevel):
    def __init__(self, parent, carrito, producto=None, info_producto=None, calcular_total=None, show_carrito=None, actualizar_productos=None):
        super().__init__(parent)
        self.title("Modificar Venta")
        self.geometry("450x540")
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
        self.color_subtexto = "#636e72"
        self.color_primario = "#0984e3"
        self.color_primario_hover = "#74b9ff"
        self.color_borde = "#dfe6e9"

        self.configure(fg_color=self.color_fondo)

        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color=self.color_header, height=65, corner_radius=0)
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)

        ctk.CTkLabel(
            self.header_frame,
            text="Modificar Venta",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color="white"
        ).pack(pady=16)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=22, pady=18)

        # Sección de cantidad
        lbl_cantidad = ctk.CTkLabel(
            self.main_frame,
            text="Cantidad:",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=self.color_texto
        )
        lbl_cantidad.pack(anchor="w", pady=(0, 5))

        self.entry_cantidad = ctk.CTkEntry(
            self.main_frame,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            placeholder_text="1",
            height=40
        )
        self.entry_cantidad.pack(fill="x", pady=(0, 16))
        self.entry_cantidad.insert(0, str(self.info_producto["cantidad"]))

        # --- CONTENEDOR PARA CHECKBOXES (Efecto Tarjeta) ---
        frame_opciones_container = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.color_card,
            corner_radius=8,
            border_width=1,
            border_color=self.color_borde
        )
        frame_opciones_container.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            frame_opciones_container,
            text="Opciones de Precio",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=self.color_texto
        ).pack(anchor="w", padx=14, pady=(12, 6))

        frame_opciones = ctk.CTkFrame(frame_opciones_container, fg_color="transparent")
        frame_opciones.pack(fill="x", padx=12, pady=(0, 12))

        frame_opciones.columnconfigure(0, weight=1)
        frame_opciones.columnconfigure(1, weight=1)
        frame_opciones.columnconfigure(2, weight=1)

        self.state_unidad = tk.BooleanVar(value=False)
        self.state_blister = tk.BooleanVar(value=False)
        self.state_caja = tk.BooleanVar(value=False)

        self.chk_box_unidad = ctk.CTkCheckBox(
            frame_opciones,
            text=f"Q{self.info_producto['precio_venta']:,.2f}\nUnidad",
            variable=self.state_unidad,
            command=lambda: self.desactivar_opciones(self.chk_box_unidad),
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=self.color_texto,
            checkbox_height=22,
            checkbox_width=22,
            corner_radius=5
        )
        self.chk_box_blister = ctk.CTkCheckBox(
            frame_opciones,
            text=f"Q{self.info_producto['precio_blister']:,.2f}\nBlíster",
            variable=self.state_blister,
            command=lambda: self.desactivar_opciones(self.chk_box_blister),
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=self.color_texto,
            checkbox_height=22,
            checkbox_width=22,
            corner_radius=5
        )
        self.chk_box_caja = ctk.CTkCheckBox(
            frame_opciones,
            text=f"Q{self.info_producto['precio_caja']:,.2f}\nCaja",
            variable=self.state_caja,
            command=lambda: self.desactivar_opciones(self.chk_box_caja),
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=self.color_texto,
            checkbox_height=22,
            checkbox_width=22,
            corner_radius=5
        )

        self.chk_box_unidad.grid(row=0, column=0, pady=5, padx=4, sticky="w")
        self.chk_box_blister.grid(row=0, column=1, pady=5, padx=4, sticky="w")
        self.chk_box_caja.grid(row=0, column=2, pady=5, padx=4, sticky="w")

        ctk.CTkLabel(
            self.main_frame,
            text="Atajos: F1 Unidad • F2 Blíster • F3 Caja",
            font=ctk.CTkFont(family="Segoe UI", size=11, slant="italic"),
            text_color=self.color_primario
        ).pack(anchor="w", pady=(0, 12))

        self.lbl_descuento = ctk.CTkLabel(
            self.main_frame,
            text="Descuento:",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=self.color_texto
        )
        self.lbl_descuento.pack(anchor="w", pady=(0, 5))

        self.entry_descuento = ctk.CTkEntry(
            self.main_frame,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            placeholder_text="0",
            height=40
        )
        self.entry_descuento.pack(fill="x", pady=(0, 18))

        self.chk_box_unidad.select()
        self.opciones = [self.chk_box_blister, self.chk_box_caja, self.chk_box_unidad]

        btn_guardar = ctk.CTkButton(
            self.main_frame,
            text="Aplicar Cambios",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=self.color_primario,
            hover_color=self.color_primario_hover,
            text_color="white",
            height=44,
            command=self.guardar
        )
        btn_guardar.pack(fill="x", pady=(5, 0))

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
            for opcion in self.opciones:
                if opcion.winfo_exists():
                    opcion.deselect()
            opcion_seleccionada.select()
        else:
            return

    def guardar(self):
        try:
            cantidad_str = self.entry_cantidad.get().strip()
            cantidad = int(cantidad_str)
        except ValueError:
            messagebox.showerror("Validación", "La cantidad debe ser un número entero.")
            self.entry_cantidad.focus()
            return

        if not (self.state_unidad.get() or self.state_blister.get() or self.state_caja.get()):
            messagebox.showerror("Validación", "Debe seleccionar al menos una opción: Unidad, Blíster o Caja.")
            return

        descuento_str = self.entry_descuento.get().strip()
        try:
            descuento = int(descuento_str) if descuento_str else 0
        except ValueError:
            descuento = 0

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