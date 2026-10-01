from .conftest import client, db_session, pytestmark

async def test_valid_date(client, db_session):
    print("valid event date")
    response = await client.post("http://localhost:8000/api/events", 
                                 headers={"Content-Type": "application/json"},
                                 json={"title": "Football", "date": "2026-10-01"})
    assert response.status_code == 201

async def test_invalid_date(client, db_session):
    print("invalid event date")
    response = await client.post("http://localhost:8000/api/events", 
                                 headers={"Content-Type": "application/json"},
                                 json={"title": "Cinema", "date": "2026-08-30"})
    assert response.status_code == 400