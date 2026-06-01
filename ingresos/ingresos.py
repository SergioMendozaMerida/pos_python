import sqlite3
from tkinter import messagebox

class Ingresos:
    def __init__(self):
        self.ingresos = []
        self.obtener_ingresos()

    def obtener_ingresos(self):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM ingresos_stock")
            ingresos_data = cursor.fetchall()
            self.ingresos.clear()
            for ingreso in ingresos_data:
                self.ingresos.append(Ingreso(ingreso[0], ingreso[1], ingreso[2], ingreso[3], ingreso[4], 
                                             ingreso[5], ingreso[6], ingreso[7], ingreso[8]))

        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al obtener los ingresos: {e}")

    def filtrar_ingresos(self, producto, proveedor, fecha_inicio, fecha_fin):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()

            if fecha_inicio == "":
                cursor.execute("SELECT MIN(fecha_ingreso) FROM ingresos_stock")
                res = cursor.fetchone()[0]
                fecha_inicio = res if res else "1900-01-01"

            if fecha_fin == "":
                cursor.execute("SELECT MAX(fecha_ingreso) FROM ingresos_stock")
                res = cursor.fetchone()[0]
                fecha_fin = res if res else "2100-12-31"
            
            # Asegurar que el fin de día se incluya si solo se da la fecha
            if len(fecha_fin) <= 10:
                fecha_fin += " 23:59:59"

            query = "SELECT * FROM ingresos_stock WHERE (fecha_ingreso >= ? AND fecha_ingreso <= ?)"
            params = [fecha_inicio, fecha_fin]

            if producto:
                query += " AND producto LIKE ?"
                params.append(f"%{producto}%")
            if proveedor:
                query += " AND proveedor LIKE ?"
                params.append(f"%{proveedor}%")

            cursor.execute(query, params)
            ingresos_data = cursor.fetchall()
            conexion.close()

            self.ingresos.clear()
            for ingreso in ingresos_data:
                self.ingresos.append(Ingreso(ingreso[0], ingreso[1], ingreso[2], ingreso[3], ingreso[4], 
                                             ingreso[5], ingreso[6], ingreso[7], ingreso[8]))
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al filtrar los ingresos: {e}")
            return False

class Ingreso:
    def __init__(self, id_ingreso, fecha_ingreso, id_producto, producto, cantidad, precio_compra, precio_venta, proveedor, usuario):
        self.id_ingreso = id_ingreso
        self.fecha_ingreso = fecha_ingreso
        self.id_producto = id_producto
        self.producto = producto
        self.cantidad = cantidad
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.proveedor = proveedor
        self.usuario = usuario