import os
import requests
from fastapi import FastAPI, Query
import uvicorn

app = FastAPI(title="Explorador Completo de TeraBox para Roku")

# Llave maestra que extrajiste previamente
NDUS_COOKIE = "YSEBUv7teHuiObGR1yrTMpe-8TMfzGalKJIkLHTd"

def explorar_directorio_terabox(ruta_carpeta="/"):
    """
    Se conecta a la API de archivos de TeraBox y lee el contenido
    completo de cualquier carpeta (por defecto la raíz '/').
    """
    lista_multimedia = []
    
    # API oficial de listado de directorios de TeraBox
    url_api = "https://terabox.com"
    
    headers = {
        "Cookie": f"ndus={NDUS_COOKIE}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    params = {
        "dir": ruta_carpeta,
        "order": "name",
        "desc": "1",
        "num": "100", # Trae hasta 100 archivos por carpeta
        "page": "1"
    }
    
    try:
        respuesta = requests.get(url_api, headers=headers, params=params, timeout=10).json()
        archivos = respuesta.get("list", [])
        
        for archivo in archivos:
            nombre = archivo.get("server_filename", "Archivo sin nombre")
            es_carpeta = archivo.get("isdir") == 1
            
            # Filtramos para que Roku solo intente reproducir formatos compatibles
            if es_carpeta or nombre.lower().endswith(('.mp4', '.mkv', '.mov', '.avi')):
                # Generamos el enlace de streaming directo de TeraBox
                id_archivo = archivo.get("fs_id")
                enlace_stream = f"https://terabox.com{id_archivo}" if not es_carpeta else ""
                
                lista_multimedia.append({
                    "titulo": "[CARPETA] " + nombre if es_carpeta else nombre,
                    "caratula": archivo.get("thumbs", {}).get("url3") or "https://unsplash.com",
                    "video_url": enlace_stream,
                    "es_directorio": es_carpeta,
                    "ruta_interna": archivo.get("path")
                })
    except Exception as e:
        print(f"Error explorando TeraBox: {e}")
        
    return lista_multimedia

def buscar_en_terabox(palabra_clave: str):
    """
    Motor de búsqueda global. Busca cualquier película, serie o video 
    en todo tu TeraBox por su nombre.
    """
    resultados_busqueda = []
    url_api = "https://terabox.com"
    
    headers = {
        "Cookie": f"ndus={NDUS_COOKIE}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    params = {
        "key": palabra_clave,
        "page": "1",
        "num": "50"
    }
    
    try:
        respuesta = requests.get(url_api, headers=headers, params=params, timeout=10).json()
        archivos = respuesta.get("list", [])
        
        for archivo in archivos:
            nombre = archivo.get("server_filename", "Archivo encontrado")
            if nombre.lower().endswith(('.mp4', '.mkv', '.mov', '.avi')):
                resultados_busqueda.append({
                    "titulo": nombre,
                    "caratula": "https://unsplash.com",
                    "video_url": f"https://terabox.com{archivo.get('fs_id')}"
                })
    except Exception as e:
        print(f"Error en la búsqueda de TeraBox: {e}")
        
    return resultados_busqueda

def extractor_estilo_addon_alfa():
    peliculas_alfa = []
    url_fuente = "https://themoviedb.org"
    try:
        respuesta = requests.get(url_fuente, timeout=8).json()
        for peli in respuesta.get("results", [])[:14]:
            peliculas_alfa.append({
                "titulo": peli.get("title", "Película de Alfa"),
                "caratula": f"https://tmdb.org{peli.get('poster_path')}",
                "video_url": "https://googleapis.com"
            })
    except:
        pass
    return peliculas_alfa

@app.get("/contenido")
def obtener_todo_el_contenido(buscar: str = Query(None), ruta: str = Query("/")):
    # Si el usuario usa el buscador desde la TV
    if buscar:
        resultados = buscar_en_terabox(buscar)
        return {"PELÍCULAS": [], "SERIES": [], "VIDEOS": resultados, "BIBLIOTECA": resultados, "COMPLEMENTOS": []}

    # Si navega de forma normal por carpetas
    archivos_terabox = explorar_directorio_terabox(ruta)
    catalogo_alfa = extractor_estilo_addon_alfa()
    
    return {
        "PELÍCULAS": catalogo_alfa, 
        "SERIES": [
            {
                "titulo": "Serie Alfa - Capítulo 1",
                "caratula": "https://unsplash.com",
                "video_url": "https://googleapis.com"
            }
        ],
        "VIDEOS": archivos_terabox,  # Muestra la raíz completa de tus carpetas de TeraBox aquí
        "BIBLIOTECA": archivos_terabox,  # También mapeado en Biblioteca
        "COMPLEMENTOS": [
            {
                "titulo": "Buscador Global TeraBox Activo",
                "caratula": "https://unsplash.com",
                "video_url": ""
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
