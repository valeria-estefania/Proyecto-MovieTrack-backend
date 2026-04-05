from utils.tmdb import obtener_recomendaciones_tmdb

def obtener_recomendaciones(tmdb_id: int, type: str = "movie") -> list:
    return obtener_recomendaciones_tmdb(tmdb_id, type)