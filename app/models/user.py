
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.db import Base
from sqlalchemy import String,Date
from datetime import date

class User(Base):
    __tablename__="user"

    id_user: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[String] = mapped_column(String(100))
    email : Mapped[String] = mapped_column(String(150),unique=True)
    password: Mapped[String] = mapped_column(String(250))
    fecha_registro: Mapped[date] = mapped_column(Date)
    