from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.db import get_db
from models.user import User
from core.hash import verificar_password
from core.jwt import crear_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.email == form.username).first()
    if not usuario or not verificar_password(form.password, usuario.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = crear_token({"id_user": usuario.id_user, "email": usuario.email})
    return {"access_token": token, "token_type": "bearer"}