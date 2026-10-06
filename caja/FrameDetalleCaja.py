import customtkinter as ctk


class FrameDetalleCaja(ctk.CTkToplevel):
    def __init__(self, parent, caja):
        super().__init__(parent)
        self.caja = caja
        self.caja.obtener_sesion_caja()

        self.color_fondo = "#f8f9fa"
        self.color_header = "#2c3e50"
        self.color_primario = "#0984e3"
        self.color_texto = "#2d3436"
        self.color_subtexto = "#636e72"
        self.color_borde = "#dfe6e9"
        self.color_exito = "#218c5a"

        self.title("Resumen de Sesión")
        self.geometry("500x660")
        self.resizable(False, False)
        self.configure(fg_color=self.color_fondo)

        self.transient(parent)
        self.grab_set()

        header = ctk.CTkFrame(
            self,
            fg_color=self.color_header,
            corner_radius=0
        )
        header.pack(fill="x")
        ctk.CTkLabel(
            header,
            text="RESUMEN DE CAJA",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        ).pack(anchor="w", padx=28, pady=(20, 2))
        ctk.CTkLabel(
            header,
            text="Detalle de la sesión actual",
            text_color="#cbd5e1",
            font=ctk.CTkFont(family="Segoe UI", size=12)
        ).pack(anchor="w", padx=28, pady=(0, 20))

        container = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color=self.color_borde
        )
        container.pack(fill="both", expand=True, padx=24, pady=(22, 16))

        info_top = ctk.CTkFrame(container, fg_color="transparent")
        info_top.pack(fill="x", padx=22, pady=(20, 16))
        info_top.grid_columnconfigure((0, 1), weight=1, uniform="session_info")

        date_info = ctk.CTkFrame(
            info_top, fg_color="#f4f7fa", corner_radius=8
        )
        date_info.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        user_info = ctk.CTkFrame(
            info_top, fg_color="#f4f7fa", corner_radius=8
        )
        user_info.grid(row=0, column=1, sticky="ew", padx=(6, 0))
        ctk.CTkLabel(
            date_info,
            text="FECHA",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=self.color_subtexto
        ).pack(anchor="w", padx=12, pady=(9, 0))
        ctk.CTkLabel(
            date_info,
            text=str(self.caja.fecha),
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=self.color_texto
        ).pack(anchor="w", padx=12, pady=(2, 9))
        ctk.CTkLabel(
            user_info,
            text="USUARIO",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=self.color_subtexto
        ).pack(anchor="w", padx=12, pady=(9, 0))
        ctk.CTkLabel(
            user_info,
            text=str(self.caja.usuario),
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=self.color_texto
        ).pack(anchor="w", padx=12, pady=(2, 9))

        ctk.CTkLabel(
            container,
            text="MOVIMIENTOS DE LA SESIÓN",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=self.color_subtexto
        ).pack(anchor="w", padx=24, pady=(0, 8))

        def crear_fila(label, valor, color_valor=None):
            row = ctk.CTkFrame(container, fg_color="transparent")
            row.pack(fill="x", padx=24, pady=7)
            row.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                row,
                text=label,
                font=ctk.CTkFont(family="Segoe UI", size=13),
                text_color=self.color_texto
            ).grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(
                row,
                text=f"Q {valor:,.2f}",
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                text_color=color_valor or self.color_texto
            ).grid(row=0, column=1, sticky="e")

        crear_fila("Saldo Inicial:", self.caja.saldo_inicial)
        crear_fila("(+) Ingresos por ventas:", self.caja.ingresos_ventas, self.color_exito)
        crear_fila("(+) Otros ingresos:", self.caja.otros_ingresos, self.color_exito)
        crear_fila("(-) Egresos y gastos:", self.caja.egresos, "#d63031")

        saldo_final = ctk.CTkFrame(
            container,
            fg_color="#edf6ff",
            corner_radius=10,
            border_width=1,
            border_color="#d4e9fc"
        )
        saldo_final.pack(fill="x", padx=20, pady=(18, 20))
        ctk.CTkLabel(
            saldo_final,
            text="SALDO ESPERADO EN CAJA",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=self.color_primario
        ).pack(anchor="w", padx=16, pady=(13, 0))
        ctk.CTkLabel(
            saldo_final,
            text=f"Q {self.caja.saldo_final:,.2f}",
            font=ctk.CTkFont(family="Segoe UI", size=25, weight="bold"),
            text_color=self.color_primario
        ).pack(anchor="w", padx=16, pady=(0, 13))

        self.btn_cerrar = ctk.CTkButton(
            self,
            text="Cerrar resumen",
            fg_color=self.color_primario,
            hover_color="#0873c4",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=44,
            corner_radius=9,
            command=self.destroy
        )
        self.btn_cerrar.pack(fill="x", padx=48, pady=(0, 22))
        self.after(100, self.btn_cerrar.focus_set)
