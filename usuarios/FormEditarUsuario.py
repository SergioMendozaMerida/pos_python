import tkinter as tk
from tkinter import messagebox

class FormEditarUsuario(tk.Toplevel):
    def __init__(self, parent, usuario, actualizar_usuario, actualizar_tabla):
        super().__init__(parent)
        self.usuario = usuario
        self.actualizar_usuario = actualizar_usuario
        self.actualizar_tabla = actualizar_tabla
        
        self.title("Editar Usuario")
        self.geometry("400x350")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)
        
        # Hace que la ventana sea modal
        self.transient(parent)
        self.grab_set()

        # Contenedor principal
        container = tk.Frame(self, bg="#ffffff", padx=25, pady=25, relief="flat", bd=1)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(container, text="EDITAR INFORMACIÓN", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=(0, 20))

        # Campo Nombre
        tk.Label(container, text="Nombre Completo:", bg="#ffffff", font=("Segoe UI", 10, "bold"), fg="#636e72").pack(anchor="w")
        self.entry_nombre = tk.Entry(container, font=("Segoe UI", 11), relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_nombre.insert(0, self.usuario.nombre)
        self.entry_nombre.pack(fill="x", pady=(5, 15))

        # Campo Usuario
        #tk.Label(container, text="Nombre de Usuario:", bg="#ffffff", font=("Segoe UI", 10, "bold"), fg="#636e72").pack(anchor="w")
        #self.entry_usuario = tk.Entry(container, font=("Segoe UI", 11), relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        #self.entry_usuario.insert(0, self.usuario.usuario)
        #self.entry_usuario.pack(fill="x", pady=(5, 20))

        # Panel de botones
        btn_frame = tk.Frame(container, bg="#ffffff")
        btn_frame.pack(fill="x", pady=(10, 0))

        self.btn_guardar = tk.Button(
            btn_frame, text="Guardar Cambios", bg="#00b894", fg="white", 
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
        nombre = self.entry_nombre.get().strip()
        #usuario = self.entry_usuario.get().strip()

        if not nombre:
            messagebox.showwarning("Campos Requeridos", "Por favor, complete todos los campos.")
            return

        # Ejecuta la función de actualización pasada por el padre
        self.actualizar_usuario(self.usuario.id_usuario, nombre, self.actualizar_tabla)
        self.destroy()