import ctypes
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import inventario.vistas.VentanaInventario as vi
import ventas.vistas.VentanaVentas as Vv
import ventas.vistas.VentanaReporteVentas as Vrv
import ventas.logica.ReporteVentas as Rv
import recibos.vistas.VentanaRecibos as VR
import login.LoginFrame as lf
import datosDeEmpresa.FrameEmpresa as FE
import datosDeEmpresa.empresa as E
import datosDeEmpresa.TerminosCondiciones as TC
import usuarios.FrameUsuarios as FU
import ingresos.VentanaIngresosStock as VIS
import egresos.VentanaEgresos as VE
import caja.VentanaSesionesCaja as VSC
import caja.caja as Caja
import licencia.Licenciamiento as Licenciamiento
from PIL import Image

myappid = 'anabel.pos.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x700")
        self.resizable(False,False)
        self.title("Anabel POS")
        #self.iconbitmap("anabel.ico")
        icono = tk.PhotoImage(file="anabel.png")
        self.iconphoto(True, icono)

        licencia = Licenciamiento.Licenciamiento()
        auth = licencia.validar()

        if not auth:
            messagebox.showerror("Licencia no válida", "El sistema no está activado. Por favor, contacte al soporte.")
            self.destroy()
            return

        self.login_frame = lf.LoginFrame(self, self.dibujar_frames)
        self.login_frame.pack(fill="both", expand=True)

        self.icon_inventory = self.obtener_imagen("assets/icons/inventory.png")
        self.icon_shoping = self.obtener_imagen("assets/icons/shopping.png")
        self.icon_reports = self.obtener_imagen("assets/icons/reports.png")
        self.icon_recibos = self.obtener_imagen("assets/icons/recibos.png")
        self.icon_egresos = self.obtener_imagen("assets/icons/egresos.png")
        self.icon_caja = self.obtener_imagen("assets/icons/caja.png")
        self.icon_users = self.obtener_imagen("assets/icons/users.png")
        self.icon_settings = self.obtener_imagen("assets/icons/settings.png")
        self.icon_info = self.obtener_imagen("assets/icons/info.png")
        self.icon_cerrarSesion = self.obtener_imagen("assets/icons/logout.png")

    def obtener_imagen(self, ruta):  
        archivo = Image.open(ruta)

        return ctk.CTkImage(
            light_image=archivo,
            dark_image=archivo,
            size=(20,20)
        )

    def dibujar_frames(self):

        self.resizable(True, True)

        self.usuario = self.login_frame.login.usuario
        self.empresa = E.Empresa()
        
        self.caja = Caja.Caja(self.usuario)
        self.ingresos_stock = VIS.VentanaIngresosStock(self)
        self.inventario = vi.VentanaInventario(self, self.usuario, self.ingresos_stock.actualizar_tabla)
        self.reporte_ventas = Rv.ReporteVentas()
        self.ventana_reporte_ventas = Vrv.VentanaReporteVentas(self, self.reporte_ventas)
        self.recibos = VR.VentanaRecibos(self)
        self.ventas = Vv.VentanaVentas(self, self.inventario.inventario,self.ventana_reporte_ventas,self.recibos.actualizar_recibos,
                                       self.ventana_reporte_ventas.actualizar_ventas, self.usuario, self.caja)
        self.datos_empresa = FE.FrameEmpresa(self, self.empresa, self.usuario)
        self.admin_usuarios = FU.FrameUsuarios(self)   
        self.ventana_egresos = VE.VentanaEgresos(self, self.caja)
        self.ventana_sesiones_caja = VSC.VentanaSesionesCaja(self)
        self.terminos_condiciones = TC.TerminosYCondiciones(self)
        
# 1. Configuración de la barra (Navbar) con un color más sobrio
        # Un azul más profundo o un gris oscuro profesional
        navbar_color = "#2c3e50" 
        button_color = "#34495e"
        text_color = "#ffffff"

        self.frm_menu_bar = tk.Frame(self, bg=navbar_color, height=50)
        self.frm_menu_bar.pack(fill="x")
        self.frm_menu_bar.pack_propagate(False) # Mantiene el alto fijo

        # Estilo para los botones en CustomTkinter
        self.btn_style = {
            "fg_color": "#34495e",
            "text_color": "#ffffff",
            "hover_color": "#1abc9c",
            "corner_radius": 6,
            "font": ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            "height": 36,
            "width": 100,
            "cursor": "hand2"
        }

        # Botón Inventario
        self.btn_inventario = ctk.CTkButton(
            self.frm_menu_bar, 
            text="Inventario",
            image=self.icon_inventory,
            command=lambda: self.draw_frames(self.inventario, self.btn_inventario),
            **self.btn_style
        )
        self.btn_inventario.pack(side="left", padx=3, pady=7)

        # Botón Ventas
        self.btn_ventas = ctk.CTkButton(
            self.frm_menu_bar,
            text="Ventas", 
            image=self.icon_shoping,
            command=lambda: self.draw_frames(self.ventas, self.btn_ventas),
            **self.btn_style
        )
        self.btn_ventas.pack(side="left", padx=3, pady=7)

        # Botón Reporte de Ventas
        self.btn_reporte_ventas = ctk.CTkButton(
            self.frm_menu_bar, 
            text="R. Ventas",
            image=self.icon_reports,
            command=lambda: self.draw_frames(self.ventana_reporte_ventas, self.btn_reporte_ventas),
            **self.btn_style
        )
        self.btn_reporte_ventas.pack(side="left", padx=3, pady=7)

        self.btn_recibos = ctk.CTkButton(
            self.frm_menu_bar, 
            text="Recibos",
            image=self.icon_recibos, 
            command=lambda: self.draw_frames(self.recibos, self.btn_recibos),
            **self.btn_style
        )
        self.btn_recibos.pack(side="left", padx=3, pady=7)

        self.btn_ingresos_stock = ctk.CTkButton(
            self.frm_menu_bar,
            text="R.I. Stock", 
            image=self.icon_reports,
            command=lambda: self.draw_frames(self.ingresos_stock, self.btn_ingresos_stock),
            **self.btn_style
        )
        self.btn_ingresos_stock.pack(side="left", padx=3, pady=7)

        self.btn_egresos = ctk.CTkButton(
            self.frm_menu_bar,
            text="Egresos",
            image=self.icon_egresos,
            command=lambda: self.draw_frames(self.ventana_egresos, self.btn_egresos),
            **self.btn_style
        )
        self.btn_egresos.pack(side="left", padx=3, pady=7)

        self.btn_sesiones_caja = ctk.CTkButton(
            self.frm_menu_bar,
            text="Sesiones Caja",
            image=self.icon_caja,
            command=lambda: self.draw_frames(self.ventana_sesiones_caja, self.btn_sesiones_caja),
            **self.btn_style
        )
        self.btn_sesiones_caja.pack(side="left", padx=3, pady=7)

        # Botón Datos de Empresa
        self.btn_datos_empresa = ctk.CTkButton(
            self.frm_menu_bar, 
            text="Configuración",
            image=self.icon_settings,
            command=lambda: self.draw_frames(self.datos_empresa, self.btn_datos_empresa),
            **self.btn_style
        )
        self.btn_datos_empresa.pack(side="left", padx=3, pady=7)
        
        if self.usuario.rol == "admin":

            # Botón Usuarios
            self.btn_usuarios = ctk.CTkButton(
                self.frm_menu_bar, 
                text="Usuarios",
                image=self.icon_users,
                command=lambda: self.draw_frames(self.admin_usuarios, self.btn_usuarios),
                **self.btn_style
            )
            self.btn_usuarios.pack(side="left", padx=3, pady=7)

        # Botón Términos y Condiciones
        self.btn_terminos = ctk.CTkButton(
            self.frm_menu_bar, 
            text="Info",
            image=self.icon_info,
            command=lambda: self.draw_frames(self.terminos_condiciones, self.btn_terminos),
            **self.btn_style
        )
        self.btn_terminos.pack(side="left", padx=3, pady=7)

        # Botón Cerrar Sesión (Alineado a la derecha)
        self.btn_logout = ctk.CTkButton(
            self.frm_menu_bar, 
            text="Cerrar",
            image=self.icon_cerrarSesion,
            command=self.cerrar_sesion,
            **self.btn_style
        )
        # Personalización de color para resaltar la acción de salida
        self.btn_logout.configure(fg_color="#a93226", hover_color="#e74c3c")
        self.btn_logout.pack(side="right", padx=6, pady=7)

        self.frames = [self.inventario, self.ventas, self.ventana_reporte_ventas, self.recibos, self.datos_empresa, 
                       self.admin_usuarios, self.ingresos_stock, self.ventana_egresos, self.ventana_sesiones_caja, self.terminos_condiciones]
        #self.ventas.pack(fill="both", expand=True)

        self.botones = [self.btn_inventario, self.btn_ventas, self.btn_reporte_ventas, self.btn_recibos, self.btn_datos_empresa, 
                        self.btn_usuarios if self.usuario.rol == "admin" else None, self.btn_ingresos_stock, self.btn_egresos, 
                        self.btn_sesiones_caja, self.btn_terminos, self.btn_logout]

        self.draw_frames(self.ventas, self.btn_ventas)

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea salir del sistema?"):
            # Limpiar todos los elementos de la ventana actual
            for widget in self.winfo_children():
                widget.destroy()

            self.state("normal")
            
            # Reiniciar al estado de Login
            self.login_frame = lf.LoginFrame(self, self.dibujar_frames)
            self.login_frame.pack(fill="both", expand=True)

            self.geometry("1200x700")
            self.resizable(False, False)

    def draw_frames(self, new_frame, boton=None):
        for frame in self.frames:
            frame.pack_forget()
        new_frame.pack(fill="both", expand=True)

        # Resetear el estilo de todos los botones
        for btn in self.botones:
            if btn:
                if btn == self.btn_logout:
                    btn.configure(fg_color="#a93226")
                else:
                    btn.configure(fg_color="#34495e")

        # Aplicar estilo al botón activo
        if boton:
            boton.configure(fg_color="#1abc9c")

ventana = VentanaPrincipal()
ventana.mainloop()