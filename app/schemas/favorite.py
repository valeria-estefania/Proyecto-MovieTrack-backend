from pydantic import BaseModel
from pydantic import ConfigDict
from datetime import date

class FavoriteBase(BaseModel):
    id_content: int

class FavoriteCreate(FavoriteBase):
    date_added: date

class FavoriteResponse(FavoriteBase):
    id_favorite: int
    date_added: date

    model_config = ConfigDict(from_attributes=True)