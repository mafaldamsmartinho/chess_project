from contextlib import asynccontextmanager

from chess.database.connection import engine
from chess.database.create_tables import create_tables
from chess.api.routes import router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


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
