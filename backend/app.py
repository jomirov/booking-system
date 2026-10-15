from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .database.db import init_models, get_engine, get_db_url
from .routers import users, events, seats, bookings
from .dependencies import generate_token, verify_token, authenticate_user
from .repositories.userrepository import UserRepository

@asynccontextmanager
async def lifespan(app: FastAPI):
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
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends(), repo: UserRepository = Depends(UserRepository)):
    user = await repo.get_user_by_email(form_data.username)
    is_authenticated = authenticate_user(user, form_data.password)

    if not is_authenticated:
        raise credentials_exception
    
    access_token = generate_token(form_data.username)
    return JSONResponse({"access_token": access_token, "token_type": "bearer"})

@app.get('/users/me')
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        email = verify_token(token)
    except:
        raise credentials_exception
    
    return JSONResponse({"current_user_email": email})