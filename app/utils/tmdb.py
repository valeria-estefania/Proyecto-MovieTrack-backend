import httpx
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

HEADERS = {
    "Authorization": f"Bearer {TMDB_API_KEY}",
    "accept": "application/json"
}

def buscar_peliculas(query: str) -> list:
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {"query": query, "language": "es-ES"}
    response = httpx.get(url, headers=HEADERS, params=params)
    return response.json().get("results", [])

def buscar_series(query: str) -> list:
    url = f"{TMDB_BASE_URL}/search/tv"
    params = {"query": query, "language": "es-ES"}
    response = httpx.get(url, headers=HEADERS, params=params)
    return response.json().get("results", [])

def detalle_pelicula(tmdb_id: int) -> dict:
    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}"
    params = {"language": "es-ES"}
    response = httpx.get(url, headers=HEADERS, params=params)
    return response.json()

def detalle_serie(tmdb_id: int) -> dict:
    url = f"{TMDB_BASE_URL}/tv/{tmdb_id}"
    params = {"language": "es-ES"}
    response = httpx.get(url, headers=HEADERS, params=params)
    return response.json()

def actores_pelicula(tmdb_id: int) -> list:
    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}/credits"
    params = {"language": "es-ES"}
    response = httpx.get(url, headers=HEADERS, params=params)
    return response.json().get("cast", [])

def generos_peliculas() -> list:
    url = f"{TMDB_BASE_URL}/genre/movie/list"
    params = {"language": "es-ES"}
    response = httpx.get(url, headers=HEADERS, params=params)
    return response.json().get("genres", [])

def plataformas_pelicula(tmdb_id: int) -> dict:
    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}/watch/providers"
    response = httpx.get(url, headers=HEADERS)
    resultados = response.json().get("results", {})
    return resultados.get("CO", resultados.get("US", {}))

def recomendaciones_pelicula(tmdb_id: int) -> list:
    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}/recommendations"
    params = {"language": "es-ES"}
    response = httpx.get(url, headers=HEADERS, params=params)
    return response.json().get("results", [])

def peliculas_populares() -> list:
    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {"language": "es-ES", "page": 1}
    response = httpx.get(url, headers=HEADERS, params=params)
    return response.json().get("results", [])

def peliculas_mejor_valoradas() -> list:
    url = f"{TMDB_BASE_URL}/movie/top_rated"
    params = {"language": "es-ES", "page": 1}
    response = httpx.get(url, headers=HEADERS, params=params)
    return response.json().get("results", [])

def peliculas_recientes() -> list:
    url = f"{TMDB_BASE_URL}/movie/now_playing"
    params = {"language": "es-ES", "page": 1}
    response = httpx.get(url, headers=HEADERS, params=params)
    return response.json().get("results", [])

def series_populares() -> list:
    url = f"{TMDB_BASE_URL}/tv/popular"
    params = {"language": "es-ES", "page": 1}
    response = httpx.get(url, headers=HEADERS, params=params)
    return response.json().get("results", [])

def series_mejor_valoradas() -> list:
    url = f"{TMDB_BASE_URL}/tv/top_rated"
    params = {"language": "es-ES", "page": 1}
    response = httpx.get(url, headers=HEADERS, params=params)
    return response.json().get("results", [])

def peliculas_por_genero(genre_id: int) -> list:
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {"language": "es-ES", "with_genres": genre_id, "page": 1}
    response = httpx.get(url, headers=HEADERS, params=params)
    return response.json().get("results", [])

def series_por_genero(genre_id: int) -> list:
    url = f"{TMDB_BASE_URL}/discover/tv"
    params = {"language": "es-ES", "with_genres": genre_id, "page": 1}
    response = httpx.get(url, headers=HEADERS, params=params)
    return response.json().get("results", [])

def obtener_plataformas() -> list:
    url = f"{TMDB_BASE_URL}/watch/providers/movie"
    params = {"language": "es-ES", "watch_region": "CO"}
    response = httpx.get(url, headers=HEADERS, params=params)
    return response.json().get("results", [])
                               
def descubrir_por_plataforma(provider_id: int, type: str = "movie") -> list:
    endpoint = "movie" if type == "movie" else "tv"
    url = f"{TMDB_BASE_URL}/discover/{endpoint}"
    params = {
        "language": "es-ES",
        "watch_region": "CO",
        "with_watch_providers": provider_id,
        "page": 1
    }
    response = httpx.get(url, headers=HEADERS, params=params)
    return response.json().get("results", [])