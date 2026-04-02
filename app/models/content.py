from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.db import Base
from sqlalchemy import String,Enum,Date,ForeignKey,Column,Table
from datetime import date



content_genre=Table(
    "content_genre",
    Base.metadata,
    Column("id_content",ForeignKey("id_content"),primary_key=True),
    Column("id_genre",ForeignKey("id_genre"),primary_key=True),)
  

class Content(Base):
    __tablename__="content"

    id_content: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    tmdb_id: Mapped[int] = mapped_column(unique=True)
    title: Mapped[String] = mapped_column(String(255))
    description: Mapped[String]= mapped_column(String(255))
    type: Mapped[String] = mapped_column(Enum("movie", "tv", name="tipo_contenido"))
    release_date:  Mapped[date] = mapped_column(Date)
    poster_url: Mapped[String] = mapped_column(String(500))
    rating: Mapped[float] = mapped_column()


    cast: Mapped['Cast'] = relationship(back_populates='content')