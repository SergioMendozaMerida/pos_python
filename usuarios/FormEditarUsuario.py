from tkinter import messagebox

import customtkinter as ctk


class FormEditarUsuario(ctk.CTkToplevel):
    def __init__(self, parent, usuario, editar_usuario, actualizar_tabla):
        super().__init__(parent)
        self.usuario = usuario
        self.editar_usuario = editar_usuario
        self.actualizar_tabla = actualizar_tabla

        self.color_fondo = "#f4f6f9"
        self.color_header = "#2c3e50"
        self.color_texto = "#2d3436"
        self.color_borde = "#dfe6e9"
        self.color_primario = "#0984e3"

        self.title("Editar usuario")
        self.geometry("460x550")
        self.resizable(False, False)
        self.configure(fg_color=self.color_fondo)
        self.transient(parent)
        self.grab_set()

        header = ctk.CTkFrame(self, fg_color=self.color_header, height=76, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header,
            text="Editar información",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        ).pack(pady=(13, 2))
        ctk.CTkLabel(
            header,
            text="Actualiza los datos, permisos y estado de esta cuenta",
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
        ).pack(anchor="w", padx=18, pady=(20, 7))

        self.entry_nombre = ctk.CTkEntry(
            card,
            placeholder_text="Escribe el nombre completo",
            height=40,
            corner_radius=8,
            border_color=self.color_borde,
            font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.entry_nombre.pack(fill="x", padx=18)
        self.entry_nombre.insert(0, self.usuario.nombre)

        ctk.CTkLabel(
            card,
            text="DPI",
            text_color=self.color_texto,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        ).pack(anchor="w", padx=18, pady=(14, 7))

        self.entry_dpi = ctk.CTkEntry(
            card,
            placeholder_text="Escribe el DPI",
            height=40,
            corner_radius=8,
            border_color=self.color_borde,
            font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.entry_dpi.pack(fill="x", padx=18)
        self.entry_dpi.insert(0, str(self.usuario.dpi or ""))

        ctk.CTkLabel(
            card,
            text="Rol / permisos",
            text_color=self.color_texto,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        ).pack(anchor="w", padx=18, pady=(14, 7))

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

        ctk.CTkLabel(
            card,
            text="Contraseña (opcional)",
            text_color=self.color_texto,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        ).pack(anchor="w", padx=18, pady=(14, 7))

        self.entry_contrasenia = ctk.CTkEntry(
            card,
            placeholder_text="Déjalo vacío para conservar la contraseña actual",
            show="●",
            height=40,
            corner_radius=8,
            border_color=self.color_borde,
            font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.entry_contrasenia.pack(fill="x", padx=18)

        ctk.CTkLabel(
            card,
            text="Estado",
            text_color=self.color_texto,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        ).pack(anchor="w", padx=18, pady=(14, 7))

        self.combo_estado = ctk.CTkComboBox(
            card,
            values=["Activo", "Inactivo"],
            state="readonly",
            height=40,
            corner_radius=8,
            border_color=self.color_borde,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            dropdown_font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.combo_estado.set("Activo" if int(self.usuario.activo) == 1 else "Inactivo")
        self.combo_estado.pack(fill="x", padx=18)

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

        self.btn_guardar = ctk.CTkButton(
            buttons,
            text="Guardar cambios",
            command=self.validar_y_guardar,
            fg_color=self.color_primario,
            hover_color="#076dbb",
            height=40,
            corner_radius=9,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        self.btn_guardar.pack(side="right")

        self._centrar(parent)
        self.after(100, self.entry_nombre.focus_set)

    def _centrar(self, parent):
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = parent.winfo_rootx() + (parent.winfo_width() - ancho) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{max(0, x)}+{max(0, y-120)}")

    def validar_y_guardar(self):
        nombre = self.entry_nombre.get().strip()
        dpi = self.entry_dpi.get().strip()
        rol = self.combo_rol.get()
        contrasenia = self.entry_contrasenia.get().strip()
        estado = 1 if self.combo_estado.get() == "Activo" else 0
        if not nombre:
            messagebox.showwarning(
                "Campos requeridos",
                "Por favor, escriba el nombre completo.",
                parent=self
            )
            return

        if contrasenia and len(contrasenia) < 6:
            messagebox.showwarning(
                "Atención",
                "La contraseña debe tener al menos 6 caracteres.",
                parent=self
            )
            return

        self.editar_usuario(
            nombre,
            dpi,
            rol,
            contrasenia,
            estado,
            self.usuario.id_usuario
        )
        self.actualizar_tabla()
        self.destroy()
