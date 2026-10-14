import os
from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from ..models.base import Base
from ..models import user, event, seat, booking

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

def get_db_url():
    return f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

def get_engine(db_url: str = Depends(get_db_url)):
    return create_async_engine(db_url)

async def init_models(engine: AsyncEngine):
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

async def drop_models(engine: AsyncEngine):
    async with engine.begin() as session:
        await session.run_sync(Base.metadata.drop_all)