import tkinter as tk
import sqlite3
from tkinter import ttk


class TerminosYCondiciones(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.terminos_y_condiciones = []

        self.crear_interfaz()

        self.obtener_terminos()


    def crear_interfaz(self):

        self.config(bg="#f4f4f4")


        # Título
        titulo = tk.Label(
            self,
            text="Anabel POS\nTérminos y Condiciones",
            font=("Segoe UI", 18, "bold"),
            bg="#1f4e79",
            fg="white",
            pady=15
        )

        titulo.pack(
            fill="x"
        )


        # Contenedor
        contenedor = tk.Frame(
            self,
            bg="#f4f4f4"
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )


        # Texto con scroll
        self.texto = tk.Text(
            contenedor,
            wrap="word",
            font=("Segoe UI", 11),
            bg="white",
            padx=15,
            pady=15
        )

        self.texto.pack(
            side="left",
            fill="both",
            expand=True
        )


        scroll = ttk.Scrollbar(
            contenedor,
            command=self.texto.yview
        )

        scroll.pack(
            side="right",
            fill="y"
        )


        self.texto.configure(
            yscrollcommand=scroll.set
        )


        self.texto.config(
            state="disabled"
        )



    def obtener_terminos(self):

        try:

            conexion = sqlite3.connect(
                "db_inventario.db"
            )

            cursor = conexion.cursor()


            cursor.execute(
                "SELECT titulo, definicion FROM terminos"
            )


            respuesta = cursor.fetchall()


            conexion.close()


            for termino in respuesta:

                self.terminos_y_condiciones.append(
                    Termino(
                        termino[0],
                        termino[1]
                    )
                )


            self.mostrar_terminos()


        except Exception as e:

            print("Error:", e)



    def mostrar_terminos(self):

        contenido = ""


        for termino in self.terminos_y_condiciones:

            contenido += "\n"
            contenido += termino.titulo
            contenido += "\n"
            contenido += "-" * 60
            contenido += "\n"
            contenido += termino.definicion
            contenido += "\n\n"


        self.texto.config(
            state="normal"
        )


        self.texto.insert(
            "1.0",
            contenido
        )


        self.texto.config(
            state="disabled"
        )



class Termino:

    def __init__(self, titulo, definicion):

        self.titulo = titulo
        self.definicion = definicion