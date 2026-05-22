import datetime

from openpyxl import Workbook

class CrearReportes:
    def __init__(self, reporte_ventas):
        self.reporte_ventas = reporte_ventas
        self.nombre = "reporte ventas"

    def set_nombre(self, nombre):
        self.nombre = nombre


    def crear_reporte_excel(self):
        WB = Workbook()

        hoja_ativa = WB.active
        hoja_ativa.title = "Reporte de Ventas"

        hoja_ativa.append(["Recibo", "Fecha", "ID Producto", "Producto", "Cantidad", "Precio", "Total"])
        for venta in self.reporte_ventas.ventas:
            hoja_ativa.append([venta.id_recibo, venta.fecha, venta.id_producto, venta.producto, venta.cantidad, venta.precio, venta.sub_total])

        WB.save(f"reportes_excel/{self.nombre}.xlsx")



    
