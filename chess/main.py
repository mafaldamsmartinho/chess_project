from chess.database.repositories import create_tables
from chess.api.routes import router
from fastapi import FastAPI

create_tables()
api = FastAPI()
api.include_router(router)
