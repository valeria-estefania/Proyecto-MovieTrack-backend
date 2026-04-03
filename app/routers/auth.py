from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.core.hash import hashear_password, verificar_password
from app.core.jwt import crear_token
import datetime

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existe = db.query(User).filter(User.email == user.email).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    nuevo_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashear_password(user.password),
        fecha_registro=datetime.date.today()
    )
    db.add(nuevo_user)
    db.commit()
    db.refresh(nuevo_user)
    return nuevo_user

@router.post("/login", response_model=Token)
def login(credenciales: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credenciales.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    if not verificar_password(credenciales.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    token = crear_token(data={"sub": str(user.id_user)})
    return {"access_token": token, "token_type": "bearer"}