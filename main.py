from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Servidor Intermedio para Roku")

# Aquí simulamos la base de datos de tus contenidos con sus carátulas de prueba
BASE_DE_DATOS_MULTIMEDIA = {
    "PELÍCULAS": [
        {
            "titulo": "Película desde TeraBox Cuenta 1",
            "caratula": "https://unsplash.com",
            "video_url": "https://googleapis.com"
        },
        {
            "titulo": "Película desde Addon Alfa",
            "caratula": "https://unsplash.com",
            "video_url": "https://googleapis.com"
        }
    ],
    "SERIES": [
        {
            "titulo": "Serie de Prueba - Capítulo 1",
            "caratula": "https://unsplash.com",
            "video_url": "https://googleapis.com"
        }
    ],
    "VIDEOS": [],
    "BIBLIOTECA": [],
    "COMPLEMENTOS": []
}

@app.get("/")
def ruta_principal():
    return {"estado": "Servidor funcionando correctamente", "mensaje": "Listo para conectar con Roku"}

# Esta ruta es la que consultará tu televisión para pintar la pantalla
@app.get("/contenido")
def obtener_contenido():
    return BASE_DE_DATOS_MULTIMEDIA

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
