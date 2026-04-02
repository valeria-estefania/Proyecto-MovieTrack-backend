from pydantic import BaseModel
from datetime import date

class ContentCreate(BaseModel):

    tmdb_id : int
    name: str
    photo_url: str
    

class ActorResponse(BaseModel):
    id_actor: int
    tmdb_id : int
    name: str
    photo_url: str