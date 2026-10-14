import pytest, os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import ASGITransport, AsyncClient

from ..app import app
from ..database.db import init_models, drop_models, get_db_url, get_engine

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
TEST_POSTGRES_HOST = os.getenv("TEST_POSTGRES_HOST")
TEST_POSTGRES_DB = os.getenv("TEST_POSTGRES_DB")

test_db_url = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{TEST_POSTGRES_HOST}:{POSTGRES_PORT}/{TEST_POSTGRES_DB}"

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