from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.user import User
from app.models.review import Review
from app.schemas.user import UserResponse
from app.schemas.review import ReviewResponse
from app.core.dependencies import verify_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


# ── Ver todos los usuarios ──────────────────────────────
@router.get("/users", response_model=list[UserResponse])
def obtener_todos_usuarios(
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    return db.query(User).all()


# ── Eliminar cualquier usuario ──────────────────────────
@router.delete("/users/{id_user}")
def eliminar_usuario(
    id_user: int,
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    usuario = db.query(User).filter(User.id_user == id_user).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.role == "admin":
        raise HTTPException(status_code=400, detail="No puedes eliminar a otro administrador")
    db.delete(usuario)
    db.commit()
    return {"message": f"Usuario {usuario.name} eliminado"}


# ── Cambiar rol de un usuario ───────────────────────────
@router.patch("/users/{id_user}/role")
def cambiar_rol(
    id_user: int,
    role: str,
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    if role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="Rol inválido. Usa 'user' o 'admin'")
    usuario = db.query(User).filter(User.id_user == id_user).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.role = role
    db.commit()
    db.refresh(usuario)
    return {"message": f"Rol de {usuario.name} cambiado a {role}"}


# ── Ver todas las reseñas ───────────────────────────────
@router.get("/reviews", response_model=list[ReviewResponse])
def obtener_todas_reviews(
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    return db.query(Review).all()


# ── Eliminar cualquier reseña ───────────────────────────
@router.delete("/reviews/{id_review}")
def eliminar_review(
    id_review: int,
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    review = db.query(Review).filter(Review.id_review == id_review).first()
    if not review:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")
    db.delete(review)
    db.commit()
    return {"message": "Reseña eliminada por administrador"}


# ── Estadísticas generales ──────────────────────────────
@router.get("/stats")
def estadisticas(
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    from app.models.favorite import Favorite
    from app.models.content import Content
    from app.models.display_status import Display_status

    return {
        "total_usuarios": db.query(User).count(),
        "total_contenido": db.query(Content).count(),
        "total_favoritos": db.query(Favorite).count(),
        "total_resenas": db.query(Review).count(),
        "contenido_visto": db.query(Display_status).filter(
            Display_status.status == "visto"
        ).count(),
        "contenido_pendiente": db.query(Display_status).filter(
            Display_status.status == "pendiente"
        ).count(),
    }