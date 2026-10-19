import tkinter as tk
from tkinter import ttk

import customtkinter as ctk

from caja.SesionesCaja import RecibosPorSesionCaja


class FrameRecibosPorSesion(ctk.CTkToplevel):
    def __init__(self, parent, recibos: list[RecibosPorSesionCaja]):
        super().__init__(parent)
        self.recibos = list(recibos)

        self.color_fondo = "#f4f6f9"
        self.color_primario = "#2c3e50"
        self.color_secundario = "#0984e3"
        self.color_texto = "#2d3436"
        self.color_subtexto = "#636e72"
        self.color_borde = "#dfe6e9"

        self.title("Recibos de la sesión")
        self.geometry("1120x700")
        self.minsize(850, 560)
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
            text="RECIBOS DE LA SESIÓN",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="white"
        ).grid(row=0, column=0, sticky="w", padx=26, pady=(18, 2))
        ctk.CTkLabel(
            encabezado,
            text="Consulta de recibos emitidos durante esta sesión de caja",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#dce4ec"
        ).grid(row=1, column=0, sticky="w", padx=26, pady=(0, 18))

    def _crear_resumen(self):
        total_recibos = sum(float(recibo.total or 0) for recibo in self.recibos)
        total_utilidad = sum(float(recibo.utilidad or 0) for recibo in self.recibos)

        resumen = ctk.CTkFrame(self, fg_color="transparent")
        resumen.grid(row=1, column=0, sticky="ew", padx=18, pady=(15, 8))
        for columna in range(3):
            resumen.grid_columnconfigure(columna, weight=1, uniform="resumen")

        datos = (
            ("RECIBOS EMITIDOS", f"{len(self.recibos):,}", "#f4f7fa", self.color_primario),
            ("TOTAL DE RECIBOS", f"Q {total_recibos:,.2f}", "#e8f3ff", self.color_secundario),
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
            text="DETALLE DE RECIBOS",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=self.color_primario
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(13, 8))

        tabla_contenedor = ctk.CTkFrame(contenedor, fg_color="transparent")
        tabla_contenedor.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        tabla_contenedor.grid_columnconfigure(0, weight=1)
        tabla_contenedor.grid_rowconfigure(0, weight=1)

        columnas = (
            "no_recibo", "fecha", "cliente", "nit", "telefono", "total",
            "utilidad", "usuario"
        )
        self.tabla_recibos = ttk.Treeview(
            tabla_contenedor,
            columns=columnas,
            show="headings",
            style="RecibosSesion.Treeview"
        )
        encabezados = (
            "No. recibo", "Fecha", "Cliente", "NIT", "Teléfono", "Total",
            "Utilidad", "Usuario"
        )
        anchos = (100, 150, 230, 130, 130, 140, 140, 140)
        anclajes = ("center", "center", "w", "center", "center", "e", "e", "w")
        for columna, encabezado, ancho, anclaje in zip(
            columnas, encabezados, anchos, anclajes
        ):
            self.tabla_recibos.heading(columna, text=encabezado)
            self.tabla_recibos.column(
                columna,
                width=ancho,
                minwidth=90,
                stretch=columna == "cliente",
                anchor=anclaje
            )

        estilo = ttk.Style(self)
        estilo.configure(
            "RecibosSesion.Treeview",
            background="white",
            foreground=self.color_texto,
            fieldbackground="white",
            rowheight=36,
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        estilo.configure(
            "RecibosSesion.Treeview.Heading",
            background="#edf1f5",
            foreground=self.color_primario,
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )
        estilo.map(
            "RecibosSesion.Treeview",
            background=[("selected", "#74b9ff")],
            foreground=[("selected", "white")]
        )
        self.tabla_recibos.tag_configure("par", background="#f7f9fb")
        self.tabla_recibos.tag_configure("impar", background="white")

        barra_vertical = ttk.Scrollbar(
            tabla_contenedor,
            orient="vertical",
            command=self.tabla_recibos.yview
        )
        barra_horizontal = ttk.Scrollbar(
            tabla_contenedor,
            orient="horizontal",
            command=self.tabla_recibos.xview
        )
        self.tabla_recibos.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )

        if self.recibos:
            self.tabla_recibos.grid(row=0, column=0, sticky="nsew")
            barra_vertical.grid(row=0, column=1, sticky="ns")
            barra_horizontal.grid(row=1, column=0, sticky="ew")
            for indice, recibo in enumerate(self.recibos):
                self.tabla_recibos.insert(
                    "",
                    tk.END,
                    iid=str(indice),
                    values=(
                        str(recibo.no_recibo),
                        str(recibo.fecha),
                        str(recibo.nombre_cliente or "—"),
                        str(recibo.nit or "—"),
                        str(recibo.telefono or "—"),
                        f"Q {float(recibo.total or 0):,.2f}",
                        f"Q {float(recibo.utilidad or 0):,.2f}",
                        str(recibo.usuario or "—")
                    ),
                    tags=("par" if indice % 2 == 0 else "impar",)
                )
        else:
            ctk.CTkLabel(
                tabla_contenedor,
                text="Esta sesión no tiene recibos registrados.",
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