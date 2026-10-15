from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.seat import Seat, SeatCreate
from .baserepository import BaseRepository

class SeatRepository(BaseRepository):
    async def create_seats(self, event_id, seats: list[SeatCreate]):
        async with AsyncSession(self.engine) as session:
            try:
                for seat in seats:
                    if seat.number <= 0 or seat.price < 0:
                        raise ValueError
                    session.add(Seat(event_id=event_id, row=seat.row, number=seat.number, price=seat.price))
                await session.commit()
            except ValueError:
                raise ValueError("seat")
            except IntegrityError:
                raise ValueError("event_id")

    async def get_seat(self, id):
        async with AsyncSession(self.engine) as session:
            res = await session.scalar(select(Seat).where(Seat.id==id))
            if not res:
                raise ValueError("id")
            return {
                "id": res.id,
                "event_id": res.event_id,
                "row": res.row,
                "number": res.number,
                "price": res.price,
                "status": res.status
            }

    async def get_seats_for_event(self, event_id):
        async with AsyncSession(self.engine) as session:
            res = await session.scalars(select(Seat).where(Seat.event_id==event_id))

            if not res:
                raise ValueError

            seats = [
                {
                    "id": seat.id,
                    "event_id": seat.event_id,
                    "row": seat.row,
                    "number": seat.number,
                    "price": seat.price,
                    "status": seat.status.value
                } for seat in res
            ]

            return seats

    async def delete_seat(self, id):
        async with AsyncSession(self.engine) as session:
            deleted_seat_id = await session.execute(delete(Seat).where(Seat.id==id).returning(Seat.id))
            await session.commit()

            if not deleted_seat_id:
                raise ValueError

    async def update_seat(self, id, new_row, new_number, new_price):
        async with AsyncSession(self.engine) as session:
            if new_number < 0 or new_price < 0:
                raise ValueError("seat")

            updated_seat_id = await session.execute(update(Seat).where(Seat.id==id).values(row=new_row, number=new_number, price=new_price).returning(Seat.id))
            await session.commit()

            if not updated_seat_id:
                raise ValueError("seat")
            