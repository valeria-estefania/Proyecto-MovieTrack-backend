from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.content import Content
from app.models.genre import Genre
from app.models.platform import Platform
from app.schemas.content import ContentResponse
from app.core.dependencies import get_current_user, verify_admin
from app.utils.tmdb import (
    buscar_peliculas, buscar_series,
    detalle_pelicula, detalle_serie,
    actores_pelicula, generos_peliculas,
    plataformas_pelicula, recomendaciones_pelicula,
    peliculas_populares, peliculas_mejor_valoradas, peliculas_recientes,
    series_populares, series_mejor_valoradas,
    peliculas_por_genero, series_por_genero
)

from datetime import datetime

router = APIRouter(prefix="/content", tags=["Content"])

# ── Filtros avanzados ───────────────────────────────────
@router.get("/filter", response_model=list[ContentResponse])
def filtrar_contenido(
    type: str | None = None,
    genre: str | None = None,
    platform: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Content)

    if type:
        query = query.filter(Content.type == type)

    if genre:
        query = query.join(Content.genre).filter(
            Genre.name.ilike(f"%{genre}%")
        )

    if platform:
        query = query.join(Content.platform).filter(
            Platform.nombre.ilike(f"%{platform}%")
        )

    resultados = query.all()
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron resultados")

    return resultados


# ── Géneros de películas desde TMDB ────────────────────
@router.get("/genre/movie/list")
def generos_movie():
    generos = generos_peliculas()
    if not generos:
        raise HTTPException(status_code=404, detail="No se encontraron géneros")
    return generos


# ── Películas populares ─────────────────────────────────
@router.get("/movie/popular")
def movies_popular():
    return peliculas_populares()


# ── Películas mejor valoradas ───────────────────────────
@router.get("/movie/top_rated")
def movies_top_rated():
    return peliculas_mejor_valoradas()


# ── Películas en cines ──────────────────────────────────
@router.get("/movie/now_playing")
def movies_now_playing():
    return peliculas_recientes()


# ── Series populares ────────────────────────────────────
@router.get("/tv/popular")
def tv_popular():
    return series_populares()


# ── Series mejor valoradas ──────────────────────────────
@router.get("/tv/top_rated")
def tv_top_rated():
    return series_mejor_valoradas()


# ── Películas por género ────────────────────────────────
@router.get("/movie/genre/{genre_id}")
def movies_by_genre(genre_id: int):
    return peliculas_por_genero(genre_id)


# ── Series por género ───────────────────────────────────
@router.get("/tv/genre/{genre_id}")
def tv_by_genre(genre_id: int):
    return series_por_genero(genre_id)


# ── Buscar películas ────────────────────────────────────
@router.get("/search/movie", response_model=list[ContentResponse])
def buscar_movie(query: str, db: Session = Depends(get_db)):
    locales = db.query(Content).filter(
        Content.title.ilike(f"%{query}%"),
        Content.type == "movie"
    ).all()
    if locales:
        return locales

    resultados = buscar_peliculas(query)
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron películas")

    nuevos = []
    for item in resultados[:5]:
        existe = db.query(Content).filter(Content.tmdb_id == item["id"]).first()
        if existe:
            nuevos.append(existe)
            continue

        release = item.get("release_date", "")
        nuevo = Content(
            tmdb_id=item["id"],
            title=item.get("title", ""),
            description=item.get("overview", ""),
            type="movie",
            release_date=datetime.strptime(release[:10], "%Y-%m-%d").date() if release else None,
            poster_url=f"https://image.tmdb.org/t/p/w500{item.get('poster_path', '')}",
            rating=item.get("vote_average", 0.0)
        )
        db.add(nuevo)
        db.flush()

        for genre_id in item.get("genre_ids", []):
            genero = db.query(Genre).filter(Genre.tmdb_id == genre_id).first()
            if genero:
                nuevo.genre.append(genero)

        db.commit()
        db.refresh(nuevo)
        nuevos.append(nuevo)

    return nuevos


# ── Buscar series ───────────────────────────────────────
@router.get("/search/tv", response_model=list[ContentResponse])
def buscar_tv(query: str, db: Session = Depends(get_db)):
    locales = db.query(Content).filter(
        Content.title.ilike(f"%{query}%"),
        Content.type == "tv"
    ).all()
    if locales:
        return locales

    resultados = buscar_series(query)
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron series")

    nuevos = []
    for item in resultados[:5]:
        existe = db.query(Content).filter(Content.tmdb_id == item["id"]).first()
        if existe:
            nuevos.append(existe)
            continue

        release = item.get("first_air_date", "")
        nuevo = Content(
            tmdb_id=item["id"],
            title=item.get("name", ""),
            description=item.get("overview", ""),
            type="tv",
            release_date=datetime.strptime(release[:10], "%Y-%m-%d").date() if release else None,
            poster_url=f"https://image.tmdb.org/t/p/w500{item.get('poster_path', '')}",
            rating=item.get("vote_average", 0.0)
        )
        db.add(nuevo)
        db.flush()

        for genre_id in item.get("genre_ids", []):
            genero = db.query(Genre).filter(Genre.tmdb_id == genre_id).first()
            if genero:
                nuevo.genre.append(genero)

        db.commit()
        db.refresh(nuevo)
        nuevos.append(nuevo)

    return nuevos


# ── Detalle de película ─────────────────────────────────
@router.get("/movie/{tmdb_id}")
def detalle_movie(tmdb_id: int):
    data = detalle_pelicula(tmdb_id)
    if not data or "id" not in data:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return data


# ── Detalle de serie ────────────────────────────────────
@router.get("/tv/{tmdb_id}")
def detalle_tv(tmdb_id: int):
    data = detalle_serie(tmdb_id)
    if not data or "id" not in data:
        raise HTTPException(status_code=404, detail="Serie no encontrada")
    return data


# ── Actores de una película ─────────────────────────────
@router.get("/movie/{tmdb_id}/credits")
def credits_movie(tmdb_id: int):
    actores = actores_pelicula(tmdb_id)
    if not actores:
        raise HTTPException(status_code=404, detail="No se encontraron actores")
    return actores


# ── Plataformas donde ver una película ─────────────────
@router.get("/movie/{tmdb_id}/watch/providers")
def providers_movie(tmdb_id: int):
    plataformas = plataformas_pelicula(tmdb_id)
    if not plataformas:
        raise HTTPException(status_code=404, detail="No hay plataformas disponibles")
    return plataformas


# ── Recomendaciones basadas en una película ─────────────
@router.get("/movie/{tmdb_id}/recommendations")
def recomendaciones_movie(tmdb_id: int):
    recomendaciones = recomendaciones_pelicula(tmdb_id)
    if not recomendaciones:
        raise HTTPException(status_code=404, detail="No hay recomendaciones disponibles")
    return recomendaciones


# ── Todo el contenido guardado en nuestra BD ───────────
@router.get("/", response_model=list[ContentResponse])
def obtener_contenido(db: Session = Depends(get_db)):
    return db.query(Content).all()


# ── Contenido por ID en nuestra BD ─────────────────────
@router.get("/{id_content}", response_model=ContentResponse)
def obtener_por_id(id_content: int, db: Session = Depends(get_db)):
    contenido = db.query(Content).filter(Content.id_content == id_content).first()
    if not contenido:
        raise HTTPException(status_code=404, detail="Contenido no encontrado")
    return contenido


# ── Eliminar contenido — solo admin ────────────────────
@router.delete("/{id_content}")
def eliminar_contenido(
    id_content: int,
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    contenido = db.query(Content).filter(Content.id_content == id_content).first()
    if not contenido:
        raise HTTPException(status_code=404, detail="Contenido no encontrado")
    db.delete(contenido)
    db.commit()
    return {"message": "Contenido eliminado correctamente"}


