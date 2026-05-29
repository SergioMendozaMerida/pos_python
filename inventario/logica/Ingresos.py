class Ingresos():
    def __init__(self, fecha, id_producto, cantidad, precio_unitario, proveedor):
        self.fecha = fecha
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.proveedor = proveedor
        self.total = cantidad * precio_unitario

    def ingresar_stock(self):
        