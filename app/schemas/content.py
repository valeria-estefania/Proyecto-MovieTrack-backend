from pydantic import BaseModel
from pydantic import ConfigDict
from datetime import date

class ContentBase(BaseModel):
    tmdb_id: int
    title: str
    description: str | None = None
    type: str
    release_date: date | None = None
    poster_url: str | None = None
    rating: float | None = None

class ContentCreate(ContentBase):
    pass

class ContentResponse(ContentBase):
    id_content: int

    model_config = ConfigDict(from_attributes=True)