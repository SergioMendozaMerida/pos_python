import sqlite3
import Recibo as R
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


r = Recibos()