import sqlite3
from tkinter import messagebox

class Empresa:
    def __init__(self):
        self.nombre = ""
        self.representante = ""
        self.nit = ""
        self.telefono = 0
        self.correo = ""
        self.direccion = ""
        self.slogan = ""

        self.obtener_datos()

    def obtener_datos(self):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM empresa")
            empresa = cursor.fetchone()
            if empresa:
                self.nombre = empresa[0]
                self.representante = empresa[1]
                self.nit = empresa[2]
                self.telefono = empresa[3]
                self.correo = empresa[4]
                self.direccion = empresa[5]
                self.slogan = empresa[6]
                conexion.close()
                return self
            else:
                #QUITAR ESTA PARTE CUANDO SE IMPLEMENTE EL MODULO DE BASE DE DATOS.
                cursor.execute("""INSERT INTO empresa (nombre, representante, nit, telefono, correo, direccion, eslogan, id)
                               values("","","","","","","",1)""")
                conexion.commit()
                conexion.close()
                return 
                
        except Exception as e:
            print(f"Error al obtener los datos de la empresa: {e}")
            return None
        
    def set_datos(self, nombre, representante, nit, telefono, correo, direccion, eslogan):
        self.nombre = nombre
        self.representante = representante
        self.nit = nit
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
        self.slogan = eslogan

        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("UPDATE empresa SET nombre = ?, representante = ?, nit = ?, telefono = ?, correo = ?, direccion = ?, eslogan = ? WHERE id = 1",
                           (self.nombre, self.representante, self.nit, self.telefono, self.correo, self.direccion, self.slogan))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Los datos de la empresa se han actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar los datos de la empresa: {e}")


    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_representante(self, representante):
        self.representante = representante

    def set_nit(self, nit):
        self.nit = nit

    def set_telefono(self, telefono):
        self.telefono = telefono

    def set_correo(self, correo):
        self.correo = correo

    def set_direccion(self, direccion):
        self.direccion = direccion

    def set_slogan(self, slogan):
        self.slogan = slogan