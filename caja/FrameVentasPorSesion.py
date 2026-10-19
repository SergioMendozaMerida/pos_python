import tkinter as tk
from tkinter import ttk

import customtkinter as ctk

from caja.SesionesCaja import VentasPorSesionCaja


class FrameVentasPorSesion(ctk.CTkToplevel):
    def __init__(self, parent, ventas: list[VentasPorSesionCaja]):
        super().__init__(parent)
        self.ventas = list(ventas)

        self.color_fondo = "#f4f6f9"
        self.color_primario = "#2c3e50"
        self.color_secundario = "#0984e3"
        self.color_texto = "#2d3436"
        self.color_subtexto = "#636e72"
        self.color_borde = "#dfe6e9"

        self.title("Ventas de la sesión")
        self.geometry("1080x700")
        self.minsize(820, 560)
        self.configure(fg_color=self.color_fondo)
        self.transient(parent)
        self.grab_set()
        self.bind("<Escape>", lambda _: self.destroy())

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._crear_encabezado()
        self._crear_resumen()
        self._crear_tabla()
        self._crear_pie()

    def _crear_encabezado(self):
        encabezado = ctk.CTkFrame(self, fg_color=self.color_primario, corner_radius=0)
        encabezado.grid(row=0, column=0, sticky="ew")
        encabezado.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            encabezado,
            text="VENTAS DE LA SESIÓN",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="white"
        ).grid(row=0, column=0, sticky="w", padx=26, pady=(18, 2))
        ctk.CTkLabel(
            encabezado,
            text="Detalle de productos vendidos y sus importes",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#dce4ec"
        ).grid(row=1, column=0, sticky="w", padx=26, pady=(0, 18))

    def _crear_resumen(self):
        cantidad_unidades = sum(float(venta.cantidad) for venta in self.ventas)
        total_descuentos = sum(float(venta.descuento) for venta in self.ventas)
        total_ventas = sum(float(venta.sub_total) for venta in self.ventas)
        total_utilidad = sum(float(venta.utilidad) for venta in self.ventas)
        unidades_texto = f"{cantidad_unidades:,.0f}" if cantidad_unidades.is_integer() else f"{cantidad_unidades:,.2f}"

        resumen = ctk.CTkFrame(self, fg_color="transparent")
        resumen.grid(row=1, column=0, sticky="ew", padx=18, pady=(15, 8))
        for columna in range(5):
            resumen.grid_columnconfigure(columna, weight=1, uniform="resumen")

        datos = (
            ("LÍNEAS DE PRODUCTO", f"{len(self.ventas):,}", "#f4f7fa", self.color_primario),
            ("UNIDADES VENDIDAS", unidades_texto, "#eaf7f0", "#218c5a"),
            ("DESCUENTOS", f"Q {total_descuentos:,.2f}", "#fff7e8", "#b7791f"),
            ("TOTAL DE VENTAS", f"Q {total_ventas:,.2f}", "#e8f3ff", self.color_secundario),
            ("UTILIDAD", f"Q {total_utilidad:,.2f}", "#f1ebfa", "#7048a3"),
        )
        for columna, (titulo, valor, color_fondo, color_valor) in enumerate(datos):
            tarjeta = ctk.CTkFrame(
                resumen,
                fg_color=color_fondo,
                corner_radius=10,
                border_width=1,
                border_color=self.color_borde
            )
            tarjeta.grid(row=0, column=columna, sticky="ew", padx=5, pady=3)
            ctk.CTkLabel(
                tarjeta,
                text=titulo,
                font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
                text_color=self.color_subtexto
            ).pack(anchor="w", padx=13, pady=(10, 1))
            ctk.CTkLabel(
                tarjeta,
                text=valor,
                font=ctk.CTkFont(family="Segoe UI", size=19, weight="bold"),
                text_color=color_valor
            ).pack(anchor="w", padx=13, pady=(0, 10))

    def _crear_tabla(self):
        contenedor = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=10,
            border_width=1,
            border_color=self.color_borde
        )
        contenedor.grid(row=2, column=0, sticky="nsew", padx=18, pady=8)
        contenedor.grid_columnconfigure(0, weight=1)
        contenedor.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            contenedor,
            text="DETALLE DE VENTAS",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=self.color_primario
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(13, 8))

        tabla_contenedor = ctk.CTkFrame(contenedor, fg_color="transparent")
        tabla_contenedor.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        tabla_contenedor.grid_columnconfigure(0, weight=1)
        tabla_contenedor.grid_rowconfigure(0, weight=1)

        columnas = (
            "producto", "cantidad", "precio", "descuento", "subtotal", "utilidad"
        )
        self.tabla_ventas = ttk.Treeview(
            tabla_contenedor,
            columns=columnas,
            show="headings",
            style="VentasSesion.Treeview"
        )
        encabezados = (
            "Producto", "Cantidad", "Precio unitario", "Descuento", "Subtotal",
            "Utilidad"
        )
        anchos = (300, 90, 130, 120, 140, 130)
        anclajes = ("w", "center", "e", "e", "e", "e")
        for columna, encabezado, ancho, anclaje in zip(
            columnas, encabezados, anchos, anclajes
        ):
            self.tabla_ventas.heading(columna, text=encabezado)
            self.tabla_ventas.column(
                columna,
                width=ancho,
                minwidth=90,
                stretch=columna == "producto",
                anchor=anclaje
            )

        estilo = ttk.Style(self)
        estilo.configure(
            "VentasSesion.Treeview",
            background="white",
            foreground=self.color_texto,
            fieldbackground="white",
            rowheight=36,
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        estilo.configure(
            "VentasSesion.Treeview.Heading",
            background="#edf1f5",
            foreground=self.color_primario,
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )
        estilo.map(
            "VentasSesion.Treeview",
            background=[("selected", "#74b9ff")],
            foreground=[("selected", "white")]
        )
        self.tabla_ventas.tag_configure("par", background="#f7f9fb")
        self.tabla_ventas.tag_configure("impar", background="white")

        barra_vertical = ttk.Scrollbar(
            tabla_contenedor,
            orient="vertical",
            command=self.tabla_ventas.yview
        )
        barra_horizontal = ttk.Scrollbar(
            tabla_contenedor,
            orient="horizontal",
            command=self.tabla_ventas.xview
        )
        self.tabla_ventas.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )

        if self.ventas:
            self.tabla_ventas.grid(row=0, column=0, sticky="nsew")
            barra_vertical.grid(row=0, column=1, sticky="ns")
            barra_horizontal.grid(row=1, column=0, sticky="ew")
            for indice, venta in enumerate(self.ventas):
                self.tabla_ventas.insert(
                    "",
                    tk.END,
                    iid=str(indice),
                    values=(
                        str(venta.producto),
                        f"{float(venta.cantidad):,g}",
                        f"Q {float(venta.precio):,.2f}",
                        f"Q {float(venta.descuento):,.2f}",
                        f"Q {float(venta.sub_total):,.2f}",
                        f"Q {float(venta.utilidad):,.2f}"
                    ),
                    tags=("par" if indice % 2 == 0 else "impar",)
                )
        else:
            ctk.CTkLabel(
                tabla_contenedor,
                text="Esta sesión no tiene ventas registradas.",
                font=ctk.CTkFont(family="Segoe UI", size=14),
                text_color=self.color_subtexto
            ).grid(row=0, column=0, sticky="nsew")

    def _crear_pie(self):
        pie = ctk.CTkFrame(self, fg_color="transparent")
        pie.grid(row=3, column=0, sticky="ew", padx=18, pady=(3, 16))
        pie.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            pie,
            text="Importes expresados en quetzales (Q).",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.color_subtexto
        ).grid(row=0, column=0, sticky="w", padx=5)
        ctk.CTkButton(
            pie,
            text="Cerrar",
            width=120,
            height=38,
            corner_radius=8,
            fg_color=self.color_secundario,
            hover_color="#0873c4",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self.destroy
        ).grid(row=0, column=1, sticky="e")
