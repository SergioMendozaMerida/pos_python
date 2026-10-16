from tkinter import messagebox

import customtkinter as ctk

import categoria.Categoria as Ct


class FrameCategoria(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Categorías")
        window_width = 750
        window_height = 550
        x = max(0, (self.winfo_screenwidth() - window_width) // 2)
        y = max(0, (self.winfo_screenheight() - window_height) // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)

        self.color_fondo = "#f8f9fa"
        self.color_header = "#2c3e50"
        self.color_primario = "#0984e3"
        self.color_exito = "#00b894"
        self.color_cancelar = "#d63031"
        self.color_texto = "#2d3436"
        self.color_subtexto = "#636e72"
        self.color_borde = "#dfe6e9"

        self.configure(fg_color=self.color_fondo)
        self.transient(parent)
        self.grab_set()

        self.categorias = Ct.Categorias()
        self.lista_categorias = self.categorias.obtener_categorias()
        self.categoria_seleccionada_id = None

        self.header_frame = ctk.CTkFrame(
            self,
            fg_color=self.color_header,
            height=60,
            corner_radius=0,
        )
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)

        ctk.CTkLabel(
            self.header_frame,
            text="Administración de Categorías",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="white",
        ).pack(pady=15)

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(
            fill="both", expand=True, padx=20, pady=(20, 12)
        )

        self.frame_categoria = ctk.CTkFrame(
            self.main_container,
            fg_color="white",
            corner_radius=10,
            border_width=1,
            border_color=self.color_borde,
        )
        self.frame_categoria.pack(
            side="left", fill="both", expand=True, padx=(0, 10)
        )

        ctk.CTkLabel(
            self.frame_categoria,
            text="Categorías Existentes",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=self.color_texto,
        ).pack(anchor="w", padx=15, pady=(14, 8))

        self.lista_visual_categorias = ctk.CTkScrollableFrame(
            self.frame_categoria,
            fg_color="transparent",
            corner_radius=0,
        )
        self.lista_visual_categorias.pack(
            fill="both", expand=True, padx=10, pady=(0, 8)
        )

        ctk.CTkButton(
            self.frame_categoria,
            text="🗑️ Eliminar Seleccionada",
            fg_color=self.color_cancelar,
            hover_color="#b92525",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            height=38,
            command=self.eliminar_categoria,
        ).pack(fill="x", padx=12, pady=(0, 12))

        self.frame_formulario = ctk.CTkFrame(
            self.main_container,
            fg_color="white",
            corner_radius=10,
            border_width=1,
            border_color=self.color_borde,
        )
        self.frame_formulario.pack(
            side="right", fill="both", expand=True
        )

        ctk.CTkLabel(
            self.frame_formulario,
            text="Agregar Nueva Categoría",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=self.color_texto,
        ).pack(anchor="w", padx=15, pady=(14, 24))

        ctk.CTkLabel(
            self.frame_formulario,
            text="Nombre de la Categoría:",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=self.color_texto,
        ).pack(anchor="w", padx=15, pady=(0, 6))

        self.entry_nombre_categoria = ctk.CTkEntry(
            self.frame_formulario,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=38,
            corner_radius=6,
            border_width=1,
            border_color=self.color_borde,
            fg_color="white",
            text_color=self.color_texto,
        )
        self.entry_nombre_categoria.pack(fill="x", padx=15)
        self.entry_nombre_categoria.bind(
            "<Return>", lambda event: self.guardar_categoria()
        )

        ctk.CTkButton(
            self.frame_formulario,
            text="✓ Guardar Categoría",
            fg_color=self.color_exito,
            hover_color="#009f7f",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            height=40,
            command=self.guardar_categoria,
        ).pack(fill="x", padx=15, pady=(12, 0))

        ctk.CTkButton(
            self,
            text="✕ Cerrar Ventana",
            fg_color=self.color_subtexto,
            hover_color="#4f5b60",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            height=36,
            command=self.destroy,
        ).pack(pady=(0, 14))

        self.dibuajar_categorias()
        self.entry_nombre_categoria.focus_set()

    def dibuajar_categorias(self):
        for widget in self.lista_visual_categorias.winfo_children():
            widget.destroy()

        if not self.lista_categorias:
            ctk.CTkLabel(
                self.lista_visual_categorias,
                text="No hay categorías registradas.",
                font=ctk.CTkFont(family="Segoe UI", size=11),
                text_color=self.color_subtexto,
            ).pack(anchor="w", padx=8, pady=8)
            return

        for indice, categoria in enumerate(self.lista_categorias, start=1):
            seleccionada = (
                categoria.id_categoria == self.categoria_seleccionada_id
            )
            ctk.CTkButton(
                self.lista_visual_categorias,
                text=f"{indice}.  {categoria.nombre_categoria}",
                anchor="w",
                fg_color="#eaf4fd" if seleccionada else "transparent",
                hover_color="#eaf4fd",
                text_color=self.color_primario if seleccionada else self.color_texto,
                font=ctk.CTkFont(family="Segoe UI", size=11),
                height=36,
                command=lambda categoria_id=categoria.id_categoria: (
                    self.seleccionar_categoria(categoria_id)
                ),
            ).pack(fill="x", pady=2)

    def seleccionar_categoria(self, categoria_id):
        self.categoria_seleccionada_id = categoria_id
        self.dibuajar_categorias()

    def guardar_categoria(self):
        nombre_categoria = self.entry_nombre_categoria.get().strip()
        if not nombre_categoria:
            messagebox.showwarning(
                "Validación",
                "Ingrese el nombre de la categoría.",
                parent=self,
            )
            self.entry_nombre_categoria.focus_set()
            return

        categoria = Ct.Categoria()
        categoria.registrar_nueva_categoria(nombre_categoria)
        self.lista_categorias = self.categorias.obtener_categorias()
        self.categoria_seleccionada_id = None
        self.dibuajar_categorias()
        self.entry_nombre_categoria.delete(0, "end")
        self.entry_nombre_categoria.focus_set()

    def eliminar_categoria(self):
        if self.categoria_seleccionada_id is None:
            messagebox.showwarning(
                "Advertencia",
                "Seleccione una categoría para eliminar.",
                parent=self,
            )
            return

        confirmacion = messagebox.askyesno(
            "Eliminar",
            "¿Está seguro de eliminar la categoría?",
            parent=self,
        )
        if not confirmacion:
            return

        categoria = Ct.Categoria()
        categoria.eliminar_categoria(self.categoria_seleccionada_id)
        self.lista_categorias = self.categorias.obtener_categorias()
        self.categoria_seleccionada_id = None
        self.dibuajar_categorias()
