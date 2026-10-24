from ..models.user import User
from ..models.event import Event
from ..models.seat import Seat
from ..models.booking import Booking

import pytest, asyncio
from datetime import datetime
from httpx import AsyncClient
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.anyio

async def test_asynchronous_requests_for_booking(client: AsyncClient, session: AsyncSession):
    session.add(User(id=77, email="testmail1281924@gmail.com", hashed_password="testpasswordasd"))
    session.add(User(id=78, email="test124mail1281924@gmail.com", hashed_password="testp124asswordasd"))
    session.add(Event(id=77, title="Concert", date=datetime.strptime("2026-12-24", "%Y-%m-%d"), location="Almaty"))
    session.add(Seat(id=77, event_id=77, row="W", number=10, price=100000))
    await session.commit()
    
    responses = await asyncio.gather(
        client.post("http://localhost:8000/api/bookings", json={"seat_id": 77, "user_id": 77}),
        client.post("http://localhost:8000/api/bookings", json={"seat_id": 77, "user_id": 78}),
        return_exceptions=True
    )

    response1, response2 = responses
    count = await session.scalar(select(func.count(Booking.id)))
    status_codes = [response1.status_code, response2.status_code]

    assert count == 1
    assert 201 in status_codes
    assert 409 in status_codes