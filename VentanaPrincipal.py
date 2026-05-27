import tkinter as tk
import inventario.vistas.VentanaInventario as vi
import ventas.vistas.VentanaVentas as Vv
import ventas.vistas.VentanaReporteVentas as Vrv
import ventas.logica.ReporteVentas as Rv
import recibos.vistas.VentanaRecibos as VR
import login.LoginFrame as lf
import datosDeEmpresa.FrameEmpresa as FE
import datosDeEmpresa.empresa as E
import usuarios.FrameUsuarios as FU

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x700")
        #self.resizable(False,False)
        self.title("Inventario")

        self.login_frame = lf.LoginFrame(self, self.dibujar_frames)
        self.login_frame.pack(fill="both", expand=True)
        
    def dibujar_frames(self):

        self.usuario = self.login_frame.login.usuario
        self.empresa = E.Empresa()
        
        self.inventario = vi.VentanaInventario(self)
        self.reporte_ventas = Rv.ReporteVentas()
        self.ventana_reporte_ventas = Vrv.VentanaReporteVentas(self, self.reporte_ventas)
        self.recibos = VR.VentanaRecibos(self)
        self.ventas = Vv.VentanaVentas(self.inventario.inventario,self.ventana_reporte_ventas,self.recibos.actualizar_recibos,self.ventana_reporte_ventas.actualizar_ventas)
        self.datos_empresa = FE.FrameEmpresa(self, self.empresa, self.usuario)
        self.admin_usuarios = FU.FrameUsuarios(self)     

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

        # Botón Reporte de Ventas
        self.btn_reporte_ventas = tk.Button(
            self.frm_menu_bar, 
            text="📊 Reporte de Ventas", 
            command=lambda: self.draw_frames(self.ventana_reporte_ventas),
            **btn_style
        )
        self.btn_reporte_ventas.pack(side="left", fill="y", padx=2)

        self.btn_recibos = tk.Button(
            self.frm_menu_bar, 
            text="🧾 Recibos", 
            command=lambda: self.draw_frames(self.recibos),
            **btn_style
        )
        self.btn_recibos.pack(side="left", fill="y", padx=2)

        # Botón Datos de Empresa
        self.btn_datos_empresa = tk.Button(
            self.frm_menu_bar, 
            text="🏢 Datos Empresa", 
            command=lambda: self.draw_frames(self.datos_empresa),
            **btn_style
        )
        self.btn_datos_empresa.pack(side="left", fill="y", padx=2)

        if self.usuario.rol == "admin":

            # Botón Usuarios
            self.btn_usuarios = tk.Button(
                self.frm_menu_bar, 
                text="👥 Usuarios", 
                command=lambda: self.draw_frames(self.admin_usuarios),
                **btn_style
            )
            self.btn_usuarios.pack(side="left", fill="y", padx=2)

        self.frames = [self.inventario, self.ventas, self.ventana_reporte_ventas, self.recibos, self.datos_empresa, 
                       self.admin_usuarios]
        self.ventas.pack(fill="both", expand=True)

    def draw_frames(self, new_frame):
        for frame in self.frames:
            frame.pack_forget()
        new_frame.pack(fill="both", expand=True)

ventana = VentanaPrincipal()
ventana.mainloop()