import tkinter as tk
from tkinter import messagebox

class FrameContrasenia(tk.Toplevel):
    def __init__(self, parent, usuario, reestablecer_callback):
        super().__init__(parent)
        self.usuario = usuario
        self.reestablecer_callback = reestablecer_callback
        
        self.title(f"Seguridad: {self.usuario.nombre}")
        self.geometry("400x320")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)

        # Hace que la ventana sea modal
        self.transient(parent)
        self.grab_set()
        self.focus_set()

        # Contenedor principal estilo "Card"
        container = tk.Frame(self, bg="#ffffff", padx=25, pady=25, relief="flat", bd=1)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(container, text="CAMBIAR CONTRASEÑA", font=("Segoe UI", 13, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=(0, 20))

        # Label Informativa
        tk.Label(container, text=f"Usuario: {self.usuario.usuario}", font=("Segoe UI", 9), bg="#ffffff", fg="#636e72").pack(anchor="w", pady=(0, 10))

        # Campo Nueva Contraseña
        tk.Label(container, text="Nueva Contraseña:", bg="#ffffff", font=("Segoe UI", 10, "bold"), fg="#636e72").pack(anchor="w")
        self.entry_contrasenia = tk.Entry(
            container, font=("Segoe UI", 11), relief="flat", highlightthickness=1, 
            highlightbackground="#dfe6e9", highlightcolor="#6c5ce7", show="●"
        )
        self.entry_contrasenia.pack(fill="x", pady=(5, 25))
        self.entry_contrasenia.focus()

        # Panel de botones
        btn_frame = tk.Frame(container, bg="#ffffff")
        btn_frame.pack(fill="x", pady=(10, 0))

        self.btn_guardar = tk.Button(
            btn_frame, text="Actualizar Llave", bg="#6c5ce7", fg="white", 
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
        nueva = self.entry_contrasenia.get().strip()
        if not nueva or len(nueva) < 6:
            messagebox.showwarning("Atención", "La contraseña debe tener al menos 6 caracteres.")
            return

        # Ejecuta la lógica de base de datos definida en Usuarios.py
        self.reestablecer_callback(self.usuario.id_usuario, nueva)
        self.destroy()
