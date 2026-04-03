from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.core.hash import hashear_password
from app.core.dependencies import get_current_user
from datetime import date

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def crear_usuario(user: UserCreate, db: Session = Depends(get_db)):
    existe = db.query(User).filter(User.email == user.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    nuevo_usuario = User(
        name=user.name,
        email=user.email,
        password=hashear_password(user.password),
        fecha_registro=date.today()
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.get("/", response_model=list[UserResponse])
def obtener_usuarios(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(User).all()

@router.get("/{id_user}", response_model=UserResponse)
def obtener_usuario(id_user: int, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.id_user == id_user).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.patch("/{id_user}", response_model=UserResponse)
def actualizar_usuario(id_user: int, datos: UserUpdate, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.id_user == id_user).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if datos.name:
        usuario.name = datos.name
    if datos.email:
        usuario.email = datos.email
    if datos.password:
        usuario.password = hashear_password(datos.password)

    db.commit()
    db.refresh(usuario)
    return usuario

@router.delete("/{id_user}")
def eliminar_usuario(
    id_user: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    usuario = db.query(User).filter(User.id_user == id_user).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}