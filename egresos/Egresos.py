import sqlite3
from tkinter import messagebox

class Egresos:
    def __init__(self):
        self.egresos = []

    def obtener_egresos(self):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM egresos")
            egresos_db = cursor.fetchall()
            self.egresos.clear()
            for e in egresos_db:
                self.egresos.append(Egreso(e[0], e[1], e[2], e[3], e[4], e[5]))
            conexion.close()
            return egresos_db
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al obtener los egresos {e}.")
            return None

    def filtrar_egresos(self, razon, proveedor, fecha_inicio, fecha_fin):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()

            query = "SELECT * FROM egresos WHERE razon LIKE ? AND proveedor LIKE ?"
            params = [f"%{razon}%", f"%{proveedor}%"]

            if fecha_inicio:
                query += " AND fecha >= ?"
                params.append(fecha_inicio)
            
            if fecha_fin:
                query += " AND fecha <= ?"
                params.append(fecha_fin)

            cursor.execute(query, params)
            egresos_db = cursor.fetchall()
            self.egresos.clear()
            for e in egresos_db:
                self.egresos.append(Egreso(e[0], e[1], e[2], e[3], e[4], e[5]))
            conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al filtrar los egresos {e}.")

class Egreso:
    def __init__(self, id_egreso, fecha, usuario, razon, proveedor, monto):
        self.id_egreso = id_egreso
        self.fecha = fecha
        self.usuario = usuario
        self.razon = razon
        self.proveedor = proveedor
        self.monto = monto

    def registrar_egreso(self):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("""INSERT INTO egresos (fecha, usuario, razon, proveedor, monto) 
                           VALUES (?, ?, ?, ?, ?)""",
                           (self.fecha, self.usuario, self.razon, self.proveedor, self.monto))
            conexion.commit()
            conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al registrar el egreso {e}.")

    def eliminar_egreso(self, id_egreso):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM egresos WHERE id_egreso = ?", (id_egreso,))
            conexion.commit()
            conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al eliminar el egreso {e}.")