from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine
from ..database.db import get_engine

class BaseRepository:
    def __init__(self, engine = Depends(get_engine)):
        self.engine: AsyncEngine = engine