import sqlite3
import os
from datetime import datetime, timedelta


class BackUpBd:
    
    def hacer_backup(self):

        # Ruta donde está tu base de datos
        ruta_bd = os.path.join(
            os.path.dirname(__file__),
            "..",
            "db_inventario.db"
        )

        ruta_bd = os.path.abspath(ruta_bd)

        # Carpeta destino
        carpeta_backup = r"C:\copia_db_pos"

        # Crear carpeta si no existe
        if not os.path.exists(carpeta_backup):
            os.makedirs(carpeta_backup)

        # Nombre del backup
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


        # Limpiar backups antiguos
        self.limpiar_backups(carpeta_backup)



    def limpiar_backups(self, carpeta_backup):

        limite = datetime.now() - timedelta(days=5)

        for archivo in os.listdir(carpeta_backup):

            ruta_archivo = os.path.join(
                carpeta_backup,
                archivo
            )

            # Solo trabajar con archivos .db
            if archivo.endswith(".db"):

                fecha_creacion = datetime.fromtimestamp(
                    os.path.getmtime(ruta_archivo)
                )

                if fecha_creacion < limite:

                    os.remove(ruta_archivo)

                    print(
                        "Backup eliminado:",
                        archivo
                    )