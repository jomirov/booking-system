import pytest
from httpx import AsyncClient
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User
from ..dependencies import verify_password

pytestmark = pytest.mark.anyio

async def test_user_creation(client: AsyncClient, session: AsyncSession):
    expected_status_code = 201
    expected_user_email = "testemail@gmail.com"

    post_response = await client.post("http://localhost:8000/api/users", json={"email": expected_user_email, "password": "testpassword123"})

    new_user = await session.scalar(select(User).order_by(desc(User.id)))
    new_user_email = new_user.email

    assert post_response.status_code == expected_status_code
    assert new_user_email == expected_user_email

async def test_user_selection(client: AsyncClient, session: AsyncSession):
    expected_status_code = 200
    expected_user_email = "selectiontestemail@gmail.com"

    session.add(User(id=10, email=expected_user_email, hashed_password="fake_hashed_password123"))
    await session.commit()

    get_response = await client.get("http://localhost:8000/api/users/10")
    
    assert get_response.status_code == expected_status_code
    assert get_response.json()["email"] == expected_user_email

async def test_user_email_and_password_update(client: AsyncClient, session: AsyncSession):
    expected_status_code = 200
    expected_new_email = "newchangedtestemail@gmail.com"
    expected_new_password = "newchangedfakepassword123"

    session.add(User(id=11, email="sometestemail@gmail.com", hashed_password="fake_hashed_password12849"))
    await session.commit()

    put_email_response = await client.put("http://localhost:8000/api/users/11/email", content=expected_new_email)
    put_password_response = await client.put("http://localhost:8000/api/users/11/password", content=expected_new_password)

    updated_user = await session.scalar(select(User).where(User.id==11))

    assert put_email_response.status_code == 200
    assert put_password_response.status_code == 200
    assert updated_user.email == expected_new_email
    assert True == verify_password(updated_user.hashed_password, expected_new_password)

async def test_user_deletion(client: AsyncClient, session: AsyncSession):
    expected_status_code = 200

    session.add(User(id=12, email="emailfordeletiontest@gmail.com", hashed_password="fakehashedpassword13894"))
    await session.commit()

    delete_response = await client.delete("http://localhost:8000/api/users/12")

    has_user_been_deleted = True if not await session.scalar(select(User).where(User.id==12)) else False

    assert delete_response.status_code == expected_status_code
    assert has_user_been_deleted == True