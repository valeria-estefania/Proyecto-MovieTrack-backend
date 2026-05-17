from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.jwt import verificar_token
from app.db.db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        return verificar_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="No autorizado")

def verify_admin(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.models.user import User
    usuario = db.query(User).filter(
        User.id_user == int(current_user["sub"])
    ).first()
    if not usuario or usuario.role != "admin":
        raise HTTPException(status_code=403, detail="Acceso solo para administradores")
    return usuario