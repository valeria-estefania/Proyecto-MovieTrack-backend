from pydantic import BaseModel
from pydantic import ConfigDict

class ActorBase(BaseModel):
    tmdb_id: int
    name: str
    photo_url: str

class ActorCreate(ActorBase):
    pass

class ActorResponse(ActorBase):
    id_actor: int

    model_config = ConfigDict(from_attributes=True)