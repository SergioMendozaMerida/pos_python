import tkinter as tk
from tkinter import ttk, messagebox
import egresos.Egresos as E
import egresos.FormRegistrarEgreso as FRE
import datetime
import egresos.CrearReporteEgresos as CRE

class VentanaEgresos(tk.Frame):
    def __init__(self, parent, caja):
        super().__init__(parent)

        self.caja = caja

        self.registros = E.Egresos()
        self.configure(bg="#f0f0f0")

        self.color_btn_filtro = "#0984e3"
        self.color_btn_filtro_seleccionado = "#b6d1e6"

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- FRAME DE FILTROS ---
        self.frame_filtros = tk.Frame(self, bg="#f0f0f0", padx=10, pady=10)
        self.frame_filtros.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.frame_filtros.grid_columnconfigure((0, 1, 2), weight=1)

        # Campos de Filtro
        tk.Label(self.frame_filtros, text="Razón / Concepto:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.entry_razon = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_razon.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=(0, 10))

        tk.Label(self.frame_filtros, text="Proveedor:", bg="#f0f0f0").grid(row=0, column=1, sticky="w", padx=(0, 5))
        self.entry_proveedor = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_proveedor.grid(row=1, column=1, sticky="ew", padx=(0, 5), pady=(0, 10))

        self.btn_buscar = tk.Button(self.frame_filtros, text="Buscar", bg="#0984e3", fg="white", relief="flat", cursor="hand2", width=15, command=self.filtrar_egresos)
        self.btn_buscar.grid(row=1, column=2, sticky="w", padx=(5, 0), pady=(0, 10))

        tk.Label(self.frame_filtros, text="Fecha inicio (AAAA-MM-DD):", bg="#f0f0f0").grid(row=2, column=0, sticky="w", padx=(0, 5))
        self.entry_fecha_inicio = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_fecha_inicio.grid(row=3, column=0, sticky="ew", padx=(0, 5), pady=(0, 10))

        tk.Label(self.frame_filtros, text="Fecha fin (AAAA-MM-DD):", bg="#f0f0f0").grid(row=2, column=1, sticky="w", padx=(0, 5))
        self.entry_fecha_fin = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_fecha_fin.grid(row=3, column=1, sticky="ew", padx=(0, 5), pady=(0, 10))

        # Eventos Enter para buscar
        self.entry_razon.bind("<Return>", lambda e: self.filtrar_egresos())
        self.entry_proveedor.bind("<Return>", lambda e: self.filtrar_egresos())

        # --- BOTONES PREDETERMINADOS ---
        self.frame_filtros_pre = tk.Frame(self.frame_filtros, bg="#f0f0f0")
        self.frame_filtros_pre.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(5, 0))
        self.frame_filtros_pre.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.btn_hoy = tk.Button(self.frame_filtros_pre, text="Egresos de Hoy", bg=self.color_btn_filtro, fg="white", relief="flat", cursor="hand2", command=self.filtrar_hoy)
        self.btn_hoy.grid(row=0, column=0, sticky="ew", padx=2)
        
        self.btn_semana = tk.Button(self.frame_filtros_pre, text="Esta Semana", bg=self.color_btn_filtro, fg="white", relief="flat", cursor="hand2", command=self.filtrar_semana)
        self.btn_semana.grid(row=0, column=1, sticky="ew", padx=2)

        self.btn_mes = tk.Button(self.frame_filtros_pre, text="Este Mes", bg=self.color_btn_filtro, fg="white", relief="flat", cursor="hand2", command=self.filtrar_mes)
        self.btn_mes.grid(row=0, column=2, sticky="ew", padx=2)

        self.btn_anio = tk.Button(self.frame_filtros_pre, text="Este Año", bg=self.color_btn_filtro, fg="white", relief="flat", cursor="hand2", command=self.filtrar_anio)
        self.btn_anio.grid(row=0, column=3, sticky="ew", padx=2)

        self.btn_limpiar = tk.Button(self.frame_filtros_pre, text="Limpiar Filtros", bg="#636e72", fg="white", relief="flat", cursor="hand2", command=self.limpiar_filtros)
        self.btn_limpiar.grid(row=0, column=4, sticky="ew", padx=2)

        self.btns_filtros = [self.btn_hoy, self.btn_semana, self.btn_mes, self.btn_anio]

        # --- TABLA ---
        self.frame_tabla = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
        self.frame_tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.frame_tabla.grid_rowconfigure(0, weight=1)
        self.frame_tabla.grid_columnconfigure(0, weight=1)

        self.tabla_egresos = ttk.Treeview(self.frame_tabla, columns=("Fecha", "Usuario", "Razon", "Proveedor", "Monto"), show="headings")
        
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

        self.scroll_y = tk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla_egresos.yview)
        self.tabla_egresos.configure(yscrollcommand=self.scroll_y.set)
        self.tabla_egresos.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")

        # --- BOTONES DE ACCIÓN ---
        self.frame_botones = tk.Frame(self, bg="#f0f0f0", padx=10, pady=10)
        self.frame_botones.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))

        self.btn_registrar = tk.Button(
            self.frame_botones, 
            text="➕ Registrar Nuevo Egreso", 
            bg="#00b894", 
            fg="white", 
            relief="flat", 
            padx=20, 
            pady=10, 
            cursor="hand2", 
            font=("Segoe UI", 10, "bold"),
            command=self.abrir_formulario_registro
        )
        self.btn_registrar.pack(side="left")

        self.btn_exportar_excel = tk.Button(
            self.frame_botones,
            text="📤 Exportar a Excel",
            bg="#27ae60",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            activebackground="#5e49b5",
            command=self.exportar_egresos_excel
        )
        self.btn_exportar_excel.pack(side="left", padx=(10, 0))

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
        self.limpiar_botones_estilo()

    def filtrar_hoy(self):
        self.limpiar_filtros_entries()
        hoy = datetime.date.today().strftime("%Y-%m-%d")
        self.registros.filtrar_egresos("", "", hoy, hoy)
        self.mostrar_egresos()
        self.resaltar_boton(self.btn_hoy)

    def filtrar_semana(self):
        self.limpiar_filtros_entries()
        hoy = datetime.date.today()
        inicio = (hoy - datetime.timedelta(days=hoy.weekday())).strftime("%Y-%m-%d")
        fin = hoy.strftime("%Y-%m-%d")
        self.registros.filtrar_egresos("", "", inicio, fin)
        self.mostrar_egresos()
        self.resaltar_boton(self.btn_semana)

    def filtrar_mes(self):
        self.limpiar_filtros_entries()
        hoy = datetime.date.today()
        inicio = hoy.replace(day=1).strftime("%Y-%m-%d")
        self.registros.filtrar_egresos("", "", inicio, "")
        self.mostrar_egresos()
        self.resaltar_boton(self.btn_mes)

    def filtrar_anio(self):
        self.limpiar_filtros_entries()
        inicio = datetime.date(datetime.date.today().year, 1, 1).strftime("%Y-%m-%d")
        self.registros.filtrar_egresos("", "", inicio, "")
        self.mostrar_egresos()
        self.resaltar_boton(self.btn_anio)

    def limpiar_filtros_entries(self):
        self.entry_razon.delete(0, tk.END)
        self.entry_proveedor.delete(0, tk.END)
        self.entry_fecha_inicio.delete(0, tk.END)
        self.entry_fecha_fin.delete(0, tk.END)

    def limpiar_filtros(self):
        self.limpiar_filtros_entries()
        self.limpiar_botones_estilo()
        self.actualizar_tabla()

    def resaltar_boton(self, btn_target):
        self.limpiar_botones_estilo()
        btn_target.config(bg=self.color_btn_filtro_seleccionado)

    def limpiar_botones_estilo(self):
        for btn in self.btns_filtros: btn.config(bg=self.color_btn_filtro)