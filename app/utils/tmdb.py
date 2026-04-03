import httpx
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

def buscar_en_tmdb(query: str, type: str = "movie") -> list:
    endpoint = "movie" if type == "movie" else "tv"
    url = f"{TMDB_BASE_URL}/search/{endpoint}"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "es-ES"
    }
    response = httpx.get(url, params=params)
    data = response.json()
    return data.get("results", [])

def obtener_detalle_tmdb(tmdb_id: int, type: str = "movie") -> dict:
    endpoint = "movie" if type == "movie" else "tv"
    url = f"{TMDB_BASE_URL}/{endpoint}/{tmdb_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "es-ES"
    }
    response = httpx.get(url, params=params)
    return response.json()