import tkinter as tk
from tkinter import messagebox, ttk

class FrameTerminarVenta(tk.Toplevel):
    def __init__(self, parent, carrito):
        super().__init__(parent)
        self.title("Resumen de Venta")
        self.geometry("400x350")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")

        self.carrito = carrito

        if self.carrito.nombre_cliente == "":
            self.carrito.nombre_cliente = "CF"
        
        # Main frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Resumen de Venta", font=("Arial", 16, "bold"), foreground="#333")
        title_label.pack(pady=(0, 20))
        
        # Receipt info frame
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        lbl_recibo = ttk.Label(info_frame, text=f"Recibo No. {self.carrito.numero_recibo}", font=("Arial", 12))
        lbl_recibo.pack(anchor=tk.W)
        
        lbl_nombre = ttk.Label(info_frame, text=f"Cliente: {self.carrito.nombre_cliente}", font=("Arial", 12))
        lbl_nombre.pack(anchor=tk.W)
        
        lbl_total = ttk.Label(info_frame, text=f"Total: Q {self.carrito.total:,.2f}", font=("Arial", 14, "bold"), foreground="#007acc")
        lbl_total.pack(anchor=tk.W, pady=(10, 0))
        
        # Payment section
        payment_frame = ttk.Frame(main_frame)
        payment_frame.pack(fill=tk.X, pady=(20, 10))
        
        ttk.Label(payment_frame, text="Ingrese la denominación de pago:", font=("Arial", 10)).pack(anchor=tk.W)
        
        self.entry_pago = ttk.Entry(payment_frame, font=("Arial", 12), width=20)
        self.entry_pago.focus_set()
        self.entry_pago.bind("<KeyRelease>", self.iniciar_espera)
        self.entry_pago.bind("<Return>", self.calcular_cambio)
        self.entry_pago.pack(pady=(5, 0))
        
        # Change label
        self.lbl_cambio = ttk.Label(payment_frame, text="Cambio: Q 0.00", font=("Arial", 12, "bold"), foreground="#28a745")
        self.lbl_cambio.pack(pady=(10, 0))
        
        # Button
        self.btn_concretar_venta = ttk.Button(main_frame, text="Finalizar Venta", command=self.concretar_venta, style="Accent.TButton")
        self.btn_concretar_venta.pack(pady=(20, 0))
        
        # Style for button
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 12, "bold"), background="#007acc", foreground="white")

        self.timer_id = None

    def iniciar_espera(self, event):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.timer_id = self.after(1000, self.calcular_cambio)

    def calcular_cambio(self, event=None):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        cambio = int(self.entry_pago.get()) - self.carrito.total
        self.lbl_cambio.configure(text=f"Q  {cambio:.2f}")

    def concretar_venta(self):
        self.carrito.concretar_venta()
        messagebox.showinfo("Venta exitosa", "Venta registrada exitosamente.")
        self.destroy()