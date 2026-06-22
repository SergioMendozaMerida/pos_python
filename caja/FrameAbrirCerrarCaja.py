import tkinter as tk
from tkinter import messagebox

class FrameAbrirCaja(tk.Toplevel):
    def __init__(self, parent, caja, actualizar_caja_callback, show_productos):
        super().__init__(parent)
        self.caja = caja
        self.actualizar_caja_callback = actualizar_caja_callback
        self.show_productos = show_productos

        # Configuración de Colores y Estilos
        self.color_fondo = "#f8f9fa"
        self.color_header = "#2c3e50"
        self.color_primario = "#0984e3"
        self.color_exito = "#00b894"
        self.color_error = "#d63031"
        self.color_texto = "#2d3436"

        self.title("Abrir Caja")
        self.geometry("400x320")
        self.resizable(False, False)
        self.configure(bg=self.color_fondo)

        # Modalidad
        self.transient(parent)
        self.grab_set()

        # Header
        header = tk.Frame(self, bg=self.color_header, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header, text="Apertura de Caja", bg=self.color_header, 
            fg="white", font=("Segoe UI", 14, "bold")
        ).pack(pady=15)

        # Contenido
        container = tk.Frame(self, bg="white", padx=30, pady=25, relief="flat", bd=1)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            container, text="Monto inicial en caja (Q):", 
            font=("Segoe UI", 10, "bold"), bg="white", fg=self.color_texto
        ).pack(anchor="w", pady=(0, 5))

        self.entry_saldo_inicial = tk.Entry(
            container, font=("Segoe UI", 14), justify="center",
            relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", 
            highlightcolor=self.color_primario
        )
        self.entry_saldo_inicial.pack(fill="x", pady=(0, 20), ipady=5)
        self.entry_saldo_inicial.focus_set()
        self.entry_saldo_inicial.bind("<Return>", lambda e: self.abrir_caja())

        # Botones
        btn_style = {"font": ("Segoe UI", 10, "bold"), "fg": "white", "bd": 0, "cursor": "hand2", "relief": "flat"}
        
        self.btn_abrir = tk.Button(
            container, text="✓ Confirmar Apertura", bg=self.color_exito,
            command=self.abrir_caja, **btn_style
        )
        self.btn_abrir.pack(fill="x", pady=(0, 10), ipady=8)

        self.btn_cancelar = tk.Button(
            container, text="✕ Cancelar", bg=self.color_error,
            command=self.destroy, **btn_style
        )
        self.btn_cancelar.pack(fill="x", ipady=8)

    def abrir_caja(self):
        try:
            saldo_inicial = float(self.entry_saldo_inicial.get())
            self.caja.abrir_caja(saldo_inicial)
            self.actualizar_caja_callback()
            self.show_productos()
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto numérico válido para el saldo inicial.")


class FrameCerrarCaja(tk.Toplevel):
    def __init__(self, parent, caja, actualizar_caja_callback, show_productos):
        super().__init__(parent)
        self.parent = parent
        self.caja = caja
        self.actualizar_caja_callback = actualizar_caja_callback
        self.show_productos = show_productos

        self.color_fondo = "#f8f9fa"
        self.color_header = "#2c3e50"
        self.color_error = "#d63031"
        self.color_neutral = "#636e72"

        self.title("Cerrar Caja")
        self.geometry("400x320")
        self.resizable(False, False)
        self.configure(bg=self.color_fondo)

        self.transient(parent)
        self.grab_set()

        header = tk.Frame(self, bg=self.color_header, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header, text="Cierre de Caja", bg=self.color_header, 
            fg="white", font=("Segoe UI", 14, "bold")
        ).pack(pady=15)

        container = tk.Frame(self, bg="white", padx=30, pady=25, relief="flat", bd=1)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            container, text="Efectivo real en caja (Q):", 
            font=("Segoe UI", 10, "bold"), bg="white"
        ).pack(anchor="w", pady=(0, 5))

        self.entry_monto_final = tk.Entry(
            container, font=("Segoe UI", 14), justify="center",
            relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", 
            highlightcolor=self.color_error
        )
        self.entry_monto_final.pack(fill="x", pady=(0, 20), ipady=5)
        self.entry_monto_final.focus_set()
        self.entry_monto_final.bind("<Return>", lambda e: self.cerrar_caja())

        btn_style = {"font": ("Segoe UI", 10, "bold"), "fg": "white", "bd": 0, "cursor": "hand2", "relief": "flat"}

        self.btn_cerrar = tk.Button(
            container, text="🔒 Finalizar Jornada", bg=self.color_error,
            command=self.cerrar_caja, **btn_style
        )
        self.btn_cerrar.pack(fill="x", pady=(0, 10), ipady=8)

        self.btn_cancelar = tk.Button(
            container, text="Cancelar", bg=self.color_neutral,
            command=self.destroy, **btn_style
        )
        self.btn_cancelar.pack(fill="x", ipady=8)

    def cerrar_caja(self):
        self.caja.obtener_sesion_caja()
        try:
            efectivo_final = float(self.entry_monto_final.get())
            
            if efectivo_final != self.caja.saldo_final:
                diferencia = efectivo_final - self.caja.saldo_final
                msg = f"Existe un descuadre de Q{diferencia:,.2f}.\n\n¿Está seguro que desea cerrar la caja con esta diferencia?"
                if not messagebox.askyesno("Aviso de Descuadre", msg):
                    return

            self.caja.cerrar_caja(efectivo_final)
            self.actualizar_caja_callback()
            self.show_productos()
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto numérico válido para el cierre.")
