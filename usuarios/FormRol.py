from tkinter import messagebox

import customtkinter as ctk


class FormRol(ctk.CTkToplevel):
    def __init__(self, parent, usuario, cambiar_rol_callback, actualizar_tabla):
        super().__init__(parent)
        self.usuario = usuario
        self.cambiar_rol_callback = cambiar_rol_callback
        self.actualizar_tabla = actualizar_tabla

        self.color_fondo = "#f4f6f9"
        self.color_header = "#2c3e50"
        self.color_texto = "#2d3436"
        self.color_subtexto = "#636e72"
        self.color_borde = "#dfe6e9"
        self.color_primario = "#e67e22"

        self.title(f"Permisos: {self.usuario.nombre}")
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
            text="Cambiar rol",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        ).pack(pady=(13, 2))
        ctk.CTkLabel(
            header,
            text="Administra los permisos de acceso del usuario",
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
            text="Rol / permisos",
            text_color=self.color_texto,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        ).pack(anchor="w", padx=18, pady=(0, 7))

        self.combo_rol = ctk.CTkComboBox(
            card,
            values=["vendedor", "admin"],
            state="readonly",
            height=40,
            corner_radius=8,
            border_color=self.color_borde,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            dropdown_font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.combo_rol.set(self.usuario.rol)
        self.combo_rol.pack(fill="x", padx=18)

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
            text="Actualizar rol",
            command=self.validar_y_guardar,
            fg_color=self.color_primario,
            hover_color="#cc6f16",
            text_color="white",
            height=40,
            corner_radius=9,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        self.btn_guardar.pack(side="right")

        self._centrar(parent)

    def _centrar(self, parent):
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = parent.winfo_rootx() + (parent.winfo_width() - ancho) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{max(0, x)}+{max(0, y)}")

    def validar_y_guardar(self):
        nuevo_rol = self.combo_rol.get()
        if not nuevo_rol:
            messagebox.showwarning(
                "Atención",
                "Seleccione un rol para el usuario.",
                parent=self
            )
            return

        self.cambiar_rol_callback(
            self.usuario.id_usuario,
            nuevo_rol,
            self.actualizar_tabla
        )
        self.destroy()
