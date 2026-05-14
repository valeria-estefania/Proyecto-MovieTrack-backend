from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.actor import Actor
from app.schemas.actor import ActorResponse

router = APIRouter(prefix="/actors", tags=["Actors"])

@router.get("/", response_model=list[ActorResponse])
def obtener_actores(db: Session = Depends(get_db)):
    return db.query(Actor).all()

@router.get("/{id_actor}", response_model=ActorResponse)
def obtener_actor(id_actor: int, db: Session = Depends(get_db)):
    actor = db.query(Actor).filter(Actor.id_actor == id_actor).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor no encontrado")
    return actor