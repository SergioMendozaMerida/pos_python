import sqlite3
import Producto as Prod

class Inventario:
    def __init__(self):
        self.productos = []
        self.conexion = sqlite3.connect("db_inventario.db")
        self.cursor = self.conexion.cursor()

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
                producto[7]
            ))

    def ingresar_producto(self, nombre, descripcion, presentacion, categoria, precio_compra, precio_venta, stock):
        self.cursor.execute("INSERT INTO productos (nombre,descripcion,presentacion,categoria,precio_venta,precio_compra,stock) VALUES(?,?,?,?,?,?,?)",
                            (nombre, descripcion,presentacion,categoria,precio_compra,precio_venta,stock))
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
                producto[7]
            ))

    def editar_producto(self, id_producto, nombre, descripcion, presentacion, categoria, precio_compra, precio_venta, stock):
        self.cursor.execute("UPDATE productos SET nombre=?, descripcion=?, presentacion=?, categoria=?, precio_compra=?, precio_venta=?, stock=? WHERE id_producto=?",
                            (nombre, descripcion, presentacion, categoria, precio_compra, precio_venta, stock, id_producto))
        self.conexion.commit()
        self.obtener_productos()

    def eliminar_producto(self, id_producto):
        self.cursor.execute("DELETE FROM productos WHERE id_producto=?", (id_producto,))
        self.conexion.commit()
        self.obtener_productos()