import tkinter as tk
from tkinter import ttk, messagebox

class FormUsuarioNuevo(tk.Toplevel):
    def __init__(self, parent, crear_usuario, actualizar_tabla):
        super().__init__(parent)
        self.parent = parent
        self.crear_usuario = crear_usuario
        self.actualizar_tabla = actualizar_tabla

        self.title("Crear Nuevo Usuario")
        self.geometry("400x500")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)

        # Hace que la ventana sea modal
        self.transient(parent)
        self.grab_set()
        self.focus_set()

        # Contenedor principal estilo "Card"
        container = tk.Frame(self, bg="#ffffff", padx=25, pady=25, relief="flat", bd=1)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(container, text="NUEVO USUARIO", font=("Segoe UI", 13, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=(0, 20))

        # Campo Nombre
        tk.Label(container, text="Nombre Completo:", bg="#ffffff", font=("Segoe UI", 10, "bold"), fg="#636e72").pack(anchor="w")
        self.entry_nombre = tk.Entry(
            container, font=("Segoe UI", 11), relief="flat", highlightthickness=1, 
            highlightbackground="#dfe6e9", highlightcolor="#00b894"
        )
        self.entry_nombre.pack(fill="x", pady=(5, 15))
        self.entry_nombre.focus()

        # Campo Usuario
        tk.Label(container, text="Usuario de Acceso:", bg="#ffffff", font=("Segoe UI", 10, "bold"), fg="#636e72").pack(anchor="w")
        self.entry_usuario = tk.Entry(
            container, font=("Segoe UI", 11), relief="flat", highlightthickness=1, 
            highlightbackground="#dfe6e9", highlightcolor="#00b894"
        )
        self.entry_usuario.pack(fill="x", pady=(5, 15))

        # Campo Contraseña
        tk.Label(container, text="Contraseña:", bg="#ffffff", font=("Segoe UI", 10, "bold"), fg="#636e72").pack(anchor="w")
        self.entry_contrasenia = tk.Entry(
            container, font=("Segoe UI", 11), relief="flat", highlightthickness=1, 
            highlightbackground="#dfe6e9", highlightcolor="#00b894", show="●"
        )
        self.entry_contrasenia.pack(fill="x", pady=(5, 15))

        # Selector de Rol
        tk.Label(container, text="Rol / Permisos:", bg="#ffffff", font=("Segoe UI", 10, "bold"), fg="#636e72").pack(anchor="w")
        self.combo_rol = ttk.Combobox(
            container, 
            values=['vendedor', 'admin'], 
            font=("Segoe UI", 11), 
            state="readonly"
        )
        self.combo_rol.set('vendedor') # Rol por defecto
        self.combo_rol.pack(fill="x", pady=(5, 25))

        # Panel de botones
        btn_frame = tk.Frame(container, bg="#ffffff")
        btn_frame.pack(fill="x", pady=(10, 0))

        self.btn_crear = tk.Button(
            btn_frame, text="Crear Usuario", bg="#00b894", fg="white", 
            relief="flat", padx=15, pady=8, cursor="hand2", font=("Segoe UI", 10, "bold"),
            command=self.validar_y_crear
        )
        self.btn_crear.pack(side="right", padx=(10, 0))

        self.btn_cancelar = tk.Button(
            btn_frame, text="Cancelar", bg="#b2bec3", fg="white", 
            relief="flat", padx=15, pady=8, cursor="hand2", font=("Segoe UI", 10, "bold"),
            command=self.destroy
        )
        self.btn_cancelar.pack(side="right")

    def validar_y_crear(self):
        nombre = self.entry_nombre.get().strip()
        usuario = self.entry_usuario.get().strip()
        contrasenia = self.entry_contrasenia.get().strip()
        rol = self.combo_rol.get()

        if not nombre or not usuario or not contrasenia or not rol:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return
        
        if len(contrasenia) < 6:
            messagebox.showwarning("Atención", "La contraseña debe tener al menos 6 caracteres.")
            return

        self.crear_usuario(nombre, usuario, contrasenia, rol)
        self.actualizar_tabla()
        self.destroy()