from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from datetime import datetime
from ..models.user import User
from ..dependencies import hash_password
from ..database.database import get_engine

class UserRepository:
    def __init__(self, engine = Depends(get_engine)):
        self.engine = engine

    async def create_user(self, email, password):
        async with AsyncSession(self.engine) as session:
            user = User(email=email, hashed_password=hash_password(password))
            session.add(user)
            await session.commit()

    async def get_all_users(self):
        async with AsyncSession(self.engine) as session:
            res = await session.execute(select(User))

            users = []

            for user in res:
                users.append({
                    "id": user[0].id,
                    "email": user[0].email,
                    "hashed_password": user[0].hashed_password,
                    "role": user[0].role.value,
                    "created_at": datetime.strftime(user[0].created_at, "%Y-%m-%d %H:%M:%S"),
                    "updated_at": datetime.strftime(user[0].updated_at, "%Y-%m-%d %H:%M:%S")
                })

            return users

    async def delete_user(self, id):
        async with AsyncSession(self.engine) as session:
            session.execute(delete(User).where(User.id==id))
            await session.commit()