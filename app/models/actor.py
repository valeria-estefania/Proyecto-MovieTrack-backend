from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.db import Base
from sqlalchemy import String


class Actor(Base):
    __tablename__="actor"

    id_actor: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tmdb_id : Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(50))
    photo_url: Mapped[str] = mapped_column(String(400))
    
    cast: Mapped[list['Cast']] = relationship(back_populates='actor')