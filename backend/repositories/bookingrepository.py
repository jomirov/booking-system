from fastapi import Depends
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from ..models.booking import Booking, BookingStatus
from ..database.database import get_engine

class BookingRepository:
    def __init__(self, engine = Depends(get_engine)):
        self.engine = engine

    async def create_booking(self, user_id, seat_id):
        async with AsyncSession(self.engine) as session:
            booking = Booking(user_id=user_id, seat_id=seat_id)
            session.add(booking)
            await session.commit()

    async def get_all_pending_bookings(self):
        async with AsyncSession(self.engine) as session:
            res = await session.scalars(select(Booking).where(Booking.status==BookingStatus.pending))

            bookings = []

            for booking in res:
                bookings.append({
                    "id": booking.id,
                    "user_id": booking.user_id,
                    "seat_id": booking.seat_id,
                    "status": booking.status.value,
                    "expires_at": datetime.strftime(booking.expires_at, "%Y-%m-%d %H:%M:%S"),
                    "created_at": datetime.strftime(booking.created_at, "%Y-%m-%d %H:%M:%S")
                })
            return bookings
            

    async def update_booking_status(self, id, status):
        async with AsyncSession(self.engine) as session:

            new_status = BookingStatus._value2member_map_[str(status, encoding="utf-8")]
            await session.execute(update(Booking).where(Booking.id==id).values(status=new_status))
            await session.commit()

    async def delete_booking(self, id):
        async with AsyncSession(self.engine) as session:
            await session.execute(delete(Booking).where(Booking.id==id))
            await session.commit()