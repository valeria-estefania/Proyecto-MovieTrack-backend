from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db import get_db
from models.review import Review
from schemas.review import ReviewCreate, ReviewResponse
from core.dependencies import get_current_user
from datetime import date

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewResponse)
def crear_review(
    data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    existe = db.query(Review).filter(
        Review.id_user == current_user["id_user"],
        Review.id_content == data.id_content
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya tienes una reseña para este contenido")

    nueva = Review(
        id_user=current_user["id_user"],
        id_content=data.id_content,
        score=data.score,
        comment=data.comment,
        date=date.today()
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/content/{id_content}", response_model=list[ReviewResponse])
def obtener_reviews_por_contenido(id_content: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.id_content == id_content).all()

@router.get("/my", response_model=list[ReviewResponse])
def obtener_mis_reviews(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Review).filter(
        Review.id_user == current_user["id_user"]
    ).all()

@router.delete("/{id_review}")
def eliminar_review(
    id_review: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    review = db.query(Review).filter(
        Review.id_review == id_review,
        Review.id_user == current_user["id_user"]
    ).first()
    if not review:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")

    db.delete(review)
    db.commit()
    return {"message": "Reseña eliminada"}