import os, time
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from ..models.base import Base
from ..models import user, event, seat, booking

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

db_url = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

try:
    engine = create_async_engine(db_url)
    print("DBMS CONNECTION IS SUCCESSFUL")
except:
    pass

def get_engine():
    return engine

async def init_models(engine: AsyncEngine):
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

async def drop_models(engine: AsyncEngine):
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.drop_all)