from .base import Base
import enum
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from sqlalchemy import Enum, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

class UserRole(enum.Enum):
    client = "CLIENT"
    event_manager = "EVENT_MANAGER"
    admin = "ADMIN"
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Enum] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.client)
    created_at: Mapped[datetime] = mapped_column(nullable=False, type_=TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(nullable=False, type_=TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)