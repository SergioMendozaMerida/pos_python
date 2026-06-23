import datetime
from pathlib import Path
from openpyxl import Workbook

class ReporteInventario:
    def __init__(self, inventario):
        self.inventario = inventario
        fecha_actual = datetime.datetime.now()
        self.nombre = f"reporte inventario {fecha_actual.strftime('%Y-%m-%d')}"

        self.ruta_documentos = Path.home() / "Documents/reportes_pos"
        self.ruta_documentos.mkdir(exist_ok=True)

    def crear_reporte_excel(self):
        WB = Workbook()

        hoja_ativa = WB.active
        hoja_ativa.title = "Reporte de Inventario"

        hoja_ativa.append(["ID Producto", "Nombre", "Código", "Descripción", "Presentación", "Categoría", "Precio Compra", "Precio Venta", "Stock"])
        for producto in self.inventario.productos:
            hoja_ativa.append([producto.id_producto, producto.nombre, producto.codigo, producto.descripcion, 
                                producto.presentacion, producto.categoria, producto.precio_compra, producto.precio_venta, producto.stock])

        WB.save(f"{self.ruta_documentos}/{self.nombre}.xlsx")
    