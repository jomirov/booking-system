from contextlib import asynccontextmanager
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, Depends, HTTPException, Cookie
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .database.db import init_models, get_engine, get_db_url
from .routers import users, events, seats, bookings
from .dependencies import generate_token, verify_token, authenticate_user
from .repositories.userrepository import UserRepository

@asynccontextmanager
async def lifespan(app: FastAPI):
    from .utils import redis
    engine = get_engine(get_db_url())
    await init_models(engine)
    yield
    # drop_models(engine)

app = FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware,
                   allow_credentials=True,
                   allow_headers=["*"],
                   allow_methods=["*"],
                   allow_origins=["*"])

app.include_router(users.router)
app.include_router(events.router)
app.include_router(seats.router)
app.include_router(bookings.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=401,
    detail="Couldn't validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

@app.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), repo: UserRepository = Depends(UserRepository)):
    try:
        user = await repo.get_user_by_email(form_data.username)
    except ValueError:
        raise credentials_exception
    
    is_authenticated = authenticate_user(user, form_data.password)

    if not is_authenticated:
        raise credentials_exception
    
    access_token = generate_token(user["id"], form_data.username)
    response = JSONResponse({"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=access_token, samesite="none", secure=True, max_age=600)
    return response

@app.delete("/token")
async def drop_token():
    response = JSONResponse({"message": "Your token is dropped"})
    response.delete_cookie("access_token")
    return response

@app.get('/users/me')
async def get_current_user(access_token: str = Cookie()):
    try:
        user = verify_token(access_token)
    except:
        raise credentials_exception
    
    return JSONResponse({"current_user_id": user["id"], "current_user_email": user["email"]})