from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db import get_db
from models.content import Content
from schemas.content import ContentCreate, ContentResponse
from core.dependencies import get_current_user

router = APIRouter(prefix="/content", tags=["Content"])

@router.get("/", response_model=list[ContentResponse])
def obtener_contenido(db: Session = Depends(get_db)):
    return db.query(Content).all()

@router.get("/{id_content}", response_model=ContentResponse)
def obtener_contenido_por_id(id_content: int, db: Session = Depends(get_db)):
    contenido = db.query(Content).filter(Content.id_content == id_content).first()
    if not contenido:
        raise HTTPException(status_code=404, detail="Contenido no encontrado")
    return contenido

@router.delete("/{id_content}")
def eliminar_contenido(
    id_content: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    contenido = db.query(Content).filter(Content.id_content == id_content).first()
    if not contenido:
        raise HTTPException(status_code=404, detail="Contenido no encontrado")
    db.delete(contenido)
    db.commit()
    return {"message": "Contenido eliminado correctamente"}