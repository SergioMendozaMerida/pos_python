import tkinter as tk
from tkinter import messagebox

class FrameEmpresa(tk.Frame):
    def __init__(self, parent, empresa, usuario):
        super().__init__(parent)

        self.empresa = empresa
        self.usuario = usuario

        self.configure(bg="#f0f0f0")

        # Centrado del contenido en el frame principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Contenedor estilo "tarjeta"
        self.container = tk.Frame(self, bg="#ffffff", padx=30, pady=30, relief="raised", bd=1)
        self.container.grid(row=0, column=0)

        # Título del Frame
        tk.Label(self.container, text="DATOS DE LA EMPRESA", font=("Arial", 16, "bold"), bg="#ffffff", fg="#333333").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Definición de campos basada en los atributos de la clase Empresa
        self.campos_info = [
            ("Nombre Comercial:", "nombre"),
            ("Representante Legal:", "representante"),
            ("NIT:", "nit"),
            ("Teléfono:", "telefono"),
            ("Correo Electrónico:", "correo"),
            ("Dirección Física:", "direccion"),
            ("Eslogan:", "slogan")
        ]

        # Diccionarios para almacenar variables y widgets
        self.vars = {}
        self.entries = {}

        # Creación dinámica de Labels y Entries
        for i, (label_text, attr) in enumerate(self.campos_info):
            valor_inicial = getattr(self.empresa, attr)
            self.vars[attr] = tk.StringVar(value=str(valor_inicial))

            tk.Label(self.container, text=label_text, bg="#ffffff", font=("Arial", 10, "bold")).grid(row=i+1, column=0, sticky="w", pady=8, padx=(0, 15))
            
            entry = tk.Entry(self.container, textvariable=self.vars[attr], width=45, font=("Arial", 11), 
                             state="readonly", relief="flat", highlightthickness=1, 
                             highlightbackground="#dfe6e9", highlightcolor="#0984e3")
            entry.grid(row=i+1, column=1, pady=8, sticky="ew")
            self.entries[attr] = entry

        # Frame para botones
        self.frame_btns = tk.Frame(self.container, bg="#ffffff")
        self.frame_btns.grid(row=len(self.campos_info) + 1, column=0, columnspan=2, pady=(25, 0))

        if self.usuario.rol == "admin":

            self.btn_editar = tk.Button(self.frame_btns, text="Editar Datos", bg="#0984e3", fg="white", 
                                    relief="flat", padx=20, pady=8, cursor="hand2", 
                                    font=("Arial", 10, "bold"), command=self.habilitar_edicion)
            self.btn_editar.pack(side="left", padx=10)

            self.btn_guardar = tk.Button(self.frame_btns, text="Guardar Cambios", bg="#00b894", fg="white", 
                                        relief="flat", padx=20, pady=8, cursor="hand2", 
                                        font=("Arial", 10, "bold"), state="disabled", command=self.guardar_cambios)
            self.btn_guardar.pack(side="left", padx=10)

    def habilitar_edicion(self):
        """Habilita los campos para escritura."""
        for entry in self.entries.values():
            entry.config(state="normal")
        
        self.btn_editar.config(state="disabled")
        self.btn_guardar.config(state="normal")
        self.entries["nombre"].focus()

    def guardar_cambios(self):
        """Actualiza el objeto empresa y vuelve a bloquear los campos."""
        try:
            self.empresa.set_datos(
                self.vars["nombre"].get(),
                self.vars["representante"].get(),
                self.vars["nit"].get(),
                int(self.vars["telefono"].get()) if self.vars["telefono"].get().isdigit() else 0,
                self.vars["correo"].get(),
                self.vars["direccion"].get(),
                self.vars["slogan"].get()
            )

            for entry in self.entries.values():
                entry.config(state="readonly")

            self.btn_editar.config(state="normal")
            self.btn_guardar.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los cambios: {e}")

        