from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.content import Content
from app.schemas.content import ContentCreate, ContentResponse
from app.core.dependencies import get_current_user
from app.utils.tmdb import buscar_en_tmdb
from datetime import datetime

router = APIRouter(prefix="/content", tags=["Content"])

@router.get("/search", response_model=list[ContentResponse])
def buscar_contenido(query: str, type: str = "movie", db: Session = Depends(get_db)):
    resultados_locales = db.query(Content).filter(
        Content.title.ilike(f"%{query}%"),
        Content.type == type
    ).all()

    if resultados_locales:
        return resultados_locales

    resultados_tmdb = buscar_en_tmdb(query, type)
    if not resultados_tmdb:
        raise HTTPException(status_code=404, detail="No se encontraron resultados")

    nuevos = []
    for item in resultados_tmdb[:5]:
        existe = db.query(Content).filter(Content.tmdb_id == item["id"]).first()
        if existe:
            nuevos.append(existe)
            continue

        title = item.get("title") or item.get("name", "")
        release = item.get("release_date") or item.get("first_air_date", "1900-01-01")

        nuevo = Content(
            tmdb_id=item["id"],
            title=title,
            description=item.get("overview", ""),
            type=type,
            release_date=datetime.strptime(release[:10], "%Y-%m-%d").date() if release else None,
            poster_url=f"https://image.tmdb.org/t/p/w500{item.get('poster_path', '')}",
            rating=item.get("vote_average", 0.0)
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        nuevos.append(nuevo)

    return nuevos

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