import tkinter as tk
from tkinter import messagebox
import inventario.vistas.VentanaInventario as vi
import ventas.vistas.VentanaVentas as Vv
import ventas.vistas.VentanaReporteVentas as Vrv
import ventas.logica.ReporteVentas as Rv
import recibos.vistas.VentanaRecibos as VR
import login.LoginFrame as lf
import datosDeEmpresa.FrameEmpresa as FE
import datosDeEmpresa.empresa as E
import usuarios.FrameUsuarios as FU
import ingresos.VentanaIngresosStock as VIS
import egresos.VentanaEgresos as VE
import caja.VentanaSesionesCaja as VSC
import caja.caja as Caja

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
        
        self.caja = Caja.Caja(self.usuario)
        self.ingresos_stock = VIS.VentanaIngresosStock(self)
        self.inventario = vi.VentanaInventario(self, self.usuario, self.ingresos_stock.actualizar_tabla)
        self.reporte_ventas = Rv.ReporteVentas()
        self.ventana_reporte_ventas = Vrv.VentanaReporteVentas(self, self.reporte_ventas)
        self.recibos = VR.VentanaRecibos(self)
        self.ventas = Vv.VentanaVentas(self.inventario.inventario,self.ventana_reporte_ventas,self.recibos.actualizar_recibos,
                                       self.ventana_reporte_ventas.actualizar_ventas, self.usuario, self.caja)
        self.datos_empresa = FE.FrameEmpresa(self, self.empresa, self.usuario)
        self.admin_usuarios = FU.FrameUsuarios(self)   
        self.ventana_egresos = VE.VentanaEgresos(self, self.caja)
        self.ventana_sesiones_caja = VSC.VentanaSesionesCaja(self)
        
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
        self.btn_style = {
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
            command=lambda: self.draw_frames(self.inventario,  self.btn_inventario),
            **self.btn_style
        )
        self.btn_inventario.pack(side="left", fill="y", padx=2)

        # Botón Ventas
        self.btn_ventas = tk.Button(
            self.frm_menu_bar, 
            text="💰 Ventas", 
            command=lambda: self.draw_frames(self.ventas, self.btn_ventas),
            **self.btn_style
        )
        self.btn_ventas.pack(side="left", fill="y", padx=2)

        # Botón Reporte de Ventas
        self.btn_reporte_ventas = tk.Button(
            self.frm_menu_bar, 
            text="📊 Reporte de Ventas", 
            command=lambda: self.draw_frames(self.ventana_reporte_ventas, self.btn_reporte_ventas),
            **self.btn_style
        )
        self.btn_reporte_ventas.pack(side="left", fill="y", padx=2)

        self.btn_recibos = tk.Button(
            self.frm_menu_bar, 
            text="🧾 Recibos", 
            command=lambda: self.draw_frames(self.recibos, self.btn_recibos),
            **self.btn_style
        )
        self.btn_recibos.pack(side="left", fill="y", padx=2)

        self.btn_ingresos_stock = tk.Button(
            self.frm_menu_bar,
            text="📥 Ingresos de Stock", 
            command=lambda: self.draw_frames(self.ingresos_stock, self.btn_ingresos_stock),
            **self.btn_style
        )
        self.btn_ingresos_stock.pack(side="left", fill="y", padx=2)

        self.btn_egresos = tk.Button(
            self.frm_menu_bar,
            text="💸 Egresos", 
            command=lambda: self.draw_frames(self.ventana_egresos, self.btn_egresos),
            **self.btn_style
        )
        self.btn_egresos.pack(side="left", fill="y", padx=2)

        self.btn_sesiones_caja = tk.Button(
            self.frm_menu_bar,
            text="🏧 Sesiones Caja", 
            command=lambda: self.draw_frames(self.ventana_sesiones_caja, self.btn_sesiones_caja),
            **self.btn_style
        )
        self.btn_sesiones_caja.pack(side="left", fill="y", padx=2)

        # Botón Datos de Empresa
        self.btn_datos_empresa = tk.Button(
            self.frm_menu_bar, 
            text="🏢 Datos Empresa", 
            command=lambda: self.draw_frames(self.datos_empresa, self.btn_datos_empresa),
            **self.btn_style
        )
        self.btn_datos_empresa.pack(side="left", fill="y", padx=2)

        if self.usuario.rol == "admin":

            # Botón Usuarios
            self.btn_usuarios = tk.Button(
                self.frm_menu_bar, 
                text="👥 Usuarios", 
                command=lambda: self.draw_frames(self.admin_usuarios, self.btn_usuarios),
                **self.btn_style
            )
            self.btn_usuarios.pack(side="left", fill="y", padx=2)

        # Botón Cerrar Sesión (Alineado a la derecha)
        self.btn_logout = tk.Button(
            self.frm_menu_bar, 
            text="🚪 Cerrar Sesión", 
            command=self.cerrar_sesion,
            **self.btn_style
        )
        # Personalización de color para resaltar la acción de salida
        self.btn_logout.configure(bg="#a93226", activebackground="#e74c3c")
        self.btn_logout.pack(side="right", fill="y", padx=5)

        self.frames = [self.inventario, self.ventas, self.ventana_reporte_ventas, self.recibos, self.datos_empresa, 
                       self.admin_usuarios, self.ingresos_stock, self.ventana_egresos, self.ventana_sesiones_caja]
        #self.ventas.pack(fill="both", expand=True)

        self.botones = [self.btn_inventario, self.btn_ventas, self.btn_reporte_ventas, self.btn_recibos, self.btn_datos_empresa, 
                        self.btn_usuarios if self.usuario.rol == "admin" else None, self.btn_ingresos_stock, self.btn_egresos, 
                        self.btn_sesiones_caja, self.btn_logout]

        self.draw_frames(self.ventas, self.btn_ventas)

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea salir del sistema?"):
            # Limpiar todos los elementos de la ventana actual
            for widget in self.winfo_children():
                widget.destroy()
            
            # Reiniciar al estado de Login
            self.login_frame = lf.LoginFrame(self, self.dibujar_frames)
            self.login_frame.pack(fill="both", expand=True)

    def draw_frames(self, new_frame, boton=None):
        for frame in self.frames:
            frame.pack_forget()
        new_frame.pack(fill="both", expand=True)

        # Resetear el estilo de todos los botones
        for btn in self.botones:
            if btn:
                btn.configure(**self.btn_style)

        # Aplicar estilo al botón activo
        if boton:
            boton.configure(bg="#1abc9c", activebackground="#1abc9c")

ventana = VentanaPrincipal()
ventana.mainloop()