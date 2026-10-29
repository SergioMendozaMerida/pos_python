
import sqlite3
from dataclasses import dataclass

@dataclass
class ProductoMasUtilidadesGeneradas:
    producto: str
    utilidad_total: float
    total_unidades_vendidas: int
    porcentaje: float

@dataclass
class ProductoMasUnidadesVendidas:
    producto: str
    total_unidades_vendidas: int
    total_utilidad: float
    porcentaje: float

class AnalisisDeVentas:

    def get_top_productos_mas_vendidos(self):
        total = 0
        try:
            conexion = sqlite3.connect("db_inventario.db")
            conexion.row_factory = sqlite3.Row
            cursor = conexion.cursor()
            cursor.execute('SELECT * FROM producto_mas_unidades_vendidas ORDER by total_unidades_vendidas DESC')
            res = cursor.fetchall()
            for p in res:
                total = total + int(p['total_unidades_vendidas'])
            productos: list[ProductoMasUnidadesVendidas] = []
            for p in res:
                productos.append(ProductoMasUnidadesVendidas(
                    producto = p['producto'],
                    total_unidades_vendidas = p['total_unidades_vendidas'],
                    total_utilidad = p['utilidad_total'],
                    porcentaje = int(p['total_unidades_vendidas']) * 100 / total
                ))
            return productos
        except Exception as e:
            return (False, e)
    
    def get_top_productos_menos_vendidos(self):
        total = 0
        try:
            conexion = sqlite3.connect("db_inventario.db")
            conexion.row_factory = sqlite3.Row
            cursor = conexion.cursor()
            cursor.execute('SELECT * FROM producto_mas_unidades_vendidas')
            res = cursor.fetchall()
            for p in res:
                total = total + int(p['total_unidades_vendidas'])
            productos: list[ProductoMasUnidadesVendidas] = []
            for p in res:
                productos.append(ProductoMasUnidadesVendidas(
                    producto = p['producto'],
                    total_unidades_vendidas = p['total_unidades_vendidas'],
                    total_utilidad = p['utilidad_total'],
                    porcentaje = int(p['total_unidades_vendidas']) * 100 / total
                ))
            return productos
        except Exception as e:
            return (False, e)

    def get_top_productos_mas_utilidades(self):
        total = 0
        try:
            conexion = sqlite3.connect("db_inventario.db")
            conexion.row_factory = sqlite3.Row
            cursor = conexion.cursor()
            cursor.execute('SELECT * FROM producto_mas_utilidades_generadas ORDER by utilidad_total DESC')
            res = cursor.fetchall()
            for p in res:
                total = total + int(p['utilidad_total'])
            productos: list[ProductoMasUtilidadesGeneradas] = []
            for p in res:
                productos.append(ProductoMasUtilidadesGeneradas(
                    producto = p['producto'],
                    utilidad_total = p['utilidad_total'],
                    total_unidades_vendidas = p['total_unidades_vendidas'],
                    porcentaje = int(p['utilidad_total']) * 100 / total
                ))
            return productos
        except Exception as e:
            return (False, e)
        
    def get_top_productos_menos_utilidades(self):
        total = 0
        try:
            conexion = sqlite3.connect("db_inventario.db")
            conexion.row_factory = sqlite3.Row
            cursor = conexion.cursor()
            cursor.execute('SELECT * FROM producto_mas_utilidades_generadas')
            res = cursor.fetchall()
            for p in res:
                total = total + int(p['utilidad_total'])
            productos: list[ProductoMasUtilidadesGeneradas] = []
            for p in res:
                productos.append(ProductoMasUtilidadesGeneradas(
                    producto = p['producto'],
                    utilidad_total = p['utilidad_total'],
                    total_unidades_vendidas = p['total_unidades_vendidas'],
                    porcentaje = int(p['utilidad_total']) * 100 / total
                ))
            return productos
        except Exception as e:
            return (False, e)
