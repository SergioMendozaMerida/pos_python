import datetime
from pathlib import Path
from openpyxl import Workbook

class ReporteIngresos:
    def __init__(self, ingresos):
        self.ingresos = ingresos
        fecha_actual = datetime.datetime.now()
        self.nombre = f"reporte ingresos stock{fecha_actual.strftime('%Y-%m-%d')}"

        self.ruta_documentos = Path.home() / "Documents/reportes_pos"
        self.ruta_documentos.mkdir(exist_ok=True)

    def crear_reporte_excel(self):
        WB = Workbook()

        hoja_ativa = WB.active
        hoja_ativa.title = "Reporte de Ingresos"

        hoja_ativa.append(["ID Ingreso", "Fecha", "ID Producto", "Producto", "Cantidad", "Precio Compra", "Precio Venta", "Proveedor"])
        for ingreso in self.ingresos.ingresos:
            hoja_ativa.append([ingreso.id_ingreso, ingreso.fecha_ingreso, ingreso.id_producto, ingreso.producto, ingreso.cantidad, 
                               ingreso.precio_compra, ingreso.precio_venta, ingreso.proveedor])

        WB.save(f"{self.ruta_documentos}/{self.nombre}.xlsx")