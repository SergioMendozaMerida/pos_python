import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk

from ventas.logica.analisis_de_ventas import AnalisisDeVentas


class FrameAnalisisDeVentas(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f4f6f9")

        self.analisis_de_ventas = AnalisisDeVentas()
        self.productos = []
        self.color_primario = "#2c3e50"
        self.color_secundario = "#0984e3"
        self.color_border = "#dfe6e9"

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.frame_contenedor_filtros = ctk.CTkFrame(
            self,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color=self.color_border
        )
        self.frame_contenedor_filtros.grid(
            row=0, column=0, sticky="ew", padx=10, pady=(6, 3)
        )
        self.frame_contenedor_filtros.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.frame_contenedor_filtros,
            text="Análisis de ventas",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_primario
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(6, 2))

        self.frame_filtros = ctk.CTkFrame(
            self.frame_contenedor_filtros,
            fg_color="transparent"
        )
        self.frame_filtros.grid(
            row=1, column=0, sticky="ew", padx=15, pady=(0, 10)
        )
        self.frame_filtros.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.frame_filtros,
            text="Mostrar:",
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=(0, 8))

        self.values = [
            "Mas Vendido",
            "Menos Vendido",
            "Mas Utilidades",
            "Menos Utilidades"
        ]
        self.input_filtros = ctk.CTkComboBox(
            self.frame_filtros,
            values=self.values,
            state="readonly",
            command=self.obtener_ventas,
            width=200,
            height=32
        )
        self.input_filtros.grid(row=0, column=1, sticky="w")
        self.input_filtros.set(self.values[0])

        self.btn_actualizar = ctk.CTkButton(
            self.frame_filtros,
            text="Actualizar",
            command=self.obtener_ventas,
            fg_color=self.color_secundario,
            hover_color="#74b9ff",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=32,
            width=100
        )
        self.btn_actualizar.grid(row=0, column=2, padx=(10, 0))

        self.frame_tabla = ctk.CTkFrame(
            self,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color=self.color_border
        )
        self.frame_tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.frame_tabla.grid_columnconfigure(0, weight=1)
        self.frame_tabla.grid_rowconfigure(0, weight=1)

        self.frame_tabla_unidades = ctk.CTkFrame(
            self.frame_tabla,
            fg_color="transparent"
        )
        self.frame_tabla_utilidades = ctk.CTkFrame(
            self.frame_tabla,
            fg_color="transparent"
        )
        self.frame_tabla_unidades.grid_columnconfigure(0, weight=1)
        self.frame_tabla_utilidades.grid_columnconfigure(0, weight=1)

        self.tabla_top_unidades_vendidas = self.crear_tabla(
            self.frame_tabla_unidades,
            "Productos por unidades vendidas",
            ("Producto", "Unidades", "Utilidad", "Porcentaje"),
            (180, 110, 130, 110)
        )
        self.tabla_top_utilidades_generadas = self.crear_tabla(
            self.frame_tabla_utilidades,
            "Productos por utilidades generadas",
            ("Producto", "Utilidades", "Unidades", "Porcentaje"),
            (180, 130, 110, 110)
        )

        self.obtener_ventas()

    def crear_tabla(self, parent, titulo, columnas, anchos):
        for columna in range(len(columnas)):
            parent.grid_columnconfigure(columna, weight=1)
        parent.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            parent,
            text=titulo,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_primario
        ).grid(row=0, column=0, columnspan=len(columnas), sticky="w", padx=15, pady=(10, 5))

        tabla_inner_frame = ctk.CTkFrame(parent, fg_color="transparent")
        tabla_inner_frame.grid(
            row=1, column=0, columnspan=len(columnas), sticky="nsew", padx=10, pady=(0, 10)
        )
        tabla_inner_frame.grid_rowconfigure(0, weight=1)
        tabla_inner_frame.grid_columnconfigure(0, weight=1)

        tabla = ttk.Treeview(
            tabla_inner_frame,
            columns=columnas,
            show="headings",
            height=10
        )
        for columna, ancho in zip(columnas, anchos):
            tabla.heading(columna, text=columna)
            tabla.column(columna, width=ancho, anchor="center")
        tabla.column("Producto", anchor="w")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#ffffff",
            foreground="#2d3436",
            rowheight=34,
            fieldbackground="#ffffff",
            borderwidth=0,
            font=("Segoe UI", 12)
        )
        style.configure(
            "Treeview.Heading",
            background="#f1f2f6",
            foreground="#2d3436",
            relief="flat",
            font=("Segoe UI", 12, "bold")
        )
        style.map(
            "Treeview",
            background=[("selected", "#74b9ff")],
            foreground=[("selected", "white")]
        )

        scroll_y = ttk.Scrollbar(
            tabla_inner_frame,
            orient="vertical",
            command=tabla.yview
        )
        tabla.configure(yscrollcommand=scroll_y.set)
        tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")

        return tabla

    def dibujar_tabla_top_ventas(self):
        for item in self.tabla_top_unidades_vendidas.get_children():
            self.tabla_top_unidades_vendidas.delete(item)

        for venta in self.productos:
            self.tabla_top_unidades_vendidas.insert(
                "",
                tk.END,
                values=(
                    venta.producto,
                    venta.total_unidades_vendidas,
                    f"Q {venta.total_utilidad:,.2f}",
                    f"{venta.porcentaje:.2f}%"
                )
            )

    def dibujar_tabla_top_utilidades(self):
        for item in self.tabla_top_utilidades_generadas.get_children():
            self.tabla_top_utilidades_generadas.delete(item)

        for venta in self.productos:
            self.tabla_top_utilidades_generadas.insert(
                "",
                tk.END,
                values=(
                    venta.producto,
                    f"Q {venta.utilidad_total:,.2f}",
                    venta.total_unidades_vendidas,
                    f"{venta.porcentaje:.2f}%"
                )
            )

    def obtener_ventas(self, seleccion=None):
        seleccion = seleccion or self.input_filtros.get()
        if seleccion in ("Mas Vendido", "Menos Vendido"):
            self.frame_tabla_unidades.grid(
                row=0, column=0, sticky="nsew"
            )
            self.frame_tabla_utilidades.grid_remove()
            if seleccion == "Mas Vendido":
                productos = self.analisis_de_ventas.get_top_productos_mas_vendidos()
            else:
                productos = self.analisis_de_ventas.get_top_productos_menos_vendidos()

            if isinstance(productos, tuple) and productos[0] is False:
                messagebox.showerror(
                    "Error",
                    f"No fue posible cargar las ventas: {productos[1]}"
                )
                return
            self.productos = productos
            self.dibujar_tabla_top_ventas()
        elif seleccion in ("Mas Utilidades", "Menos Utilidades"):
            self.frame_tabla_utilidades.grid(
                row=0, column=0, sticky="nsew"
            )
            self.frame_tabla_unidades.grid_remove()
            if seleccion == "Mas Utilidades":
                productos = self.analisis_de_ventas.get_top_productos_mas_utilidades()
            else:
                productos = self.analisis_de_ventas.get_top_productos_menos_utilidades()

            if isinstance(productos, tuple) and productos[0] is False:
                messagebox.showerror(
                    "Error",
                    f"No fue posible cargar las utilidades: {productos[1]}"
                )
                return
            self.productos = productos
            self.dibujar_tabla_top_utilidades()
