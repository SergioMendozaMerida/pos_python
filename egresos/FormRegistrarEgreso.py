import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import egresos.Egresos as E

class FormRegistrarEgreso(tk.Toplevel):
    def __init__(self, parent, caja, actualizarEgresos=None):
        super().__init__(parent)
        self.title("Registrar Egreso")
        self.geometry("400x420")
        self.resizable(False, False)
        self.parent = parent
        self.actualizarEgresos = actualizarEgresos
        self.caja = caja

        self.configure(bg="#f5f6fa")

        # Estilos y Colores
        self.primary_color = "#0984e3"
        self.success_color = "#00b894"
        self.danger_color = "#d63031"

        # Hacer la ventana modal
        self.transient(parent)
        self.grab_set()

        tk.Label(
            self, text="NUEVO EGRESO", font=("Segoe UI", 14, "bold"), 
            bg="#f5f6fa", fg=self.primary_color
        ).pack(pady=20)

        # Contenedor de formulario
        container = tk.Frame(self, bg="white", padx=20, pady=20, relief="solid", bd=1)
        container.pack(padx=20, fill="both", expand=True)

        tk.Label(container, text="Razón / Concepto:", font=("Segoe UI", 10, "bold"), bg="white").pack(anchor="w")
        self.entry_razon = tk.Entry(container, font=("Segoe UI", 11), bd=1, relief="solid")
        self.entry_razon.pack(fill="x", pady=(5, 15))

        tk.Label(container, text="Proveedor (Opcional):", font=("Segoe UI", 10, "bold"), bg="white").pack(anchor="w")
        self.entry_proveedor = tk.Entry(container, font=("Segoe UI", 11), bd=1, relief="solid")
        self.entry_proveedor.pack(fill="x", pady=(5, 15))

        tk.Label(container, text="Monto (Q):", font=("Segoe UI", 10, "bold"), bg="white").pack(anchor="w")
        self.entry_monto = tk.Entry(container, font=("Segoe UI", 11), bd=1, relief="solid")
        self.entry_monto.pack(fill="x", pady=(5, 15))

        # Botones
        btn_frame = tk.Frame(self, bg="#f5f6fa")
        btn_frame.pack(fill="x", pady=20)

        tk.Button(
            btn_frame, text="Registrar", bg=self.success_color, fg="white", 
            font=("Segoe UI", 10, "bold"), command=self.registrar, cursor="hand2", width=12
        ).pack(side="left", padx=(40, 10))

        tk.Button(
            btn_frame, text="Cancelar", bg=self.danger_color, fg="white", 
            font=("Segoe UI", 10, "bold"), command=self.destroy, cursor="hand2", width=12
        ).pack(side="right", padx=(10, 40))

    def registrar(self):
        razon = self.entry_razon.get().strip()
        proveedor = self.entry_proveedor.get().strip()
        monto = self.entry_monto.get().strip()

        if not razon or not monto:
            messagebox.showwarning("Atención", "Por favor complete la razón y el monto.")
            return

        try:
            monto_val = float(monto)
            nuevo_egreso = E.Egreso(None, datetime.date.today(), self.caja.usuario, razon, proveedor, monto_val)
            nuevo_egreso.registrar_egreso()
            if self.actualizarEgresos: self.actualizarEgresos()
            messagebox.showinfo("Éxito", "Egreso registrado correctamente.")
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido.")