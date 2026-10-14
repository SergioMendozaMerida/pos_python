from tkinter import messagebox

import customtkinter as ctk


class FrameContrasenia(ctk.CTkToplevel):
    def __init__(self, parent, usuario, reestablecer_callback):
        super().__init__(parent)
        self.usuario = usuario
        self.reestablecer_callback = reestablecer_callback

        self.color_fondo = "#f4f6f9"
        self.color_header = "#2c3e50"
        self.color_texto = "#2d3436"
        self.color_subtexto = "#636e72"
        self.color_primario = "#6c5ce7"
        self.color_borde = "#dfe6e9"

        self.title(f"Seguridad: {self.usuario.nombre}")
        self.geometry("460x365")
        self.resizable(False, False)
        self.configure(fg_color=self.color_fondo)
        self.transient(parent)
        self.grab_set()

        header = ctk.CTkFrame(self, fg_color=self.color_header, height=76, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header,
            text="Cambiar contraseña",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        ).pack(pady=(13, 2))
        ctk.CTkLabel(
            header,
            text="Define una nueva clave de acceso para esta cuenta",
            text_color="#dfe6e9",
            font=ctk.CTkFont(family="Segoe UI", size=11)
        ).pack()

        card = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color=self.color_borde
        )
        card.pack(fill="both", expand=True, padx=18, pady=16)

        ctk.CTkLabel(
            card,
            text=f"Usuario: {self.usuario.usuario}",
            text_color=self.color_subtexto,
            font=ctk.CTkFont(family="Segoe UI", size=12)
        ).pack(anchor="w", padx=18, pady=(18, 16))

        ctk.CTkLabel(
            card,
            text="Nueva contraseña",
            text_color=self.color_texto,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        ).pack(anchor="w", padx=18, pady=(0, 6))

        self.entry_contrasenia = ctk.CTkEntry(
            card,
            placeholder_text="Mínimo 6 caracteres",
            show="●",
            height=40,
            corner_radius=8,
            border_color=self.color_borde,
            font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.entry_contrasenia.pack(fill="x", padx=18)
        buttons = ctk.CTkFrame(card, fg_color="transparent")
        buttons.pack(fill="x", padx=18, pady=(20, 18))

        self.btn_cancelar = ctk.CTkButton(
            buttons,
            text="Cancelar",
            command=self.destroy,
            fg_color="#636e72",
            hover_color="#4d585c",
            height=40,
            corner_radius=9,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        self.btn_cancelar.pack(side="right", padx=(8, 0))

        self.btn_guardar = ctk.CTkButton(
            buttons,
            text="Actualizar contraseña",
            command=self.validar_y_guardar,
            fg_color=self.color_primario,
            hover_color="#574b90",
            height=40,
            corner_radius=9,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        self.btn_guardar.pack(side="right")

        self._centrar(parent)
        self.after(100, self.entry_contrasenia.focus_set)

    def _centrar(self, parent):
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = parent.winfo_rootx() + (parent.winfo_width() - ancho) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{max(0, x)}+{max(0, y)}")

    def validar_y_guardar(self):
        nueva = self.entry_contrasenia.get().strip()
        if not nueva or len(nueva) < 6:
            messagebox.showwarning(
                "Atención",
                "La contraseña debe tener al menos 6 caracteres.",
                parent=self
            )
            return

        self.reestablecer_callback(self.usuario.id_usuario, nueva)
        self.destroy()
