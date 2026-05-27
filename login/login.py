import sqlite3
from tkinter import messagebox

class Login:
    def __init__(self):
        
        self.usuario = Usuario(0,"","","","")

    def comprobar_credenciales(self, usuario, contrasena):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND contrasenia = ? and activo = 1", (usuario, contrasena))
            usuario_activo = cursor.fetchone()
            conexion.close()

            if usuario_activo:
                self.usuario = Usuario(usuario_activo[0], usuario_activo[1], usuario_activo[2], usuario_activo[4], usuario_activo[5])
                return True
            else:
                return False
        except Exception as e:
            print(f"Error al comprobar las credenciales: {e}")
            return False
        
class Usuario:
    def __init__(self, id_usuario, nombre, usuario, activo, rol):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.usuario = usuario
        self.contrasenia = ""
        self.activo = activo
        self.rol = rol