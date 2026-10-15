from tkinter import messagebox

import login.login as lg
import sqlite3


class Usuarios:
    def __init__(self):

        self.usuarios = []
        self.obtener_usuarios()

    def obtener_usuarios(self):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM usuarios")
            usuarios = cursor.fetchall()
            conexion.close()
            for usuario in usuarios:
                self.usuarios.append(lg.Usuario(usuario[0], usuario[1], usuario[2], usuario[4], 
                                                usuario[5], usuario[6]))
        except:
            messagebox.showerror("Error", "Se produjo un error al obtener los usuarios.")

    def crear_usuario(self, nombre, usuario, contrasenia, rol, dpi):

        for u in self.usuarios:
            if usuario == u.usuario:
                messagebox.showerror("No se puede crear el usuario.", f"El usuario {usuario} ya existe, no pueden haber usuarios duplicados.")
                return

        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, usuario, contrasenia, rol, activo, dpi) VALUES (?, ?, ?, ?,1,?)", 
                           (nombre, usuario, contrasenia, rol, dpi))
            conexion.commit()
            conexion.close()
            self.obtener_usuarios()
            messagebox.showinfo("Éxito", "Usuario creado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al crear el usuario. {e}")

    def editar_usuario(self, nombre, dpi, rol, contrasenia, estado, id):

        try:
            with sqlite3.connect("db_inventario.db") as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    "UPDATE usuarios SET nombre = ?, dpi = ?, rol = ?, "
                    "contrasenia = CASE WHEN ? = '' THEN contrasenia ELSE ? END, "
                    "activo = ? WHERE id = ?",
                    (nombre, dpi, rol, contrasenia, contrasenia, estado, id)
                )
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al guardar los cambios. {e}")
        
    