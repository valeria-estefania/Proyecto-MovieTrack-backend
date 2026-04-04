from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.db import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin, UserResponse, Token
from core.security import hash_password, verify_password, create_access_token
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
        password=hash_password(user.password),
        fecha_registro=datetime.date.today()
    )
    db.add(nuevo_user)
    db.commit()
    db.refresh(nuevo_user)
    return nuevo_user

# @router.post("/login", response_model=Token)
# def login(credenciales: UserLogin, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == credenciales.email).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Credenciales incorrectas"
#         )

#     if not verify_password(credenciales.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Credenciales incorrectas"
#         )

#     token = create_access_token(data={"sub": str(user.id_user)})
#     return {"access_token": token, "token_type": "bearer"}


from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token(data={"sub": str(user.id_user)})

    return {"access_token": token, "token_type": "bearer"}