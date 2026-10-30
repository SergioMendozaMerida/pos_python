
import sqlite3
import sys
from pathlib import Path

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ventas.logica.analisis_de_ventas import AnalisisDeVentas, ProductoMasUnidadesVendidas

class GraficoVentas(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="#1e1e1e")
        self.analisis = AnalisisDeVentas()

        # Crear figura
        self.fig = Figure(
            figsize=(6, 4),
            dpi=100,
            facecolor="#1e1e1e"
        )

        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#1e1e1e")

        self.ventas = self.get_top_productos_mas_vendidos()
        print(self.ventas)

        productos = []
        utilidades = []

        for v in self.ventas:
            productos.append(v.producto)
            utilidades.append(v.total_unidades_vendidas)


        self.ax.barh(
            productos,
            utilidades,
            color="#01a6e6"
        )

        # Invertir orden para mostrar el mayor arriba
        self.ax.invert_yaxis()

        self.ax.set_title(
            "Productos más vendidos",
            color="white"
        )

        self.ax.tick_params(
            axis="both",
            colors="white",
            labelsize=8
        )

        # Integrar con CustomTkinter
        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=self
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    def get_top_productos_mas_vendidos(self):
        total = 0
        try:
            conexion = sqlite3.connect("../../db_inventario.db")
            conexion.row_factory = sqlite3.Row
            cursor = conexion.cursor()
            cursor.execute('SELECT * FROM producto_mas_unidades_vendidas ORDER by total_unidades_vendidas DESC')
            res = cursor.fetchall()
            for p in res:
                total = total + int(p['total_unidades_vendidas'])
            productos: list[ProductoMasUnidadesVendidas] = []
            for p in res:
                productos.append(ProductoMasUnidadesVendidas(
                    producto = p['producto'],
                    total_unidades_vendidas = p['total_unidades_vendidas'],
                    total_utilidad = p['utilidad_total'],
                    porcentaje = int(p['total_unidades_vendidas']) * 100 / total
                ))
            return productos
        except Exception as e:
            return (False, e)


# Ventana principal
app = ctk.CTk()
app.geometry("800x600")

grafico = GraficoVentas(app)
grafico.pack(fill="both", expand=True, padx=20, pady=20)

app.mainloop()
