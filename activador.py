import subprocess
import sqlite3

class Activador:

    def __init__(self):
        try:
            licencia = self.obtener_uuid_sistema()
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("UPDATE datos_equipo SET uuid =? WHERE id_equipo = 1", (licencia,))
            conexion.commit()
            conexion.close()
            print("activación realizada exitosamente")
        except Exception as e:
            print(f"Error al activar el prodcuto {e}")

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


Activador()