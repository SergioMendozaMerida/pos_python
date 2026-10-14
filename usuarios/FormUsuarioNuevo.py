from tkinter import messagebox

import customtkinter as ctk


class FormUsuarioNuevo(ctk.CTkToplevel):
    def __init__(self, parent, crear_usuario, actualizar_tabla):
        super().__init__(parent)
        self.crear_usuario = crear_usuario
        self.actualizar_tabla = actualizar_tabla

        self.color_fondo = "#f4f6f9"
        self.color_header = "#2c3e50"
        self.color_texto = "#2d3436"
        self.color_borde = "#dfe6e9"
        self.color_primario = "#00b894"

        self.title("Crear nuevo usuario")
        self.geometry("460x600")
        self.resizable(False, False)
        self.configure(fg_color=self.color_fondo)
        self.transient(parent)
        self.grab_set()

        header = ctk.CTkFrame(self, fg_color=self.color_header, height=76, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header,
            text="Nuevo usuario",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        ).pack(pady=(13, 2))
        ctk.CTkLabel(
            header,
            text="Crea una cuenta y asigna sus permisos de acceso",
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
            text="Nombre completo",
            text_color=self.color_texto,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        ).pack(anchor="w", padx=18, pady=(16, 5))
        self.entry_nombre = self._crear_entry(card, "Nombre y apellidos")
        self.entry_nombre.pack(fill="x", padx=18)

        ctk.CTkLabel(
            card,
            text="DPI",
            text_color=self.color_texto,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        ).pack(anchor="w", padx=18, pady=(12, 5))
        self.entry_dpi = self._crear_entry(card, "Número de DPI")
        self.entry_dpi.pack(fill="x", padx=18)

        ctk.CTkLabel(
            card,
            text="Usuario de acceso",
            text_color=self.color_texto,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        ).pack(anchor="w", padx=18, pady=(12, 5))
        self.entry_usuario = self._crear_entry(card, "Nombre de usuario")
        self.entry_usuario.pack(fill="x", padx=18)

        ctk.CTkLabel(
            card,
            text="Contraseña",
            text_color=self.color_texto,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        ).pack(anchor="w", padx=18, pady=(12, 5))
        self.entry_contrasenia = self._crear_entry(card, "Mínimo 6 caracteres", show="●")
        self.entry_contrasenia.pack(fill="x", padx=18)

        ctk.CTkLabel(
            card,
            text="Rol / permisos",
            text_color=self.color_texto,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        ).pack(anchor="w", padx=18, pady=(12, 5))
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
        self.combo_rol.set("vendedor")
        self.combo_rol.pack(fill="x", padx=18)

        buttons = ctk.CTkFrame(card, fg_color="transparent")
        buttons.pack(fill="x", padx=18, pady=(16, 16))

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

        self.btn_crear = ctk.CTkButton(
            buttons,
            text="Crear usuario",
            command=self.validar_y_crear,
            fg_color=self.color_primario,
            hover_color="#009476",
            height=40,
            corner_radius=9,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        self.btn_crear.pack(side="right")

    def _crear_entry(self, parent, placeholder, show=None):
        return ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            show=show,
            height=40,
            corner_radius=8,
            border_color=self.color_borde,
            font=ctk.CTkFont(family="Segoe UI", size=13)
        )

    def validar_y_crear(self):
        nombre = self.entry_nombre.get().strip()
        usuario = self.entry_usuario.get().strip()
        contrasenia = self.entry_contrasenia.get().strip()
        rol = self.combo_rol.get()
        dpi = self.entry_dpi.get().strip()

        if not nombre or not dpi or not usuario or not contrasenia or not rol:
            messagebox.showwarning(
                "Atención",
                "Todos los campos son obligatorios.",
                parent=self
            )
            return

        if len(contrasenia) < 6:
            messagebox.showwarning(
                "Atención",
                "La contraseña debe tener al menos 6 caracteres.",
                parent=self
            )
            return

        self.crear_usuario(nombre, usuario, contrasenia, rol, dpi)
        self.actualizar_tabla()
        self.destroy()
