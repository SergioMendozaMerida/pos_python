import tkinter as tk
from tkinter import ttk, messagebox

class FormRol(tk.Toplevel):
    def __init__(self, parent, usuario, cambiar_rol_callback, actualizar_tabla):
        super().__init__(parent)
        self.usuario = usuario
        self.cambiar_rol_callback = cambiar_rol_callback
        self.actualizar_tabla = actualizar_tabla
        
        self.title(f"Permisos: {self.usuario.nombre}")
        self.geometry("400x300")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)

        # Hace que la ventana sea modal
        self.transient(parent)
        self.grab_set()
        self.focus_set()

        # Contenedor principal estilo "Card"
        container = tk.Frame(self, bg="#ffffff", padx=25, pady=25, relief="flat", bd=1)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(container, text="CAMBIAR ROL", font=("Segoe UI", 13, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=(0, 20))

        # Label Informativa
        tk.Label(container, text=f"Usuario: {self.usuario.usuario}", font=("Segoe UI", 9), bg="#ffffff", fg="#636e72").pack(anchor="w", pady=(0, 10))

        # Selector de Rol
        tk.Label(container, text="Seleccione el nuevo rol:", bg="#ffffff", font=("Segoe UI", 10, "bold"), fg="#636e72").pack(anchor="w")
        
        roles = ['vendedor', 'admin']
        self.combo_rol = ttk.Combobox(
            container, 
            values=roles, 
            font=("Segoe UI", 11), 
            state="readonly"
        )
        self.combo_rol.set(self.usuario.rol) # Establece el rol actual por defecto
        self.combo_rol.pack(fill="x", pady=(5, 25))

        # Panel de botones
        btn_frame = tk.Frame(container, bg="#ffffff")
        btn_frame.pack(fill="x", pady=(10, 0))

        self.btn_guardar = tk.Button(
            btn_frame, text="Actualizar Rol", bg="#fdcb6e", fg="#2d3436", 
            relief="flat", padx=15, pady=8, cursor="hand2", font=("Segoe UI", 10, "bold"),
            command=self.validar_y_guardar
        )
        self.btn_guardar.pack(side="right", padx=(10, 0))

        self.btn_cancelar = tk.Button(
            btn_frame, text="Cancelar", bg="#b2bec3", fg="white", 
            relief="flat", padx=15, pady=8, cursor="hand2", font=("Segoe UI", 10, "bold"),
            command=self.destroy
        )
        self.btn_cancelar.pack(side="right")

    def validar_y_guardar(self):
        nuevo_rol = self.combo_rol.get()
        
        # Ejecuta la lógica de base de datos definida en Usuarios.py
        self.cambiar_rol_callback(self.usuario.id_usuario, nuevo_rol, self.actualizar_tabla)

        self.destroy()