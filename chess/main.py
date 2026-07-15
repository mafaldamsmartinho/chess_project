from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from chess.api.routes import router
from chess.database.connection import engine
from chess.database.create_tables import create_tables


@asynccontextmanager
async def lifespan(api: FastAPI):
    try:
        create_tables()
        yield
    finally:
        engine.dispose()

api = FastAPI(lifespan=lifespan)
api.include_router(router=router)
api.mount(path="/ui", app=StaticFiles(directory="frontend", html=True), name="frontend")
