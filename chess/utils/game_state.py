from chess.models.board import ALLOWED_POSITIONS
from chess.models.game import Game


def split_opponents(game: Game) -> list[list[str]]:
    """Splits player turn pieces into one list, and possible moves into another list"""
    start_positions: list = []
    end_positions: list = []

    for el in ALLOWED_POSITIONS:
        piece = game.board.get_piece(position=el)
        if piece is not None and piece.colour == game.turn:
            start_positions.append(el)
        else:
            end_positions.append(el)
    return [start_positions, end_positions]
