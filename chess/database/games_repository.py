from chess.models.board import Board
from chess.utils.serialization import SerializedBoard, serialize_board

from chess.database.models import Games, Players, GameStatus, GameTurn

from sqlalchemy import or_, select
from sqlalchemy.orm import aliased, Session


def create_game(white_id: int, black_id: int, board_state: Board, session: Session) -> int:
    """Create new game"""
    board_dict = serialize_board(board=board_state)
    game = Games(white_id=white_id, black_id=black_id, board=board_dict)
    session.add(game)
    session.flush()
    return game.id


def get_game_by_id(game_id: int, session: Session) -> Games | None:
    """Returns game details from DB"""
    return session.get(Games, game_id)


def update_game(game_id: int, current_turn: GameTurn, status: GameStatus, board_state: SerializedBoard, session: Session) -> Games | None:
    """Updates game status, turn and board current state in DB"""
    game_data = session.get(Games, game_id)
    if game_data is None:
        return None

    game_data.turn = GameTurn(current_turn).value
    game_data.status = GameStatus(status).value
    game_data.board = board_state
    session.flush()
    return game_data


def get_active_bot_game_ids(session: Session) -> list[int]:
    """Returns all active games where bots are playing"""
    white_player = aliased(Players)
    black_player = aliased(Players)

    statement = (
        select(Games.id)
        .join(white_player, Games.white_id == white_player.id)
        .join(black_player, Games.black_id == black_player.id)
        .where(
            Games.status == GameStatus.ONGOING,
            or_(
                (Games.turn == GameTurn.WHITE) & (white_player.bot.is_(True)),
                (Games.turn == GameTurn.BLACK) & (black_player.bot.is_(True)),
            ),
        )
    )
    return list(session.scalars(statement).all())
