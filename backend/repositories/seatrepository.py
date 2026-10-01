from fastapi import Depends
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.seat import Seat, SeatStatus
from ..database.database import get_engine

class SeatRepository:
    def __init__(self, engine = Depends(get_engine)):
        self.engine = engine

    async def create_seat(self, event_id, row, number, price):
        async with AsyncSession(self.engine) as session:
            seat = Seat(event_id=event_id, row=row, number=number, price=price)
            session.add(seat)
            await session.commit()

    async def get_seat_for_event_and_update_status_reserved(self, id, event_id):
        async with AsyncSession(self.engine) as session:
            seat = await session.scalar(select(Seat).where(Seat.id==id and Seat.event_id==event_id).with_for_update())
            seat.status = SeatStatus.reserved
            await session.commit()

    async def get_seats_for_event(self, event_id):
        async with AsyncSession(self.engine) as session:
            res = await session.execute(select(Seat).where(Seat.event_id==event_id))

            seats = []

            for seat in res:
                seats.append({
                    "id": seat[0].id,
                    "event_id": seat[0].id,
                    "row": seat[0].row,
                    "number": seat[0].number,
                    "price": seat[0].price
                })

            return seats

    async def update_seat_status(self, id, status):
        async with AsyncSession(self.engine) as session:
            await session.execute(update(Seat).where(Seat.id==id).values(status=status))
            await session.commit()


    async def delete_seat(self, id):
        async with AsyncSession(self.engine) as session:
            await session.execute(delete(Seat).where(Seat.id==id))
            await session.commit()