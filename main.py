import os
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Servidor Avanzado Kodi Clone")

# Configuración segura de tus 4 cuentas de TeraBox mediante variables de entorno
CUENTAS_TERABOX = {
    "cuenta_1": {"usuario": os.getenv("TERABOX_USER_1", "correo1@gmail.com"), "clave": os.getenv("TERABOX_PASS_1", "password123")},
    "cuenta_2": {"usuario": os.getenv("TERABOX_USER_2", "correo2@gmail.com"), "clave": os.getenv("TERABOX_PASS_2", "password456")},
    "cuenta_3": {"usuario": os.getenv("TERABOX_USER_3", "correo3@gmail.com"), "clave": os.getenv("TERABOX_PASS_3", "password789")},
    "cuenta_4": {"usuario": os.getenv("TERABOX_USER_4", "correo4@gmail.com"), "clave": os.getenv("TERABOX_PASS_4", "password012")},
}

def conectar_terabox_y_extraer_videos(cuenta_id: str):
    """
    Función interna: Aquí el servidor usa las credenciales para entrar a TeraBox
    y extraer las URLs reales de tus archivos MP4/MKV.
    """
    credenciales = CUENTAS_TERABOX.get(cuenta_id)
    # Simulación de extracción de enlaces directos de alta velocidad desde TeraBox
    return [
        {
            "titulo": f"Película TeraBox ({cuenta_id})",
            "caratula": "https://unsplash.com",
            "video_url": "https://googleapis.com"
        }
    ]

def extraer_contenido_addon_alfa():
    """
    Función interna: Ejecuta el raspado de enlaces imitando al addon Alfa de Kodi
    """
    return [
        {
            "titulo": "Serie desde Addon Alfa - Cap 1",
            "caratula": "https://unsplash.com",
            "video_url": "https://googleapis.com"
        }
    ]

@app.get("/contenido")
def obtener_todo_el_contenido():
    # El servidor unifica todas las fuentes en un solo JSON estructurado para Roku
    contenido_cuenta_1 = conectar_terabox_y_extraer_videos("cuenta_1")
    contenido_cuenta_2 = conectar_terabox_y_extraer_videos("cuenta_2")
    contenido_alfa = extraer_contenido_addon_alfa()
    
    peliculas = contenido_cuenta_1 + contenido_cuenta_2
    series = contenido_alfa
    
    return {
        "PELÍCULAS": peliculas,
        "SERIES": series,
        "VIDEOS": [
            {
                "titulo": "Video Familiar - Cuenta 3",
                "caratula": "https://unsplash.com",
                "video_url": "https://googleapis.com"
            }
        ],
        "BIBLIOTECA": peliculas + series, # Muestra todo lo unificado aquí
        "COMPLEMENTOS": [
            {
                "titulo": "Addon Alfa Instalado",
                "caratula": "https://unsplash.com",
                "video_url": "" # Los complementos listan secciones, no un video directo
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
