import sqlite3
import recibos.logica.Recibo as R
from tkinter import messagebox


class Recibos:
    def __init__(self):
        self.recibos = []
        self.obtener_recibos()


    def obtener_recibos(self):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM recibos")
            recibos = cursor.fetchall()
            conexion.close()
            self.recibos.clear()
            for recibo in recibos:
                self.recibos.append(R.Recibo(recibo[0], recibo[1], recibo[2], recibo[3], recibo[4], recibo[5], recibo[6], recibo[7]))

            for recibo in self.recibos:
                recibo.obtener_ventas()
            
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al obtener los recibos {e}.")

    def filtrar_recibos(self, no_recibo, nombre_cliente, dpi, nit, fecha_inicio, fecha_fin):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()

            if fecha_inicio == "":
                cursor.execute("SELECT MIN(fecha) FROM recibos")
                res = cursor.fetchone()[0]
                fecha_inicio = res if res else "1900-01-01"

            if fecha_fin == "":
                cursor.execute("SELECT MAX(fecha) FROM recibos")
                res = cursor.fetchone()[0]
                fecha_fin = res if res else "2100-12-31"

            # Construcción dinámica de la consulta
            query = "SELECT * FROM recibos WHERE (fecha >= ? AND fecha <= ?)"
            params = [fecha_inicio, fecha_fin]

            if no_recibo:
                query += " AND no_recibo = ?"
                params.append(no_recibo)
            if nombre_cliente:
                query += " AND nombre_cliente LIKE ?"
                params.append(f"%{nombre_cliente}%")
            if dpi:
                query += " AND dpi LIKE ?"
                params.append(f"%{dpi}%")
            if nit:
                query += " AND nit LIKE ?"
                params.append(f"%{nit}%")

            cursor.execute(query, params)
            recibos = cursor.fetchall()
            if recibos.__len__() == 0:
                messagebox.showerror("Error", "No se encontraron recibos que cumplan con los criterios de búsqueda.")
                return
            conexion.close()
            self.recibos.clear()
            for recibo in recibos:
                self.recibos.append(R.Recibo(recibo[0], recibo[1], recibo[2], recibo[3], recibo[4], recibo[5], recibo[6], recibo[7]))

            for recibo in self.recibos:
                recibo.obtener_ventas()
            
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al filtrar los recibos {e}.")
