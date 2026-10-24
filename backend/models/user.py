from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column, Mapped
from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)