from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os
from pathlib import Path
import datosDeEmpresa.empresa as empresa


class CrearRecibo:
    def __init__(self, carrito_compras):
        self.carrito_compras = carrito_compras
        self.numero_recibo = carrito_compras.numero_recibo
        self.fecha = carrito_compras.fecha
        self.total = carrito_compras.total
        self.nombre_cliente = carrito_compras.nombre_cliente
        self.direccion = carrito_compras.direccion
        self.telefono = carrito_compras.telefono
        self.dpi = carrito_compras.dpi
        self.nit = carrito_compras.nit
        self.productos = carrito_compras.productos

        self.empresa = empresa.Empresa()

        self.ruta_documentos = Path.home() / "Documents/recibos_pos"

    def crear_recibo(self):
        if self.empresa.impresion:
            self.generar_recibo_carta()
        else:
            self.generar_recibo_pequenio()


    def generar_recibo_carta(self):
        c = canvas.Canvas(str(self.ruta_documentos / f"recibo_{self.numero_recibo}.pdf"), pagesize=letter)
        width, height = letter

        # --- DATOS DE LA EMPRESA ---
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 50, self.empresa.nombre.upper())
        c.setFont("Helvetica", 9)
        c.drawString(50, height - 62, f"Dirección: {self.empresa.direccion}")
        c.drawString(50, height - 74, f"NIT: {self.empresa.nit} | Tel: {self.empresa.telefono}")
        c.drawString(50, height - 86, f"Email: {self.empresa.correo}")
        if self.empresa.slogan:
            c.setFont("Helvetica-Oblique", 9)
            c.drawString(50, height - 98, f'"{self.empresa.slogan}"')

        # --- ENCABEZADO ---
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(width/2, height - 130, "RECIBO DE VENTA")
        
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(550, height - 50, f"RECIBO No: {self.numero_recibo}")
        c.drawRightString(550, height - 65, f"FECHA: {self.fecha}")

        # --- INFORMACIÓN DEL CLIENTE (Dentro de un marco) ---
        c.setLineWidth(1)
        c.rect(50, height - 230, 512, 85) # x, y, ancho, alto
        
        c.setFont("Helvetica-Bold", 11)
        c.drawString(60, height - 165, "DATOS DEL CLIENTE")
        
        c.setFont("Helvetica", 10)
        c.drawString(65, height - 185, f"Cliente: {self.nombre_cliente}")
        c.drawString(65, height - 200, f"Dirección: {self.direccion}")
        c.drawString(65, height - 215, f"NIT: {self.nit}")
        
        c.drawString(350, height - 185, f"Teléfono: {self.telefono}")
        c.drawString(350, height - 200, f"DPI: {self.dpi}")

        # --- TABLA DE PRODUCTOS ---
        y = height - 270
        # Líneas de la tabla
        c.setLineWidth(1.5)
        c.line(50, y + 5, 562, y + 5) # Línea superior encabezado
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, y - 10, "PRODUCTO")
        c.drawRightString(350, y - 10, "PRECIO UNIT.")
        c.drawRightString(430, y - 10, "CANT.")
        c.drawRightString(550, y - 10, "SUBTOTAL")
        
        c.line(50, y - 15, 562, y - 15) # Línea inferior encabezado
        
        y -= 35
        c.setFont("Helvetica", 10)
        for p in self.productos:
            c.drawString(60, y, str(p['nombre'])[:45]) # Limitar largo de nombre
            c.drawRightString(350, y, f"Q {p['precio_venta']:,.2f}")
            c.drawRightString(430, y, str(p['cantidad']))
            c.drawRightString(550, y, f"Q {p['sub_total']:,.2f}")
            y -= 20

        # --- TOTAL ---
        y -= 10
        c.setLineWidth(1)
        c.line(400, y, 562, y)
        y -= 20
        c.setFont("Helvetica-Bold", 14)
        c.drawString(400, y, "TOTAL:")
        c.drawRightString(550, y, f"Q {self.total:,.2f}")

        # --- PIE DE PÁGINA ---
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(width/2, 50, "¡Gracias por su preferencia!")

        c.save()
        os.startfile(str(self.ruta_documentos / f"recibo_{self.numero_recibo}.pdf"))


    def generar_recibo_pequenio(self):
        # Definimos el ancho para papel térmico de 80mm (formato POS estándar)
        width = 80 * mm
        # Calculamos el alto dinámicamente según la cantidad de productos para evitar cortes
        items_count = len(self.productos)
        estimated_height = (100 + (items_count * 12) + 40) * mm
        height = max(150 * mm, estimated_height)

        c = canvas.Canvas(str(self.ruta_documentos / f"recibo_{self.numero_recibo}.pdf"), pagesize=(width, height))
        y = height - 10 * mm

        # --- DATOS DE LA EMPRESA ---
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(width/2, y, self.empresa.nombre.upper())
        y -= 5 * mm
        c.setFont("Helvetica", 7)
        c.drawCentredString(width/2, y, self.empresa.direccion)
        y -= 3.5 * mm
        c.drawCentredString(width/2, y, f"NIT: {self.empresa.nit} | Tel: {self.empresa.telefono}")
        y -= 3.5 * mm
        if self.empresa.slogan:
            c.setFont("Helvetica-Oblique", 7)
            c.drawCentredString(width/2, y, f'"{self.empresa.slogan}"')
            y -= 5 * mm
        
        c.setLineWidth(0.5)
        c.line(5 * mm, y, width - 5 * mm, y)
        y -= 7 * mm

        # --- ENCABEZADO ---
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width/2, y, "TICKET DE VENTA")
        y -= 6 * mm
        
        c.setFont("Helvetica", 8)
        c.drawCentredString(width/2, y, f"No: {self.numero_recibo}")
        y -= 4 * mm
        c.drawCentredString(width/2, y, f"Fecha: {self.fecha}")
        y -= 6 * mm
        
        c.line(5 * mm, y, width - 5 * mm, y)
        y -= 5 * mm
        
        # --- INFORMACIÓN DEL CLIENTE ---
        c.setFont("Helvetica-Bold", 8)
        c.drawString(7 * mm, y, f"CLIENTE: {self.nombre_cliente}")
        y -= 4 * mm
        c.setFont("Helvetica", 8)
        if self.nit and self.nit != "CF":
            c.drawString(7 * mm, y, f"NIT: {self.nit}")
            y -= 4 * mm
        
        y -= 2 * mm
        c.line(5 * mm, y, width - 5 * mm, y)
        y -= 6 * mm
        
        # --- PRODUCTOS ---
        c.setFont("Helvetica-Bold", 8)
        c.drawString(7 * mm, y, "Cant.  Descripción")
        c.drawRightString(width - 7 * mm, y, "Total")
        y -= 5 * mm
        
        c.setFont("Helvetica", 8)
        for p in self.productos:
            # Línea de producto: Cantidad x Nombre ... Total
            c.drawString(7 * mm, y, f"{p['cantidad']} x {str(p['nombre'])[:25]}")
            c.drawRightString(width - 7 * mm, y, f"Q{p['sub_total']:,.2f}")
            y -= 5 * mm
        
        y -= 2 * mm
        c.line(35 * mm, y, width - 7 * mm, y)
        y -= 6 * mm
        
        # --- TOTAL ---
        c.setFont("Helvetica-Bold", 11)
        c.drawString(35 * mm, y, "TOTAL:")
        c.drawRightString(width - 7 * mm, y, f"Q {self.total:,.2f}")
        
        # --- PIE ---
        y -= 15 * mm
        c.setFont("Helvetica-Oblique", 8)
        c.drawCentredString(width/2, y, "¡Gracias por su compra!")
        
        c.save()
        os.startfile(str(self.ruta_documentos / f"recibo_{self.numero_recibo}.pdf"))