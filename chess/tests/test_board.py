import pytest

from chess.models.enums import GameTurn, PieceType
from chess.models.board import Board
from chess.models.piece import Piece


class TestInitSetupBoard:
    def test_init_board_size_when_setup(self):
        board = Board()
        assert len(board.board) == 8
        assert all(len(row) == 8 for row in board.board)

    def test_correct_number_pieces_when_setup(self):
        board = Board()
        pieces_number = sum(
            el is not None for row in board.board for el in row)
        assert pieces_number == 32

    def test_correct_colours_when_setup(self):
        board = Board()
        white_pieces = 0
        black_pieces = 0

        for row in board.board:
            for piece in row:
                if piece is None:
                    continue

                if piece.colour == GameTurn.WHITE:
                    white_pieces += 1
                elif piece.colour == GameTurn.BLACK:
                    black_pieces += 1

        assert white_pieces == 16
        assert black_pieces == 16


class TestIsValidPosition:
    @pytest.mark.parametrize(
        "position, expected",
        [
            ("a2", True),
            ("h8", True),
            ("z9", False),
            ("a9", False),
        ]
    )
    def test_returns_bool_when_valid_position(self, position, expected):
        board = Board()
        assert board.is_valid_position(position=position) == expected


class TestIsValidPositionIndex:
    @pytest.mark.parametrize(
        "position, expected",
        [
            ((0, 0), True),
            ((1, 4), True),
            ((-1, 6), False),
            ((3, 8), False),
        ]
    )
    def test_returns_bool_when_valid_position_index(self, position, expected):
        board = Board()
        assert board.is_valid_position_index(
            index_position=position) == expected


class TestPositionToIndex:
    @pytest.mark.parametrize(
        "position, expected", [
            ("a2", (1, 0)),
            ("b6", (5, 1))
        ]
    )
    def test_position_to_index_valid(self, position, expected):
        board = Board()
        assert board.position_to_index(position=position) == expected

    def test_position_to_index_invalid(self):
        board = Board()
        with pytest.raises(ValueError):
            board.position_to_index("z9")


class TestIndexToPosition:
    @pytest.mark.parametrize(
        "index_position, expected",
        [
            ((0, 0), "a1"),
            ((1, 1), "b2"),
            ((7, 7), "h8"),
        ],
    )
    def test_index_to_position_valid(self, index_position, expected):
        board = Board()
        assert board.index_to_position(index_position=index_position) == expected

    def test_index_to_position_invalid_column(self):
        board = Board()
        with pytest.raises(IndexError):
            board.index_to_position(index_position=(0, 8))


class TestGetPiece:
    def test_get_piece_occupied_square(self):
        board = Board()
        piece = board.get_piece(position="a1")

        assert piece is not None
        assert piece.colour == GameTurn.WHITE
        assert piece.type == PieceType.ROOK

    def test_get_piece_empty_square(self):
        board = Board()
        assert board.get_piece(position="a3") is None

    def test_get_piece_invalid_position(self):
        board = Board()
        with pytest.raises(ValueError):
            board.get_piece(position="z9")


class TestGetPieceByIndex:
    def test_get_piece_by_index_occupied_square(self):
        board = Board()
        piece = board.get_piece_by_index(index_position=(7, 4))

        assert piece is not None
        assert piece.colour == GameTurn.BLACK
        assert piece.type == PieceType.KING

    def test_get_piece_by_index_empty_square(self):
        board = Board()
        assert board.get_piece_by_index(index_position=(3, 3)) is None


class TestSetPiece:
    def test_set_piece_places_piece(self):
        board = Board()
        piece = Piece(colour=GameTurn.WHITE, type=PieceType.QUEEN, index=2)

        board.set_piece(index_position=(3, 3), piece=piece)

        assert board.get_piece_by_index(index_position=(3, 3)) == piece

    def test_set_piece_removes_piece(self):
        board = Board()

        board.set_piece(index_position=(0, 0), piece=None)

        assert board.get_piece_by_index(index_position=(0, 0)) is None

    def test_set_piece_replaces_piece(self):
        board = Board()
        piece = Piece(colour=GameTurn.BLACK, type=PieceType.KNIGHT, index=3)

        board.set_piece(index_position=(0, 0), piece=piece)

        assert board.get_piece_by_index(index_position=(0, 0)) == piece


class TestMovePiece:
    def test_move_piece_reaches_destination(self):
        board = Board()
        piece = board.get_piece_by_index(index_position=(1, 0))

        board.move_piece(start=(1, 0), end=(2, 0))

        assert board.get_piece_by_index(index_position=(2, 0)) == piece

    def test_move_piece_start_becomes_empty(self):
        board = Board()

        board.move_piece(start=(1, 0), end=(2, 0))

        assert board.get_piece_by_index(index_position=(1, 0)) is None

    def test_move_piece_captures_or_overwrites_destination(self):
        board = Board()
        piece = board.get_piece_by_index(index_position=(0, 0))

        board.move_piece(start=(0, 0), end=(7, 0))

        assert board.get_piece_by_index(index_position=(7, 0)) == piece

    def test_move_piece_empty_start_makes_destination_empty(self):
        board = Board()

        board.move_piece(start=(3, 3), end=(1, 0))

        assert board.get_piece_by_index(index_position=(3, 3)) is None
        assert board.get_piece_by_index(index_position=(1, 0)) is None


class TestToDict:
    def test_to_dict_has_board_shape(self):
        board = Board()
        board_dict = board.to_dict()

        assert len(board_dict) == 8
        assert all(len(row) == 8 for row in board_dict)

    def test_to_dict_converts_piece(self):
        board = Board()

        assert board.to_dict()[0][0] == {
            "colour": GameTurn.WHITE,
            "type": PieceType.ROOK.value,
            "index": 1,
        }

    def test_to_dict_keeps_empty_squares(self):
        board = Board()

        assert board.to_dict()[3][3] is None

    def test_to_dict_returns_expected_values_after_board_change(self):
        board = Board()
        piece = Piece(colour=GameTurn.BLACK, type=PieceType.QUEEN, index=4)

        board.set_piece(index_position=(3, 3), piece=piece)
        board.set_piece(index_position=(0, 0), piece=None)
        board_dict = board.to_dict()

        assert board_dict[3][3] == {
            "colour": GameTurn.BLACK,
            "type": PieceType.QUEEN.value,
            "index": 4,
        }
        assert board_dict[0][0] is None
