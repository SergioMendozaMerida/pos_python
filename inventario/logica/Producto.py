class Producto:
    def __init__(self, id_producto, nombre, descripcion, presentacion, categoria, precio_compra, precio_venta, precio_blister, precio_caja, stock, codigo_producto):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.presentacion = presentacion
        self.categoria = categoria
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.precio_blister = precio_blister
        self.precio_caja = precio_caja
        self.stock = stock
        self.codigo = codigo_producto
        self.utilidad = float(self.precio_venta) - float(self.precio_compra)