import pytest
from datetime import datetime, timedelta
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from ..models.event import Event

pytestmark = pytest.mark.anyio

async def test_event_creation(client: AsyncClient, session: AsyncSession):
    expected_status_code = 201
    expected_event_title = "testeventtitle"
    
    response = await client.post('http://localhost:8000/api/events', json={"title": expected_event_title, "date": "2027-05-22", "location": "Almaty"})

    event = await session.scalar(select(Event).order_by(desc(Event.id)))

    assert response.status_code == expected_status_code
    assert event.title == expected_event_title

async def test_event_selection(client: AsyncClient, session: AsyncSession):
    expected_status_code = 200
    expected_event_title = "someeventitle"
    expected_event_date = datetime.now() + timedelta(days=30)
    expected_event_location = "Almaty"

    session.add(Event(id=10, title=expected_event_title, date=expected_event_date, location=expected_event_location))
    await session.commit()

    response = await client.get("http://localhost:8000/api/events/10")

    assert response.status_code == expected_status_code
    assert response.json()["title"] == expected_event_title
    assert response.json()["date"] == datetime.strftime(expected_event_date, "%Y-%m-%d")
    assert response.json()["location"] == expected_event_location

async def test_event_deletion(client: AsyncClient, session: AsyncSession):
    expected_status_code = 200

    session.add(Event(id=11, title="someeventtitle", date=datetime.now() + timedelta(days=30), location="Almaty"))
    await session.commit()

    response = await client.delete("http://localhost:8000/api/events/11")
    
    has_event_been_deleted = True if not await session.scalar(select(Event).where(Event.id==11)) else False

    assert response.status_code == expected_status_code
    assert True == has_event_been_deleted