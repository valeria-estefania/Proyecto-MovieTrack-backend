from pydantic import BaseModel
from pydantic import ConfigDict

class GenreBase(BaseModel):
    tmdb_id: int
    name: str

class GenreCreate(GenreBase):
    pass

class GenreResponse(GenreBase):
    id_genre: int

    model_config = ConfigDict(from_attributes=True)