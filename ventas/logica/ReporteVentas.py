import sqlite3
import ventas.logica.Venta as Venta

class ReporteVentas:
    def __init__(self):
        self.ventas = []
        self.total_ventas = 0.0
        self.tres_productos_mas_vendidos = []
        self.obtener_ventas()
        
    def obtener_ventas(self):
        conexion = sqlite3.connect("db_inventario.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM ventas")
        ventas = cursor.fetchall()
        self.ventas.clear()
        self.total_ventas = 0.0
        for v in ventas:
            self.ventas.append(Venta.Venta(v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8],v[9])) # Aquí se almacenarán las ventas, cada venta podría ser un diccionario con detalles como fecha, producto, cantidad, etc.
            self.total_ventas += int(v[7])
        conexion.close()
        self.obtener_productos_mas_vendidos("","")
        return ventas
    
    def filtrar_ventas(self, fecha_inicio, fecha_fin, nombre_producto):
        conexion = sqlite3.connect("db_inventario.db")
        cursor = conexion.cursor()

        if fecha_inicio == "":
            fecha_inicio = cursor.execute("SELECT MIN(fecha) FROM ventas").fetchone()[0]

        if fecha_fin == "":
            fecha_fin = cursor.execute("SELECT MAX(fecha) FROM ventas").fetchone()[0]

        cursor.execute("SELECT * FROM ventas WHERE fecha >= ? AND fecha <= ? AND producto LIKE ?", (fecha_inicio, fecha_fin, f"%{nombre_producto}%"))
        ventas_filtradas = cursor.fetchall()
        

        self.ventas.clear()
        self.total_ventas = 0.0
        for venta in ventas_filtradas:
            self.ventas.append(Venta.Venta(venta[0], venta[1], venta[2], venta[3], venta[4], venta[5], venta[6], venta[7], venta[8], venta[9])) # Aquí se almacenarán las ventas filtradas, cada venta podría ser un diccionario con detalles como fecha, producto, cantidad, etc.
            self.total_ventas += venta[7]
        conexion.close()
        self.obtener_productos_mas_vendidos(fecha_inicio, fecha_fin)


    #corregir o eliminar este método, está mal
    def obtener_productos_mas_vendidos(self, fecha_inicio, fecha_fin):
        conexion = sqlite3.connect("db_inventario.db")
        cursor = conexion.cursor()

        if fecha_inicio == "":
            fecha_inicio = cursor.execute("SELECT MIN(fecha) FROM ventas").fetchone()[0]

        if fecha_fin == "":
            fecha_fin = cursor.execute("SELECT MAX(fecha) FROM ventas").fetchone()[0]

        cursor.execute("""
            SELECT producto, SUM(cantidad) as total_vendido
            FROM ventas
            WHERE fecha >= ? AND fecha <= ?
            GROUP BY producto
            ORDER BY total_vendido DESC
            LIMIT 3
        """,(fecha_inicio, fecha_fin))
        productos_mas_vendidos = cursor.fetchall()
        conexion.close()
        self.tres_productos_mas_vendidos.clear()
        for venta in productos_mas_vendidos:
            self.tres_productos_mas_vendidos.append(venta[0])

        
