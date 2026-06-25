import subprocess
import sqlite3
import customtkinter as ctk


class Activador(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Activador - Anabel POS")
        self.geometry("420x220")
        self.resizable(False, False)

        # Ajustes de apariencia (no críticos si la función no está disponible)
        try:
            ctk.set_appearance_mode("System")
            ctk.set_default_color_theme("blue")
        except Exception:
            pass

        # Contenedor principal centrado con padding
        container = ctk.CTkFrame(self, corner_radius=8)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        self.lbl_titulo = ctk.CTkLabel(container, text="Activador Anabel POS", font=("Segoe UI", 16, "bold"))
        self.lbl_titulo.pack(pady=(6, 12))

        # Botón central
        self.btn_activar = ctk.CTkButton(container, text="Activar", width=140, height=40, command=self.activar)
        self.btn_activar.pack(pady=(0, 12))

        # Estado (más notorio visualmente)
        self.lbl_estado = ctk.CTkLabel(container, text="Estado: Pendiente", font=("Segoe UI", 12, "bold"), text_color="#e67e22")
        self.lbl_estado.pack()

    def activar(self):
        # Deshabilitar botón para evitar múltiples pulsaciones
        try:
            self.btn_activar.configure(state="disabled")
        except Exception:
            pass

        try:
            licencia = self.obtener_uuid_sistema()
            conexion = sqlite3.connect("db_inventario.db")
            cursor = conexion.cursor()
            cursor.execute("UPDATE datos_equipo SET uuid = ? WHERE id_equipo = 1", (licencia,))
            conexion.commit()
            conexion.close()
            self.lbl_estado.configure(text="Estado: Producto Activado", text_color="#00b894")
        except Exception as e:
            # Mostrar error en etiqueta y en consola
            self.lbl_estado.configure(text="Estado: Error al activar", text_color="#d63031")
            print(f"Error al activar el producto: {e}")
        finally:
            try:
                self.btn_activar.configure(state="normal")
            except Exception:
                pass

    def obtener_uuid_sistema(self):
        comando = [
            "powershell",
            "-Command",
            "(Get-CimInstance Win32_ComputerSystemProduct).UUID"
        ]

        try:
            salida = subprocess.check_output(comando, text=True, stderr=subprocess.DEVNULL)
            return salida.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"No se pudo obtener UUID del sistema: {e}")


if __name__ == "__main__":
    Activador().mainloop()