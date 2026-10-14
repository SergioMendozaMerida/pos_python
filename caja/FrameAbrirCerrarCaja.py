import customtkinter as ctk
from tkinter import messagebox


class FrameAbrirCaja(ctk.CTkToplevel):
    def __init__(self, parent, caja, actualizar_caja_callback, show_productos):
        super().__init__(parent)
        self.caja = caja
        self.actualizar_caja_callback = actualizar_caja_callback
        self.show_productos = show_productos

        # Configuración de Colores y Estilos
        self.color_fondo = "#f4f6f9"
        self.color_header = "#2c3e50"
        self.color_primario = "#0984e3"
        self.color_exito = "#00b894"
        self.color_neutral = "#636e72"
        self.color_texto = "#2d3436"

        self.title("Abrir Caja")
        self.geometry("460x420")
        self.resizable(False, False)
        self.configure(fg_color=self.color_fondo)

        # Modalidad
        self.transient(parent)
        self.grab_set()

        # Header
        header = ctk.CTkFrame(self, fg_color=self.color_header, height=82, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header,
            text="Apertura de Caja",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=19, weight="bold")
        ).pack(pady=(13, 0))
        ctk.CTkLabel(
            header,
            text="Inicia una nueva jornada de ventas",
            text_color="#dfe6e9",
            font=ctk.CTkFont(family="Segoe UI", size=12)
        ).pack(pady=(2, 12))

        # Contenido
        container = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color="#dfe6e9"
        )
        container.pack(fill="both", expand=True, padx=24, pady=22)

        ctk.CTkLabel(
            container,
            text="Monto inicial en caja (Q):",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_texto
        ).pack(anchor="w", padx=30, pady=(26, 8))

        self.entry_saldo_inicial = ctk.CTkEntry(
            container,
            font=ctk.CTkFont(family="Segoe UI", size=14),
            justify="center",
            border_color=self.color_primario,
            border_width=1,
            height=48
        )
        self.entry_saldo_inicial.pack(fill="x", padx=30, pady=(0, 24))
        self.entry_saldo_inicial.focus_set()
        self.entry_saldo_inicial.bind("<Return>", lambda e: self.abrir_caja())

        # Botones
        btn_style = {
            "font": ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            "text_color": "white",
            "height": 46,
            "corner_radius": 10,
            "cursor": "hand2"
        }

        self.btn_abrir = ctk.CTkButton(
            container,
            text="✓ Confirmar Apertura",
            fg_color=self.color_exito,
            hover_color="#009f7f",
            command=self.abrir_caja,
            **btn_style
        )
        self.btn_abrir.pack(fill="x", padx=30, pady=(0, 12))

        self.btn_cancelar = ctk.CTkButton(
            container,
            text="✕ Cancelar",
            fg_color=self.color_neutral,
            hover_color="#4d585c",
            command=self.destroy,
            **btn_style
        )
        self.btn_cancelar.pack(fill="x", padx=30, pady=(0, 26))

        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def abrir_caja(self):
        try:
            saldo_inicial = float(self.entry_saldo_inicial.get())
            self.caja.abrir_caja(saldo_inicial)
            self.actualizar_caja_callback()
            self.show_productos(cantidad=10)
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto numérico válido para el saldo inicial.")


class FrameCerrarCaja(ctk.CTkToplevel):
    def __init__(self, parent, caja, actualizar_caja_callback, show_productos):
        super().__init__(parent)
        self.parent = parent
        self.caja = caja
        self.actualizar_caja_callback = actualizar_caja_callback
        self.show_productos = show_productos

        self.color_fondo = "#f4f6f9"
        self.color_header = "#2c3e50"
        self.color_primario = "#0984e3"
        self.color_error = "#d63031"
        self.color_neutral = "#636e72"

        self.title("Cerrar Caja")
        self.geometry("460x420")
        self.resizable(False, False)
        self.configure(fg_color=self.color_fondo)

        self.transient(parent)
        self.grab_set()

        header = ctk.CTkFrame(self, fg_color=self.color_header, height=82, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header,
            text="Cierre de Caja",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=19, weight="bold")
        ).pack(pady=(13, 0))
        ctk.CTkLabel(
            header,
            text="Registra el efectivo al finalizar la jornada",
            text_color="#dfe6e9",
            font=ctk.CTkFont(family="Segoe UI", size=12)
        ).pack(pady=(2, 12))

        container = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color="#dfe6e9"
        )
        container.pack(fill="both", expand=True, padx=24, pady=22)

        ctk.CTkLabel(
            container,
            text="Efectivo real en caja (Q):",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_header
        ).pack(anchor="w", padx=30, pady=(26, 8))

        self.entry_monto_final = ctk.CTkEntry(
            container,
            font=ctk.CTkFont(family="Segoe UI", size=14),
            justify="center",
            border_color=self.color_primario,
            border_width=1,
            height=48
        )
        self.entry_monto_final.pack(fill="x", padx=30, pady=(0, 24))
        self.entry_monto_final.focus_set()
        self.entry_monto_final.bind("<Return>", lambda e: self.cerrar_caja())

        btn_style = {
            "font": ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            "text_color": "white",
            "height": 46,
            "corner_radius": 10,
            "cursor": "hand2"
        }

        self.btn_cerrar = ctk.CTkButton(
            container,
            text="🔒 Finalizar Jornada",
            fg_color=self.color_error,
            hover_color="#b92527",
            command=self.cerrar_caja,
            **btn_style
        )
        self.btn_cerrar.pack(fill="x", padx=30, pady=(0, 12))

        self.btn_cancelar = ctk.CTkButton(
            container,
            text="Cancelar",
            fg_color=self.color_neutral,
            hover_color="#4d585c",
            command=self.destroy,
            **btn_style
        )
        self.btn_cancelar.pack(fill="x", padx=30, pady=(0, 26))

        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

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
            self.show_productos(cantidad=10)  # Mostrar solo los primeros 10 productos después del cierre
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto numérico válido para el cierre.")
