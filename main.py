import os
import requests
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Servidor con Extractor Alfa Activo")

# Configuración segura de tus cuentas de TeraBox
CUENTAS_TERABOX = {
    "cuenta_1": {"usuario": os.getenv("TERABOX_USER_1", "correo1@gmail.com"), "clave": os.getenv("TERABOX_PASS_1", "clave1")},
    "cuenta_2": {"usuario": os.getenv("TERABOX_USER_2", "correo2@gmail.com"), "clave": os.getenv("TERABOX_PASS_2", "clave2")},
    "cuenta_3": {"usuario": os.getenv("TERABOX_USER_3", "correo3@gmail.com"), "clave": os.getenv("TERABOX_PASS_3", "clave3")},
    "cuenta_4": {"usuario": os.getenv("TERABOX_USER_4", "correo4@gmail.com"), "clave": os.getenv("TERABOX_PASS_4", "clave4")},
}

def extractor_estilo_addon_alfa():
    """
    Simula al Addon Alfa de Kodi. Se conecta por internet a un indexador 
    de películas real y extrae los títulos y carátulas actuales.
    """
    peliculas_encontradas = []
    
    # Usamos una API pública de cine para traer contenido real y dinámico
    url_fuente = "https://themoviedb.org"
    
    try:
        # El servidor simula el raspado (scraping) de la web
        respuesta = requests.get(url_fuente, timeout=8).json()
        resultados = respuesta.get("results", [])
        
        # Tomamos las primeras 14 películas para llenar la cuadrícula de tu Roku
        for peli in resultados[:14]:
            titulo = peli.get("title", "Película sin título")
            ruta_poster = peli.get("poster_path")
            
            # Construimos la URL real de la carátula de la película
            caratula_url = f"https://tmdb.org{ruta_poster}" if ruta_poster else "https://unsplash.com"
            
            peliculas_encontradas.append({
                "titulo": titulo,
                "caratula": caratula_url,
                # Enlace de video público de prueba (Roku requiere enlaces que terminen en .mp4)
                "video_url": "https://googleapis.com"
            })
            
    except Exception as e:
        print(f"Error en el extractor estilo Alfa: {e}")
        # Contenido de respaldo por si el internet del servidor falla
        peliculas_encontradas.append({
            "titulo": "Película de prueba (Error de conexión)",
            "caratula": "https://unsplash.com",
            "video_url": "https://googleapis.com"
        })
        
    return peliculas_encontradas

@app.get("/contenido")
def obtener_todo_el_contenido():
    # Activamos el extractor estilo Alfa para la pestaña de Películas
    catalogo_alfa = extractor_estilo_addon_alfa()
    
    return {
        "PELÍCULAS": catalogo_alfa, 
        "SERIES": [
            {
                "titulo": "Serie Alfa - Cap 1 (Prueba)",
                "caratula": "https://unsplash.com",
                "video_url": "https://googleapis.com"
            }
        ],
        "VIDEOS": [],
        "BIBLIOTECA": [],
        "COMPLEMENTOS": [
            {
                "titulo": "Conector Alfa Integrado v1.0",
                "caratula": "https://unsplash.com",
                "video_url": ""
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)