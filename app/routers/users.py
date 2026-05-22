from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.user import User
from app.models.favorite import Favorite
from app.models.review import Review
from app.models.display_status import Display_status
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserProfileResponse
from app.core.hash import hashear_password
from app.core.dependencies import get_current_user
from datetime import date

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def crear_usuario(user: UserCreate, db: Session = Depends(get_db)):
    existe = db.query(User).filter(User.email == user.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya esta registrado")
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

@router.get("/me", response_model=UserResponse)
def obtener_mi_perfil(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    usuario = db.query(User).filter(User.id_user == int(current_user["sub"])).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.get("/search", response_model=UserResponse)
def buscar_usuario_por_email(
    email: str = Query(..., description="Email exacto del usuario a buscar"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    usuario = db.query(User).filter(User.email == email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.get("/{id_user}/profile", response_model=UserProfileResponse)
def obtener_perfil_completo(
    id_user: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    usuario = db.query(User).filter(User.id_user == id_user).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    favorites = db.query(Favorite).filter(Favorite.id_user == id_user).all()
    reviews   = db.query(Review).filter(Review.id_user == id_user).all()
    statuses  = db.query(Display_status).filter(Display_status.id_user == id_user).all()
    return UserProfileResponse(
        id_user=usuario.id_user,
        name=usuario.name,
        email=usuario.email,
        fecha_registro=usuario.fecha_registro,
        favorites=[
            {"id_favorite": f.id_favorite, "id_content": f.id_content, "date_added": f.date_added}
            for f in favorites
        ],
        reviews=[
            {"id_review": r.id_review, "id_content": r.id_content,
             "score": r.score, "comment": r.comment, "date": r.date}
            for r in reviews
        ],
        statuses=[
            {"id_status": s.id_status, "id_content": s.id_content, "status": s.status}
            for s in statuses
        ],
    )

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