import pytest

from chess.models.board import Board
from chess.models.enums import GameTurn, PieceType
from chess.models.piece import Piece
from chess.utils.serialization import deserialize_board, serialize_board


@pytest.fixture
def empty_board():
    board = Board()
    for row in range(8):
        for col in range(8):
            board.set_piece(index_position=(row, col), piece=None)
    return board


def test_serialize_board_returns_board_dict(empty_board):
    piece = Piece(colour=GameTurn.WHITE, type=PieceType.QUEEN, index=1)
    empty_board.set_piece(index_position=(3, 3), piece=piece)

    serialized_board = serialize_board(board=empty_board)

    assert serialized_board == empty_board.to_dict()
    assert serialized_board[3][3] == {
        "colour": GameTurn.WHITE,
        "type": PieceType.QUEEN.value,
        "index": 1,
    }


class TestDeserializeBoard:
    def test_deserialize_board_rebuilds_piece_objects(self, empty_board):
        empty_board.set_piece(
            index_position=(3, 3),
            piece=Piece(colour=GameTurn.BLACK, type=PieceType.KNIGHT, index=2),
        )

        board = deserialize_board(boardstate=empty_board.to_dict())
        piece = board.get_piece_by_index(index_position=(3, 3))

        assert piece is not None
        assert piece.colour == GameTurn.BLACK
        assert piece.type == PieceType.KNIGHT
        assert piece.index == 2

    def test_deserialize_board_preserves_empty_squares(self, empty_board):
        board = deserialize_board(boardstate=empty_board.to_dict())

        assert board.get_piece_by_index(index_position=(0, 0)) is None
        assert board.get_piece_by_index(index_position=(7, 7)) is None

    def test_deserialize_board_replaces_default_setup(self, empty_board):
        board = deserialize_board(boardstate=empty_board.to_dict())

        pieces_count = sum(
            piece is not None for row in board.board for piece in row
        )
        assert pieces_count == 0

    def test_deserialize_board_accepts_serialized_starting_board(self):
        starting_board = Board()

        board = deserialize_board(boardstate=starting_board.to_dict())

        assert board.get_piece(position="a1").type == PieceType.ROOK
        assert board.get_piece(position="e8").type == PieceType.KING
        assert board.get_piece(position="e8").colour == GameTurn.BLACK
