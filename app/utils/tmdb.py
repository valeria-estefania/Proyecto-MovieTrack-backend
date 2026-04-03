import httpx
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

HEADERS = {
    "Authorization": f"Bearer {TMDB_API_KEY}",
    "accept": "application/json"
}

def buscar_en_tmdb(query: str, type: str = "movie") -> list:
    endpoint = "movie" if type == "movie" else "tv"
    url = f"{TMDB_BASE_URL}/search/{endpoint}"
    params = {"query": query, "language": "es-ES"}
    response = httpx.get(url, headers=HEADERS, params=params)
    data = response.json()
    return data.get("results", [])

def obtener_detalle_tmdb(tmdb_id: int, type: str = "movie") -> dict:
    endpoint = "movie" if type == "movie" else "tv"
    url = f"{TMDB_BASE_URL}/{endpoint}/{tmdb_id}"
    params = {"language": "es-ES"}
    response = httpx.get(url, headers=HEADERS, params=params)
    return response.json()