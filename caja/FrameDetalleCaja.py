import tkinter as tk

class FrameDetalleCaja(tk.Toplevel):
    def __init__(self, parent, caja):
        super().__init__(parent)
        self.caja = caja
        self.caja.obtener_sesion_caja()

        # Configuración de Estilos
        self.color_fondo = "#f8f9fa"
        self.color_header = "#2c3e50"
        self.color_primario = "#0984e3"
        self.color_texto = "#2d3436"
        self.color_subtexto = "#636e72"

        self.title("Resumen de Sesión")
        self.geometry("450x550")
        self.resizable(False, False)
        self.configure(bg=self.color_fondo)

        # Hacer la ventana modal
        self.transient(parent)
        self.grab_set()

        # Header
        header = tk.Frame(self, bg=self.color_header, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header, text="📋 Detalle de Caja Actual", bg=self.color_header, 
            fg="white", font=("Segoe UI", 14, "bold")
        ).pack(pady=15)

        # Contenedor Principal (Tarjeta)
        container = tk.Frame(self, bg="white", padx=25, pady=20, relief="flat", bd=1)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Datos de Cabecera (Fecha y Usuario)
        info_top = tk.Frame(container, bg="white")
        info_top.pack(fill="x", pady=(0, 15))
        
        tk.Label(info_top, text=f"📅 Fecha: {self.caja.fecha}", font=("Segoe UI", 10), bg="white", fg=self.color_subtexto).pack(side="left")
        tk.Label(info_top, text=f"👤 Usuario: {self.caja.usuario}", font=("Segoe UI", 10, "bold"), bg="white", fg=self.color_subtexto).pack(side="right")

        # Separador
        tk.Frame(container, bg="#dfe6e9", height=1).pack(fill="x", pady=10)

        # Función auxiliar para filas de datos
        def crear_fila(label, valor, color_valor=None):
            if color_valor is None: color_valor = self.color_texto
            row = tk.Frame(container, bg="white", pady=5)
            row.pack(fill="x")
            tk.Label(row, text=label, font=("Segoe UI", 11), bg="white", fg=self.color_texto).pack(side="left")
            tk.Label(row, text=f"Q {valor:,.2f}", font=("Segoe UI", 11, "bold"), bg="white", fg=color_valor).pack(side="right")

        # Lista de valores financieros
        crear_fila("Saldo Inicial:", self.caja.saldo_inicial)
        crear_fila("(+) Ingresos por Ventas:", self.caja.ingresos_ventas, "#27ae60")
        crear_fila("(+) Otros Ingresos:", self.caja.otros_ingresos, "#27ae60")
        crear_fila("(-) Egresos / Gastos:", self.caja.egresos, "#d63031")
        
        # Separador para el total esperado
        tk.Frame(container, bg="#dfe6e9", height=1).pack(fill="x", pady=15)
        
        # Saldo Final / Esperado
        row_total = tk.Frame(container, bg="white")
        row_total.pack(fill="x")
        tk.Label(row_total, text="Saldo Esperado en Caja:", font=("Segoe UI", 12, "bold"), bg="white", fg=self.color_primario).pack(side="left")
        tk.Label(row_total, text=f"Q {self.caja.saldo_final:,.2f}", font=("Segoe UI", 14, "bold"), bg="white", fg=self.color_primario).pack(side="right")

        # Botón Cerrar
        self.btn_cerrar = tk.Button(
            self, text="Entendido / Cerrar", bg=self.color_header, fg="white",
            font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
            command=self.destroy
        )
        self.btn_cerrar.pack(fill="x", padx=45, pady=(0, 25), ipady=8)