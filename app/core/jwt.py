from jose import jwt
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def crear_token(data: dict) -> str:
    payload = data.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    payload.update({"exp": expiracion})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise ValueError("Token inválido o expirado")