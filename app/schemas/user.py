from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict
from datetime import date

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class UserResponse(UserBase):
    id_user: int
    fecha_registro: date
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
