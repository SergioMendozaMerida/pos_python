from tkinter import messagebox
import customtkinter as ctk
import datetime
import egresos.Egresos as E


class FormRegistrarEgreso(ctk.CTkToplevel):
    def __init__(self, parent, caja, actualizarEgresos=None):
        super().__init__(parent)
        self.title("Registrar Egreso")
        self.geometry("480x570")
        self.resizable(False, False)
        self.parent = parent
        self.actualizarEgresos = actualizarEgresos
        self.caja = caja

        self.configure(fg_color="#f4f6f9")

        # Estilos y colores
        self.primary_color = "#0984e3"
        self.success_color = "#00b894"
        self.neutral_color = "#636e72"
        self.header_color = "#2c3e50"
        self.text_color = "#2d3436"
        self.border_color = "#dfe6e9"

        self.transient(parent)
        self.grab_set()

        header = ctk.CTkFrame(
            self,
            fg_color=self.header_color,
            height=96,
            corner_radius=0
        )
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header,
            text="Registrar egreso",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="white"
        ).pack(pady=(17, 0))
        ctk.CTkLabel(
            header,
            text="Registra un gasto de la jornada de caja",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#dfe6e9"
        ).pack(pady=(2, 12))

        container = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color=self.border_color
        )
        container.pack(padx=26, pady=24, fill="both", expand=True)

        estilo_etiqueta = ctk.CTkFont(
            family="Segoe UI",
            size=13,
            weight="bold"
        )
        estilo_entrada = {
            "font": ctk.CTkFont(family="Segoe UI", size=13),
            "height": 44,
            "corner_radius": 8,
            "border_width": 1,
            "border_color": self.border_color,
            "fg_color": "white",
            "text_color": self.text_color
        }

        form = ctk.CTkFrame(container, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=30, pady=(28, 20))

        ctk.CTkLabel(
            form,
            text="Razón o concepto",
            font=estilo_etiqueta,
            text_color=self.text_color
        ).pack(anchor="w")
        self.entry_razon = ctk.CTkEntry(form, **estilo_entrada)
        self.entry_razon.pack(fill="x", pady=(7, 20))

        ctk.CTkLabel(
            form,
            text="Proveedor (opcional)",
            font=estilo_etiqueta,
            text_color=self.text_color
        ).pack(anchor="w")
        self.entry_proveedor = ctk.CTkEntry(form, **estilo_entrada)
        self.entry_proveedor.pack(fill="x", pady=(7, 20))

        ctk.CTkLabel(
            form,
            text="Monto (Q)",
            font=estilo_etiqueta,
            text_color=self.text_color
        ).pack(anchor="w")
        self.entry_monto = ctk.CTkEntry(form, **estilo_entrada)
        self.entry_monto.pack(fill="x", pady=(7, 28))

        for entry in (
            self.entry_razon,
            self.entry_proveedor,
            self.entry_monto
        ):
            entry.bind("<Return>", lambda event: self.registrar())

        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.pack(fill="x")
        ctk.CTkButton(
            btn_frame,
            text="Registrar egreso",
            fg_color=self.success_color,
            hover_color="#009f7f",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=self.registrar,
            cursor="hand2",
            height=46,
            corner_radius=10
        ).pack(side="left", expand=True, fill="x", padx=(0, 8))

        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color=self.neutral_color,
            hover_color="#4d585c",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=self.destroy,
            cursor="hand2",
            height=46,
            corner_radius=10
        ).pack(side="left", expand=True, fill="x", padx=(8, 0))

        self.entry_razon.focus_set()
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

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