from chess.database.repositories import create_tables
from chess.api.routes import router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

create_tables()
api = FastAPI()
api.include_router(router=router)
api.mount(path="/ui", app=StaticFiles(directory="frontend", html=True), name="frontend")
