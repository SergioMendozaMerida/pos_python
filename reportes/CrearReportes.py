import datetime
import os
from pathlib import Path
from openpyxl import Workbook

class CrearReportes:
    def __init__(self, reporte_ventas):
        self.reporte_ventas = reporte_ventas
        self.nombre = "reporte ventas"
        
        self.ruta_documentos = Path.home() / "Documents/reportes_pos"
        self.ruta_documentos.mkdir(exist_ok=True)

    def set_nombre(self, nombre):
        self.nombre = nombre


    def crear_reporte_excel(self):
        WB = Workbook()

        hoja_ativa = WB.active
        hoja_ativa.title = "Reporte de Ventas"

        hoja_ativa.append(["Recibo", "Fecha", "ID Producto", "Producto", "Cantidad", "Precio", "Total","Utilidad"])
        for venta in self.reporte_ventas.ventas:
            hoja_ativa.append([venta.id_recibo, venta.fecha, venta.id_producto, venta.producto, venta.cantidad, 
                               venta.precio, venta.sub_total, venta.utilidad])

        WB.save(f"{self.ruta_documentos}/{self.nombre}.xlsx")



    
