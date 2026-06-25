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
                self.usuarios.append(lg.Usuario(usuario[0], usuario[1], usuario[2], usuario[4], usuario[5]))
        except:
            messagebox.showerror("Error", "Se produjo un error al obtener los usuarios.")

    def crear_usuario(self, nombre, usuario, contrasenia, rol):

        for u in self.usuarios:
            if usuario == u.usuario:
                messagebox.showerror("No se puede crear el usuario.", f"El usuario {usuario} ya existe, no pueden haber usuarios duplicados.")
                return

        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, usuario, contrasenia, rol, activo) VALUES (?, ?, ?, ?,1)", (nombre, usuario, contrasenia, rol))
            conexion.commit()
            conexion.close()
            self.obtener_usuarios()
            messagebox.showinfo("Éxito", "Usuario creado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al crear el usuario. {e}")

    def reestablcer_contrasenia(self, id_usuario, nueva_contrasenia):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("UPDATE usuarios SET contrasenia = ? WHERE id = ?", (nueva_contrasenia, id_usuario))
            conexion.commit()
            conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al reestablecer la contraseña. {e}")

    def editar_usuario(self, id_usuario, nombre, actualizar_tabla):

        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("UPDATE usuarios SET nombre = ? WHERE id = ?", (nombre, id_usuario))
            conexion.commit()
            conexion.close()
            self.obtener_usuarios()
            actualizar_tabla()
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al editar el usuario. {e}")

    def cambiar_rol(self, id_usuario, nuevo_rol, actualizar_tabla):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("UPDATE usuarios SET rol = ? WHERE id = ?", (nuevo_rol, id_usuario))
            conexion.commit()
            conexion.close()
            self.obtener_usuarios()
            actualizar_tabla()
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al cambiar el rol del usuario. {e}")

    def inactivar_usuario(self, id_usuario):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("UPDATE usuarios SET activo = 0 WHERE id = ?", (id_usuario,))
            conexion.commit()
            conexion.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al inactivar el usuario. {e}")

    def activar_usuario(self, id_usuario):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("UPDATE usuarios SET activo = 1 WHERE id = ?", (id_usuario,))
            conexion.commit()
            conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al activar el usuario. {e}")




        
    