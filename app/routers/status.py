from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db import get_db
from models.display_status import Display_status
from schemas.display_status import DisplayStatusCreate, DisplayStatusResponse
from core.dependencies import get_current_user

router = APIRouter(prefix="/status", tags=["Status"])

@router.post("/", response_model=DisplayStatusResponse)
def agregar_status(
    data: DisplayStatusCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    existe = db.query(Display_status).filter(
        Display_status.id_user == current_user["id_user"],
        Display_status.id_content == data.id_content
    ).first()

    if existe:
        existe.status = data.status
        db.commit()
        db.refresh(existe)
        return existe

    nuevo = Display_status(
        id_user=current_user["id_user"],
        id_content=data.id_content,
        status=data.status
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[DisplayStatusResponse])
def obtener_status(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Display_status).filter(
        Display_status.id_user == current_user["id_user"]
    ).all()

@router.delete("/{id_status}")
def eliminar_status(
    id_status: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    status = db.query(Display_status).filter(
        Display_status.id_status == id_status,
        Display_status.id_user == current_user["id_user"]
    ).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status no encontrado")

    db.delete(status)
    db.commit()
    return {"message": "Status eliminado"}