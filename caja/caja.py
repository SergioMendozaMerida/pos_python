import datetime


class Caja:
    def __init__(self, usuario):
        self.fecha = None
        self.usuario = usuario
        self.saldo_inicial = 0
        self.ingresos_ventas = 0
        self.otros_ingresos = 0
        self.egresos = 0
        self.saldo_final = 0
        self.estado = False

    def abrir_caja(self, saldo_inicial=0):
        self.fecha = datetime.date.today()
        self.saldo_inicial = saldo_inicial
        self.ingresos_ventas = 0
        self.otros_ingresos = 0
        self.egresos = 0
        self.saldo_final = saldo_inicial
        self.estado = True
        print(self.estado)

    def cerrar_caja(self):
        self.saldo_final = self.saldo_inicial + self.ingresos_ventas + self.otros_ingresos - self.egresos
        self.estado = False
        print(self.estado)