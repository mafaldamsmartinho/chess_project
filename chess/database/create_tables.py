from chess.database.connection import engine
from chess.database.models import Base


def create_tables() -> None:
    """Creates players, games and moves tables if does not exist"""
    Base.metadata.create_all(bind=engine)


