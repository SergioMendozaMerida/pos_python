import customtkinter as ctk

from inventario.logica.Inventario import (
    Inventario,
    ViewProductosSinMovimiento,
    ViewProductosStockBajo,
)


class VentanaNotificaciones(ctk.CTkToplevel):
    def __init__(self, parent, inventario: Inventario):
        super().__init__(parent)
        self.inventario = inventario

        self.color_fondo = "#f8f9fa"
        self.color_header = "#2c3e50"
        self.color_primario = "#0984e3"
        self.color_texto = "#2d3436"
        self.color_subtexto = "#636e72"
        self.color_borde = "#dfe6e9"
        self.color_alerta = "#e67e22"

        self.title("Notificaciones de inventario")
        window_width = 900
        window_height = 620
        x = max(0, (self.winfo_screenwidth() - window_width) // 2)
        y = max(0, (self.winfo_screenheight() - window_height) // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.minsize(700, 480)
        self.configure(fg_color=self.color_fondo)
        self.transient(parent)
        self.grab_set()

        header = ctk.CTkFrame(
            self, fg_color=self.color_header, height=60, corner_radius=0
        )
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header,
            text="Notificaciones de inventario",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="white",
        ).pack(pady=16)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=18, pady=18)

        self.productos_sin_movimiento: list[ViewProductosSinMovimiento] = (
            self.inventario.productos_sin_movimiento()
        )
        self.productos_stock_bajo: list[ViewProductosStockBajo] = (
            self.inventario.productos_stock_bajo()
        )

        self._crear_panel(
            self.main_frame,
            "Productos sin movimiento",
            len(self.productos_sin_movimiento),
            self.color_primario,
            self.productos_sin_movimiento,
            self._crear_tarjeta_sin_movimiento,
        )
        self._crear_panel(
            self.main_frame,
            "Productos con stock bajo",
            len(self.productos_stock_bajo),
            self.color_alerta,
            self.productos_stock_bajo,
            self._crear_tarjeta_stock_bajo,
        )

    def _crear_panel(self, parent, titulo, cantidad, color, productos, crear_tarjeta):
        panel = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=8,
            border_width=1,
            border_color=self.color_borde,
        )
        panel.pack(side="left", fill="both", expand=True, padx=6)

        encabezado = ctk.CTkFrame(panel, fg_color="transparent")
        encabezado.pack(fill="x", padx=14, pady=(14, 8))
        ctk.CTkLabel(
            encabezado,
            text=titulo,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=color,
            anchor="w",
        ).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(
            encabezado,
            text=str(cantidad),
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="white",
            fg_color=color,
            corner_radius=10,
            width=32,
            height=24,
        ).pack(side="right")

        lista = ctk.CTkScrollableFrame(
            panel,
            fg_color="transparent",
            scrollbar_button_color=self.color_borde,
        )
        lista.pack(fill="both", expand=True, padx=8, pady=(0, 10))

        if productos:
            for producto in productos:
                crear_tarjeta(lista, producto)
        else:
            ctk.CTkLabel(
                lista,
                text="No hay productos que requieran atención.",
                font=ctk.CTkFont(family="Segoe UI", size=11),
                text_color=self.color_subtexto,
                wraplength=300,
            ).pack(fill="x", padx=8, pady=18)

    def _crear_tarjeta_sin_movimiento(self, parent, producto: ViewProductosSinMovimiento):
        self._crear_tarjeta(
            parent,
            self.color_primario,
            producto.nombre,
            f"Última venta: {producto.fecha or 'Sin registro'}",
            f"{producto.dias} días sin movimiento",
        )

    def _crear_tarjeta_stock_bajo(self, parent, producto: ViewProductosStockBajo):
        self._crear_tarjeta(
            parent,
            self.color_alerta,
            producto.nombre,
            f"Stock mínimo: {producto.stock_minimo}",
            destacado=f"Stock actual: {producto.stock}",
        )

    def _crear_tarjeta(self, parent, color, nombre, detalle, destacado=None):
        tarjeta = ctk.CTkFrame(
            parent,
            fg_color=self.color_fondo,
            height=92,
            corner_radius=6,
            border_width=1,
            border_color=self.color_borde,
        )
        tarjeta.pack_propagate(False)
        tarjeta.pack(fill="x", padx=4, pady=5)
        ctk.CTkFrame(
            tarjeta, fg_color=color, width=4, corner_radius=0
        ).pack(side="left", fill="y")
        contenido = ctk.CTkFrame(tarjeta, fg_color="transparent")
        contenido.pack(side="left", fill="x", expand=True, padx=9, pady=7)
        ctk.CTkLabel(
            contenido,
            text=nombre,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=self.color_texto,
            anchor="w",
            wraplength=320,
        ).pack(fill="x")
        ctk.CTkLabel(
            contenido,
            text=detalle,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=color,
            anchor="w",
            wraplength=320,
        ).pack(fill="x", pady=(5, 0))
        if destacado:
            ctk.CTkLabel(
                contenido,
                text=destacado,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color=color,
                anchor="w",
                wraplength=320,
            ).pack(fill="x", pady=(3, 0))
