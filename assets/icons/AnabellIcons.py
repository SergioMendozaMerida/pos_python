import os
import sys
import customtkinter as ctk
from PIL import Image

class AnabellIcons:
    # 1. Ruta absoluta basada en la ubicación de este archivo (evita fallos de directorio)
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    _RUTA_ICONOS = os.path.join(_BASE_DIR)

    # 2. Diccionario de Caché para reutilizar objetos CTkImage en memoria
    _cache = {}

    @classmethod
    def obtener_imagen(cls, nombre: str, size: tuple = (18, 18), nombre_dark: str = None) -> ctk.CTkImage:
        """
        Carga y devuelve un CTkImage optimizado con sistema de caché.
        
        :param nombre: Nombre del archivo sin extensión (ej: 'inventory')
        :param size: Tupla (ancho, alto) para el tamaño del icono
        :param nombre_dark: (Opcional) Nombre del icono para el modo oscuro
        """
        clave_cache = f"{nombre}_{nombre_dark}_{size}"

        # Si el icono ya fue cargado previamente con este tamaño, lo devolvemos desde la memoria
        if clave_cache in cls._cache:
            return cls._cache[clave_cache]

        ruta_light = os.path.join(cls._RUTA_ICONOS, f"{nombre}.png")

        try:
            archivo_light = Image.open(ruta_light)
            
            # Carga alternativa para modo oscuro si se especifica
            if nombre_dark:
                ruta_dark = os.path.join(cls._RUTA_ICONOS, f"{nombre_dark}.png")
                archivo_dark = Image.open(ruta_dark)
            else:
                archivo_dark = archivo_light

            # Crear el icono de CustomTkinter
            icono_ctk = ctk.CTkImage(
                light_image=archivo_light,
                dark_image=archivo_dark,
                size=size
            )

            # Guardar en caché antes de retornar
            cls._cache[clave_cache] = icono_ctk
            return icono_ctk

        except FileNotFoundError:
            print(f"[Error AnabellIcons] No se encontró el archivo de icono: '{ruta_light}'", file=sys.stderr)
            return None
        except Exception as e:
            print(f"[Error AnabellIcons] Error inesperado al cargar '{nombre}': {e}", file=sys.stderr)
            return None