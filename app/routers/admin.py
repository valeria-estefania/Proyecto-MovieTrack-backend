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
    favoritos_subq = (
        db.query(
            Favorite.id_content,
            func.count(Favorite.id_favorite).label("total_favoritos")
        )
        .group_by(Favorite.id_content)
        .subquery()
    )

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
# Top 10 por favoritos
# ─────────────────────────────────────────────
@router.get("/top/favoritos")
def top_por_favoritos(
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    favoritos_subq = (
        db.query(
            Favorite.id_content,
            func.count(Favorite.id_favorite).label("total_favoritos")
        )
        .group_by(Favorite.id_content)
        .subquery()
    )

    resultados = (
        db.query(
            Content,
            func.coalesce(favoritos_subq.c.total_favoritos, 0).label("total_favoritos"),
        )
        .outerjoin(favoritos_subq, Content.id_content == favoritos_subq.c.id_content)
        .order_by(func.coalesce(favoritos_subq.c.total_favoritos, 0).desc())
        .limit(10)
        .all()
    )

    return [
        {
            "id_content": c.id_content,
            "title": c.title,
            "type": c.type,
            "poster_url": c.poster_url,
            "total_favoritos": total_fav,
        }
        for c, total_fav in resultados
    ]


# ─────────────────────────────────────────────
# Top 10 por rating de reviews
# ─────────────────────────────────────────────
@router.get("/top/reviews")
def top_por_reviews(
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    rating_subq = (
        db.query(
            Review.id_content,
            func.avg(Review.score).label("avg_score"),
            func.count(Review.id_review).label("total_reviews")
        )
        .group_by(Review.id_content)
        .having(func.count(Review.id_review) >= 3)
        .subquery()
    )

    resultados = (
        db.query(
            Content,
            rating_subq.c.avg_score,
            rating_subq.c.total_reviews,
        )
        .join(rating_subq, Content.id_content == rating_subq.c.id_content)
        .order_by(rating_subq.c.avg_score.desc())
        .limit(10)
        .all()
    )

    return [
        {
            "id_content": c.id_content,
            "title": c.title,
            "type": c.type,
            "poster_url": c.poster_url,
            "avg_score": round(float(avg_score), 1),
            "total_reviews": total_rev,
        }
        for c, avg_score, total_rev in resultados
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

# ─────────────────────────────────────────────
# Distribución de scores de reviews
# ─────────────────────────────────────────────
@router.get("/stats/scores")
def distribucion_scores(
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    resultados = (
        db.query(
            Review.score,
            func.count(Review.id_review).label("total")
        )
        .group_by(Review.score)
        .order_by(Review.score.asc())
        .all()
    )

    # Garantiza que los 10 valores (1-10) siempre estén presentes
    scores_map = {score: total for score, total in resultados}
    return [
        {"score": i, "total": scores_map.get(i, 0)}
        for i in range(1, 11)
    ]

# ─────────────────────────────────────────────
# Usuarios más activos (por reviews escritas)
# ─────────────────────────────────────────────
@router.get("/stats/usuarios-activos")
def usuarios_mas_activos(
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    resultados = (
        db.query(
            User.id_user,
            User.name,
            User.email,
            func.count(Review.id_review).label("total_reviews")
        )
        .join(Review, Review.id_user == User.id_user)
        .group_by(User.id_user, User.name, User.email)
        .order_by(func.count(Review.id_review).desc())
        .limit(10)
        .all()
    )

    return [
        {
            "id_user": id_user,
            "name": name,
            "email": email,
            "total_reviews": total_reviews,
        }
        for id_user, name, email, total_reviews in resultados
    ]


# ─────────────────────────────────────────────
# Registros de usuarios por mes
# ─────────────────────────────────────────────
@router.get("/stats/registros-por-mes")
def registros_por_mes(
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    resultados = (
        db.query(
            func.to_char(User.fecha_registro, "YYYY-MM").label("mes"),
            func.count(User.id_user).label("total")
        )
        .group_by(func.to_char(User.fecha_registro, "YYYY-MM"))
        .order_by(func.to_char(User.fecha_registro, "YYYY-MM").asc())
        .all()
    )

    return [
        {"mes": mes, "total": total}
        for mes, total in resultados
    ]

# ─────────────────────────────────────────────
# Favoritos por tipo de contenido (movie vs tv)
# ─────────────────────────────────────────────
@router.get("/stats/favoritos-por-tipo")
def favoritos_por_tipo(
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    resultados = (
        db.query(
            Content.type,
            func.count(Favorite.id_favorite).label("total")
        )
        .join(Favorite, Favorite.id_content == Content.id_content)
        .group_by(Content.type)
        .all()
    )

    return [
        {"type": tipo, "total": total}
        for tipo, total in resultados
    ]