import tkinter as tk

class FrameTerminarVenta(tk.Toplevel):
    def __init__(self, parent, recibo, total, nombre_cliente):
        super().__init__(parent)

        self.total = total

        
        lbl_recibo = tk.Label(self, text=f"Recibo No. {recibo}")
        lbl_recibo.pack()
        lbl_nombre = tk.Label(self, text=f"cliente: {nombre_cliente}")
        lbl_nombre.pack()
        lbl_total = tk.Label(self, text=f"Total Q    {total:,.2f}")
        lbl_total.pack()

        tk.Label(self, text="Ingrese la denominación de pago: ").pack()
        self.entry_pago = tk.Entry(self)
        self.entry_pago.bind("<Return>", lambda e: self.calcular_cambio)

    def calcular_cambio(self):
        cambio = int(self.entry_pago.get()) - self.total