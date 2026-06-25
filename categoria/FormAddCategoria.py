import tkinter as tk
from tkinter import messagebox
import categoria.Categoria as cat

class FormAddCategoria(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Agregar Categoría")
        self.geometry("420x250")
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

        self.configure(bg=self.color_fondo)

        header_frame = tk.Frame(self, bg=self.color_header, height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="Agregar nueva categoría",
            font=("Segoe UI", 13, "bold"),
            bg=self.color_header,
            fg="white"
        ).pack(pady=12)

        body_frame = tk.Frame(self, bg=self.color_fondo)
        body_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            body_frame,
            text="Nombre de categoría:",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w", pady=(0, 8))

        self.entry_nombre_categoria = tk.Entry(
            body_frame,
            font=("Segoe UI", 11),
            bg=self.color_entrada,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=self.color_borde,
            highlightcolor=self.color_primario
        )
        self.entry_nombre_categoria.pack(fill="x", ipady=8)

        botones_frame = tk.Frame(body_frame, bg=self.color_fondo)
        botones_frame.pack(fill="x", pady=(20, 0))

        btn_guardar = tk.Button(
            botones_frame,
            text="✓ Guardar",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_exito,
            fg="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.guardar_categoria
        )
        btn_guardar.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=5)

        btn_cancelar = tk.Button(
            botones_frame,
            text="✕ Cancelar",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_cancelar,
            fg="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.destroy
        )
        btn_cancelar.pack(side="left", fill="x", expand=True, pady=5)

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.transient(parent)
        self.grab_set()
        self.entry_nombre_categoria.focus()

    def guardar_categoria(self):
        nombre_categoria = self.entry_nombre_categoria.get().strip()
        if not nombre_categoria:
            messagebox.showwarning("Validación", "Debe ingresar el nombre de la categoría.")
            self.entry_nombre_categoria.focus()
            return

        self.categoria.registrar_nueva_categoria(nombre_categoria)
        self.destroy()

        