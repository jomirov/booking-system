import enum
from pydantic import BaseModel
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped
from .base import Base

class SeatStatus(enum.Enum):
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
    status: Mapped[Enum] = mapped_column(Enum(SeatStatus), nullable=False, default=SeatStatus.free)

class SeatCreate(BaseModel):
    event_id: int
    row: str
    number: int
    price: int
