import tkinter as tk
import VentanaInventario as vi
import VentanaVentas as Vv

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x700")
        self.resizable(False,False)
        self.title("Inventario")
        self.inventario = vi.VentanaInventario(self)
        self.ventas = Vv.VentanaVentas(self.inventario.inventario)

# 1. Configuración de la barra (Navbar) con un color más sobrio
        # Un azul más profundo o un gris oscuro profesional
        navbar_color = "#2c3e50" 
        button_color = "#34495e"
        text_color = "#ffffff"

        self.frm_menu_bar = tk.Frame(self, bg=navbar_color, height=50)
        self.frm_menu_bar.pack(fill="x")
        self.frm_menu_bar.pack_propagate(False) # Mantiene el alto fijo

        # Estilo para los botones: flat, sin bordes gruesos y con cursor de mano
        # Cambia "flat": True por "relief": "flat"
        btn_style = {
            "bg": button_color,
            "fg": text_color,
            "activebackground": "#1abc9c",
            "activeforeground": "white",
            "relief": "flat",    # <--- Esta es la opción correcta
            "bd": 0,             # Border width en 0 refuerza el efecto flat
            "padx": 15,
            "font": ("Segoe UI", 10, "bold"),
            "cursor": "hand2"
        }

        # Botón Inventario
        self.btn_inventario = tk.Button(
            self.frm_menu_bar, 
            text="📦 Inventario", 
            command=lambda: self.draw_frames(self.inventario),
            **btn_style
        )
        self.btn_inventario.pack(side="left", fill="y", padx=2)

        # Botón Ventas
        self.btn_ventas = tk.Button(
            self.frm_menu_bar, 
            text="💰 Ventas", 
            command=lambda: self.draw_frames(self.ventas),
            **btn_style
        )
        self.btn_ventas.pack(side="left", fill="y", padx=2)

        self.frames = [self.inventario, self.ventas]
        self.ventas.pack(fill="both", expand=True)

    def draw_frames(self, new_frame):
        for frame in self.frames:
            frame.pack_forget()
        new_frame.pack(fill="both", expand=True)

ventana = VentanaPrincipal()
ventana.mainloop()