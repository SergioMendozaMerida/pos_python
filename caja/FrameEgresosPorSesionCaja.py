import tkinter as tk
from tkinter import ttk

import customtkinter as ctk

from egresos.Egresos import Egreso


class FrameEgresosPorSesionCaja(ctk.CTkToplevel):
    def __init__(self, parent, egresos: list[Egreso]):
        super().__init__(parent)
        self.egresos = list(egresos)

        self.color_fondo = "#f4f6f9"
        self.color_primario = "#2c3e50"
        self.color_secundario = "#0984e3"
        self.color_texto = "#2d3436"
        self.color_subtexto = "#636e72"
        self.color_borde = "#dfe6e9"

        self.title("Egresos de la sesión")
        self.geometry("1080x680")
        self.minsize(820, 540)
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
            text="EGRESOS DE LA SESIÓN",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="white"
        ).grid(row=0, column=0, sticky="w", padx=26, pady=(18, 2))
        ctk.CTkLabel(
            encabezado,
            text="Detalle de gastos y salidas de efectivo registrados",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#dce4ec"
        ).grid(row=1, column=0, sticky="w", padx=26, pady=(0, 18))

    def _crear_resumen(self):
        total_egresos = sum(float(egreso.monto) for egreso in self.egresos)

        resumen = ctk.CTkFrame(self, fg_color="transparent")
        resumen.grid(row=1, column=0, sticky="ew", padx=18, pady=(15, 8))
        resumen.grid_columnconfigure((0, 1), weight=1, uniform="resumen")

        datos = (
            ("EGRESOS REGISTRADOS", f"{len(self.egresos):,}", "#f4f7fa", self.color_primario),
            ("TOTAL DE EGRESOS", f"Q {total_egresos:,.2f}", "#fff1f0", "#c0392b"),
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
            text="DETALLE DE EGRESOS",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=self.color_primario
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(13, 8))

        tabla_contenedor = ctk.CTkFrame(contenedor, fg_color="transparent")
        tabla_contenedor.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        tabla_contenedor.grid_columnconfigure(0, weight=1)
        tabla_contenedor.grid_rowconfigure(0, weight=1)

        columnas = ("fecha", "usuario", "razon", "proveedor", "monto")
        self.tabla_egresos = ttk.Treeview(
            tabla_contenedor,
            columns=columnas,
            show="headings",
            style="EgresosSesion.Treeview"
        )
        encabezados = ("Fecha", "Usuario", "Razón / Concepto", "Proveedor", "Monto")
        anchos = (130, 150, 300, 220, 150)
        anclajes = ("center", "w", "w", "w", "e")
        for columna, encabezado, ancho, anclaje in zip(
            columnas, encabezados, anchos, anclajes
        ):
            self.tabla_egresos.heading(columna, text=encabezado)
            self.tabla_egresos.column(
                columna,
                width=ancho,
                minwidth=90,
                stretch=columna in {"razon", "proveedor"},
                anchor=anclaje
            )

        estilo = ttk.Style(self)
        estilo.configure(
            "EgresosSesion.Treeview",
            background="white",
            foreground=self.color_texto,
            fieldbackground="white",
            rowheight=36,
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        estilo.configure(
            "EgresosSesion.Treeview.Heading",
            background="#edf1f5",
            foreground=self.color_primario,
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )
        estilo.map(
            "EgresosSesion.Treeview",
            background=[("selected", "#74b9ff")],
            foreground=[("selected", "white")]
        )
        self.tabla_egresos.tag_configure("par", background="#f7f9fb")
        self.tabla_egresos.tag_configure("impar", background="white")

        barra_vertical = ttk.Scrollbar(
            tabla_contenedor,
            orient="vertical",
            command=self.tabla_egresos.yview
        )
        barra_horizontal = ttk.Scrollbar(
            tabla_contenedor,
            orient="horizontal",
            command=self.tabla_egresos.xview
        )
        self.tabla_egresos.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )

        if self.egresos:
            self.tabla_egresos.grid(row=0, column=0, sticky="nsew")
            barra_vertical.grid(row=0, column=1, sticky="ns")
            barra_horizontal.grid(row=1, column=0, sticky="ew")
            for indice, egreso in enumerate(self.egresos):
                self.tabla_egresos.insert(
                    "",
                    tk.END,
                    iid=str(indice),
                    values=(
                        str(egreso.fecha),
                        str(egreso.usuario),
                        str(egreso.razon),
                        str(egreso.proveedor),
                        f"Q {float(egreso.monto):,.2f}"
                    ),
                    tags=("par" if indice % 2 == 0 else "impar",)
                )
        else:
            ctk.CTkLabel(
                tabla_contenedor,
                text="Esta sesión no tiene egresos registrados.",
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