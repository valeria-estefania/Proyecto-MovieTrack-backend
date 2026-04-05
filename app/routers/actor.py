from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db import get_db
from models.content import Content
from services.actor_services import get_o_guardar_actores
from schemas.cast import CastResponse

router = APIRouter(prefix="/actors", tags=["Actors"])

@router.get("/{tmdb_id}", response_model=list[CastResponse])
def get_actores(tmdb_id: int, db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.tmdb_id == tmdb_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Contenido no encontrado")
    return get_o_guardar_actores(db, content.id_content, tmdb_id)