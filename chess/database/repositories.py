from chess.database.connection import get_connection
from psycopg2.extras import Json


#  Creates new player row
def create_player(name: str):

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""--sql
                INSERT INTO players (name)
                VALUES (%s)
                RETURNING id;""", (name,))

    player_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return player_id


#  Creates a new game row, with auto id, starting as white.
def create_game(white_id, black_id, board_state):

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""--sql
                INSERT INTO games (white_id, black_id, status, turn, board)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;""", (white_id, black_id, 'ongoing',
                                   'white', Json(board_state),))

    game_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return game_id


#  Returns game details from a game_id
def get_game(game_id):

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""--sql
                SELECT * FROM games WHERE id = %s""", (game_id,))

    game_data = cur.fetchone()
    if game_data is None:
        raise Exception(f'There is no game id {game_id}')

    cur.close()
    conn.close()
    return game_data


#  Updates game status, turn and board current state based on game_id
def update_game(game_id, current_turn, status, board_state):
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
    if update_game_data is None:
        raise Exception(f'Update for game id {game_id} not succsessful')

    conn.commit()
    cur.close()
    conn.close()
    return update_game_data


#  Saves move to move history table
def save_move(game_id, move_number, start, end, piece, captured_piece):
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


#  Returns moves data from specific game
def get_moves(game_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""--sql
                SELECT * FROM moves WHERE id = %s""", (game_id,))

    move_data = cur.fetchall()
    if move_data is None:
        raise Exception(f'There is no moves for this game id {game_id}')

    cur.close()
    conn.close()
    return move_data


def create_tables():  # Creates players, games states and moves history tables if does not exist yet
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""--sql
                CREATE TABLE IF NOT EXISTS players (id SERIAL
                PRIMARY KEY, name TEXT NOT NULL);""")

    cur.execute("""--sql
                CREATE TABLE IF NOT EXISTS games (id SERIAL
                PRIMARY KEY, white_id INTEGER, black_id INTEGER,
                status TEXT NOT NULL CHECK ( status IN ('ongoing',
                'white_win', 'black_win', 'draw')),
                turn TEXT NOT NULL CHECK ( turn IN ('black',
                'white')), board JSONB);""")

    cur.execute("""--sql
                CREATE TABLE IF NOT EXISTS moves (id SERIAL
                PRIMARY KEY, game_id INTEGER, move_number INTEGER,
                start_square TEXT NOT NULL, end_square TEXT NOT NULL,
                piece TEXT NOT NULL, captured_piece TEXT);""")

    conn.commit()
    cur.close()
    conn.close()
