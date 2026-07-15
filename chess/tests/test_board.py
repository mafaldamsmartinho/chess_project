import pytest

from chess.models.board import Board


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
