from pydantic import BaseModel
from pydantic import ConfigDict

class CastBase(BaseModel):
    character: str

class CastCreate(CastBase):
    id_content: int
    id_actor: int

class CastResponse(CastBase):
    id_cast: int
    id_content: int
    id_actor: int

    model_config = ConfigDict(from_attributes=True)