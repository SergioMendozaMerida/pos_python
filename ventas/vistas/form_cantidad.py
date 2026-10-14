from tkinter import messagebox

import customtkinter as ctk

class FormCantidad(ctk.CTkToplevel):
    def __init__(self, parent, producto, agregar_cantidad):
        super().__init__(parent)
        self.title("Cantidad de Producto")
        self.geometry("360x235")
        self.resizable(False, False)

        self.cantidad = 1
        self.agregar_cantidad = agregar_cantidad
        self.producto = producto

        self.color_fondo = "#f4f6f9"
        self.color_header = "#2c3e50"
        self.color_primario = "#0984e3"
        self.color_exito = "#00b894"
        self.color_neutral = "#636e72"
        self.color_texto = "#2d3436"
        self.color_borde = "#dfe6e9"
        self.configure(fg_color=self.color_fondo)

        self.transient(parent)
        self.grab_set()

        header = ctk.CTkFrame(
            self,
            fg_color=self.color_header,
            height=68,
            corner_radius=0
        )
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header,
            text="Cantidad del producto",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        ).pack(pady=(7, 0))
        ctk.CTkLabel(
            header,
            text="Indica cuántas unidades deseas agregar",
            text_color="#dfe6e9",
            font=ctk.CTkFont(family="Segoe UI", size=11)
        ).pack(pady=(0, 7))

        card = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color=self.color_borde
        )
        card.pack(fill="both", expand=True, padx=16, pady=12)

        ctk.CTkLabel(
            card,
            text="Unidades a vender",
            text_color=self.color_texto,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        ).pack(anchor="w", padx=16, pady=(10, 4))

        self.entry_cantidad = ctk.CTkEntry(
            card,
            placeholder_text="Ingrese la cantidad",
            font=ctk.CTkFont(family="Segoe UI", size=16),
            height=38,
            corner_radius=8,
            border_width=1,
            border_color=self.color_primario,
            justify="center"
        )
        self.entry_cantidad.pack(padx=16, fill="x")
        self.entry_cantidad.set(1)
        self.entry_cantidad.bind("<Return>", lambda event: self.aceptar())

        botones = ctk.CTkFrame(card, fg_color="transparent")
        botones.pack(fill="x", padx=16, pady=(12, 12))

        self.btn_aceptar = ctk.CTkButton(
            botones,
            text="Aceptar",
            command=self.aceptar,
            fg_color=self.color_exito,
            hover_color="#009f7f",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=38,
            corner_radius=9
        )
        self.btn_aceptar.pack(side="left", expand=True, fill="x", padx=(0, 6))

        self.btn_cancelar = ctk.CTkButton(
            botones,
            text="Cancelar",
            command=self.cancelar,
            fg_color=self.color_neutral,
            hover_color="#4d585c",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=38,
            corner_radius=9
        )
        self.btn_cancelar.pack(side="left", expand=True, fill="x", padx=(6, 0))

        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.after(100, self.enfocar_entry_cantidad)

    def enfocar_entry_cantidad(self):
        self.entry_cantidad.focus_set()
        self.entry_cantidad.select_range(0, "end")

    def aceptar(self):
        cantidad = self.entry_cantidad.get()

        try:
            cantidad = float(cantidad)

            if cantidad <= 0:
                messagebox.showerror('Error', 'Ingrese una cantidad valida.')
            else:
                self.agregar_cantidad(self.producto, cantidad)
                self.destroy()
        except Exception as e:
            messagebox.showerror('Error', 'Ingrese una cantidad valida.')
            return False

    def cancelar(self):
        self.destroy()