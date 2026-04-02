from pydantic import BaseModel
from datetime import date

class ContentCreate(BaseModel):

    tmdb_id: int
    title: str
    description: str
    type:str
    release_date: date
    poster_url: str
    rating: float

class ContentResponse(BaseModel):
    
    id_content: int
    tmdb_id: int
    title: str
    description: str
    type:str
    release_date: date
    poster_url: str
    rating: float


