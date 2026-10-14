from enum import Enum
from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import List
from .base import Base

class SeatStatus(Enum):
    free = "FREE"
    reserved = "RESERVED"
    booked = "BOOKED"

class Seat(Base):
    __tablename__ = "seats"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    row: Mapped[str] = mapped_column(nullable=False)
    number: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[SeatStatus] = mapped_column(default=SeatStatus.free)

class SeatCreate(BaseModel):
    row: str
    number: int
    price: int