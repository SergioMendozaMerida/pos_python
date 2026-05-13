class Producto:
    def __init__(self, id_producto, nombre, descripcion, presentacion, categoria, precio_compra, precio_venta, stock):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.presentacion = presentacion
        self.categoria = categoria
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.stock = stock