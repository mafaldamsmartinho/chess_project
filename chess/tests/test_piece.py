import pytest

from chess.models.enums import PieceType, GameTurn
from chess.models.piece import Piece


class TestPieceInit:
    def test_valid_piece(self):
        assert Piece(colour=GameTurn("black").value, type=PieceType.KING, index=1)

    def test_invalid_piece_colour(self):
        with pytest.raises(ValueError):
            Piece(colour="Blue", type=PieceType.ROOK, index=1)

    def test_invalid_piece_type(self):
        with pytest.raises(ValueError):
            Piece(colour=GameTurn("black").value, type="human", index=1)
