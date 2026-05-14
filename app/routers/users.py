from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.core.hash import hashear_password
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def mi_perfil(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    usuario = db.query(User).filter(
        User.id_user == int(current_user["sub"])
    ).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.patch("/me", response_model=UserResponse)
def actualizar_perfil(
    datos: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    usuario = db.query(User).filter(
        User.id_user == int(current_user["sub"])
    ).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if datos.name:
        usuario.name = datos.name
    if datos.email:
        usuario.email = datos.email
    if datos.password:
        usuario.password_hash = hashear_password(datos.password)  

    db.commit()
    db.refresh(usuario)
    return usuario

@router.delete("/me")
def eliminar_cuenta(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    usuario = db.query(User).filter(
        User.id_user == int(current_user["sub"])
    ).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    return {"message": "Cuenta eliminada correctamente"}