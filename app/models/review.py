from sqlalchemy import ForeignKey, Integer, Text, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.db import Base
from datetime import date

class Review(Base):
    __tablename__ = "review"

    id_review : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_user : Mapped[int] = mapped_column(ForeignKey("user.id_user"))
    id_content : Mapped[int] = mapped_column(ForeignKey("content.id_content"))
    score : Mapped[int] = mapped_column(Integer)
    comment : Mapped[str] = mapped_column(Text)
    date : Mapped[date] = mapped_column(Date)
