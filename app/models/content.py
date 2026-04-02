from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.db import Base
from sqlalchemy import String,Enum,Date,ForeignKey,Column,Table, Integer
from datetime import date



content_genre=Table(
    "content_genre",
    Base.metadata,
    Column("id_content", Integer, ForeignKey("content.id_content"),primary_key=True),
    Column("id_genre",Integer, ForeignKey("genre.id_genre"),primary_key=True),
)

content_platform = Table(
    "content_platform", Base.metadata,
    Column("id_content", Integer, ForeignKey("content.id_content"), primary_key= True),
    Column("id_platform", Integer, ForeignKey("platform.id_platform"), primary_key= True),
)

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


    genre : Mapped[list["Genre"]] = relationship(secondary=content_genre,  back_populates="content")
    platform : Mapped[list["Platform"]] = relationship(secondary=content_platform, back_populates="content")
    cast : Mapped[list["Cast"]] = relationship(back_populates="content")
    favorite : Mapped[list["Favorite"]] = relationship(back_populates="content")
    status : Mapped[list["Display_status"]] = relationship(back_populates="content")
    review : Mapped[list["Review"]] = relationship(back_populates="content")
