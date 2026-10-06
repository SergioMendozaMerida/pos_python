import customtkinter as ctk
from tkinter import messagebox
import recibos.logica.CrearRecibo as RV


class FrameTerminarVenta(ctk.CTkToplevel):
    def __init__(self, parent, carrito, limpiar_carrito, actualizar_recibos, actualizar_ventas, usuario, calcular_total):
        super().__init__(parent)
        self.title("Resumen de Venta")
        self.geometry("440x550")
        self.resizable(False, False)
        self.configure(fg_color="#f4f6f9")
        self.transient(parent)
        self.grab_set()

        self.carrito = carrito
        self.limpiar_carrito = limpiar_carrito
        self.actualizar_recibos = actualizar_recibos
        self.actualizar_ventas = actualizar_ventas
        self.usuario = usuario
        self.calcular_total = calcular_total
        self.timer_id = None

        if self.carrito.nombre_cliente == "":
            self.carrito.nombre_cliente = "CF"

        self.protocol("WM_DELETE_WINDOW", self.cerrar)

        header = ctk.CTkFrame(self, fg_color="#2c3e50", corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(
            header,
            text="FINALIZAR VENTA",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color="white"
        ).pack(anchor="w", padx=28, pady=(18, 2))
        ctk.CTkLabel(
            header,
            text="Verifique el resumen e ingrese el pago recibido",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#cbd5e1"
        ).pack(anchor="w", padx=28, pady=(0, 18))

        content = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color="#dfe6e9"
        )
        content.pack(fill="x", padx=22, pady=(18, 12))

        ctk.CTkLabel(
            content,
            text=f"RECIBO  No. {self.carrito.numero_recibo}",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#636e72"
        ).pack(anchor="w", padx=22, pady=(20, 4))
        ctk.CTkLabel(
            content,
            text=f"Cliente: {self.carrito.nombre_cliente}",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color="#2d3436"
        ).pack(anchor="w", padx=22)

        total_card = ctk.CTkFrame(content, fg_color="#edf6ff", corner_radius=10)
        total_card.pack(fill="x", padx=18, pady=(16, 18))
        ctk.CTkLabel(
            total_card,
            text="TOTAL A PAGAR",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#636e72"
        ).pack(anchor="w", padx=16, pady=(11, 0))
        ctk.CTkLabel(
            total_card,
            text=f"Q {self.carrito.total:,.2f}",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color="#0984e3"
        ).pack(anchor="w", padx=16, pady=(0, 11))

        ctk.CTkLabel(
            content,
            text="Pago recibido (Q)",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#2d3436"
        ).pack(anchor="w", padx=22, pady=(0, 6))
        self.entry_pago = ctk.CTkEntry(
            content,
            font=ctk.CTkFont(family="Segoe UI", size=16),
            placeholder_text="Ingrese el monto recibido",
            justify="right",
            height=42,
            border_color="#dfe6e9"
        )
        self.entry_pago.pack(fill="x", padx=22)
        self.entry_pago.bind("<KeyRelease>", self.iniciar_espera)
        self.entry_pago.bind("<Return>", self.concretar_venta)

        self.lbl_cambio = ctk.CTkLabel(
            content,
            text="Cambio: Q 0.00",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color="#218c5a"
        )
        self.lbl_cambio.pack(anchor="e", padx=22, pady=(10, 10))

        self.btn_concretar_venta = ctk.CTkButton(
            self,
            text="✓  Finalizar venta",
            command=self.concretar_venta,
            fg_color="#218c5a",
            hover_color="#176e46",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            height=46,
            corner_radius=9
        )
        self.btn_concretar_venta.pack(fill="x", padx=48, pady=(0, 16))

        self.after(100, self.entry_pago.focus_set)

    def iniciar_espera(self, event):
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
        self.timer_id = self.after(500, self.calcular_cambio)

    def calcular_cambio(self, event=None):
        self.timer_id = None
        try:
            cambio = float(self.entry_pago.get()) - self.carrito.total
            self.lbl_cambio.configure(text=f"Cambio: Q {cambio:,.2f}")
            return True
        except ValueError:
            self.lbl_cambio.configure(
                text=f"{self.entry_pago.get()} no es un número válido."
            )
            return False

    def cerrar(self):
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.destroy()

    def concretar_venta(self, event=None):
        self.carrito.concretar_venta()
        messagebox.showinfo("Venta exitosa", "Venta registrada exitosamente.")
        self.limpiar_carrito()
        cv = RV.CrearRecibo(self.carrito)
        cv.crear_recibo()
        self.carrito.vaciar_carrito()
        self.limpiar_carrito()
        self.actualizar_ventas()
        self.actualizar_recibos()
        self.calcular_total()
        self.cerrar()
