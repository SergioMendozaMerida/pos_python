import tkinter as tk
from tkinter import ttk, messagebox
import caja.SesionesCaja as SC
import datetime

class VentanaSesionesCaja(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.logica = SC.SesionesCaja()
        self.configure(bg="#f0f0f0")

        self.primary_color = "#0984e3"
        self.color_btn_filtro = "#0984e3"
        self.color_btn_filtro_seleccionado = "#b6d1e6"

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- FRAME DE FILTROS ---
        self.frame_filtros = tk.Frame(self, bg="#f0f0f0", padx=10, pady=10)
        self.frame_filtros.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.frame_filtros.grid_columnconfigure((0, 1, 2), weight=1)

        # Campos de Filtro
        tk.Label(self.frame_filtros, text="Usuario:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.entry_usuario = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor=self.primary_color)
        self.entry_usuario.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=(0, 10))

        tk.Label(self.frame_filtros, text="Fecha inicio (AAAA-MM-DD):", bg="#f0f0f0").grid(row=0, column=1, sticky="w", padx=(0, 5))
        self.entry_fecha_inicio = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor=self.primary_color)
        self.entry_fecha_inicio.grid(row=1, column=1, sticky="ew", padx=(0, 5), pady=(0, 10))

        tk.Label(self.frame_filtros, text="Fecha fin (AAAA-MM-DD):", bg="#f0f0f0").grid(row=0, column=2, sticky="w", padx=(0, 5))
        self.entry_fecha_fin = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor=self.primary_color)
        self.entry_fecha_fin.grid(row=1, column=2, sticky="ew", padx=(0, 5), pady=(0, 10))

        self.btn_buscar = tk.Button(self.frame_filtros, text="Buscar", bg=self.primary_color, fg="white", relief="flat", cursor="hand2", width=15, command=self.filtrar_sesiones)
        self.btn_buscar.grid(row=1, column=3, sticky="w", padx=(5, 0), pady=(0, 10))

        # Eventos
        self.entry_usuario.bind("<Return>", lambda e: self.filtrar_sesiones())

        # --- BOTONES PREDETERMINADOS ---
        self.frame_filtros_pre = tk.Frame(self.frame_filtros, bg="#f0f0f0")
        self.frame_filtros_pre.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(5, 0))
        self.frame_filtros_pre.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.btn_hoy = tk.Button(self.frame_filtros_pre, text="Hoy", bg=self.color_btn_filtro, fg="white", relief="flat", cursor="hand2", command=self.filtrar_hoy)
        self.btn_hoy.grid(row=0, column=0, sticky="ew", padx=2)
        
        self.btn_semana = tk.Button(self.frame_filtros_pre, text="Semana", bg=self.color_btn_filtro, fg="white", relief="flat", cursor="hand2", command=self.filtrar_semana)
        self.btn_semana.grid(row=0, column=1, sticky="ew", padx=2)

        self.btn_mes = tk.Button(self.frame_filtros_pre, text="Mes", bg=self.color_btn_filtro, fg="white", relief="flat", cursor="hand2", command=self.filtrar_mes)
        self.btn_mes.grid(row=0, column=2, sticky="ew", padx=2)

        self.btn_anio = tk.Button(self.frame_filtros_pre, text="Año", bg=self.color_btn_filtro, fg="white", relief="flat", cursor="hand2", command=self.filtrar_anio)
        self.btn_anio.grid(row=0, column=3, sticky="ew", padx=2)

        self.btn_limpiar = tk.Button(self.frame_filtros_pre, text="Limpiar Filtros", bg="#636e72", fg="white", relief="flat", cursor="hand2", command=self.limpiar_filtros)
        self.btn_limpiar.grid(row=0, column=4, sticky="ew", padx=2)

        self.btns_filtros = [self.btn_hoy, self.btn_semana, self.btn_mes, self.btn_anio]

        # --- TABLA ---
        self.frame_tabla = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
        self.frame_tabla.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.frame_tabla.grid_rowconfigure(0, weight=1)
        self.frame_tabla.grid_columnconfigure(0, weight=1)

        cols = ("Fecha", "Usuario", "S. Inicial", "Ventas", "Gastos", "S. Final", "Cierre", "Dif.", "Estado")
        self.tabla_sesiones = ttk.Treeview(self.frame_tabla, columns=cols, show="headings")
        
        for col in cols:
            self.tabla_sesiones.heading(col, text=col)
            self.tabla_sesiones.column(col, width=90, anchor="center")

        self.scroll_y = tk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla_sesiones.yview)
        self.scroll_x = tk.Scrollbar(self.frame_tabla, orient="horizontal", command=self.tabla_sesiones.xview)
        self.tabla_sesiones.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.tabla_sesiones.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.actualizar_tabla()

    def actualizar_tabla(self):
        self.logica.obtener_sesiones()
        self.mostrar_sesiones()

    def mostrar_sesiones(self):
        for item in self.tabla_sesiones.get_children():
            self.tabla_sesiones.delete(item)

        for s in self.logica.sesiones:
            estado_txt = "Abierta" if s.estado else "Cerrada"
            self.tabla_sesiones.insert("", tk.END, values=(
                s.fecha, s.usuario, f"Q{s.saldo_inicial:,.2f}", f"Q{s.ingresos_ventas:,.2f}",
                f"Q{s.egresos:,.2f}", f"Q{s.saldo_final:,.2f}", f"Q{s.efectivo_final:,.2f}",
                f"Q{s.diferencia:,.2f}", estado_txt
            ))

    def filtrar_sesiones(self):
        self.logica.filtrar_sesiones(self.entry_fecha_inicio.get(), self.entry_fecha_fin.get(), self.entry_usuario.get())
        self.mostrar_sesiones()
        self.limpiar_botones_estilo()

    def filtrar_hoy(self):
        self.limpiar_filtros_entries()
        hoy = datetime.date.today().strftime("%Y-%m-%d")
        self.logica.filtrar_sesiones(hoy, hoy, "")
        self.mostrar_sesiones()
        self.resaltar_boton(self.btn_hoy)

    def filtrar_semana(self):
        self.limpiar_filtros_entries()
        hoy = datetime.date.today()
        inicio = (hoy - datetime.timedelta(days=hoy.weekday())).strftime("%Y-%m-%d")
        fin = hoy.strftime("%Y-%m-%d")
        self.logica.filtrar_sesiones(inicio, fin, "")
        self.mostrar_sesiones()
        self.resaltar_boton(self.btn_semana)

    def filtrar_mes(self):
        self.limpiar_filtros_entries()
        hoy = datetime.date.today()
        inicio = hoy.replace(day=1).strftime("%Y-%m-%d")
        self.logica.filtrar_sesiones(inicio, "", "")
        self.mostrar_sesiones()
        self.resaltar_boton(self.btn_mes)

    def filtrar_anio(self):
        self.limpiar_filtros_entries()
        inicio = datetime.date(datetime.date.today().year, 1, 1).strftime("%Y-%m-%d")
        self.logica.filtrar_sesiones(inicio, "", "")
        self.mostrar_sesiones()
        self.resaltar_boton(self.btn_anio)

    def limpiar_filtros_entries(self):
        self.entry_usuario.delete(0, tk.END)
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