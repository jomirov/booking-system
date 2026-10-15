from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from .baserepository import BaseRepository
from ..models.user import User
from ..dependencies import hash_password

class UserRepository(BaseRepository):
    async def create_user(self, email, password):
        async with AsyncSession(self.engine) as session:
            hashed_password = hash_password(password)
            
            user = User(email=email, hashed_password=hashed_password)

            session.add(user)
            await session.commit()

    async def get_user(self, id):
        async with AsyncSession(self.engine) as session:
            res = await session.scalar(select(User).where(User.id==id))

            if not res:
                raise ValueError

            return {
                "id": res.id,
                "email": res.email,
                "hashed_password": res.hashed_password
            }

    async def delete_user(self, id):
        async with AsyncSession(self.engine) as session:
            deleted_user_id = await session.execute(delete(User).where(User.id==id).returning(User.id))
            if not deleted_user_id:
                raise ValueError
            await session.commit()

    async def update_email(self, id, new_email):
        async with AsyncSession(self.engine) as session:
            updated_user_id = await session.execute(update(User).where(User.id==id).values(email=new_email).returning(User.id))
            if not updated_user_id:
                raise ValueError
            await session.commit()

    async def update_password(self, id, new_password):
        async with AsyncSession(self.engine) as session:
            new_hashed_password = hash_password(new_password)
            updated_user_id = await session.execute(update(User).where(User.id==id).values(hashed_password=new_hashed_password).returning(User.id))
            if not updated_user_id:
                raise ValueError
            
            await session.commit()