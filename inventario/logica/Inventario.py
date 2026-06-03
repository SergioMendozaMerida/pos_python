from datetime import datetime
import sqlite3
import inventario.logica.Producto as Prod

class Inventario:
    def __init__(self, usuario):
        self.productos = []
        self.conexion = sqlite3.connect("db_inventario.db")
        self.cursor = self.conexion.cursor()
        self.usuario = usuario

    def agregar_productos(self, producto):
        self.productos.append(producto)

    def obtener_productos(self):
        self.productos.clear()
        self.cursor.execute("SELECT * FROM productos")
        productos = self.cursor.fetchall()
        
        for producto in productos:
            self.agregar_productos(Prod.Producto(
                producto[0],
                producto[1],
                producto[2],
                producto[3],
                producto[4],
                producto[5],
                producto[6],
                producto[7],
                producto[8]
            ))

    def ingresar_producto(self, nombre, codigo, descripcion, presentacion, categoria, precio_compra, precio_venta, stock):
        self.cursor.execute("INSERT INTO productos (nombre,codigo_producto,descripcion,presentacion,categoria,precio_venta,precio_compra,stock) VALUES(?,?,?,?,?,?,?,?)",
                            (nombre, codigo, descripcion,presentacion,categoria,precio_compra,precio_venta,stock))
        self.conexion.commit()
        self.obtener_productos()

    def mostrar_productos(self):
        for producto in self.productos:
            print(f"{producto.nombre} {producto.descripcion}")

    def buscar_producto(self, nombre, descripcion):
        self.cursor.execute("SELECT * FROM productos WHERE nombre LIKE ? AND descripcion LIKE ?",(f"%{nombre}%", f"%{descripcion}%"))
        productos = self.cursor.fetchall()
        self.productos.clear()
        for producto in productos:
            self.agregar_productos(Prod.Producto(
                producto[0],
                producto[1],
                producto[2],
                producto[3],
                producto[4],
                producto[5],
                producto[6],
                producto[7],
                producto[8]
            ))

    def buscar_producto_por_codigo(self, codigo):
        self.cursor.execute("SELECT * FROM productos WHERE codigo_producto=?", (codigo,))
        producto = self.cursor.fetchone()
        if producto:
            return Prod.Producto(
                producto[0],
                producto[1],
                producto[2],
                producto[3],
                producto[4],
                producto[5],
                producto[6],
                producto[7],
                producto[8]
            )
        else:
            return None
        
    def buscar_producto_por_nombre(self, nombre):
        self.cursor.execute("SELECT * FROM productos WHERE nombre=?", (nombre,))
        producto = self.cursor.fetchone()
        if producto:
            return Prod.Producto(
                producto[0],
                producto[1],
                producto[2],
                producto[3],
                producto[4],
                producto[5],
                producto[6],
                producto[7],
                producto[8]
            )
        else:
            return None
        
    def buscar_ingresar_stock_por_codigo(self, codigo):
        self.cursor.execute("SELECT * FROM productos WHERE codigo_producto=?", (codigo,))
        producto = self.cursor.fetchone()
        if producto:
            return Prod.Producto(
                producto[0],
                producto[1],
                producto[2],
                producto[3],
                producto[4],
                producto[5],
                producto[6],
                producto[7],
                producto[8]
            )
        else:
            return None
        
    def buscar_ingresar_stock_por_nombre(self, nombre):
        self.cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{nombre}%",))
        producto = self.cursor.fetchone()
        if producto:
            return Prod.Producto(
                producto[0],
                producto[1],
                producto[2],
                producto[3],
                producto[4],
                producto[5],
                producto[6],
                producto[7],
                producto[8]
            )
        else:
            return None
        
    def aumentar_stock(self, id_producto, nombre_producto,cantidad, precio_compra, precio_venta, proveedor=""):
        hoy = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO ingresos_stock (fecha_ingreso, id_producto, cantidad, precio_compra, precio_venta, proveedor, usuario, producto) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                            (hoy, id_producto, cantidad, precio_compra, precio_venta, proveedor, self.usuario.usuario, nombre_producto))

        self.conexion.commit()
        self.obtener_productos()

        """self.cursor.execute("UPDATE productos SET stock = stock + ?, precio_compra = ?, precio_venta = ? WHERE id_producto=?", (cantidad, precio_compra, precio_venta, id_producto))
        self.conexion.commit()
        self.obtener_productos()"""

    def editar_producto(self, id_producto, nombre, descripcion, presentacion, categoria, precio_compra, precio_venta, stock):
        self.cursor.execute("UPDATE productos SET nombre=?, descripcion=?, presentacion=?, categoria=?, precio_compra=?, precio_venta=?, stock=? WHERE id_producto=?",
                            (nombre, descripcion, presentacion, categoria, precio_compra, precio_venta, stock, id_producto))
        self.conexion.commit()
        self.obtener_productos()

    def eliminar_producto(self, id_producto):
        self.cursor.execute("DELETE FROM productos WHERE id_producto=?", (id_producto,))
        self.conexion.commit()
        self.obtener_productos()