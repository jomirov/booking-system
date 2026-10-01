from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from ..models.user import UserCreate
from ..repositories.userrepository import UserRepository

router = APIRouter()

@router.post('/api/users')
async def make_user(user: UserCreate, repo: UserRepository = Depends(UserRepository)):
    try:
        await repo.create_user(user.email, user.password)
    except IntegrityError:
        HTTPException(status_code=409, detail="User is already exist")
    return JSONResponse({"message": "User has been created"}, status_code=201)

@router.get('/api/users')
async def show_all_users(repo: UserRepository = Depends(UserRepository)):
    users = await repo.get_all_users()
    return JSONResponse(users)

@router.delete('/api/users/{id}')
async def remove_user(id: int, repo: UserRepository = Depends(UserRepository)):
    await repo.delete_user(id)
    return JSONResponse({"message": "User has been removed"})