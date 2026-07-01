from chess.database.connection import get_connection


def create_tables() -> None:
    """Creates players, games and moves tables if does not exist"""
    conn = get_connection()
    cur = conn.cursor()

    file = open(file='chess/database/schema.sql', mode='r')
    schema = file.read()

    cur.execute(schema)
    conn.commit()
    cur.close()
    conn.close()
