import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import usuarios.usuarios as U
import usuarios.FormEditarUsuario as FEU
import usuarios.FormContrasenia as FC
import usuarios.FormRol as FR
import usuarios.FormUsuarioNuevo as FUN

class FrameUsuarios(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f4f6f9")
        self.usuarios = U.Usuarios()

        # Configuración de colores
        self.color_fondo = "#f4f6f9"
        self.color_primario = "#2c3e50"
        self.color_secundario = "#0984e3"
        self.color_boton = "#27ae60"
        self.color_cancelar = "#d63031"
        self.color_border = "#dfe6e9"

        # Configuración de pesos para que la tabla se expanda
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 1. PANEL SUPERIOR: Crear Usuario
        self.frame_superior = ctk.CTkFrame(
            self, 
            fg_color="#ffffff", 
            corner_radius=8,
            border_width=1,
            border_color=self.color_border
        )
        self.frame_superior.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(
            self.frame_superior, 
            text="👥 GESTIÓN DE USUARIOS", 
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), 
            text_color=self.color_primario
        ).pack(side="left", padx=15, pady=12)

        self.btn_crear = ctk.CTkButton(
            self.frame_superior, 
            text="+ Crear Nuevo Usuario", 
            fg_color="#00b894", 
            hover_color="#009476",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=38,
            command=self.abrir_formulario_crear
        )
        self.btn_crear.pack(side="right", padx=15, pady=12)

        # 2. PANEL CENTRAL: Tabla de Usuarios
        self.frame_tabla = ctk.CTkFrame(
            self, 
            fg_color="#ffffff", 
            corner_radius=8,
            border_width=1,
            border_color=self.color_border
        )
        self.frame_tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.frame_tabla.grid_rowconfigure(0, weight=1)
        self.frame_tabla.grid_columnconfigure(0, weight=1)

        tabla_inner_frame = ctk.CTkFrame(self.frame_tabla, fg_color="transparent")
        tabla_inner_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        tabla_inner_frame.grid_rowconfigure(0, weight=1)
        tabla_inner_frame.grid_columnconfigure(0, weight=1)

        columnas = ("id", "nombre", "usuario", "rol", "estado")
        self.tabla = ttk.Treeview(tabla_inner_frame, columns=columnas, show="headings", selectmode="browse")

        # Definición de cabeceras
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre Completo")
        self.tabla.heading("usuario", text="Usuario de Acceso")
        self.tabla.heading("rol", text="Rol / Permisos")
        self.tabla.heading("estado", text="Estado")

        # Configuración de columnas
        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("nombre", width=250, anchor="w")
        self.tabla.column("usuario", width=150, anchor="center")
        self.tabla.column("rol", width=150, anchor="center")
        self.tabla.column("estado", width=100, anchor="center")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#2d3436",
                        rowheight=34,
                        fieldbackground="#ffffff",
                        borderwidth=0,
                        font=("Segoe UI", 12))

        style.configure("Treeview.Heading",
                        background="#f1f2f6",
                        foreground="#2d3436",
                        relief="flat",
                        font=("Segoe UI", 12, "bold"))

        style.map("Treeview", 
                background=[('selected', "#74b9ff")],
                foreground=[('selected', "white")])

        # Scrollbar
        self.scroll_y = ttk.Scrollbar(tabla_inner_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=self.scroll_y.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")

        # 3. PANEL INFERIOR: Botones de Acción
        self.frame_acciones = ctk.CTkFrame(
            self, 
            fg_color="#ffffff", 
            corner_radius=8,
            border_width=1,
            border_color=self.color_border
        )
        self.frame_acciones.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))

        btn_act_font = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")

        self.btn_inactivar = ctk.CTkButton(
            self.frame_acciones, 
            text="🚫 Inactivar", 
            fg_color="#e17055", 
            hover_color="#d63031",
            text_color="white",
            font=btn_act_font,
            height=40,
            command=self.inactivar
        )
        self.btn_inactivar.pack(side="left", padx=10, pady=10)

        self.btn_activar = ctk.CTkButton(
            self.frame_acciones, 
            text="✅ Activar", 
            fg_color="#00b894", 
            hover_color="#009476",
            text_color="white",
            font=btn_act_font,
            height=40,
            command=self.activar
        )
        self.btn_activar.pack(side="left", padx=(0, 10), pady=10)

        self.btn_editar = ctk.CTkButton(
            self.frame_acciones, 
            text="✏️ Editar Datos", 
            fg_color=self.color_secundario, 
            hover_color="#74b9ff",
            text_color="white",
            font=btn_act_font,
            height=40,
            command=self.editar
        )
        self.btn_editar.pack(side="left", padx=(0, 10), pady=10)

        self.btn_pass = ctk.CTkButton(
            self.frame_acciones, 
            text="🔑 Cambiar Contraseña", 
            fg_color="#6c5ce7", 
            hover_color="#574b90",
            text_color="white",
            font=btn_act_font,
            height=40,
            command=self.cambiar_password
        )
        self.btn_pass.pack(side="left", padx=(0, 10), pady=10)

        self.btn_rol = ctk.CTkButton(
            self.frame_acciones, 
            text="🛡️ Cambiar Rol", 
            fg_color="#e67e22", 
            hover_color="#d35400",
            text_color="white",
            font=btn_act_font,
            height=40,
            command=self.cambiar_rol
        )
        self.btn_rol.pack(side="left", padx=(0, 10), pady=10)

        self.actualizar_tabla()

    def actualizar_tabla(self):
        """Limpia y recarga los datos de la tabla desde la base de datos."""
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        self.usuarios.usuarios = []
        self.usuarios.obtener_usuarios()

        for u in self.usuarios.usuarios:
            estado_texto = "ACTIVO" if int(u.activo) == 1 else "INACTIVO"
            self.tabla.insert("", "end", iid=u.id_usuario, values=(
                u.id_usuario, u.nombre, u.usuario, u.rol, estado_texto
            ))

    def inactivar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return messagebox.showwarning("Atención", "Seleccione un usuario de la tabla.")
        id_u = seleccion[0]
        for u in self.usuarios.usuarios:
            if int(u.id_usuario) == int(id_u):
                usuario = u.usuario
                break
        if messagebox.askyesno("Confirmar", f"¿Está seguro que desea INACTIVAR al usuario {usuario}?"):
            self.usuarios.inactivar_usuario(id_u)
            self.actualizar_tabla()

    def activar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return messagebox.showwarning("Atención", "Seleccione un usuario de la tabla.")
        id_u = seleccion[0]
        self.usuarios.activar_usuario(id_u)
        self.actualizar_tabla()

    def editar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return messagebox.showwarning("Atención", "Seleccione un usuario de la tabla.")
        id_u = seleccion[0]
        
        for u in self.usuarios.usuarios:
            if int(u.id_usuario) == int(id_u):
                seleccion = u
                break

        formulario = FEU.FormEditarUsuario(self, seleccion, self.usuarios.editar_usuario, self.actualizar_tabla)
        self.actualizar_tabla()

    def cambiar_password(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return messagebox.showwarning("Atención", "Seleccione un usuario de la tabla.")
        id_u = seleccion[0]
        
        for u in self.usuarios.usuarios:
            if int(u.id_usuario) == int(id_u):
                seleccion = u
                break

        formulario = FC.FrameContrasenia(self, seleccion, self.usuarios.reestablcer_contrasenia)
        self.actualizar_tabla()

    def cambiar_rol(self): 
        seleccion = self.tabla.selection()
        if not seleccion:
            return messagebox.showwarning("Atención", "Seleccione un usuario de la tabla.")
        id_u = seleccion[0]

        for u in self.usuarios.usuarios:
            if int(u.id_usuario) == int(id_u):
                seleccion = u
                break

        formulario = FR.FormRol(self, seleccion, self.usuarios.cambiar_rol, self.actualizar_tabla)

    def abrir_formulario_crear(self): 
        formulario = FUN.FormUsuarioNuevo(self, self.usuarios.crear_usuario, self.actualizar_tabla)
