from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.db.db import get_db

from app.models.user import User
from app.models.review import Review
from app.models.favorite import Favorite
from app.models.content import Content
from app.models.display_status import Display_status

from app.schemas.user import UserResponse
from app.schemas.review import ReviewResponse, ReviewWithContext

from app.core.dependencies import verify_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# ─────────────────────────────────────────────
# Obtener todos los usuarios
# ─────────────────────────────────────────────
@router.get("/users", response_model=list[UserResponse])
def obtener_todos_usuarios(
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    usuarios = db.query(User).all()
    return usuarios


# ─────────────────────────────────────────────
# Eliminar usuario
# ─────────────────────────────────────────────
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
        raise HTTPException(status_code=400, detail="No puedes eliminar otro administrador")

    db.delete(usuario)
    db.commit()

    return {"message": f"Usuario {usuario.name} eliminado"}


# ─────────────────────────────────────────────
# Cambiar rol
# ─────────────────────────────────────────────
@router.patch("/users/{id_user}/role")
def cambiar_rol(
    id_user: int,
    role: str,
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    if role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="Rol inválido")

    usuario = db.query(User).filter(User.id_user == id_user).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.role = role
    db.commit()
    db.refresh(usuario)

    return {"message": f"Rol actualizado a {role}"}


# ─────────────────────────────────────────────
# Obtener todas las reviews (con contexto)
# ─────────────────────────────────────────────
@router.get("/reviews", response_model=list[ReviewWithContext])
def obtener_todas_reviews(
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    reviews = (
        db.query(Review)
        .options(
            joinedload(Review.user),
            joinedload(Review.content)
        )
        .order_by(Review.date.desc())
        .all()
    )
    return reviews


# ─────────────────────────────────────────────
# Reviews recientes (últimas 5) para dashboard
# ─────────────────────────────────────────────
@router.get("/recent-reviews", response_model=list[ReviewWithContext])
def reviews_recientes(
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    reviews = (
        db.query(Review)
        .options(
            joinedload(Review.user),
            joinedload(Review.content)
        )
        .order_by(Review.date.desc())
        .limit(5)
        .all()
    )
    return reviews


# ─────────────────────────────────────────────
# Eliminar review
# ─────────────────────────────────────────────
@router.delete("/reviews/{id_review}")
def eliminar_review(
    id_review: int,
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    review = db.query(Review).filter(Review.id_review == id_review).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review no encontrada")

    db.delete(review)
    db.commit()

    return {"message": "Review eliminada"}


# ─────────────────────────────────────────────
# Contenido con estadísticas de uso
# ─────────────────────────────────────────────
@router.get("/content")
def contenido_con_stats(
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    # Conteo de favoritos por contenido
    favoritos_subq = (
        db.query(
            Favorite.id_content,
            func.count(Favorite.id_favorite).label("total_favoritos")
        )
        .group_by(Favorite.id_content)
        .subquery()
    )

    # Promedio de score de reviews por contenido
    rating_subq = (
        db.query(
            Review.id_content,
            func.avg(Review.score).label("avg_score"),
            func.count(Review.id_review).label("total_reviews")
        )
        .group_by(Review.id_content)
        .subquery()
    )

    resultados = (
        db.query(
            Content,
            func.coalesce(favoritos_subq.c.total_favoritos, 0).label("total_favoritos"),
            func.coalesce(rating_subq.c.avg_score, None).label("avg_score"),
            func.coalesce(rating_subq.c.total_reviews, 0).label("total_reviews"),
        )
        .outerjoin(favoritos_subq, Content.id_content == favoritos_subq.c.id_content)
        .outerjoin(rating_subq, Content.id_content == rating_subq.c.id_content)
        .order_by(func.coalesce(favoritos_subq.c.total_favoritos, 0).desc())
        .all()
    )

    return [
        {
            "id_content": c.id_content,
            "tmdb_id": c.tmdb_id,
            "title": c.title,
            "type": c.type,
            "poster_url": c.poster_url,
            "release_date": c.release_date.isoformat() if c.release_date else None,
            "rating": c.rating,
            "total_favoritos": total_fav,
            "avg_score": round(float(avg_score), 1) if avg_score is not None else None,
            "total_reviews": total_rev,
        }
        for c, total_fav, avg_score, total_rev in resultados
    ]


# ─────────────────────────────────────────────
# Estadísticas generales
# ─────────────────────────────────────────────
@router.get("/stats")
def estadisticas(
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    total_usuarios = db.query(User).count()
    total_contenido = db.query(Content).count()
    total_favoritos = db.query(Favorite).count()
    total_reviews = db.query(Review).count()

    contenido_visto = db.query(Display_status).filter(
        Display_status.status == "visto"
    ).count()

    contenido_pendiente = db.query(Display_status).filter(
        Display_status.status == "pendiente"
    ).count()

    return {
        "total_usuarios": total_usuarios,
        "total_contenido": total_contenido,
        "total_favoritos": total_favoritos,
        "total_reviews": total_reviews,
        "contenido_visto": contenido_visto,
        "contenido_pendiente": contenido_pendiente,
    }
