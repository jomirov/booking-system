import datetime
from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.event import Event
from ..database.database import get_engine

class EventRepository:
    def __init__(self, engine = Depends(get_engine)):
        self.engine = engine

    async def create_event(self, title, date):
        async with AsyncSession(self.engine) as session:
            dtime = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            event = Event(title=title, date=dtime)
            session.add(event)
            await session.commit()

    async def get_all_events(self):
        async with AsyncSession(self.engine) as session:
            res = await session.execute(select(Event))

            events = []

            for event in res:
                events.append({
                    "id": event[0].id,
                    "title": event[0].title,
                    "date": datetime.strftime(event[0].date, "%Y-%m-%d")
                })

            return events

    async def delete_event(self, id):
        async with AsyncSession(self.engine) as session:
            await session.execute(delete(Event).where(Event.id==id))
            await session.commit()