import sqlite3
import subprocess

class Licenciamiento:
    def __init__(self):
        self.activacion = False

        self.validar()
        
    def obtener_uuid_sistema(self):
        comando = [
            "powershell",
            "-Command",
            "(Get-CimInstance Win32_ComputerSystemProduct).UUID"
        ]

        return subprocess.check_output(
            comando,
            text=True
        ).strip()
    
    def obtener_uuid_database(self):
        try:
            conexion = sqlite3.connect("../db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT uuid FROM datos_equipo")
            uuid_db = cursor.fetchone()
            conexion.close()
            return uuid_db[0]
        except Exception as e:
            print(f"Error al obtener el UUID de la base de datos: {e}")
            return None
        
    def validar(self):
        uuid_sistema = self.obtener_uuid_sistema()
        uuid_db = self.obtener_uuid_database()
        
        if uuid_sistema == uuid_db:
            self.activacion = True
            return True
        else:
            self.activacion = False
            return False
                    
print(Licenciamiento().validar())

