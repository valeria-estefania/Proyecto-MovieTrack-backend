from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.db import Base
from app.models.content import content_platform

class Platform(Base):
    __tablename__ = "platform"

    id_platform : Mapped[int] = mapped_column(primary_key= True, autoincrement= True)
    nombre : Mapped[str] = mapped_column(String(100))
    logo_url : Mapped[str] = mapped_column(String(300))

    content : Mapped[list["Content"]] = relationship (secondary= content_platform,back_populates= "platform")

