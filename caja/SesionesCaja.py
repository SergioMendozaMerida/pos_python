import sqlite3
from tkinter import messagebox

class SesionesCaja:
    def __init__(self):
        self.sesiones = []

    def obtener_sesiones(self):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM caja")
            sesiones_db = cursor.fetchall()
            self.sesiones.clear()
            for s in sesiones_db:
                self.sesiones.append(SesionCaja(s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9], s[10], bool(s[11])))
            conexion.close()
            return sesiones_db
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al obtener las sesiones de caja {e}.")
            return None
        
    def filtrar_sesiones(self, fecha_inicio, fecha_fin, usuario):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()

            if fecha_inicio == "":
                cursor.execute("SELECT MIN(fecha) FROM caja")
                res = cursor.fetchone()[0]
                fecha_inicio = res if res else "1900-01-01"

            if fecha_fin == "":
                cursor.execute("SELECT MAX(fecha) FROM caja")
                res = cursor.fetchone()[0]
                fecha_fin = res if res else "2100-12-31"

            query = "SELECT * FROM caja WHERE fecha >= ? AND fecha <= ?"
            params = [fecha_inicio, fecha_fin]

            if usuario:
                query += " AND usuario LIKE ?"
                params.append(f"%{usuario}%")

            cursor.execute(query, params)
            sesiones_db = cursor.fetchall()
            self.sesiones.clear()
            for s in sesiones_db:
                self.sesiones.append(SesionCaja(s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9], s[10], bool(s[11])))
            
            conexion.close()
            return sesiones_db
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al filtrar las sesiones de caja {e}.")
            return None

class SesionCaja:
    def __init__(self, id_sesion, fecha, usuario, saldo_inicial, ingresos_ventas, otros_ingresos, egresos, saldo_final, efectivo_final, diferencia, utilidad_generada, estado):
        self.id_sesion = id_sesion
        self.fecha = fecha
        self.usuario = usuario
        self.saldo_inicial = saldo_inicial
        self.ingresos_ventas = ingresos_ventas
        self.otros_ingresos = otros_ingresos
        self.egresos = egresos
        self.saldo_final = saldo_final
        self.efectivo_final = efectivo_final
        self.diferencia = diferencia
        self.utilidad_generada = utilidad_generada
        self.estado = estado

            