from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database.db import init_models, get_engine, get_db_url
from .routers import users

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
# app.include_router(events.router)
# app.include_router(seats.router)
# app.include_router(bookings.router)