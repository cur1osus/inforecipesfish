from sqlalchemy import (
    BigInteger,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Section(Base):
    __tablename__ = "sections"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    recipes: Mapped[list["Recipe"]] = relationship(back_populates="section", cascade="all, delete-orphan")


class Recipe(Base):
    __tablename__ = "recipes"

    section_id: Mapped[int] = mapped_column(ForeignKey("sections.id"), nullable=False)
    section: Mapped["Section"] = relationship(back_populates="recipes")

    name: Mapped[str] = mapped_column(String(500), nullable=False)
    text: Mapped[str] = mapped_column(String(2000), nullable=False)


class UserDB(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
