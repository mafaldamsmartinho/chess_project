from typing import Any

from fastapi import HTTPException
from psycopg2.extras import Json

from chess.database.db_manager import get_connection, release_connection
from chess.models.enums import GameStatus, GameTurn
from chess.models.board import Board
from chess.utils.serialization import serialize_board


def create_game(white_id: int, black_id: int, board_state: Board) -> int:
    """Create new game"""
    pool_conn = get_connection()
    cur = pool_conn.cursor()
    board_dict: Json = serialize_board(board=board_state)
    cur.execute("""--sql
                INSERT INTO games (white_id, black_id, status, turn, board)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;""", (white_id, black_id, GameStatus.ONGOING.value,
                                   GameTurn.WHITE.value, board_dict,))

    game_id = cur.fetchone()[0]
    pool_conn.commit()
    cur.close()
    release_connection(conn=pool_conn)
    return game_id


def get_game_by_id(game_id: int) -> tuple[int, int, int, str, str, Any]:
    """Returns game details from DB"""
    pool_conn = get_connection()
    cur = pool_conn.cursor()
    cur.execute("""--sql
                SELECT * FROM games WHERE id = %s""", (game_id,))

    game_data = cur.fetchone()
    if not game_data:
        raise HTTPException(status_code=404, detail=f'error DB: Game id {game_id} not found')

    cur.close()
    release_connection(conn=pool_conn)
    return game_data


def update_game(game_id: int, current_turn: GameTurn | str, status: GameStatus | str, board_state: list[list[dict[str, str | int] | None]]) -> tuple[int, int, int, str, str, Any]:
    """Updates game status, turn and board current state in DB"""
    pool_conn = get_connection()
    cur = pool_conn.cursor()
    current_turn_value = GameTurn(current_turn).value
    status_value = GameStatus(status).value
    cur.execute("""--sql
                UPDATE games SET
                turn = %s,
                status = %s,
                board = %s
                WHERE id = %s;""",
                (current_turn_value, status_value, Json(board_state), game_id,))
    pool_conn.commit()
    cur.close()
    release_connection(conn=pool_conn)
    return


def get_active_bot_game_ids() -> list[int] | None:
    """Returns all active games where bots are playing"""
    pool_conn = get_connection()
    cur = pool_conn.cursor()
    cur.execute("""--sql
                    SELECT g.id
                    FROM games g
                    JOIN players w ON g.white_id = w.id
                    JOIN players b ON g.black_id = b.id
                    WHERE g.status = %s
                    AND (
                        (g.turn = %s AND w.bot = true)
                        OR
                        (g.turn = %s AND b.bot = true)
                    );""", (GameStatus.ONGOING.value, GameTurn.WHITE.value, GameTurn.BLACK.value,))
    games = cur.fetchall()
    if not games:
        return []
    bot_games = []
    for el in games:
        bot_games.append(el[0])

    cur.close()
    release_connection(conn=pool_conn)
    return bot_games
