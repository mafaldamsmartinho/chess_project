from fastapi import HTTPException

from chess.database.connection import get_connection
from chess.database.games_repository import get_game_by_id


def create_player(name: str, bot: bool) -> int:
    """Creates new player in DB and returns id"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""--sql
                INSERT INTO players (name, bot)
                VALUES (%s, %s)
                RETURNING id;""", (name, bot,))

    player_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return player_id


def get_player_id_by_name_and_bot(name: str, bot: bool) -> int | None:
    """Checks if player already exists"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""--sql
                SELECT id FROM players WHERE name = %s and bot = %s;""", (name, bot,))

    player = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return player[0] if player is not None else None


def get_players_by_game_id(game_id: int) -> tuple[str, str, bool, bool]:
    """Get player ids from a game id"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""--sql
                SELECT players.name, players.bot
                FROM games
                JOIN players ON games.white_id = players.id
                WHERE games.id = %s;""", (game_id,))
    white_player, white_player_bot = cur.fetchone()
    cur.execute("""--sql
                SELECT players.name, players.bot
                FROM games
                JOIN players ON games.black_id = players.id
                WHERE games.id = %s;""", (game_id,))
    black_player, black_player_bot = cur.fetchone()

    if get_game_by_id(game_id=game_id) is None:
        raise HTTPException(status_code=404, detail=f"Game id {game_id} not found")
    cur.close()
    conn.close()
    return white_player, black_player, white_player_bot, black_player_bot
