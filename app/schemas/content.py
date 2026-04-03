from pydantic import BaseModel
from pydantic import ConfigDict
from datetime import date

class ContentBase(BaseModel):
    tmdb_id: int
    title: str
    description: str
    type: str
    release_date: date
    poster_url: str
    rating: float

class ContentCreate(ContentBase):
    pass

class ContentResponse(ContentBase):
    id_content: int

    model_config = ConfigDict(from_attributes=True)