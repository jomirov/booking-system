import os
from dotenv import load_dotenv, set_key
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from ..models.base import Base
from ..models import booking, event, seat, user

load_dotenv()

def get_db_url():
    PSQL_USERNAME = os.getenv("PSQL_USERNAME")
    PSQL_PASSWORD = os.getenv("PSQL_PASSWORD")
    PSQL_HOST = os.getenv("PSQL_HOST")
    DB_NAME = os.getenv("DB_NAME")
    db_url = f"postgresql+asyncpg://{PSQL_USERNAME}:{PSQL_PASSWORD}@{PSQL_HOST}/{DB_NAME}"
    return db_url

def get_engine(db_url: str = Depends(get_db_url)):
    return create_async_engine(db_url)

async def init_models(engine):
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

async def drop_models(engine):
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.drop_all)