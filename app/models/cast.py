
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.db import Base
from sqlalchemy import String,ForeignKey


class Cast(Base):
    __tablename__="Cast"

    id_cast: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_content : Mapped[int] = mapped_column(ForeignKey('content.id_content'))
    id_actor: Mapped[int] = mapped_column(ForeignKey('actor.id_actor'))
    character: Mapped[String] = mapped_column(String(40))

    content: Mapped['Content'] = relationship(back_populates='cast')
    actor: Mapped['Actor'] = relationship(back_populates='cast')