import sqlite3
from tkinter import messagebox

from egresos.Egresos import Egreso

class SesionesCaja:
    def __init__(self):
        self.sesiones = []

    def obtener_sesiones(self):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM caja ORDER BY id_sesion DESC")
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

    def obtener_ventas_sesion_caja(self, id_sesion) -> VentasPorSesionCaja | str:
        list_ventas: list[VentasPorSesionCaja] = []

        try:
            conexion = sqlite3.connect('db_inventario.db')
            cursor = conexion.cursor()
            cursor.execute(
                'SELECT * FROM view_ventas_por_sesion_caja WHERE id_sesion_caja = ?',
                (id_sesion,)
            )
            ventas_sesion = cursor.fetchall()

            for ventas in ventas_sesion:
                list_ventas.append(
                    VentasPorSesionCaja(
                        ventas[4],
                        ventas[5],
                        ventas[6],
                        ventas[10],
                        ventas[7],
                        ventas[12]
                    )
                )
            conexion.close()
            return (True, list_ventas)

        except Exception as e:
            return(False, e)

    def obtener_recibos_sesion_caja(self, id_sesion):
        list_ventas: list[RecibosPorSesionCaja] = []

        try:
            conexion = sqlite3.connect('db_inventario.db')
            cursor = conexion.cursor()
            cursor.execute(
                'SELECT * FROM recibos WHERE id_sesion_caja = ?',
                (id_sesion,)
            )
            recibos_sesion = cursor.fetchall()

            for recibo in recibos_sesion:
                list_ventas.append(
                    RecibosPorSesionCaja(
                        recibo[0],
                        recibo[1],
                        recibo[2],
                        recibo[3],
                        recibo[4],
                        recibo[5],
                        recibo[6],
                        recibo[7],
                        recibo[8],
                        recibo[9],
                        recibo[10]
                    )
                )
            conexion.close()
            return (True, list_ventas)

        except Exception as e:
            return(False, e)

    def obtener_egresos_sesion_caja(self, id_sesion):
        list_egresos: list[Egreso] = []

        try:
            conexion = sqlite3.connect('db_inventario.db')
            cursor = conexion.cursor()
            cursor.execute(
                'SELECT * FROM egresos WHERE id_sesion_caja = ?',
                (id_sesion,)
            )
            egresos_sesion = cursor.fetchall()

            for egreso in egresos_sesion:
                list_egresos.append(
                    Egreso(
                        egreso[0],
                        egreso[1],
                        egreso[2],
                        egreso[3],
                        egreso[4],
                        egreso[5],
                        egreso[6]
                    )
                )
            conexion.close()
            return (True, list_egresos)

        except Exception as e:
            return(False, e)


class RecibosPorSesionCaja:
    def __init__(self, no_recibo, nombre_cliente, direccion, dpi, nit, telefono, fecha, total, usuario, utilidad, id_sesion_caja):
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
        self.utilidad = utilidad
        self.id_sesion_caja = id_sesion_caja

class VentasPorSesionCaja:
    def __init__(self, producto, precio, cantidad, descuento, sub_total, utilidad):
        self.producto = producto
        self.precio = precio
        self.cantidad = cantidad
        self.descuento = descuento
        self.sub_total = sub_total
        self.utilidad = utilidad

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

            