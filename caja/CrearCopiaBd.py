import sqlite3
import os
from datetime import datetime

class BackUpBd:
    
    def hacer_backup(self):

        # Ruta donde está tu base de datos (misma carpeta que main.py)
        ruta_bd = os.path.join(
            os.path.dirname(__file__),
            "..",
            "db_inventario.db"   # cambia esto por el nombre real de tu BD
        )

        ruta_bd = os.path.abspath(ruta_bd)

        # Carpeta destino en C:
        carpeta_backup = r"C:\copia_db_pos"

        # Crear carpeta si no existe
        if not os.path.exists(carpeta_backup):
            os.makedirs(carpeta_backup)

        # Nombre del backup con fecha y hora
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        archivo_backup = os.path.join(
            carpeta_backup,
            f"backup_{fecha}.db"
        )

        # Crear copia usando SQLite Backup API
        conexion_origen = sqlite3.connect(ruta_bd)
        conexion_destino = sqlite3.connect(archivo_backup)

        with conexion_destino:
            conexion_origen.backup(conexion_destino)

        conexion_destino.close()
        conexion_origen.close()