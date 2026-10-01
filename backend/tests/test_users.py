from sqlalchemy import select, func
from ..models.user import User
from .conftest import db_session, client, pytestmark

async def test_user_creation(db_session, client):
    print("user creation")
    test_email = "testemail@gmail.com"
    test_password = "testpassword123"

    response = await client.post("http://localhost:8000/api/users", 
                      headers={"Content-Type": "application/json"}, 
                      json={"email": test_email, "password": test_password})

    assert response.status_code == 201
    
    result = await db_session.scalar(select(User))
    assert result.email == test_email

async def test_email_uniqueness(db_session, client):
    print("unique email")
    test_email = "uniquemail@gmail.com"
    test_password = "testpassword123"
    
    for i in range(1):
        response = await client.post("http://localhost:8000/api/users",
                                    headers = {"Content-Type": "application/json"},
                                    json={"email": test_email, "password": test_password})
        if i == 1:
            assert response.status_code == 409

    count = await db_session.scalar(select(func.count(User.id)).where(User.email==test_email))
    assert count == 1