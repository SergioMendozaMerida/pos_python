import tkinter as tk
from tkinter import messagebox
import login.login as lg

class LoginFrame(tk.Frame):
    def __init__(self, parent, dibujar_frames):
        super().__init__(parent)

        self.dibujar_frames = dibujar_frames

        # Colores del tema
        self.color_fondo = "#f8f9fa"
        self.color_navy = "#2c3e50"
        self.color_primario = "#0984e3"
        self.color_borde = "#dfe6e9"
        self.color_texto = "#2d3436"

        self.configure(bg=self.color_fondo) 
        self.login = lg.Login()

        # Configura el grid principal para centrar la tarjeta de login
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
        self.login_elements_frame = tk.Frame(self, bg="#ffffff", relief="solid", bd=1, highlightthickness=0)
        self.login_elements_frame.grid(row=1, column=1, sticky="") # Centrado en la celda central
        
        # Configurar columnas del frame de login para que el contenido use todo el ancho
        self.login_elements_frame.grid_columnconfigure(0, weight=1)

        # --- ENCABEZADO DE LA TARJETA ---
        self.header_login = tk.Frame(self.login_elements_frame, bg=self.color_navy, pady=20)
        self.header_login.grid(row=0, column=0, sticky="ew")

        tk.Label(
            self.header_login, 
            text="ACCESO AL SISTEMA", 
            bg=self.color_navy, 
            font=("Segoe UI", 16, "bold"), 
            fg="white"
        ).pack()

        # --- CUERPO DEL FORMULARIO ---
        self.form_container = tk.Frame(self.login_elements_frame, bg="#ffffff", padx=40, pady=30)
        self.form_container.grid(row=1, column=0, sticky="nsew")

        # Etiqueta y campo de entrada para el usuario
        tk.Label(self.form_container, text="Usuario", bg="#ffffff", font=("Segoe UI", 10, "bold"), fg=self.color_texto).pack(anchor="w", pady=(0, 5))
        self.entry_usuario = tk.Entry(
            self.form_container, 
            width=35, 
            font=("Segoe UI", 11), 
            relief="flat", 
            highlightthickness=1, 
            highlightbackground=self.color_borde, 
            highlightcolor=self.color_primario
        )
        self.entry_usuario.pack(fill="x", ipady=5, pady=(0, 20))
        
        # Etiqueta y campo de entrada para la contraseña
        tk.Label(self.form_container, text="Contraseña", bg="#ffffff", font=("Segoe UI", 10, "bold"), fg=self.color_texto).pack(anchor="w", pady=(0, 5))
        self.entry_contrasena = tk.Entry(
            self.form_container, 
            show="*", 
            width=35, 
            font=("Segoe UI", 11), 
            relief="flat", 
            highlightthickness=1, 
            highlightbackground=self.color_borde, 
            highlightcolor=self.color_primario
        )
        self.entry_contrasena.pack(fill="x", ipady=5, pady=(0, 30))

        # Botón de inicio de sesión
        self.btn_login = tk.Button(
            self.form_container, 
            text="Entrar", 
            bg=self.color_primario, 
            fg="white", 
            relief="flat", 
            cursor="hand2", 
            font=("Segoe UI", 12, "bold"), 
            command=self.login_attempt,
            activebackground="#0769b5",
            activeforeground="white"
        )
        self.btn_login.pack(fill="x", ipady=8)

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
