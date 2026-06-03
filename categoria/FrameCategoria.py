import tkinter as tk
import categoria.Categoria as Ct
from tkinter import ttk, messagebox

class FrameCategoria(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Categorías")
        self.geometry("750x550")
        self.resizable(False, False)
        
        # Colores coordinados y estilos
        self.color_fondo = "#f8f9fa"
        self.color_header = "#2c3e50"
        self.color_primario = "#0984e3"
        self.color_exito = "#00b894"
        self.color_cancelar = "#d63031"
        self.color_entrada = "#ffffff"
        self.color_texto = "#2d3436"
        self.color_borde = "#dfe6e9"

        self.configure(bg=self.color_fondo)

        self.categorias = Ct.Categorias()
        self.lista_categorias = self.categorias.obtener_categorias()

        # Header superior
        self.header_frame = tk.Frame(self, bg=self.color_header, height=60)
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)

        tk.Label(
            self.header_frame,
            text="Administración de Categorías",
            font=("Segoe UI", 16, "bold"),
            bg=self.color_header,
            fg="white"
        ).pack(pady=15)

        # Contenedor principal para las dos columnas
        self.main_container = tk.Frame(self, bg=self.color_fondo)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # --- COLUMNA IZQUIERDA: Listado de Categorías ---
        self.frame_categoria = tk.LabelFrame(
            self.main_container, 
            text="Categorías Existentes", 
            font=("Segoe UI", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto,
            padx=10, 
            pady=10
        )
        self.frame_categoria.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.tabla_categorias = ttk.Treeview(self.frame_categoria, columns=("id", "nombre"), show="headings", height=8)
        self.tabla_categorias.heading("id", text="#")
        self.tabla_categorias.heading("nombre", text="Nombre de Categoría")
        self.tabla_categorias.column("id", width=40, anchor="center")
        self.tabla_categorias.column("nombre", width=180, anchor="w")
        self.tabla_categorias.pack(fill="both", expand=True)

        tk.Button(
            self.frame_categoria, 
            text="🗑️ Eliminar Seleccionada", 
            bg=self.color_cancelar, 
            fg="white", 
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            pady=5,
            command=self.eliminar_categoria
        ).pack(fill="x", pady=(10, 0))

        # --- COLUMNA DERECHA: Formulario de Registro ---
        self.frame_formulario = tk.LabelFrame(
            self.main_container, 
            text="Agregar Nueva Categoría", 
            font=("Segoe UI", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto,
            padx=15, 
            pady=10
        )
        self.frame_formulario.pack(side="right", fill="both", expand=True)

        tk.Label(self.frame_formulario, text="Nombre de la Categoría:", bg=self.color_fondo, fg=self.color_texto, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 5))
        self.entry_nombre_categoria = tk.Entry(
            self.frame_formulario, 
            font=("Segoe UI", 10), 
            bg=self.color_entrada, 
            relief="flat", 
            bd=0, 
            highlightthickness=1, 
            highlightbackground=self.color_borde,
            highlightcolor=self.color_primario
        )
        self.entry_nombre_categoria.pack(fill="x", pady=(0, 20), ipady=4)

        tk.Button(
            self.frame_formulario, 
            text="✓ Guardar Categoría", 
            bg=self.color_exito, 
            fg="white", 
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            pady=10,
            command=self.guardar_categoria
        ).pack(fill="x")

        # Botón Cancelar (fuera de los paneles)
        tk.Button(
            self, 
            text="✕ Cerrar Ventana", 
            bg="#636e72", 
            fg="white", 
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=8,
            command=self.destroy
        ).pack(pady=(0, 20))

        self.dibuajar_categorias()
        self.transient(parent)
        self.grab_set()

    def dibuajar_categorias(self):
        self.tabla_categorias.delete(*self.tabla_categorias.get_children())

        for i, categoria in enumerate(self.lista_categorias, start=1):
            self.tabla_categorias.insert("", "end", iid=categoria.id_categoria, values=(i, categoria.nombre_categoria))
        

    def guardar_categoria(self):
        categoria = Ct.Categoria()
        nombre_categoria = self.entry_nombre_categoria.get()
        if nombre_categoria:
            categoria.registrar_nueva_categoria(nombre_categoria)
            self.lista_categorias.append(categoria)
            self.lista_categorias = self.categorias.obtener_categorias()
            self.dibuajar_categorias()
            self.entry_nombre_categoria.delete(0, tk.END)

    def eliminar_categoria(self):
        selected_item = self.tabla_categorias.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una categoría para eliminar.")
            return

        categoria_id = self.tabla_categorias.item(selected_item, "values")[0]
        categoria = Ct.Categoria()
        categoria.eliminar_categoria(categoria_id)
        self.lista_categorias = self.categorias.obtener_categorias()
        self.dibuajar_categorias()
