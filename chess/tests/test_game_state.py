import pytest

from chess.models.board import Board
from chess.models.enums import GameTurn, PieceType
from chess.models.game import Game
from chess.models.piece import Piece
from chess.utils.game_state import split_opponents


@pytest.fixture
def empty_board():
    board = Board()
    for row in range(8):
        for col in range(8):
            board.set_piece(index_position=(row, col), piece=None)
    return board


def place_piece(board: Board, position: str, colour: GameTurn, piece_type: PieceType):
    board.set_piece(
        index_position=board.position_to_index(position),
        piece=Piece(colour=colour, type=piece_type, index=1),
    )


class TestSplitOpponents:
    def test_split_opponents_returns_current_turn_positions(self):
        game = Game(turn=GameTurn.WHITE)

        start_positions, end_positions = split_opponents(game=game)

        assert len(start_positions) == 16
        assert len(end_positions) == 48
        assert (0, 4) in start_positions
        assert (1, 4) in start_positions
        assert (7, 4) in end_positions
        assert (3, 3) in end_positions

    def test_split_opponents_uses_game_turn(self):
        game = Game(turn=GameTurn.BLACK)

        start_positions, end_positions = split_opponents(game=game)

        assert len(start_positions) == 16
        assert len(end_positions) == 48
        assert (7, 4) in start_positions
        assert (6, 4) in start_positions
        assert (0, 4) in end_positions

    def test_split_opponents_keeps_board_scan_order(self):
        game = Game(turn=GameTurn.WHITE)

        start_positions, _ = split_opponents(game=game)

        assert start_positions[:4] == [(0, 0), (1, 0), (0, 1), (1, 1)]

    def test_split_opponents_handles_custom_board(self, empty_board):
        game = Game(turn=GameTurn.WHITE)
        place_piece(empty_board, "e1", GameTurn.WHITE, PieceType.KING)
        place_piece(empty_board, "h8", GameTurn.BLACK, PieceType.KING)
        game.set_board(empty_board)

        start_positions, end_positions = split_opponents(game=game)

        assert start_positions == [(0, 4)]
        assert len(end_positions) == 63
        assert (7, 7) in end_positions
