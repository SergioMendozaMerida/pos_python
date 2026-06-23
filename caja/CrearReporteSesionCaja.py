import datetime
from pathlib import Path
from openpyxl import Workbook

class ReporteSesionesCaja:
    def __init__(self, sesiones_caja):
        self.sesiones_caja = sesiones_caja
        fecha_actual = datetime.datetime.now()
        self.nombre = f"reporte sesiones caja {fecha_actual.strftime('%Y-%m-%d')}"

        self.ruta_documentos = Path.home() / "Documents/reportes_pos"
        self.ruta_documentos.mkdir(exist_ok=True)

    def crear_reporte_excel(self):
        WB = Workbook()

        hoja_ativa = WB.active
        hoja_ativa.title = "Reporte de Sesiones Caja"

        hoja_ativa.append(["ID Sesión", "Fecha", "Usuario", "Saldo Inicial", "Ingresos Ventas", "Otros Ingresos", "Egresos", 
                           "Saldo Final", "Efectivo Final", "Diferencia", "Utilidad Generada", "Estado"])
        for sesion in self.sesiones_caja.sesiones:
            hoja_ativa.append([sesion.id_sesion, sesion.fecha, sesion.usuario, sesion.saldo_inicial, 
                               sesion.ingresos_ventas, sesion.otros_ingresos, sesion.egresos, sesion.saldo_final, sesion.efectivo_final, 
                               sesion.diferencia, sesion.utilidad_generada, sesion.estado])

        WB.save(f"{self.ruta_documentos}/{self.nombre}.xlsx")
