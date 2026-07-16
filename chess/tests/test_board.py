import pytest

from chess.models.board import Board
# from chess.models.enums import PieceType


class TestInitSetupBoard:
    def test_init_board_size_when_setup(self):
        board = Board()
        assert len(board.board) == 8
        assert all(len(row) == 8 for row in board.board)

    # def test_correct_number_pieces_when_setup(self):
    #     board = Board()
    #     for row in board.board:
    #         for el in row:
    #             if el == Piece
    #     assert len(board.board) == 8
    #     assert all(el == Piece for row in board.board)


class TestIsValidPosition:
    @pytest.mark.parametrize(
        "position, expected",
        [
            ("a2", True),
            ("h8", True),
            ("z9", False),
            ("a9", False),
        ],
    )
    def test_returns_bool_when_valid_position(self, position, expected):
        board = Board()
        assert board.is_valid_position(position=position) == expected
