import datetime
import sqlite3
from tkinter import messagebox


class Caja:
    def __init__(self, usuario):
        self.id_sesion = None
        self.fecha = None
        self.usuario = usuario.usuario
        self.saldo_inicial = 0
        self.ingresos_ventas = 0
        self.otros_ingresos = 0
        self.egresos = 0
        self.saldo_final = 0
        self.efectivo_final = 0
        self.diferencia = 0
        self.utilidad_generada = 0
        self.estado = False

        self.obtener_sesion_caja()

    def abrir_caja(self, saldo_inicial=0):
        self.fecha = datetime.date.today()
        self.saldo_inicial = saldo_inicial
        self.saldo_final = saldo_inicial
        self.ingresos_ventas = 0
        self.otros_ingresos = 0
        self.egresos = 0

        self.estado = True
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("""INSERT INTO caja (fecha, usuario, saldo_inicial, ingresos_ventas, otros_ingresos, egresos, saldo_final, 
                           efectivo_final, diferencia, utilidad_generada, estado) 
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                           (self.fecha, self.usuario, self.saldo_inicial, self.ingresos_ventas, self.otros_ingresos, self.egresos,
                            self.saldo_final, self.efectivo_final, self.diferencia, self.utilidad_generada, self.estado))
            conexion.commit()
            conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al abrir la caja {e}.")
        

    def cerrar_caja(self, efectivo_final):
        self.obtener_sesion_caja()
                    
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            self.estado = False
            cursor.execute("""UPDATE caja SET estado = ?, efectivo_final = ?, diferencia = ? 
                           WHERE id_sesion = ?""", (self.estado, efectivo_final, efectivo_final - self.saldo_final, self.id_sesion))
            conexion.commit()
            conexion.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al cerrar la caja {e}.")
        

    def obtener_sesion_caja(self):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor() 
            cursor.execute("SELECT * FROM caja WHERE id_sesion = (SELECT MAX(id_sesion) FROM caja) AND usuario LIKE ? AND estado = 1",
                           (self.usuario,))
            sesion = cursor.fetchone()
            
            if sesion:
                self.id_sesion = sesion[0]
                self.fecha = sesion[1]
                self.usuario = sesion[2]
                self.saldo_inicial = sesion[3]
                self.ingresos_ventas = sesion[4]
                self.otros_ingresos = sesion[5]
                self.egresos = sesion[6]
                self.saldo_final = sesion[7]
                self.efectivo_final = sesion[8]
                self.diferencia = sesion[9]
                self.utilidad_generada = sesion[10]
                self.estado = bool(sesion[11])
                return
            conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al obtener la sesión de caja {e}.")
            return None