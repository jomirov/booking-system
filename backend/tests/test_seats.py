import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from datetime import datetime, timedelta

from .base_test import pytestmark, client, session
from ..models.seat import Seat, SeatStatus
from ..models.event import Event

pytest.mark.usefixtures("client")
pytest.mark.usefixtures("session")

async def test_seats_creation(client: AsyncClient, session: AsyncSession):
    expected_status_code = 201

    expected_seats = []
    for i in range(1, 6):
        expected_seats.append({
            "row": "A",
            "number": i,
            "price": 10000,
        })

    session.add(Event(id=5, title="sometitle", date=datetime.now()+timedelta(days=30)))
    await session.commit()
    response = await client.post("http://localhost:8000/api/seats?event_id=5", json=expected_seats)

    q = await session.execute(select(Seat.row, Seat.number, Seat.price))
    seats = [{"row": seat.row, "number": seat.number, "price": seat.price} for seat in q]

    assert response.status_code == expected_status_code
    assert seats == expected_seats

async def test_seats_selection_by_event(client: AsyncClient, session: AsyncSession):
    expected_status_code = 200
    test_data = [[10,10,"B",1,15000], [11,10,"B",2,15000]]
    expected_data = [
        {
            "id": data[0],
            "event_id": data[1],
            "row": data[2],
            "number": data[3],
            "price": data[4],
            "status": SeatStatus.free.value
        } for data in test_data
    ]

    session.add(Event(id=10, title="sometitle", date=datetime.now() + timedelta(days=30)))
    session.add(Seat(id=test_data[0][0], event_id=test_data[0][1], row=test_data[0][2], number=test_data[0][3], price=test_data[0][4]))
    session.add(Seat(id=test_data[1][0], event_id=test_data[1][1], row=test_data[1][2], number=test_data[1][3], price=test_data[1][4]))
    await session.commit()

    response = await client.get("http://localhost:8000/api/seats?event_id=10")

    assert response.status_code == expected_status_code
    assert response.json() == expected_data


async def test_seat_deletion(client: AsyncClient, session: AsyncSession):
    expected_status_code = 200

    session.add(Event(id=15, title="someevent", date=datetime.now() + timedelta(days=30)))
    session.add(Seat(id=15, event_id=15, row="C", number=12, price=20000))
    await session.commit()
    response = await client.delete("http://localhost:8000/api/seats/15")

    has_seat_been_deleted = True if not await session.scalar(select(Seat).where(Seat.id==15)) else False

    assert response.status_code == expected_status_code
    assert True == has_seat_been_deleted

async def test_seat_update(client: AsyncClient, session: AsyncSession):
    expected_status_code = 200
    expected_updated_seat = {
        "row": "E",
        "number": 27,
        "price": 25000
    }

    session.add(Event(id=30, title="someeventtitle123", date=datetime.now() + timedelta(days=29)))
    session.add(Seat(id=25, event_id=30, row="D", number=25, price=20000))
    await session.commit()

    response = await client.put("http://localhost:8000/api/seats/25", json={"row": expected_updated_seat["row"], "number": expected_updated_seat["number"], "price": expected_updated_seat["price"]})

    q = await session.scalar(select(Seat).where(Seat.id==25))
    updated_seat = {
        "row": q.row,
        "number": q.number,
        "price": q.price
    }

    assert response.status_code == expected_status_code
    assert updated_seat == expected_updated_seat