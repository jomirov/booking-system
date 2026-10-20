from datetime import datetime, timezone
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from .baserepository import BaseRepository
from ..models.event import Event

class EventRepository(BaseRepository):
    async def create_event(self, title, date):
        async with AsyncSession(self.engine) as session:
            date_parsed = datetime.strptime(date, "%Y-%m-%d")
            if date_parsed.timestamp() < datetime.now(tz=timezone.utc).timestamp():
                raise ValueError

            event = Event(title=title, date=datetime.strptime(date, "%Y-%m-%d"))
            session.add(event)
            await session.commit()

    async def get_active_events(self):
        async with AsyncSession(self.engine) as session:
            res = await session.scalars(select(Event).where(Event.date > datetime.now(timezone.utc)))

            events = [
                {
                    "id": event.id,
                    "title": event.title,
                    "date": datetime.strftime(event.date, "%Y-%m-%d")
                } for event in res
            ]

            return events

    async def get_event(self, id):
        async with AsyncSession(self.engine) as session:
            event = await session.scalar(select(Event).where(Event.id==id))

            if not event:
                raise ValueError

            return {
                "id": event.id,
                "title": event.title,
                "date": datetime.strftime(event.date, "%Y-%m-%d")
            }

    async def delete_event(self, id):
        async with AsyncSession(self.engine) as session:
            deleted_event_id = await session.execute(delete(Event).where(Event.id==id).returning(Event.id))
            await session.commit()
            
            if not deleted_event_id:
                raise ValueError

    async def update_event_title(self, id, new_title):
        async with AsyncSession(self.engine) as session:
            updated_event_id = await session.execute(update(Event).where(Event.id==id).values(title=new_title).returning(Event.id))
            await session.commit()

            if not updated_event_id:
                raise ValueError