from chess.database.models import Moves

from sqlalchemy import select
from sqlalchemy.orm import Session


def save_move(game_id: int, move_number: int, start: str, end: str, piece: str, captured_piece: str | None, session: Session) -> int:
    """Adds new move into DB"""
    move = Moves(game_id=game_id, move_number=move_number,
                 start_square=start, end_square=end, piece=piece,
                 captured_piece=captured_piece)
    session.add(move)
    session.flush()
    return move.id


def get_moves_by_game_id(game_id: int, session: Session) -> list[Moves]:
    """Returns moves data from a game."""
    statement = (
        select(Moves)
        .where(Moves.game_id == game_id)
        .order_by(Moves.move_number)
    )
    return list(session.scalars(statement).all())
