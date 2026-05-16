from pydantic import BaseModel
from pydantic import ConfigDict
from enum import Enum

class StatusEnum(str, Enum):
    visto = "visto"
    no_visto = "no visto"
    pendiente = "pendiente"

class DisplayStatusBase(BaseModel):
    id_content: int
    status: StatusEnum

class DisplayStatusCreate(DisplayStatusBase):
    pass

class DisplayStatusResponse(DisplayStatusBase):
    id_status: int

    model_config = ConfigDict(from_attributes=True)