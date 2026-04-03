from pydantic import BaseModel, EmailStr
import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id_user: int
    name: str
    email: str
    fecha_registro: datetime.date

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str