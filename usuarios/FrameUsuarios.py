import tkinter as tk
from tkinter import ttk, messagebox
import usuarios.usuarios as U
import usuarios.FormEditarUsuario as FEU
import usuarios.FormContrasenia as FC
import usuarios.FormRol as FR
import usuarios.FormUsuarioNuevo as FUN

class FrameUsuarios(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.usuarios = U.Usuarios()
        self.configure(bg="#f0f0f0")

        # Configuración de pesos para que la tabla se expanda
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- PANEL SUPERIOR: Crear Usuario ---
        self.frame_superior = tk.Frame(self, bg="#ffffff", padx=20, pady=15, relief="flat", bd=1)
        self.frame_superior.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        tk.Label(self.frame_superior, text="👥 GESTIÓN DE USUARIOS", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#2c3e50").pack(side="left")

        self.btn_crear = tk.Button(
            self.frame_superior, text="+ Crear Nuevo Usuario", bg="#00b894", fg="white",
            relief="flat", padx=20, pady=8, cursor="hand2", font=("Segoe UI", 10, "bold"),
            command=self.abrir_formulario_crear
        )
        self.btn_crear.pack(side="right")

        # --- PANEL CENTRAL: Tabla de Usuarios ---
        self.frame_tabla = tk.Frame(self, bg="#ffffff", padx=10, pady=10, relief="flat", bd=1)
        self.frame_tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.frame_tabla.grid_rowconfigure(0, weight=1)
        self.frame_tabla.grid_columnconfigure(0, weight=1)

        columnas = ("id", "nombre", "usuario", "rol", "estado")
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", selectmode="browse")

        # Definición de cabeceras
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre Completo")
        self.tabla.heading("usuario", text="Usuario de Acceso")
        self.tabla.heading("rol", text="Rol / Permisos")
        self.tabla.heading("estado", text="Estado")

        # Configuración de columnas
        self.tabla.column("id", width=50, anchor="center")
        self.tabla.column("nombre", width=250, anchor="w")
        self.tabla.column("usuario", width=150, anchor="center")
        self.tabla.column("rol", width=150, anchor="center")
        self.tabla.column("estado", width=100, anchor="center")

        # Scrollbar
        self.scroll_y = tk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=self.scroll_y.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")

        # --- PANEL INFERIOR: Botones de Acción ---
        self.frame_acciones = tk.Frame(self, bg="#ffffff", padx=10, pady=15, relief="flat", bd=1)
        self.frame_acciones.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        btn_act_style = {"relief": "flat", "padx": 15, "pady": 8, "cursor": "hand2", "font": ("Segoe UI", 9, "bold")}

        self.btn_inactivar = tk.Button(self.frame_acciones, text="🚫 Inactivar", bg="#e17055", fg="white", command=self.inactivar, **btn_act_style)
        self.btn_inactivar.pack(side="left", padx=5)

        self.btn_activar = tk.Button(self.frame_acciones, text="✅ Activar", bg="#55efc4", fg="#2d3436", command=self.activar, **btn_act_style)
        self.btn_activar.pack(side="left", padx=5)

        self.btn_editar = tk.Button(self.frame_acciones, text="✏️ Editar Datos", bg="#0984e3", fg="white", command=self.editar, **btn_act_style)
        self.btn_editar.pack(side="left", padx=5)

        self.btn_pass = tk.Button(self.frame_acciones, text="🔑 Cambiar Contraseña", bg="#6c5ce7", fg="white", command=self.cambiar_password, **btn_act_style)
        self.btn_pass.pack(side="left", padx=5)

        self.btn_rol = tk.Button(self.frame_acciones, text="🛡️ Cambiar Rol", bg="#fdcb6e", fg="#2d3436", command=self.cambiar_rol, **btn_act_style)
        self.btn_rol.pack(side="left", padx=5)

        self.actualizar_tabla()

    def actualizar_tabla(self):
        """Limpia y recarga los datos de la tabla desde la base de datos."""
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        self.usuarios.usuarios = [] # Limpiamos lista actual para evitar duplicados al recargar
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

    # Métodos para implementar en la siguiente fase
    def editar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return messagebox.showwarning("Atención", "Seleccione un usuario de la tabla.")
        id_u = seleccion[0]
        
        for u in self.usuarios.usuarios:
            if int(u.id_usuario) == int(id_u):
                seleccion = u
                break

        formulario = FEU.FormEditarUsuario(self, seleccion, self.usuarios.editar_usuario)


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

        
