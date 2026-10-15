import pytest, os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import ASGITransport, AsyncClient

from ..app import app
from ..database.db import init_models, drop_models, get_db_url, get_engine

load_dotenv()

test_db_url = f"postgresql+asyncpg://postgres:testpassword123@localhost:5432/test_booking_system"

pytestmark = pytest.mark.anyio

@pytest.fixture(name="session")
async def session():
    app.dependency_overrides[get_db_url] = lambda: test_db_url
    engine = get_engine(test_db_url)
    await init_models(engine)
    async with AsyncSession(engine) as session:
        yield session
    await drop_models(engine)

@pytest.fixture(name="client")
async def client():
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport)
    yield client
#--volume test-db:/var/lib/postgresql -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=testpassword123 -e POSTGRES_DB=test_booking_system -p 5432:5432 postgres