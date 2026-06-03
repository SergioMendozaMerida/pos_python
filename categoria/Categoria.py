import sqlite3
from tkinter import messagebox

class Categorias:
    def __init__(self):
        self.categorias = []

    def obtener_categorias(self):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM categorias")
            categorias_db = cursor.fetchall()
            self.categorias.clear()
            for c in categorias_db:
                self.categorias.append(Categoria(c[0], c[1]))
            conexion.close()
            return self.categorias
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al obtener las categorías {e}.")
            return None


class Categoria:
    def __init__(self, id_categoria=None, nombre_categoria=None):
        self.id_categoria = id_categoria
        self.nombre_categoria = nombre_categoria

    def registrar_nueva_categoria(self, nombre_categoria):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM categorias WHERE categoria = ?", (nombre_categoria,))
            categoria_db = cursor.fetchone()
            if categoria_db:
                messagebox.showwarning("Categoría existente", "La categoría ya existe.")
                return None
            cursor.execute("INSERT INTO categorias (categoria) VALUES (?)", (nombre_categoria,))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Categoría registrada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al registrar la categoría {e}.")
            return None
        
    def eliminar_categoria(self, id_categoria):
        try:
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM categorias WHERE id_categoria = ?", (id_categoria,))
            conexion.commit()
            conexion.close
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al eliminar la categoría {e}.")