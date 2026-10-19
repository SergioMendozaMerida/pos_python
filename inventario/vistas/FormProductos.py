from tkinter import messagebox

import customtkinter as ctk

import categoria.Categoria as Cat
import categoria.FormAddCategoria as FAC


class FormProductos(ctk.CTkToplevel):
    def __init__(self, parent, inventario, actualizar_callback=None, usuario=None):
        super().__init__(parent)
        self.parent = parent
        self.inventario = inventario
        self.actualizar_callback = actualizar_callback
        self.usuario = usuario.usuario

        self.categorias = Cat.Categorias().lista_categorias

        self.color_fondo = "#f8f9fa"
        self.color_header = "#2c3e50"
        self.color_primario = "#0984e3"
        self.color_exito = "#00b894"
        self.color_cancelar = "#d63031"
        self.color_entrada = "#ffffff"
        self.color_texto = "#2d3436"
        self.color_borde = "#dfe6e9"

        self.title("Registro de Producto")
        x = max(0, (self.winfo_screenwidth() - 520) // 2)
        self.geometry(f"520x720+{x}+20")
        self.resizable(False, False)
        self.configure(fg_color=self.color_fondo)
        self.transient(parent)
        self.grab_set()

        self.header_frame = ctk.CTkFrame(
            self, fg_color=self.color_header, height=60, corner_radius=0
        )
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)

        ctk.CTkLabel(
            self.header_frame,
            text="Ingreso de Nuevo Producto",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="white",
        ).pack(pady=15)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        row1_frame = self._crear_fila(self.main_frame, (0, 15))
        col1_frame = self._crear_columna(row1_frame, (0, 10))
        self._crear_label(col1_frame, "Nombre *")
        self.entry_nombre = self._crear_entrada(col1_frame)

        col2_frame = self._crear_columna(row1_frame)
        self._crear_label(col2_frame, "Código")
        self.entry_codigo = self._crear_entrada(col2_frame)

        row2_frame = self._crear_fila(self.main_frame, (0, 15))
        col_cat_frame = self._crear_columna(row2_frame, (0, 10))
        self._crear_label(col_cat_frame, "Categoría")

        self.entry_categoria = ctk.CTkComboBox(
            col_cat_frame,
            font=ctk.CTkFont(family="Segoe UI", size=10),
            values=self.categorias,
            state="readonly",
            height=36,
            corner_radius=6,
            border_color=self.color_borde,
            fg_color=self.color_entrada,
            text_color=self.color_texto,
            button_color=self.color_primario,
            button_hover_color="#74b9ff",
        )
        if self.categorias:
            self.entry_categoria.set(self.categorias[0])
        self.entry_categoria.pack(fill="x")

        ctk.CTkButton(
            col_cat_frame,
            text="Categoría",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            fg_color=self.color_primario,
            hover_color="#74b9ff",
            text_color="white",
            height=36,
            command=self.abrir_frame_categoria,
        ).pack(fill="x", pady=(10, 0))

        col_pres_frame = self._crear_columna(row2_frame)
        self._crear_label(col_pres_frame, "Presentación")
        self.entry_presentacion = self._crear_entrada(col_pres_frame)

        self._crear_label(self.main_frame, "Descripción")
        self.entry_descripcion = self._crear_entrada(self.main_frame)
        self.entry_descripcion.pack(fill="x", pady=(0, 15))

        row_precios = self._crear_fila(self.main_frame, (0, 15))
        col_compra = self._crear_columna(row_precios, (0, 10))
        self._crear_label(col_compra, "Precio Compra Q")
        self.entry_precio_compra = self._crear_entrada(col_compra)

        col_venta = self._crear_columna(row_precios)
        self._crear_label(col_venta, "Precio Venta Q")
        self.entry_precio_venta = self._crear_entrada(col_venta)

        row_precios_adicionales = self._crear_fila(self.main_frame, (0, 15))
        col_blister = self._crear_columna(row_precios_adicionales, (0, 10))
        self._crear_label(col_blister, "Precio Blister Q")
        self.entry_precio_blister = self._crear_entrada(col_blister)
        self.entry_precio_blister.insert(0, "0")

        col_caja = self._crear_columna(row_precios_adicionales)
        self._crear_label(col_caja, "Precio Caja Q")
        self.entry_precio_caja = self._crear_entrada(col_caja)
        self.entry_precio_caja.insert(0, "0")

        row_stock = self._crear_fila(self.main_frame, (0, 20))
        col_stock = self._crear_columna(row_stock, (0, 10))
        self._crear_label(col_stock, "Stock *")
        self.entry_stock = self._crear_entrada(col_stock)

        col_stock_minimo = self._crear_columna(row_stock)
        self._crear_label(col_stock_minimo, "Stock mínimo *")
        self.entry_stock_minimo = self._crear_entrada(col_stock_minimo)

        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", side="bottom")

        self.btn_guardar = ctk.CTkButton(
            btn_frame,
            text="✓ Guardar",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=self.color_exito,
            hover_color="#009f7f",
            text_color="white",
            height=40,
            command=self.guardar_producto,
        )
        self.btn_guardar.pack(side="left", padx=(0, 10))

        self.btn_cancelar = ctk.CTkButton(
            btn_frame,
            text="✕ Cancelar",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=self.color_cancelar,
            hover_color="#b92525",
            text_color="white",
            height=40,
            command=self.cerrar,
        )
        self.btn_cancelar.pack(side="left")

        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.entry_nombre.focus_set()

    def _crear_fila(self, parent, pady):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=pady)
        return frame

    def _crear_columna(self, parent, padx=(0, 0)):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(side="left", fill="both", expand=True, padx=padx)
        return frame

    def _crear_label(self, parent, text):
        ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=self.color_texto,
        ).pack(anchor="w", pady=(0, 5))

    def _crear_entrada(self, parent):
        entry = ctk.CTkEntry(
            parent,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            height=36,
            corner_radius=6,
            border_width=1,
            border_color=self.color_borde,
            fg_color=self.color_entrada,
            text_color=self.color_texto,
        )
        entry.pack(fill="x")
        return entry

    def abrir_frame_categoria(self):
        categoria_ventana = FAC.FormAddCategoria(self)
        self.wait_window(categoria_ventana)
        self.actualizar_categorias()

    def actualizar_categorias(self):
        self.categorias = Cat.Categorias().lista_categorias
        self.entry_categoria.configure(values=self.categorias)

    def guardar_producto(self):
        nombre = self.entry_nombre.get().strip()
        codigo = self.entry_codigo.get().strip()
        descripcion = self.entry_descripcion.get().strip()
        presentacion = self.entry_presentacion.get().strip()
        categoria = self.entry_categoria.get().strip()
        precio_compra = self.entry_precio_compra.get().strip()
        precio_venta = self.entry_precio_venta.get().strip()
        precio_blister = self.entry_precio_blister.get().strip()
        precio_caja = self.entry_precio_caja.get().strip()
        stock = self.entry_stock.get().strip()
        stock_minimo = self.entry_stock_minimo.get().strip()

        if not nombre:
            messagebox.showwarning(
                "Validación",
                "Debe ingresar el nombre del producto.",
                parent=self,
            )
            return

        if self.inventario.buscar_producto_por_codigo(codigo):
            messagebox.showwarning(
                "Validación",
                "El código del producto ya existe, no pueden existir dos productos con el mismo código.",
                parent=self,
            )
            self.entry_codigo.focus_set()
            return

        try:
            precio_compra_val = float(precio_compra) if precio_compra else 0.0
            precio_venta_val = float(precio_venta) if precio_venta else 0.0
            precio_blister_val = float(precio_blister) if precio_blister else 0.0
            precio_caja_val = float(precio_caja) if precio_caja else 0.0
            stock_val = int(stock)
            stock_minimo_val = int(stock_minimo)
        except ValueError:
            messagebox.showwarning(
                "Validación",
                "Precio, stock y stock mínimo deben ser numéricos.",
                parent=self,
            )
            return

        self.inventario.ingresar_producto(
            nombre,
            codigo,
            descripcion,
            presentacion,
            categoria,
            precio_compra_val,
            precio_venta_val,
            precio_blister_val,
            precio_caja_val,
            stock_val,
            stock_minimo_val,
            self.usuario
        )

        if self.actualizar_callback:
            self.actualizar_callback()

        messagebox.showinfo(
            "Éxito",
            "El producto se ha ingresado correctamente.",
            parent=self,
        )
        self.destroy()

    def cerrar(self):
        self.destroy()
