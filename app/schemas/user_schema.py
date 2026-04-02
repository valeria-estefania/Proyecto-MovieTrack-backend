from pydantic import BaseModel
from datetime import date

class UserCreate(BaseModel):
    name: str
    email : str
    password: str
   
class UserResponse(BaseModel):
    name: str
    email: str
    register_date: date

class UserUpdate(BaseModel):
  name: str | None = None
  password: str | None = None
  email: str | None = None
