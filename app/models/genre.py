from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.db import Base
from sqlalchemy import String,Date
from datetime import date
from models.content import content_genre

class Genre(Base):
    __tablename__="genre"

    id_genre: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tmdb_id : Mapped[int] = mapped_column(unique=True)
    name: Mapped[String] = mapped_column(String(50))

    content : Mapped[list["Content"]] = relationship(
        secondary= content_genre,
        back_populates= "genre"
    )
    