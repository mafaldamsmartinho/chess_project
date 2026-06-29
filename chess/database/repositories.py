from chess.database.connection import get_connection
from psycopg2.extras import Json
from chess.models.board import Board
from chess.models.piece import Piece
from fastapi import HTTPException


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


def check_player(name: str, bot: bool) -> int:
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


def get_players(game_id: int) -> tuple:
    """Get player ids from a game id"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""--sql
                SELECT players.name
                FROM games
                JOIN players ON games.white_id = players.id
                WHERE games.id = %s;""", (game_id,))
    white_player = cur.fetchone()[0]
    cur.execute("""--sql
                SELECT players.name
                FROM games
                JOIN players ON games.black_id = players.id
                WHERE games.id = %s;""", (game_id,))
    black_player = cur.fetchone()[0]

    if get_game(game_id) is None:
        raise HTTPException(status_code=404, detail=f"Game id {game_id} not found")
    cur.close()
    conn.close()
    return white_player, black_player


def create_game(white_id, black_id, board_state) -> int:
    """Create new game"""
    conn = get_connection()
    cur = conn.cursor()
    board_dict: Json = serialize_board(board_state)
    cur.execute("""--sql
                INSERT INTO games (white_id, black_id, status, turn, board)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;""", (white_id, black_id, 'ongoing',
                                   'white', board_dict,))

    game_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return game_id


def get_game(game_id) -> list:
    """Returns game details from DB"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""--sql
                SELECT * FROM games WHERE id = %s""", (game_id,))

    game_data = cur.fetchone()
    if not game_data:
        raise HTTPException(status_code=404, detail=f'error DB: Game id {game_id} not found')

    cur.close()
    conn.close()
    return game_data


def update_game(game_id, current_turn, status, board_state) -> list:
    """Updates game status, turn and board current state in DB"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""--sql
                UPDATE games SET
                turn = %s,
                status = %s,
                board = %s
                WHERE id = %s;""",
                (current_turn, status, Json(board_state), game_id,))
    cur.execute("""--sql
                SELECT * FROM games
                WHERE id = %s;""", (game_id,))
    update_game_data = cur.fetchone()
    if not update_game_data:
        raise Exception(f'Game id {game_id} update not succsessful')

    conn.commit()
    cur.close()
    conn.close()
    return update_game_data


def save_move(game_id, move_number, start, end, piece, captured_piece) -> int:
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


def get_moves(game_id: int) -> list[list]:
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


def get_bot_games() -> list:
    """Returns all active games where bots are playing"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""--sql
                    SELECT g.id
                    FROM games g
                    JOIN players w ON g.white_id = w.id
                    JOIN players b ON g.black_id = b.id
                    WHERE g.status = 'ongoing'
                    AND (
                        (g.turn = 'white' AND w.bot = true)
                        OR
                        (g.turn = 'black' AND b.bot = true)
                    );""",)
    bot_games = cur.fetchall()
    cur.close()
    conn.close()
    return bot_games


def create_tables() -> None:
    """Creates players, games and moves tables if does not exist"""
    conn = get_connection()
    cur = conn.cursor()

    file = open('chess/database/schema.sql', 'r')
    schema = file.read()

    cur.execute(schema)
    conn.commit()
    cur.close()
    conn.close()


def serialize_board(board: Board) -> Json:
    """Converts board dict into a json"""
    return Json(board.to_dict())


def deserialize_board(data) -> Board:
    """Converts json board into a board list of el None or Piece"""
    board = Board()
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            if el is not None:
                colour = el.get('colour')
                type = el.get('type')
                index = el.get('index')
                board.board[i][j] = Piece(colour, type, index)
            else:
                board.board[i][j] = None
    return board
