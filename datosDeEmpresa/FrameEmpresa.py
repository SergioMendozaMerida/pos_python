import customtkinter as ctk


class FrameEmpresa(ctk.CTkFrame):
    def __init__(self, parent, empresa, usuario):
        super().__init__(parent, fg_color="#f4f6f9")

        self.empresa = empresa
        self.usuario = usuario
        self.color_primario = "#2c3e50"
        self.color_acento = "#0984e3"
        self.color_borde = "#dfe6e9"
        self.color_texto = "#2d3436"

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.container = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color=self.color_borde
        )
        self.container.grid(row=0, column=0, padx=30, pady=30)
        self.container.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.container,
            text="DATOS DE LA EMPRESA",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=self.color_primario
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=30, pady=(26, 22))

        self.campos_info = [
            ("Nombre Comercial:", "nombre"),
            ("Representante Legal:", "representante"),
            ("NIT:", "nit"),
            ("Teléfono:", "telefono"),
            ("Correo Electrónico:", "correo"),
            ("Dirección Física:", "direccion"),
            ("Eslogan:", "slogan"),
            ("Impresión (Carta/Ticket):", "impresion")
        ]

        self.vars = {}
        self.entries = {}

        for i, (label_text, attr) in enumerate(self.campos_info, start=1):
            valor_inicial = getattr(self.empresa, attr)
            if attr == "impresion":
                self.vars[attr] = ctk.StringVar(
                    value="Carta" if valor_inicial else "Ticket"
                )
            else:
                self.vars[attr] = ctk.StringVar(value=str(valor_inicial))

            ctk.CTkLabel(
                self.container,
                text=label_text,
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                text_color=self.color_texto
            ).grid(row=i, column=0, sticky="w", padx=(30, 18), pady=7)

            if attr == "impresion":
                widget = ctk.CTkComboBox(
                    self.container,
                    variable=self.vars[attr],
                    values=["Carta", "Ticket"],
                    state="disabled",
                    width=440,
                    height=36,
                    font=ctk.CTkFont(family="Segoe UI", size=12),
                    border_color=self.color_borde,
                    button_color=self.color_acento,
                    button_hover_color="#0873c4"
                )
            else:
                widget = ctk.CTkEntry(
                    self.container,
                    textvariable=self.vars[attr],
                    state="disabled",
                    width=440,
                    height=36,
                    font=ctk.CTkFont(family="Segoe UI", size=12),
                    border_color=self.color_borde,
                    text_color=self.color_texto
                )
            widget.grid(row=i, column=1, sticky="ew", padx=(0, 30), pady=7)
            self.entries[attr] = widget

        self.frame_btns = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_btns.grid(
            row=len(self.campos_info) + 1,
            column=0,
            columnspan=2,
            pady=(24, 26)
        )

        if self.usuario.rol == "admin":
            button_style = {
                "font": ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                "text_color": "white",
                "height": 40,
                "corner_radius": 8,
                "cursor": "hand2"
            }
            self.btn_editar = ctk.CTkButton(
                self.frame_btns,
                text="Editar datos",
                fg_color=self.color_acento,
                hover_color="#0873c4",
                command=self.habilitar_edicion,
                **button_style
            )
            self.btn_editar.pack(side="left", padx=8)

            self.btn_guardar = ctk.CTkButton(
                self.frame_btns,
                text="Guardar cambios",
                fg_color="#00a878",
                hover_color="#008f66",
                state="disabled",
                command=self.guardar_cambios,
                **button_style
            )
            self.btn_guardar.pack(side="left", padx=8)

    def habilitar_edicion(self):
        """Habilita los campos para escritura."""
        for attr, widget in self.entries.items():
            widget.configure(state="readonly" if attr == "impresion" else "normal")

        self.btn_editar.configure(state="disabled")
        self.btn_guardar.configure(state="normal")
        self.entries["nombre"].focus_set()

    def guardar_cambios(self):
        """Actualiza el objeto empresa y vuelve a bloquear los campos."""
        telefono = self.vars["telefono"].get()
        self.empresa.set_datos(
            self.vars["nombre"].get(),
            self.vars["representante"].get(),
            self.vars["nit"].get(),
            int(telefono) if telefono.isdigit() else 0,
            self.vars["correo"].get(),
            self.vars["direccion"].get(),
            self.vars["slogan"].get(),
            self.vars["impresion"].get() == "Carta"
        )

        for widget in self.entries.values():
            widget.configure(state="disabled")

        self.btn_editar.configure(state="normal")
        self.btn_guardar.configure(state="disabled")
