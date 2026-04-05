from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.db import get_db
from models.content import Content
from services.genre_services import get_o_guardar_generos
from schemas.genre import GenreResponse
from fastapi import HTTPException

router = APIRouter(prefix="/genres", tags=["Genres"])

@router.get("/{tmdb_id}", response_model=list[GenreResponse])
def get_generos(
    tmdb_id: int,
    type: str = Query(default="movie", enum=["movie", "tv"]),
    db: Session = Depends(get_db)
):
    content = db.query(Content).filter(Content.tmdb_id == tmdb_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Contenido no encontrado")
    return get_o_guardar_generos(db, content.id_content, type)