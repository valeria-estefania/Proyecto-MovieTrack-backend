from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.db import Base
from sqlalchemy import String,Date
from datetime import date

class User(Base):
    __tablename__="user"

    id_user: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    email : Mapped[str] = mapped_column(String(150),unique=True)
    password_hash: Mapped[str] = mapped_column(String(250))
    fecha_registro: Mapped[date] = mapped_column(Date)

    favorite : Mapped[list["Favorite"]] = relationship(back_populates="user")
    status : Mapped[list["Display_status"]] = relationship(back_populates="user")
    review : Mapped[list["Review"]] = relationship(back_populates="user")
    