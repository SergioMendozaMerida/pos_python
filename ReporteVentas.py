import sqlite3
import Venta

class ReporteVentas:
    def __init__(self):
        self.ventas = [] 
        self.obtener_ventas()
        
        
    def obtener_ventas(self):
        conexion = sqlite3.connect("db_inventario.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM ventas")
        ventas = cursor.fetchall()
        for v in ventas:
           self.ventas.append(Venta.Venta(v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7])) # Aquí se almacenarán las ventas, cada venta podría ser un diccionario con detalles como fecha, producto, cantidad, etc.

        conexion.close()
        return ventas
