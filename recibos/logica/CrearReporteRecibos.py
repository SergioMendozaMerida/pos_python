import datetime
from pathlib import Path
from openpyxl import Workbook

class CrearReporteRecibos:
    def __init__(self, recibos):
        self.recibos = recibos
        fecha_actual = datetime.datetime.now()
        self.nombre = f"reporte recibos {fecha_actual.strftime('%Y-%m-%d')}"

        self.ruta_documentos = Path.home() / "Documents/reportes_pos"
        self.ruta_documentos.mkdir(exist_ok=True)

    def crear_reporte_excel(self):
        WB = Workbook()

        hoja_ativa = WB.active
        hoja_ativa.title = "Reporte de Recibos"

        hoja_ativa.append(["Recibo", "Cliente", "Dirección", "DPI", "NIT","Teléfono", "Fecha", "Total", "Total", "Utilidad", "Usuario"])
        for recibo in self.recibos.recibos:
            hoja_ativa.append([recibo.no_recibo, recibo.nombre_cliente, recibo.direccion, recibo.dpi, recibo.nit, recibo.telefono, recibo.fecha, 
                               recibo.total, recibo.total, recibo.utilidad, recibo.usuario])

        WB.save(f"{self.ruta_documentos}/{self.nombre}.xlsx")