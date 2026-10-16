from tkinter import messagebox

import customtkinter as ctk

import categoria.Categoria as cat


class FormAddCategoria(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Agregar Categoría")
        window_width = 420
        window_height = 250
        x = max(0, (self.winfo_screenwidth() - window_width) // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+20")
        self.resizable(False, False)

        self.categoria = cat.Categoria()

        self.color_fondo = "#f8f9fa"
        self.color_header = "#2c3e50"
        self.color_primario = "#0984e3"
        self.color_exito = "#00b894"
        self.color_cancelar = "#d63031"
        self.color_entrada = "#ffffff"
        self.color_texto = "#2d3436"
        self.color_borde = "#dfe6e9"

        self.configure(fg_color=self.color_fondo)
        self.transient(parent)
        self.grab_set()

        header_frame = ctk.CTkFrame(
            self,
            fg_color=self.color_header,
            height=50,
            corner_radius=0,
        )
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        ctk.CTkLabel(
            header_frame,
            text="Agregar nueva categoría",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="white",
        ).pack(pady=12)

        body_frame = ctk.CTkFrame(self, fg_color="transparent")
        body_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            body_frame,
            text="Nombre de categoría:",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=self.color_texto,
        ).pack(anchor="w", pady=(0, 8))

        self.entry_nombre_categoria = ctk.CTkEntry(
            body_frame,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=38,
            corner_radius=6,
            border_width=1,
            border_color=self.color_borde,
            fg_color=self.color_entrada,
            text_color=self.color_texto,
        )
        self.entry_nombre_categoria.pack(fill="x")
        self.entry_nombre_categoria.bind(
            "<Return>", lambda event: self.guardar_categoria()
        )

        botones_frame = ctk.CTkFrame(body_frame, fg_color="transparent")
        botones_frame.pack(fill="x", pady=(16, 0))

        btn_guardar = ctk.CTkButton(
            botones_frame,
            text="✓ Guardar",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            fg_color=self.color_exito,
            hover_color="#009f7f",
            text_color="white",
            height=38,
            command=self.guardar_categoria,
        )
        btn_guardar.pack(side="left", fill="x", expand=True, padx=(0, 8))

        btn_cancelar = ctk.CTkButton(
            botones_frame,
            text="✕ Cancelar",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            fg_color=self.color_cancelar,
            hover_color="#b92525",
            text_color="white",
            height=38,
            command=self.destroy,
        )
        btn_cancelar.pack(side="left", fill="x", expand=True)

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.after(0, self.entry_nombre_categoria.focus_set)

    def guardar_categoria(self):
        nombre_categoria = self.entry_nombre_categoria.get().strip()
        if not nombre_categoria:
            messagebox.showwarning(
                "Validación",
                "Debe ingresar el nombre de la categoría.",
                parent=self,
            )
            self.entry_nombre_categoria.focus_set()
            return

        self.categoria.registrar_nueva_categoria(nombre_categoria)
        self.destroy()
