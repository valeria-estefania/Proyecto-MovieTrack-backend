from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.db import Base

class Display_status(Base):
    __tablename__ = "display_status"

    id_status : Mapped[int] = mapped_column(primary_key= True, autoincrement= True)
    id_user : Mapped[int] = mapped_column(ForeignKey("user.id_user"))
    id_content : Mapped[int] = mapped_column(ForeignKey("content.id_content"))
    status : Mapped[str] = mapped_column(Enum("visto", "pendiente", name="status_type"))

    usuario : Mapped["User"] = relationship(back_populates="status")
    content : Mapped["Content"] = relationship(back_populates= "status")

