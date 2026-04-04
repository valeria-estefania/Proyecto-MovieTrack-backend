from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from core.jwt import verificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        return verificar_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="No autorizado")