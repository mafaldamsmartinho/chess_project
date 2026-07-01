from chess.database.connection import get_connection


def save_move(game_id: int, move_number: int, start: str, end: str, piece: str, captured_piece: str | None) -> int:
    """Adds new move into DB"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""--sql
                INSERT INTO moves (game_id, move_number,
                start_square, end_square,
                piece, captured_piece)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;""",
                (game_id, move_number,
                 start, end,
                 piece, captured_piece,))

    move_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()
    return move_id


def get_moves_by_game_id(game_id: int) -> list[tuple[int, int, int, str, str, str, str | None]]:
    """Returns moves data from game id"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""--sql
                SELECT * FROM moves WHERE game_id = %s""", (game_id,))

    move_data = cur.fetchall()
    if move_data is None:
        return []

    cur.close()
    conn.close()
    return move_data
