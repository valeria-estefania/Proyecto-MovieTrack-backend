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

# Schema enriquecido para el panel admin
class UserSummary(BaseModel):
    id_user: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class ContentSummary(BaseModel):
    id_content: int
    title: str
    type: str
    poster_url: str | None = None

    model_config = ConfigDict(from_attributes=True)

class ReviewWithContext(BaseModel):
    id_review: int
    score: int
    comment: str
    date: date
    id_content: int
    id_user: int
    user: UserSummary
    content: ContentSummary

    model_config = ConfigDict(from_attributes=True)
