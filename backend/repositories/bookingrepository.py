from datetime import datetime, timezone
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from .baserepository import BaseRepository
from ..models.booking import Booking, BookingStatus

class BookingRepository(BaseRepository):
    async def create_booking(self, user_id, seat_id):
        async with AsyncSession(self.engine) as session:
            try:
                session.add(Booking(user_id=user_id, seat_id=seat_id))
                await session.commit()
            except IntegrityError:
                raise ValueError("Given user or seat is not found")

    async def update_expired_bookings(self):
        async with AsyncSession(self.engine) as session:
            await session.execute(update(Booking).where(Booking.expires_at <= datetime.now(tz=timezone.utc)).values(status=BookingStatus.expired))
            await session.commit()

    async def update_booking_status(self, id, new_status):
        async with AsyncSession(self.engine) as session:
            try:
                status = BookingStatus._value2member_map_[new_status]
                updated_booking_id = await session.execute(update(Booking).where(Booking.id==id).values(status=status).returning(Booking.id))
                
                if not updated_booking_id:
                    raise ValueError("id")

                await session.commit()
            except KeyError:
                raise ValueError("Status")