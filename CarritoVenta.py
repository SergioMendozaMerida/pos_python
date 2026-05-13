import datetime
import sqlite3

class CarrtioVenta:
    def __init__(self):
        self.productos = []
        self.numero_recibo = 0
        self.fecha = datetime.date.today()
        self.total = 0
        self.nombre_cliente = ""
        self.direccion = ""
        self.telefono = ""
        self.dpi = ""
        self.nit = ""

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
        for prod in self.productos:
            if prod["id_producto"] == id:
                prod["cantidad"] += cantidad
                return
            
        conexion = sqlite3.connect("db_inventario.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM  productos WHERE id_producto = ?", (id,))
        p = cursor.fetchone()
        conexion.close()

        if cantidad > int(p[7]):
            print(f"Cantidad no disponible: cantidad actual = {p[7]}.")
            return False
        else: 
            p_carrito = {
                "id_producto": p[0],
                "nombre": p[1],
                "precio_venta": p[6],
                "stock": p[7],
                "cantidad": cantidad,
                "sub_total": cantidad*p[6]
            }
        
            self.productos.append(p_carrito)
            self.calcular_total()
            return True

    def calcular_total(self):
        self.total = 0
        for producto in self.productos:
            self.total += producto["sub_total"]
    
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
            cursor.execute('INSERT INTO ventas (id_producto,producto,precio,cantidad,sub_total) VALUES (?,?,?,?,?)',
                           (p['id_producto'],p['nombre'],p['precio_venta'],p['cantidad'],p['sub_total']))
            conexion.commit()

        cursor.execute('INSERT INTO recibos (nombre_cliente,direccion,DPI,NIT,telefono,fecha,total) VALUES(?,?,?,?,?,?,?)',
                       (self.nombre_cliente,self.direccion,self.dpi,self.nit,self.telefono,self.fecha,self.total))
        conexion.commit()
        conexion.close()
        self.productos.clear()
        self.total = 0
        self.nombre_cliente = ""
        self.direccion = ""
        self.telefono = ""
        self.dpi = ""
        self.nit = ""

    

carrito = CarrtioVenta()

