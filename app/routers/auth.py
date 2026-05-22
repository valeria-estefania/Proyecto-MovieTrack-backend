from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

import datetime

from app.db.db import get_db
from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
)

from app.core.hash import (
    hashear_password,
    verificar_password,
)

from app.core.jwt import crear_token


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


# =========================
# REGISTER
# =========================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    usuario: UserCreate,
    db: Session = Depends(get_db)
):

    existe = db.query(User).filter(
        User.email == usuario.email
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado"
        )

    nuevo_usuario = User(
        name=usuario.name,
        email=usuario.email,
        password_hash=hashear_password(
            usuario.password
        ),
        fecha_registro=datetime.date.today(),

        # IMPORTANTE
        role="user"
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


# =========================
# LOGIN NORMAL
# =========================

@router.post("/login")
def login(
    credenciales: UserLogin,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == credenciales.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado"
        )

    if not verificar_password(
        credenciales.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Contraseña incorrecta"
        )

    token = crear_token(
        data={
            "sub": str(user.id_user),
            "email": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",

        "user": {
            "id": user.id_user,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }


# =========================
# LOGIN SWAGGER
# =========================

@router.post(
    "/token",
    include_in_schema=False
)
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado"
        )

    if not verificar_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Contraseña incorrecta"
        )

    token = crear_token(
        data={
            "sub": str(user.id_user),
            "email": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",

        "user": {
            "id": user.id_user,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }