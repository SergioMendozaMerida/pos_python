import sqlite3
from tkinter import messagebox
import ventas.logica.Venta as V


class Recibo:
    def __init__(self, no_recibo, nombre_cliente, direccion, dpi, nit, telefono, fecha, total, usuario):
        self.no_recibo = no_recibo
        self.nombre_cliente = nombre_cliente
        self.direccion = direccion
        self.dpi = dpi
        self.nit = nit
        self.telefono = telefono
        self.fecha = fecha
        self.total = total
        self.utilidad = 0
        self.usuario = usuario
        self.ventas = []

    def obtener_ventas(self):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM ventas WHERE id_recibo = ?", (self.no_recibo,))
            ventas = cursor.fetchall()
            conexion.close()
            for venta in ventas:
                self.ventas.append(V.Venta(venta[0], venta[1], venta[2], venta[3], venta[4], venta[5], venta[6], venta[7], venta[8], venta[9]))
                #costo por cantidad menos subtotal
                self.utilidad += venta[7] - (venta[6] * venta[9])
        except:
            messagebox.showerror("Error", "Se produjo un error al obtener las ventas.")


    
        