import tkinter as tk
from tkinter import messagebox

class FrameAbrirCaja(tk.Toplevel):
    def __init__(self, parent, caja, btn_abrir_cerrar_caja, show_productos):
        super().__init__(parent)
        self.caja = caja
        self.btn_abrir_cerrar_caja = btn_abrir_cerrar_caja
        self.show_productos = show_productos
        self.title("Abrir Caja")
        self.geometry("300x200")
        self.resizable(False, False)

        tk.Label(
            self,
            text="Ingrese el saldo inicial para abrir la caja",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=20)

        self.entry_saldo_inicial = tk.Entry(self, font=("Segoe UI", 12), justify="center")
        self.entry_saldo_inicial.pack(pady=10)

        btn_abrir = tk.Button(
            self,
            text="Abrir Caja",
            bg="#27ae60",
            fg="white",
            cursor='hand2',
            command=self.abrir_caja
        )
        btn_abrir.pack(fill="x", padx=50, pady=(0, 10), ipady=8)

        btn_cancelar = tk.Button(
            self,
            text="Cancelar",
            bg="#e74c3c",
            fg="white",
            cursor='hand2',
            command=self.destroy
        )
        btn_cancelar.pack(fill="x", padx=50, ipady=8)

    def abrir_caja(self):
        self.caja.abrir_caja()
        self.btn_abrir_cerrar_caja.config(text="Cerrar Caja")
        self.show_productos()
        self.destroy()

class FrameCerrarCaja(tk.Toplevel):
    def __init__(self, parent, caja, btn_abrir_cerrar_caja, show_productos):
        super().__init__(parent)
        self.caja = caja
        self.btn_abrir_cerrar_caja = btn_abrir_cerrar_caja
        self.show_productos = show_productos
        self.title("Cerrar Caja")
        self.geometry("300x200")
        self.resizable(False, False)

        tk.Label(
            self,
            text="Ingrese el monto final para cerrar la caja",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=20)

        self.entry_monto_final = tk.Entry(self, font=("Segoe UI", 12), justify="center")
        self.entry_monto_final.pack(pady=10)

        btn_cerrar = tk.Button(
            self,
            text="Cerrar Caja",
            bg="#e74c3c",
            fg="white",
            cursor='hand2',
            command=self.cerrar_caja
        )
        btn_cerrar.pack(fill="x", padx=50, pady=(0, 10), ipady=8)

        btn_cancelar = tk.Button(
            self,
            text="Cancelar",
            bg="#636e72",
            fg="white",
            cursor='hand2',
            command=self.destroy
        )
        btn_cancelar.pack(fill="x", padx=50, ipady=8)

    def cerrar_caja(self):
        self.caja.cerrar_caja()
        self.btn_abrir_cerrar_caja.config(text="Abrir Caja")
        self.show_productos()
        self.destroy()