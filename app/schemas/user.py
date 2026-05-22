from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict
from datetime import date

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class UserResponse(UserBase):
    id_user: int
    fecha_registro: date
    role: str
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class FavoriteInProfile(BaseModel):
    id_favorite: int
    id_content: int
    date_added: date
    model_config = ConfigDict(from_attributes=True)

class ReviewInProfile(BaseModel):
    id_review: int
    id_content: int
    score: int
    comment: str
    date: date
    model_config = ConfigDict(from_attributes=True)

class StatusInProfile(BaseModel):
    id_status: int
    id_content: int
    status: str
    model_config = ConfigDict(from_attributes=True)

class UserProfileResponse(BaseModel):
    id_user: int
    name: str
    email: EmailStr
    fecha_registro: date
    favorites: list[FavoriteInProfile]
    reviews: list[ReviewInProfile]
    statuses: list[StatusInProfile]
    model_config = ConfigDict(from_attributes=True)