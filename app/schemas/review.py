from pydantic import BaseModel
from pydantic import ConfigDict
from datetime import date

class ReviewBase(BaseModel):
    score: int
    comment: str

class ReviewCreate(ReviewBase):
    id_content: int

class ReviewUpdate(BaseModel):
    score: int | None = None
    comment: str | None = None

class ReviewResponse(ReviewBase):
    id_review: int
    id_content: int
    date: date

    model_config = ConfigDict(from_attributes=True)