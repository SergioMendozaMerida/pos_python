import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import egresos.Egresos as E
import egresos.FormRegistrarEgreso as FRE
import datetime
import egresos.CrearReporteEgresos as CRE
from assets.icons.AnabellIcons import AnabellIcons

class VentanaEgresos(ctk.CTkFrame):
    def __init__(self, parent, caja):
        super().__init__(parent, fg_color="#f4f6f9")

        self.caja = caja
        self.registros = E.Egresos()
        
        # Configuración de colores
        self.color_fondo = "#f4f6f9"
        self.color_primario = "#2c3e50"
        self.color_secundario = "#0984e3"
        self.color_boton = "#27ae60"
        self.color_cancelar = "#d63031"
        self.color_border = "#dfe6e9"

        self.color_btn_filtro = "#0984e3"
        self.color_btn_filtro_seleccionado = "#5dade2"

        self.icono_buscar = AnabellIcons.obtener_imagen("search_inventory")
        self.icono_limpiar = AnabellIcons.obtener_imagen("clean")
        self.icono_registrar = AnabellIcons.obtener_imagen("add")
        self.icono_exportar = AnabellIcons.obtener_imagen("export")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 1. FRAME DE FILTROS
        self.frame_contenedor_filtros = ctk.CTkFrame(
            self, 
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color=self.color_border
        )
        self.frame_contenedor_filtros.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.frame_contenedor_filtros.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.frame_contenedor_filtros,
            text="Filtros de Egresos",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_primario
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(10, 8))

        # Fila horizontal única para los 4 campos y el botón buscar
        self.frame_filtros = ctk.CTkFrame(self.frame_contenedor_filtros, fg_color="transparent")
        self.frame_filtros.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 5))
        self.frame_filtros.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame_filtros.grid_columnconfigure(5, weight=0)
        self.frame_filtros.grid_columnconfigure(6, weight=0)

        # 1. Razón / Concepto
        ctk.CTkLabel(
            self.frame_filtros, 
            text="Razón / Concepto:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(0, 2))
        
        self.entry_razon = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Razón o concepto...",
            height=36
        )
        self.entry_razon.grid(row=1, column=0, sticky="ew", padx=(0, 10))

        # 2. Proveedor
        ctk.CTkLabel(
            self.frame_filtros, 
            text="Proveedor:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=0, column=1, sticky="w", padx=(0, 5), pady=(0, 2))
        
        self.entry_proveedor = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Proveedor...",
            height=36
        )
        self.entry_proveedor.grid(row=1, column=1, sticky="ew", padx=(0, 10))

        # 3. Fecha Inicio
        ctk.CTkLabel(
            self.frame_filtros, 
            text="Fecha inicio:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=0, column=2, sticky="w", padx=(0, 5), pady=(0, 2))
        
        self.entry_fecha_inicio = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="YYYY-MM-DD",
            height=36
        )
        self.entry_fecha_inicio.grid(row=1, column=2, sticky="ew", padx=(0, 10))

        # 4. Fecha Fin
        ctk.CTkLabel(
            self.frame_filtros, 
            text="Fecha fin:", 
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        ).grid(row=0, column=3, sticky="w", padx=(0, 5), pady=(0, 2))
        
        self.entry_fecha_fin = ctk.CTkEntry(
            self.frame_filtros, 
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="YYYY-MM-DD",
            height=36
        )
        self.entry_fecha_fin.grid(row=1, column=3, sticky="ew", padx=(0, 10))

        # 5. Botón Buscar
        self.btn_buscar = ctk.CTkButton(
            self.frame_filtros,
            text="Buscar",
            image=self.icono_buscar,
            fg_color=self.color_secundario,
            hover_color="#74b9ff",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            width=100,
            command=self.filtrar_egresos
        )
        self.btn_buscar.grid(row=1, column=5, sticky="ew", padx=3)

        # Eventos Enter para buscar
        self.entry_razon.bind("<Return>", lambda e: self.filtrar_egresos())
        self.entry_proveedor.bind("<Return>", lambda e: self.filtrar_egresos())
        self.entry_fecha_inicio.bind("<Return>", lambda e: self.filtrar_egresos())
        self.entry_fecha_fin.bind("<Return>", lambda e: self.filtrar_egresos())

        self.lbl_filtros_pre = ctk.CTkLabel(
            self.frame_filtros,
            text="Filtros predeterminados:",
            text_color=self.color_primario,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        self.lbl_filtros_pre.grid(row=0, column=4, sticky="w", padx=3, pady=(0, 2))

        self.filtros_pre = ctk.CTkComboBox(
            self.frame_filtros,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            values=["Todo", "Hoy", "Semana", "Mes", "Año"],
            height=36,
            state="readonly",
            command=lambda valor: {
                "Todo": self.limpiar_filtros,
                "Hoy": self.filtrar_hoy,
                "Semana": self.filtrar_semana,
                "Mes": self.filtrar_mes,
                "Año": self.filtrar_anio
            }[valor]()
        )
        self.filtros_pre.set("Todo")
        self.filtros_pre.grid(row=1, column=4, sticky="ew", padx=3)

        self.btn_limpiar = ctk.CTkButton(
            self.frame_filtros,
            text="Limpiar",
            image=self.icono_limpiar,
            fg_color=self.color_cancelar,
            hover_color="#c0392b",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=36,
            command=self.limpiar_filtros
        )
        self.btn_limpiar.grid(row=1, column=6, sticky="ew", padx=3)

        # 2. FRAME TABLA
        self.frame_tabla = ctk.CTkFrame(
            self,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color=self.color_border
        )
        self.frame_tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.frame_tabla.grid_rowconfigure(1, weight=1)
        self.frame_tabla.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.frame_tabla,
            text="Historial de Egresos",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.color_primario
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(10, 5))

        tabla_inner_frame = ctk.CTkFrame(self.frame_tabla, fg_color="transparent")
        tabla_inner_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        tabla_inner_frame.grid_rowconfigure(0, weight=1)
        tabla_inner_frame.grid_columnconfigure(0, weight=1)

        self.tabla_egresos = ttk.Treeview(
            tabla_inner_frame, 
            columns=("Fecha", "Usuario", "Razon", "Proveedor", "Monto"), 
            show="headings", 
            height=10
        )
        
        self.tabla_egresos.heading("Fecha", text="Fecha")
        self.tabla_egresos.heading("Usuario", text="Usuario")
        self.tabla_egresos.heading("Razon", text="Razón / Concepto")
        self.tabla_egresos.heading("Proveedor", text="Proveedor")
        self.tabla_egresos.heading("Monto", text="Monto")

        self.tabla_egresos.column("Fecha", width=120, anchor="center")
        self.tabla_egresos.column("Usuario", width=120, anchor="center")
        self.tabla_egresos.column("Razon", width=250, anchor="w")
        self.tabla_egresos.column("Proveedor", width=150, anchor="w")
        self.tabla_egresos.column("Monto", width=100, anchor="e")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#2d3436",
                        rowheight=34,
                        fieldbackground="#ffffff",
                        borderwidth=0,
                        font=("Segoe UI", 12))

        style.configure("Treeview.Heading",
                        background="#f1f2f6",
                        foreground="#2d3436",
                        relief="flat",
                        font=("Segoe UI", 12, "bold"))

        style.map("Treeview", 
                background=[('selected', "#74b9ff")],
                foreground=[('selected', "white")])

        self.scroll_y = ttk.Scrollbar(tabla_inner_frame, orient="vertical", command=self.tabla_egresos.yview)
        self.tabla_egresos.configure(yscrollcommand=self.scroll_y.set)
        self.tabla_egresos.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")

        # 3. BOTONES DE ACCIÓN
        self.frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones.grid(row=2, column=0, sticky="ew", padx=10, pady=(2, 10))

        self.btn_registrar = ctk.CTkButton(
            self.frame_botones,
            text="Registrar Nuevo Egreso",
            image=self.icono_registrar,
            fg_color="#00b894",
            hover_color="#009476",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=40,
            command=self.abrir_formulario_registro
        )
        self.btn_registrar.pack(side="left", padx=(0, 10))

        self.btn_exportar_excel = ctk.CTkButton(
            self.frame_botones,
            text="Exportar a Excel",
            image=self.icono_exportar,
            fg_color="#27ae60",
            hover_color="#229954",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            height=40,
            command=self.exportar_egresos_excel
        )
        self.btn_exportar_excel.pack(side="left")

        self.actualizar_tabla()

    def exportar_egresos_excel(self):
        if not self.registros.egresos:
            messagebox.showwarning("Advertencia", "No hay egresos para exportar.")
            return
        reporte = CRE.CrearReporteEgresos(self.registros)
        reporte.crear_reporte_excel()
        messagebox.showinfo("Éxito", f"Reporte de egresos exportado exitosamente a {reporte.ruta_documentos}/{reporte.nombre}.xlsx")

    def actualizar_tabla(self):
        self.registros.obtener_egresos()
        self.mostrar_egresos()

    def mostrar_egresos(self):
        for item in self.tabla_egresos.get_children():
            self.tabla_egresos.delete(item)

        for e in self.registros.egresos:
            self.tabla_egresos.insert("", tk.END, values=(
                e.fecha, e.usuario, e.razon, e.proveedor, f"Q {float(e.monto):,.2f}"
            ))

    def abrir_formulario_registro(self):
        if self.caja.estado == False:
            messagebox.showerror("Caja Cerrada", "Debe abrir la caja para poder registrar un egreso.")
            return

        FRE.FormRegistrarEgreso(self, self.caja, self.actualizar_tabla)

    def filtrar_egresos(self):
        self.registros.filtrar_egresos(self.entry_razon.get(), self.entry_proveedor.get(), self.entry_fecha_inicio.get(), self.entry_fecha_fin.get())
        self.mostrar_egresos()

    def filtrar_hoy(self):
        self.limpiar_filtros_entries()
        hoy = datetime.date.today().strftime("%Y-%m-%d")
        self.registros.filtrar_egresos("", "", hoy, hoy)
        self.mostrar_egresos()

    def filtrar_semana(self):
        self.limpiar_filtros_entries()
        hoy = datetime.date.today()
        inicio = (hoy - datetime.timedelta(days=hoy.weekday())).strftime("%Y-%m-%d")
        fin = hoy.strftime("%Y-%m-%d")
        self.registros.filtrar_egresos("", "", inicio, fin)
        self.mostrar_egresos()

    def filtrar_mes(self):
        self.limpiar_filtros_entries()
        hoy = datetime.date.today()
        inicio = hoy.replace(day=1).strftime("%Y-%m-%d")
        self.registros.filtrar_egresos("", "", inicio, "")
        self.mostrar_egresos()

    def filtrar_anio(self):
        self.limpiar_filtros_entries()
        inicio = datetime.date(datetime.date.today().year, 1, 1).strftime("%Y-%m-%d")
        self.registros.filtrar_egresos("", "", inicio, "")
        self.mostrar_egresos()

    def limpiar_filtros_entries(self):
        self.entry_razon.delete(0, tk.END)
        self.entry_proveedor.delete(0, tk.END)
        self.entry_fecha_inicio.delete(0, tk.END)
        self.entry_fecha_fin.delete(0, tk.END)

    def limpiar_filtros(self):
        self.limpiar_filtros_entries()
        self.actualizar_tabla()