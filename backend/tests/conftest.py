import pytest, os
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient, ASGITransport
from ..database.database import get_engine, get_db_url, init_models, drop_models
from ..app import app

pytestmark = pytest.mark.anyio

@pytest.fixture
async def client():
    transport = ASGITransport(app)
    client = AsyncClient(transport=transport)
    yield client

@pytest.fixture
async def db_session():
    db_url = f"postgresql+asyncpg://{os.getenv("PSQL_USERNAME")}:{os.getenv("PSQL_PASSWORD")}@{os.getenv("PSQL_HOST")}/{os.getenv("TEST_DB_NAME")}"
    app.dependency_overrides[get_db_url] = lambda: db_url
    engine = get_engine(db_url)
    await init_models(engine)
    async with AsyncSession(engine) as session:
        yield session
    await drop_models(engine)