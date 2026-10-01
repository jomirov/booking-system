import enum
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta
from sqlalchemy import ForeignKey, Enum, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class BookingStatus(enum.Enum):
    paid = "PAID"
    pending = "PENDING"
    expired = "EXPIRED"
    cancelled = "CANCELLED"

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    seat_id: Mapped[int] = mapped_column(ForeignKey("seats.id"), nullable=False)
    status: Mapped[Enum] = mapped_column(Enum(BookingStatus), nullable=False, default=BookingStatus.pending)
    expires_at: Mapped[datetime] = mapped_column(nullable=False, default=(datetime.now(timezone.utc) + timedelta(minutes=10)), type_=TIMESTAMP(timezone=True))
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now(timezone.utc), type_=TIMESTAMP(timezone=True))

class BookingCreate(BaseModel):
    user_id: int
    seat_id: int