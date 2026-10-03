import customtkinter as ctk
from assets.icons.AnabellIcons import AnabellIcons

class TablaSesionesCaja(ctk.CTkFrame):
    def __init__(self, parent, sesiones_caja):
        super().__init__(parent, fg_color="transparent")
        self.sesiones_caja = sesiones_caja
        self.encabezados_columnas = [
            "Fecha", "Usuario", "Saldo inicial", "Ventas", "Gastos",
            "Saldo final", "Cierre", "Diferencia", "Estado"
        ]
        self.alineaciones_columnas = ("w", "w", "e", "e", "e", "e", "e", "e", "center")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.create_widgets()

    def create_widgets(self):
        self.frame_encabezados = ctk.CTkFrame(
            self,
            fg_color="#eaf0f5",
            corner_radius=6
        )
        self.frame_encabezados.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        for column_index, encabezado in enumerate(self.encabezados_columnas):
            self.frame_encabezados.grid_columnconfigure(column_index, weight=1, uniform="columnas")
            ctk.CTkLabel(
                self.frame_encabezados,
                text=encabezado,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color="#34495e",
                anchor=self.alineaciones_columnas[column_index]
            ).grid(row=0, column=column_index, sticky="ew", padx=9, pady=11)

        self.frame_filas = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )
        self.frame_filas.grid(row=1, column=0, sticky="nsew")
        self.frame_filas.grid_columnconfigure(0, weight=1)
        self.actualizar(self.sesiones_caja)

    def actualizar(self, sesiones_caja):
        self.sesiones_caja = sesiones_caja
        for widget in self.frame_filas.winfo_children():
            widget.destroy()

        if not self.sesiones_caja:
            ctk.CTkLabel(
                self.frame_filas,
                text="No hay sesiones para mostrar",
                font=ctk.CTkFont(family="Segoe UI", size=13),
                text_color="#636e72"
            ).grid(row=0, column=0, sticky="ew", pady=28)
            return

        for row_index, sesion in enumerate(self.sesiones_caja):
            color_fila = "#ffffff" if row_index % 2 == 0 else "#f6f8fa"
            frame_fila = ctk.CTkFrame(
                self.frame_filas,
                fg_color=color_fila,
                corner_radius=5,
                border_width=1,
                border_color="#edf0f2"
            )
            frame_fila.grid(row=row_index, column=0, sticky="ew", pady=2)

            for column_index in range(len(self.encabezados_columnas)):
                frame_fila.grid_columnconfigure(column_index, weight=1, uniform="columnas")

            valores = (
                str(sesion.fecha),
                str(sesion.usuario),
                f"Q {float(sesion.saldo_inicial or 0):,.2f}",
                f"Q {float(sesion.ingresos_ventas or 0):,.2f}",
                f"Q {float(sesion.egresos or 0):,.2f}",
                f"Q {float(sesion.saldo_final or 0):,.2f}",
                f"Q {float(sesion.efectivo_final or 0):,.2f}",
                f"Q {float(sesion.diferencia or 0):,.2f}",
                "Abierta" if sesion.estado else "Cerrada"
            )

            for column_index, (valor, alineacion) in enumerate(zip(valores, self.alineaciones_columnas)):
                if column_index == 8:
                    icono_estado = AnabellIcons.obtener_imagen("lock_open_black") if sesion.estado else AnabellIcons.obtener_imagen("lock")
                    color_estado = "#00ff80" if sesion.estado else "#fc0707"
                    texto_estado = "#000000" if sesion.estado else "#ffffff"
                    frame_estado = ctk.CTkFrame(
                        frame_fila,
                        fg_color=color_estado,
                        corner_radius=4
                    )
                    frame_estado.grid(row=0, column=column_index, padx=9, pady=10)

                    ctk.CTkLabel(
                        frame_estado,
                        text="",
                        image=icono_estado,
                        fg_color="transparent"
                    ).grid(row=0, column=0, padx=(8, 0), pady=5)
                    ctk.CTkLabel(
                        frame_estado,
                        text=valor,
                        font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                        text_color=texto_estado,
                        fg_color="transparent"
                    ).grid(row=0, column=1, padx=(6, 8), pady=5)
                else:
                    etiqueta = ctk.CTkLabel(
                        frame_fila,
                        text=valor,
                        font=ctk.CTkFont(family="Segoe UI", size=11),
                        text_color="#2d3436",
                        anchor=alineacion
                    )
                    etiqueta.grid(row=0, column=column_index, sticky="ew", padx=9, pady=10)
