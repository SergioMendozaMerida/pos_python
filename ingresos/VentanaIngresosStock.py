import tkinter as tk
from tkinter import ttk, messagebox
import ingresos.ingresos as I
import datetime

class VentanaIngresosStock(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.registros = I.Ingresos()
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
        tk.Label(self.frame_filtros, text="Producto:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.entry_producto = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_producto.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=(0, 10))

        tk.Label(self.frame_filtros, text="Proveedor:", bg="#f0f0f0").grid(row=0, column=1, sticky="w", padx=(0, 5))
        self.entry_proveedor = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_proveedor.grid(row=1, column=1, sticky="ew", padx=(0, 5), pady=(0, 10))

        self.btn_buscar = tk.Button(self.frame_filtros, text="Buscar", bg="#0984e3", fg="white", relief="flat", cursor="hand2", width=15, command=self.filtrar_ingresos)
        self.btn_buscar.grid(row=1, column=2, sticky="w", padx=(5, 0), pady=(0, 10))

        tk.Label(self.frame_filtros, text="Fecha inicio (AAAA-MM-DD):", bg="#f0f0f0").grid(row=2, column=0, sticky="w", padx=(0, 5))
        self.entry_fecha_inicio = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_fecha_inicio.grid(row=3, column=0, sticky="ew", padx=(0, 5), pady=(0, 10))

        tk.Label(self.frame_filtros, text="Fecha fin (AAAA-MM-DD):", bg="#f0f0f0").grid(row=2, column=1, sticky="w", padx=(0, 5))
        self.entry_fecha_fin = tk.Entry(self.frame_filtros, bg="#ffffff", relief="flat", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor="#0984e3")
        self.entry_fecha_fin.grid(row=3, column=1, sticky="ew", padx=(0, 5), pady=(0, 10))

        # Eventos Enter para buscar
        self.entry_producto.bind("<Return>", lambda e: self.filtrar_ingresos())
        self.entry_proveedor.bind("<Return>", lambda e: self.filtrar_ingresos())

        # --- BOTONES PREDETERMINADOS ---
        self.frame_filtros_pre = tk.Frame(self.frame_filtros, bg="#f0f0f0")
        self.frame_filtros_pre.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(5, 0))
        self.frame_filtros_pre.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.btn_hoy = tk.Button(self.frame_filtros_pre, text="Ingresos de Hoy", bg=self.color_btn_filtro, fg="white", relief="flat", cursor="hand2", command=self.filtrar_hoy)
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

        self.tabla_ingresos = ttk.Treeview(self.frame_tabla, columns=( "Fecha", "Producto", "Cantidad", "Precio Compra", "Precio Venta", 
                                                          "Proveedor", "Usuario"), show="headings")
        
        self.tabla_ingresos.heading("Fecha", text="Fecha")
        self.tabla_ingresos.heading("Producto", text="Producto")
        self.tabla_ingresos.heading("Cantidad", text="Cantidad")
        self.tabla_ingresos.heading("Precio Compra", text="Precio Compra")
        self.tabla_ingresos.heading("Precio Venta", text="Precio Venta")
        self.tabla_ingresos.heading("Proveedor", text="Proveedor")
        self.tabla_ingresos.heading("Usuario", text="Usuario")

        self.tabla_ingresos.column("Fecha", width=130, anchor="center")
        self.tabla_ingresos.column("Producto", width=180, anchor="w")
        self.tabla_ingresos.column("Cantidad", width=80, anchor="center")
        self.tabla_ingresos.column("Precio Compra", width=100, anchor="e")
        self.tabla_ingresos.column("Precio Venta", width=100, anchor="e")
        self.tabla_ingresos.column("Proveedor", width=130, anchor="w")
        self.tabla_ingresos.column("Usuario", width=100, anchor="center")

        self.scroll_y = tk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla_ingresos.yview)
        self.tabla_ingresos.configure(yscrollcommand=self.scroll_y.set)
        self.tabla_ingresos.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")

        self.actualizar_tabla()

    def actualizar_tabla(self):
        # 1. Forzamos a la lógica a traer los datos más recientes de la base de datos
        self.registros.obtener_ingresos()
        # 2. Mostramos los datos en la interfaz
        self.mostrar_ingresos()

    def mostrar_ingresos(self):
        # Limpia la tabla y dibuja lo que esté actualmente en self.registros.ingresos
        for item in self.tabla_ingresos.get_children():
            self.tabla_ingresos.delete(item)

        for ingreso in self.registros.ingresos:
            self.tabla_ingresos.insert("", tk.END, values=(
                ingreso.fecha_ingreso,
                ingreso.producto,
                ingreso.cantidad,
                f"Q {float(ingreso.precio_compra):,.2f}",
                f"Q {float(ingreso.precio_venta):,.2f}",
                ingreso.proveedor,
                ingreso.usuario
            ))

    def filtrar_ingresos(self):
        producto = self.entry_producto.get()
        proveedor = self.entry_proveedor.get()
        f_inicio = self.entry_fecha_inicio.get()
        f_fin = self.entry_fecha_fin.get()

        self.registros.filtrar_ingresos(producto, proveedor, f_inicio, f_fin)
        self.mostrar_ingresos()
        self.limpiar_botones_estilo()

    def filtrar_hoy(self):
        self.limpiar_filtros_entries()
        hoy = datetime.date.today().strftime("%Y-%m-%d")
        self.registros.filtrar_ingresos("", "", hoy, hoy)
        self.mostrar_ingresos()
        self.resaltar_boton(self.btn_hoy)

    def filtrar_semana(self):
        self.limpiar_filtros_entries()
        hoy = datetime.date.today()
        inicio = (hoy - datetime.timedelta(days=hoy.weekday())).strftime("%Y-%m-%d")
        fin = hoy.strftime("%Y-%m-%d")
        self.registros.filtrar_ingresos("", "", inicio, fin)
        self.mostrar_ingresos()
        self.resaltar_boton(self.btn_semana)

    def filtrar_mes(self):
        self.limpiar_filtros_entries()
        hoy = datetime.date.today()
        inicio = hoy.replace(day=1).strftime("%Y-%m-%d")
        self.registros.filtrar_ingresos("", "", inicio, "")
        self.mostrar_ingresos()
        self.resaltar_boton(self.btn_mes)

    def filtrar_anio(self):
        self.limpiar_filtros_entries()
        inicio = datetime.date(datetime.date.today().year, 1, 1).strftime("%Y-%m-%d")
        self.registros.filtrar_ingresos("", "", inicio, "")
        self.mostrar_ingresos()
        self.resaltar_boton(self.btn_anio)

    def limpiar_filtros(self):
        self.limpiar_filtros_entries()
        self.limpiar_botones_estilo()
        self.actualizar_tabla()

    def limpiar_filtros_entries(self):
        self.entry_producto.delete(0, tk.END)
        self.entry_proveedor.delete(0, tk.END)
        self.entry_fecha_inicio.delete(0, tk.END)
        self.entry_fecha_fin.delete(0, tk.END)

    def resaltar_boton(self, btn_target):
        self.limpiar_botones_estilo()
        btn_target.config(bg=self.color_btn_filtro_seleccionado)

    def limpiar_botones_estilo(self):
        for btn in self.btns_filtros:
            btn.config(bg=self.color_btn_filtro)