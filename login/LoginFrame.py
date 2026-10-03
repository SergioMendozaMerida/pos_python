import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import login.login as lg
from PIL import Image, ImageTk
from assets.icons.AnabellIcons import AnabellIcons

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, dibujar_frames):
        super().__init__(parent, fg_color="#f8f9fa")

        self.dibujar_frames = dibujar_frames

        # Colores del tema
        self.color_fondo = "#f8f9fa"
        self.color_navy = "#2c3e50"
        self.color_primario = "#0984e3"
        self.color_borde = "#dfe6e9"
        self.color_texto = "#2d3436"

        # --- IMAGEN DE FONDO ---
        ruta_imagen = "./img/fondo.jpg"
        try:
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((1200, 700))
            self.fondo_img = ImageTk.PhotoImage(imagen)

            self.fondo = tk.Label(
                self,
                image=self.fondo_img,
                bd=0,
                highlightthickness=0
            )
            self.fondo.place(
                x=0,
                y=0,
                relwidth=1,
                relheight=1
            )
        except Exception:
            pass

        self.login = lg.Login()
        #self.iconos = AbI.AnabellIcons()

        #creando imagenes
        #self.icon_user = self.obtener_imagen("assets/icons/user.png")
        self.icon_user = AnabellIcons.obtener_imagen('user_black')
        self.icon_password = AnabellIcons.obtener_imagen('password_black')
        self.icon_login = AnabellIcons.obtener_imagen('login')

        #self.icon_password = self.iconos.obtener_imagen('password')
        #self.icon_login = self.iconos.obtener_imagen('login')

        # Grid principal para centrar la tarjeta de login
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        # Tarjeta contenedora de login
        self.login_elements_frame = ctk.CTkFrame(
            self, 
            fg_color="#ffffff", 
            corner_radius=12,
            border_width=1,
            border_color=self.color_borde
        )
        self.login_elements_frame.grid(row=1, column=1, sticky="")
        self.login_elements_frame.grid_columnconfigure(0, weight=1)

        # --- ENCABEZADO DE LA TARJETA ---
        self.header_login = ctk.CTkFrame(
            self.login_elements_frame, 
            fg_color=self.color_navy, 
            corner_radius=0
        )
        self.header_login.grid(row=0, column=0, sticky="ew")

        ctk.CTkLabel(
            self.header_login, 
            text="INICIO DE SESIÓN", 
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), 
            text_color="white"
        ).pack(pady=18, padx=40)

        # --- CUERPO DEL FORMULARIO ---
        self.form_container = ctk.CTkFrame(
            self.login_elements_frame, 
            fg_color="#ffffff",
            corner_radius=0
        )
        self.form_container.grid(row=1, column=0, sticky="nsew", padx=35, pady=25)

        # Usuario
        ctk.CTkLabel(
            self.form_container, 
            text="  Usuario", 
            image=self.icon_user,
            compound="left",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), 
            text_color=self.color_texto
        ).pack(anchor="w", pady=(0, 6))
        
        self.entry_usuario = ctk.CTkEntry(
            self.form_container, 
            font=ctk.CTkFont(family="Segoe UI", size=12), 
            placeholder_text="Ingrese su usuario...",
            width=280,
            height=40
        )
        self.entry_usuario.pack(fill="x", pady=(0, 18))
        
        # Contraseña
        ctk.CTkLabel(
            self.form_container, 
            text="  Contraseña", 
            image=self.icon_password,
            compound="left",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), 
            text_color=self.color_texto
        ).pack(anchor="w", pady=(0, 6))
        
        self.entry_contrasena = ctk.CTkEntry(
            self.form_container, 
            show="*", 
            font=ctk.CTkFont(family="Segoe UI", size=12), 
            placeholder_text="••••••••",
            width=280,
            height=40
        )
        self.entry_contrasena.pack(fill="x", pady=(0, 25))

        # Botón Entrar
        self.btn_login = ctk.CTkButton(
            self.form_container, 
            text="Entrar",
            image=self.icon_login,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), 
            fg_color="#01b11e", 
            hover_color="#2cff60",
            text_color="white", 
            height=44,
            command=self.login_attempt
        )
        self.btn_login.pack(fill="x", pady=(5, 0))

        self.entry_usuario.focus()
        self.entry_usuario.bind("<Return>", lambda event: self.entry_contrasena.focus())
        self.entry_contrasena.bind("<Return>", lambda event: self.login_attempt())

    def obtener_imagen(self, ruta):  
        try:
            archivo = Image.open(ruta)
            return ctk.CTkImage(
                light_image=archivo,
                dark_image=archivo,
                size=(18, 18)
            )
        except Exception:
            return None

    def login_attempt(self):
        username = self.entry_usuario.get()
        password = self.entry_contrasena.get()
        respuesta = self.login.comprobar_credenciales(username, password)
        if respuesta:
            self.dibujar_frames()
            self.destroy()
        else:
            messagebox.showerror("Credenciales invalidas", "Usuario o contraseña incorrectos.")
