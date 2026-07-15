from chess.models.board import NUM_COLS, NUM_ROWS
from chess.models.game import Game


def split_opponents(game: Game) -> list[list[tuple[int, int]]]:
    """Splits player turn pieces into one list, and the rest in another."""
    start_positions: list = []
    end_positions: list = []

    for col in range(NUM_COLS):
        for row in range(NUM_ROWS):
            piece = game.board.get_piece_by_index(index_position=(row, col))
            if piece is not None and piece.colour == game.turn:
                start_positions.append((row, col))
            else:
                end_positions.append((row, col))
    return [start_positions, end_positions]
