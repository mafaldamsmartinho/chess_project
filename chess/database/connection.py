from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


DATABASE_URL = ("postgresql+psycopg2://postgres:2000@localhost:5432/postgres")

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=5,
                       max_overflow=20,)
# pool_pre_ping - Test connections before giving them to the application.
# pool_size - Maximum permanent connections in the pool.
# max_overflow - Extra temporary connections allowed when the pool is full.

SessionLocal = sessionmaker(bind=engine, autoflush=False,
                            expire_on_commit=False,)
# bind=engine → sessions created by SessionLocal use this database/engine.
# autoflush=False → SQLAlchemy won't automatically send pending changes to the DB before queries; you control flushing more explicitly.
# expire_on_commit=False → after commit(), your object's attributes remain accessible without SQLAlchemy automatically reloading them from the database.


def get_session() -> Generator[Session, None, None]:
    """Provide a database session and always close it afterwards."""
    with SessionLocal() as session:
        yield session