class Venta:
    def __init__(self, id_venta, id_recibo, fecha, id_producto, producto, precio, 
                 cantidad, sub_total, usuario, costo, descuento=None):
        
        self.id_venta = id_venta
        self.id_recibo = id_recibo
        self.fecha = fecha
        self.id_producto = id_producto
        self.producto = producto
        self.precio = precio
        self.cantidad = cantidad
        self.sub_total = sub_total
        self.usuario = usuario # Este campo se puede llenar con el nombre del usuario que realizó la venta, si es necesario
        self.costo = costo
        self.utilidad = float(self.sub_total) - (float(self.costo) * float(self.cantidad))
        
        if (descuento is None) or (descuento == ""):
            self.descuento = 0.0
        else:
            self.descuento = float(descuento)
        