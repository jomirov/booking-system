import datetime
from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime.date] = mapped_column(nullable=False)

class EventCreate(BaseModel):
    title: str
    date: str