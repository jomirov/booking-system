from datetime import datetime, date
from pydantic import BaseModel
from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(Date, nullable=False)

class EventCreate(BaseModel):
    title: str
    location: str
    date: str