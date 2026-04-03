from pydantic import BaseModel
from pydantic import ConfigDict

class DisplayStatusBase(BaseModel):
    status: str  # "visto" | "pendiente"

class DisplayStatusCreate(DisplayStatusBase):
    id_content: int

class DisplayStatusResponse(DisplayStatusBase):
    id_status: int
    id_content: int

    model_config = ConfigDict(from_attributes=True)