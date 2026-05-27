import sqlite3
from tkinter import messagebox


class Recibo:
    def __init__(self, no_recibo, nombre_cliente, direccion, dpi, nit, telefono, fecha, total):
        self.no_recibo = no_recibo
        self.nombre_cliente = nombre_cliente
        self.direccion = direccion
        self.dpi = dpi
        self.nit = nit
        self.telefono = telefono
        self.fecha = fecha
        self.total = total
        self.ventas = []

    def obtener_ventas(self):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM ventas WHERE id_recibo = ?", (self.no_recibo,))
            ventas = cursor.fetchall()
            conexion.close()
            for venta in ventas:
                self.ventas.append(venta)
        except:
            messagebox.showerror("Error", "Se produjo un error al obtener las ventas.")


    
        