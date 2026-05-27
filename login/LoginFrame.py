import tkinter as tk
from tkinter import messagebox
import login.login as lg

class LoginFrame(tk.Frame):
    def __init__(self, parent, dibujar_frames):
        super().__init__(parent)

        self.dibujar_frames = dibujar_frames

        self.configure(bg="#f0f0f0") # Fondo para toda la pantalla de login
        self.login = lg.Login()


        # Configura el frame principal para expandirse y centrar su contenido
        # Las filas y columnas con weight=1 actúan como "padding" que se expande,
        # empujando el contenido (login_elements_frame) al centro.
        self.grid_rowconfigure(0, weight=1) # Fila superior de padding
        self.grid_rowconfigure(1, weight=0) # Fila para el frame de elementos de login (no se expande verticalmente)
        self.grid_rowconfigure(2, weight=1) # Fila inferior de padding
        self.grid_columnconfigure(0, weight=1) # Columna izquierda de padding
        self.grid_columnconfigure(1, weight=0) # Columna para el frame de elementos de login (no se expande horizontalmente)
        self.grid_columnconfigure(2, weight=1) # Columna derecha de padding

        # Crea un sub-frame para contener los elementos de login (entradas, botones)
        # Este frame será el que se centre en la ventana.
        self.login_elements_frame = tk.Frame(self, bg="#ffffff", padx=40, pady=40, relief="raised", bd=2)
        self.login_elements_frame.grid(row=1, column=1, sticky="") # Centrado en la celda central

        # Configura el grid del login_elements_frame para que sus contenidos se expandan horizontalmente
        self.login_elements_frame.grid_columnconfigure(0, weight=1)

        # Título del formulario de login
        tk.Label(self.login_elements_frame, text="INICIO DE SESIÓN", bg="#ffffff", font=("Arial", 18, "bold"), fg="#333333").grid(row=0, column=0, pady=(0, 25))

        # Etiqueta y campo de entrada para el usuario
        tk.Label(self.login_elements_frame, text="Usuario:", bg="#ffffff", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=(0, 5))
        self.entry_usuario = tk.Entry(self.login_elements_frame, width=30, font=("Arial", 12), relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_usuario.grid(row=2, column=0, sticky="ew", padx=5, pady=(0, 15))
        
        # Etiqueta y campo de entrada para la contraseña
        tk.Label(self.login_elements_frame, text="Contraseña:", bg="#ffffff", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=(0, 5))
        self.entry_contrasena = tk.Entry(self.login_elements_frame, show="*", width=30, font=("Arial", 12), relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_contrasena.grid(row=4, column=0, sticky="ew", padx=5, pady=(0, 15))

        # Botón de inicio de sesión
        self.btn_login = tk.Button(self.login_elements_frame, text="Iniciar Sesión", bg="#0984e3", fg="white", relief="flat", cursor="hand2", font=("Arial", 12, "bold"), command=self.login_attempt)
        self.btn_login.grid(row=5, column=0, sticky="ew", padx=5, pady=(10, 0))

        self.entry_usuario.focus()
        self.entry_usuario.bind("<Return>", lambda event: self.entry_contrasena.focus())
        self.entry_contrasena.bind("<Return>", lambda event: self.login_attempt())

    def login_attempt(self):

        username = self.entry_usuario.get()
        password = self.entry_contrasena.get()
        respuesta = self.login.comprobar_credenciales(username, password)
        if respuesta:
            self.dibujar_frames()
            self.destroy()
        else:
            messagebox.showerror("Credenciales invalidas", "Usuario o contraseña incorrectos.")
