from datetime import datetime, timezone, timedelta
from enum import Enum
from pydantic import BaseModel
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class BookingStatus(Enum):
    pending = "PENDING"
    paid = "PAID"
    expired = "EXPIRED"
    cancelled = "CANCELLED"

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    seat_id: Mapped[int] = mapped_column(ForeignKey("seats.id"), nullable=False)
    status: Mapped[BookingStatus] = mapped_column(nullable=False, default=BookingStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(tz=timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=(datetime.now(tz=timezone.utc)+timedelta(minutes=5)))

class BookingCreate(BaseModel):
    user_id: int
    seat_id: int