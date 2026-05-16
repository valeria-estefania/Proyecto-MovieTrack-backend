from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.core.hash import hashear_password, verificar_password
from app.core.jwt import crear_token
import datetime
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(usuario: UserCreate, db: Session = Depends(get_db)):
    existe = db.query(User).filter(User.email == usuario.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    nuevo_usuario = User(
        name=usuario.name,
        email=usuario.email,
        password_hash=hashear_password(usuario.password),
        fecha_registro=datetime.date.today()
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)  
    return nuevo_usuario

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verificar_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = crear_token(data={"sub": str(user.id_user)})

    return {"access_token": token, "token_type": "bearer"}