import datetime
from pathlib import Path
from openpyxl import Workbook

class CrearReporteEgresos:
    def __init__(self, egresos):
        self.egresos = egresos
        fecha_actual = datetime.datetime.now()
        self.nombre = f"reporte egresos {fecha_actual.strftime('%Y-%m-%d')}"

        self.ruta_documentos = Path.home() / "Documents/reportes_pos"
        self.ruta_documentos.mkdir(exist_ok=True)

    def crear_reporte_excel(self):
        WB = Workbook()

        hoja_ativa = WB.active
        hoja_ativa.title = "Reporte de Egresos"

        hoja_ativa.append(["ID Egreso", "Fecha","Usuario", "Razón", "Proveedor", "Monto"])
        for egreso in self.egresos.egresos:
            hoja_ativa.append([egreso.id_egreso, egreso.fecha, egreso.usuario, 
                               egreso.razon, egreso.proveedor, egreso.monto])

        WB.save(f"{self.ruta_documentos}/{self.nombre}.xlsx")