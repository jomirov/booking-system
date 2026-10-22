from datetime import datetime, timezone
from sqlalchemy import select, update, and_, asc
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
                raise ValueError("Given user or seat id is not found")

    async def get_booking(self, id):
        async with AsyncSession(self.engine) as session:
            booking = await session.scalar(select(Booking).where(Booking.id==id))

            if not booking:
                raise Exception()

            return {
                "id": booking.id,
                "seat_id": booking.seat_id,
                "user_id": booking.user_id,
                "status": booking.status.value,
                "created_at": datetime.strftime(booking.created_at, "%Y-%m-%d %H:%M:%S"),
                "expires_at": datetime.strftime(booking.expires_at, "%Y-%m-%d %H:%M:%S")
            }

    async def update_expired_bookings(self):
        async with AsyncSession(self.engine) as session:
            res = await session.execute(update(Booking).where(
                and_(Booking.expires_at <= datetime.now(tz=timezone.utc),                                                    
                    Booking.status == BookingStatus.pending))
                    .values(status=BookingStatus.expired).returning(Booking.seat_id))
            await session.commit()
            updated_seats_id = [row[0] for row in res]
            return updated_seats_id

    async def update_booking_status(self, id, new_status):
        async with AsyncSession(self.engine) as session:
            try:
                status = BookingStatus._value2member_map_[new_status]
                updated_booking_id = await session.execute(update(Booking).where(Booking.id==id).values(status=status).returning(Booking.id))
                
                if not updated_booking_id:
                    raise ValueError("id")

                await session.commit()
            except KeyError:
                raise ValueError("status")

    async def update_inactive_user_bookings_status_except_one(self, seat_id, user_id):
        async with AsyncSession(self.engine) as session:
            res = await session.execute(update(Booking).where(
                and_(and_(Booking.seat_id != seat_id, Booking.user_id==user_id), Booking.status==BookingStatus.pending)
            ).values(status=BookingStatus.cancelled).returning(Booking.seat_id))
            await session.commit()
            updated_bookings_seats_id = [row[0] for row in res]
            return updated_bookings_seats_id

    async def get_active_user_booking(self, user_id):
        async with AsyncSession(self.engine) as session:
            booking = await session.scalar(select(Booking).where(and_(Booking.user_id==user_id, 
                                                                      Booking.status==BookingStatus.pending)))
            
            return None if not booking else {
                "id": booking.id,
                "seat_id": booking.seat_id,
                "user_id": booking.user_id,
                "status": booking.status.value,
                "created_at": datetime.strftime(booking.created_at, "%Y-%m-%d %H:%M:%S"),
                "expires_at": datetime.strftime(booking.expires_at, "%Y-%m-%d %H:%M:%S")
            }

    async def get_bookings(self):
        async with AsyncSession(self.engine) as session:
            res = await session.scalars(select(Booking).order_by(asc(Booking.id)))

            bookings = [
                {
                    "id": booking.id,
                    "user_id": booking.user_id,
                    "seat_id": booking.seat_id,
                    "status": booking.status.value,
                    "created_at": datetime.strftime(booking.created_at, "%Y-%m-%d %H:%M:%S"),
                    "expires_at": datetime.strftime(booking.expires_at, "%Y-%m-%d %H:%M:%S")
                } for booking in res
            ]

            return bookings