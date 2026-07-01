from contextlib import asynccontextmanager

from chess.database.repositories import create_tables
from chess.database.db_manager import disconnect_database, connect_database
from chess.api.routes import router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(api: FastAPI):
    connect_database()
    try:
        create_tables()
        yield
    finally:
        disconnect_database()


api = FastAPI(lifespan=lifespan)
api.include_router(router=router)
api.mount(path="/ui", app=StaticFiles(directory="frontend", html=True), name="frontend")
