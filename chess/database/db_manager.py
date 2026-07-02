from psycopg2 import pool
from psycopg2.extensions import connection


postgreSQL_pool: pool.SimpleConnectionPool | None = None


def connect_database() -> None:
    """Create the database connection pool when the app starts."""
    global postgreSQL_pool
    if postgreSQL_pool is not None:
        return

    postgreSQL_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=20,
        user="postgres",
        password="2000",
        host="127.0.0.1",
        port="5432",
        database="postgres",
    )


def disconnect_database() -> None:
    """Close all pooled database connections when the app stops."""
    global postgreSQL_pool
    if postgreSQL_pool is None:
        return

    postgreSQL_pool.closeall()
    postgreSQL_pool = None


def get_connection() -> connection:
    """Get a database connection from the pool."""
    if postgreSQL_pool is None:
        connect_database()
    return postgreSQL_pool.getconn()


def release_connection(conn: connection) -> None:
    """Return a database connection to the pool."""
    if postgreSQL_pool is None:
        conn.close()
        return

    postgreSQL_pool.putconn(conn)
