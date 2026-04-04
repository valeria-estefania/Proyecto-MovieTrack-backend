from pydantic import BaseModel
from pydantic import ConfigDict

class PlatformBase(BaseModel):
    nombre: str
    logo_url: str

class PlatformCreate(PlatformBase):
    pass

class PlatformResponse(PlatformBase):
    id_platform: int

    model_config = ConfigDict(from_attributes=True)