from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db import get_db
from models.favorite import Favorite
from schemas.favorite import FavoriteCreate, FavoriteResponse
from core.dependencies import get_current_user
from datetime import date

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.post("/", response_model=FavoriteResponse)
def agregar_favorito(
    favorito: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    existe = db.query(Favorite).filter(
        Favorite.id_user == current_user["id_user"],
        Favorite.id_content == favorito.id_content
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya está en favoritos")

    nuevo = Favorite(
        id_user=current_user["id_user"],
        id_content=favorito.id_content,
        date_added=date.today()
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[FavoriteResponse])
def obtener_favoritos(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Favorite).filter(
        Favorite.id_user == current_user["id_user"]
    ).all()

@router.delete("/{id_favorite}")
def eliminar_favorito(
    id_favorite: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    favorito = db.query(Favorite).filter(
        Favorite.id_favorite == id_favorite,
        Favorite.id_user == current_user["id_user"]
    ).first()
    if not favorito:
        raise HTTPException(status_code=404, detail="Favorito no encontrado")

    db.delete(favorito)
    db.commit()
    return {"message": "Eliminado de favoritos"}