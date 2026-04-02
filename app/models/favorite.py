from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.db import Base
from datetime import date

class Favorite(Base):
    __tablename__ = "favorite"

    id_favorite : Mapped[int] = mapped_column(primary_key=True, autoincrement= True)
    id_user : Mapped[int] = mapped_column(ForeignKey("user.id_user"))
    id_content : Mapped[int] = mapped_column(ForeignKey("content.id_content"))
    date_added : Mapped[date] = mapped_column(Date)
