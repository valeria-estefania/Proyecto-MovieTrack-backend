from sqlalchemy.orm import Session
from models.genre import Genre
from models.content import content_genre
from schemas.genre import GenreResponse
from utils.tmdb import obtener_generos_tmdb

def get_o_guardar_generos(db: Session, id_content: int, type: str = "movie") -> list[GenreResponse]:
    existentes = db.query(content_genre).filter(content_genre.id_content == id_content).all()
    if existentes:
        return [GenreResponse.model_validate(cg.genre) for cg in existentes]

    generos_tmdb = obtener_generos_tmdb(type)

    for tmdb_id, nombre in generos_tmdb.items():
        genero = db.query(Genre).filter(Genre.tmdb_id == tmdb_id).first()
        if not genero:
            genero = Genre(tmdb_id=tmdb_id, name=nombre)
            db.add(genero)
            db.flush()

        existe_relacion = db.query(content_genre).filter(
            content_genre.id_content == id_content,
            content_genre.id_genre == genero.id_genre
        ).first()
        if not existe_relacion:
            db.add(content_genre(id_content=id_content, id_genre=genero.id_genre))

    db.commit()
    guardados = db.query(content_genre).filter(content_genre.id_content == id_content).all()
    return [GenreResponse.model_validate(cg.genre) for cg in guardados]