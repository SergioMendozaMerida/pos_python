import tkinter as tk
from tkinter import ttk

class FrameDetalleRecibo(tk.Toplevel):
    def __init__(self, parent, recibo):
        super().__init__(parent)
        self.recibo = recibo
        
        self.title(f"Detalle de Recibo No. {self.recibo.no_recibo}")
        self.geometry("600x650")
        self.configure(bg="#f8f9fa")
        self.resizable(False, False)

        # Estilos de colores
        self.color_header = "#2c3e50"
        self.color_texto = "#2d3436"
        self.color_primario = "#0984e3"
        self.color_borde = "#dfe6e9"

        # --- Header ---
        header_frame = tk.Frame(self, bg=self.color_header, height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text=f"Recibo No. {self.recibo.no_recibo}",
            bg=self.color_header,
            fg="white",
            font=("Segoe UI", 16, "bold")
        ).pack(side="left", padx=20, pady=15)

        tk.Label(
            header_frame,
            text=f"Fecha: {self.recibo.fecha}",
            bg=self.color_header,
            fg="#bdc3c7",
            font=("Segoe UI", 11)
        ).pack(side="right", padx=20, pady=15)

        # --- Frame de Información del Cliente ---
        info_frame = tk.LabelFrame(
            self, 
            text=" Datos del Cliente ", 
            font=("Segoe UI", 10, "bold"),
            bg="#f8f9fa",
            fg=self.color_header,
            padx=15, 
            pady=15
        )
        info_frame.pack(fill="x", padx=20, pady=20)

        # Grid para etiquetas de datos
        labels = [
            ("Cliente:", self.recibo.nombre_cliente, 0, 0),
            ("DPI:", self.recibo.dpi, 0, 1),
            ("Dirección:", self.recibo.direccion, 1, 0),
            ("NIT:", self.recibo.nit, 1, 1),
            ("Teléfono:", self.recibo.telefono, 2, 0)
        ]

        for text, value, row, col in labels:
            lbl_title = tk.Label(info_frame, text=text, font=("Segoe UI", 9, "bold"), bg="#f8f9fa", fg="#636e72")
            lbl_title.grid(row=row*2, column=col, sticky="w", padx=10)
            
            lbl_value = tk.Label(info_frame, text=value if value else "N/A", font=("Segoe UI", 10), bg="#f8f9fa", fg=self.color_texto)
            lbl_value.grid(row=row*2+1, column=col, sticky="w", padx=10, pady=(0, 10))

        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)

        # --- Tabla de Productos (Ventas) ---
        table_frame = tk.Frame(self, bg="white", bd=1, relief="solid", highlightbackground=self.color_borde)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        columnas = ("producto", "precio", "cantidad", "subtotal")
        self.tabla = ttk.Treeview(table_frame, columns=columnas, show="headings", height=8)
        
        self.tabla.heading("producto", text="Producto")
        self.tabla.heading("precio", text="Precio Unit.")
        self.tabla.heading("cantidad", text="Cant.")
        self.tabla.heading("subtotal", text="Subtotal")

        self.tabla.column("producto", width=250, anchor="w")
        self.tabla.column("precio", width=90, anchor="e")
        self.tabla.column("cantidad", width=60, anchor="center")
        self.tabla.column("subtotal", width=100, anchor="e")

        self.tabla.pack(fill="both", expand=True)

        # Llenar la tabla con las ventas del recibo
        # venta[4]=producto, venta[5]=precio, venta[6]=cantidad, venta[7]=subtotal
        for v in self.recibo.ventas:
            self.tabla.insert("", "end", values=(
                v.producto, 
                f"Q {v.precio:,.2f}", 
                v.cantidad, 
                f"Q {v.sub_total:,.2f}"
            ))

        # --- Footer con Total ---
        footer_frame = tk.Frame(self, bg="#f8f9fa")
        footer_frame.pack(fill="x", padx=20, pady=(0, 20))

        tk.Label(
            footer_frame,
            text=f"TOTAL: Q {self.recibo.total:,.2f}",
            font=("Segoe UI", 16, "bold"),
            bg="#f8f9fa",
            fg=self.color_primario
        ).pack(side="right")

        self.btn_cerrar = tk.Button(
            footer_frame, text="Cerrar", bg="#636e72", fg="white", 
            relief="flat", padx=20, pady=5, cursor="hand2", command=self.destroy
        )
        self.btn_cerrar.pack(side="left")