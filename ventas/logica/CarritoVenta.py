import datetime
import sqlite3
from tkinter import messagebox

class CarrtioVenta:
    def __init__(self,usuario):
        self.productos = []
        self.numero_recibo = 0
        self.fecha = datetime.date.today()
        self.total = 0
        self.nombre_cliente = ""
        self.direccion = ""
        self.telefono = ""
        self.dpi = ""
        self.nit = ""
        self.utilidad = 0

        self.usuario = usuario

        self.obtener_numero_recibo()
        
    def set_datos_cliente(self, nombre, direccion, telefono, dpi, nit):
        self.nombre_cliente = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.dpi = dpi
        self.nit = nit

    def obtener_numero_recibo(self):
        conexion = sqlite3.connect("db_inventario.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT MAX(no_recibo) FROM  recibos")
        p = cursor.fetchone()
        if p[0] is None:
            self.numero_recibo = 1
            return
        
        self.numero_recibo = p[0]+1
        conexion.close()

    def agregar_producto(self, id, cantidad):
            
        conexion = sqlite3.connect("db_inventario.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM  productos WHERE id_producto = ?", (id,))
        p = cursor.fetchone()
        conexion.close()

        for prod in self.productos:
            if prod["id_producto"] == id:
                if cantidad + prod["cantidad"] > int(p[9]):
                    messagebox.showwarning("Stock insuficiente", f"No hay suficiente stock para agregar {cantidad} unidades de {prod['nombre']}. Stock disponible: {p[7] - prod['cantidad']}")
                    return False
                prod["cantidad"] += cantidad
                prod["sub_total"] = prod["precio_venta"] * prod["cantidad"]
                return True

        if cantidad > int(p[9]):
            return False
        else: 
            p_carrito = {
                "id_producto": p[0],
                "nombre": p[1],
                "precio_compra": p[5],
                "precio_venta": float(p[6]),
                "precio_blister": float(p[7]),
                "precio_caja": float(p[8]),
                "stock": p[9],
                "cantidad": cantidad,
                "sub_total": cantidad*float(p[6])
            }
        
            self.productos.append(p_carrito)
            self.calcular_total()
            return True

    def calcular_total(self):
        self.total = 0
        for producto in self.productos:
            self.total += producto["sub_total"]

    def cambiar_cantidad(self, nueva_cantidad, id):

        conexion = sqlite3.connect("db_inventario.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM  productos WHERE id_producto = ?", (id,))
        p = cursor.fetchone()
        conexion.close()

        for prod in self.productos:
            if prod["id_producto"] == id:
                if nueva_cantidad > int(p[9]):
                    return False
                prod["cantidad"] = nueva_cantidad
                prod["sub_total"] = prod["precio_venta"] * prod["cantidad"]
                self.calcular_total()
                return True

    def cambiar_cantidad_unidades(self, nueva_cantidad, tipo_unidad, id):
        conexion = sqlite3.connect("db_inventario.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM  productos WHERE id_producto = ?", (id,))
        p = cursor.fetchone()
        conexion.close()

        for prod in self.productos:
            if prod["id_producto"] == id:
                if nueva_cantidad > int(p[9]):
                    messagebox.showerror("Error", "Cantidad no disponible.")
                    return False
                
                if tipo_unidad == "unidad":
                    prod["precio_venta"] = float(p[6])
                if tipo_unidad == "blister":
                    prod["precio_venta"] = float(p[7])
                if tipo_unidad == "caja":
                    prod["precio_venta"] = float(p[8])

                prod["cantidad"] = nueva_cantidad
                prod["sub_total"] = prod["precio_venta"] * prod["cantidad"]
                self.calcular_total()
                return True
    
    def cancelar_venta(self):
        self.productos.clear()
        self.nombre_cliente = ""
        self.direccion = ""
        self.telefono = ""
        self.dpi = ""
        self.nit = ""
    
    def concretar_venta(self):
        conexion = sqlite3.connect("db_inventario.db")
        cursor = conexion.cursor()
        for p in self.productos:
            cursor.execute('INSERT INTO ventas (id_producto,producto,precio,cantidad,sub_total,id_recibo,fecha,usuario,costo) VALUES (?,?,?,?,?,?,?,?,?)',
                           (p['id_producto'],p['nombre'],p['precio_venta'],p['cantidad'],p['sub_total'],self.numero_recibo,self.fecha,self.usuario.usuario,p['precio_compra']))
            self.utilidad += p['sub_total'] - (p['precio_compra'] * p['cantidad'])
            conexion.commit()

        cursor.execute('INSERT INTO recibos (nombre_cliente,direccion,DPI,NIT,telefono,fecha,total,usuario, utilidad) VALUES(?,?,?,?,?,?,?,?,?)',
                       (self.nombre_cliente,self.direccion,self.dpi,self.nit,self.telefono,self.fecha,self.total,self.usuario.usuario,self.utilidad))
        conexion.commit()
        self.utilidad = 0
        #self.vaciar_carrito()
        conexion.close()

    def quitar_producto(self, id_producto):
        for producto in self.productos:
            if producto["id_producto"] == id_producto:
                self.productos.remove(producto)
                break
    
    def vaciar_carrito(self):
        self.productos.clear()
        self.total = 0
        self.nombre_cliente = ""
        self.direccion = ""
        self.telefono = ""
        self.dpi = ""
        self.nit = ""
        self.obtener_numero_recibo()
