from sqlalchemy import select, delete, update, asc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.seat import Seat, SeatCreate, SeatStatus
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
                "status": res.status.value
            }

    async def get_seats_for_event(self, event_id):
        async with AsyncSession(self.engine) as session:
            res = await session.scalars(select(Seat).where(Seat.event_id==event_id).order_by(asc(Seat.row)))

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

    async def update_seat_status(self, id, new_status):
        async with AsyncSession(self.engine) as session:
            await session.execute(select(Seat).where(Seat.id==id).with_for_update(nowait=True))
            status = SeatStatus._value2member_map_[new_status]
            updated_seat_id = await session.execute(update(Seat).where(Seat.id==id).values(status=status).returning(Seat.id))
            await session.commit()

            if not updated_seat_id:
                raise ValueError
            
    async def update_many_seats_status(self, seats_id, new_status):
        async with AsyncSession(self.engine) as session:
            status = SeatStatus._value2member_map_[new_status]
        
            await session.execute(update(Seat).where(Seat.id.in_(seats_id)).values(status=status))
            await session.commit()