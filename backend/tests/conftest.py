import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from httpx import ASGITransport, AsyncClient

from ..app import app
from ..database.db import get_engine, drop_models, init_models

test_db_url = f"postgresql+asyncpg://postgres:testpassword123@localhost:5432/test_booking_system"

@pytest.fixture(scope="function", autouse=True)
async def session():
    test_engine = create_async_engine(test_db_url)
    app.dependency_overrides[get_engine] = lambda: test_engine
    await init_models(test_engine)
    async with AsyncSession(test_engine) as session:
        yield session
    await drop_models(test_engine)

@pytest.fixture(scope="function", autouse=True)
def client():
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport)
    yield client
#--volume test-db:/var/lib/postgresql -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=testpassword123 -e POSTGRES_DB=test_booking_system -p 5432:5432 postgres