import pytest

from chess.models.board import Board
from chess.models.enums import GameTurn, PieceType
from chess.models.game import Game
from chess.models.piece import Piece
from chess.services import move_validator


@pytest.fixture
def board():
    return Board()


@pytest.fixture
def empty_board():
    board = Board()
    for row in range(8):
        for col in range(8):
            board.set_piece(index_position=(row, col), piece=None)
    return board


def place_piece(
    board: Board,
    position: str,
    piece_type: PieceType,
    colour: GameTurn,
) -> Piece:
    piece = Piece(colour=colour, type=piece_type, index=1)
    board.set_piece(index_position=board.position_to_index(position), piece=piece)
    return piece


class TestGetPositionIndex:
    def test_get_position_index_converts_string_position(self, board):
        assert move_validator.get_position_index(board=board, position="e2") == (1, 4)

    def test_get_position_index_keeps_index_tuple(self, board):
        assert move_validator.get_position_index(board=board, position=(3, 4)) == (
            3,
            4,
        )


class TestIsValidMove:
    def test_is_valid_move_returns_false_when_start_square_empty(self, empty_board):
        assert not move_validator.is_valid_move(
            board=empty_board,
            start_position="e4",
            end_position="e5",
            current_turn=GameTurn.WHITE,
        )

    def test_is_valid_move_returns_false_when_piece_has_wrong_turn(self, empty_board):
        place_piece(empty_board, "e2", PieceType.PAWN, GameTurn.BLACK)

        assert not move_validator.is_valid_move(
            board=empty_board,
            start_position="e2",
            end_position="e3",
            current_turn=GameTurn.WHITE,
        )

    def test_is_valid_move_returns_false_when_capturing_own_piece(self, empty_board):
        place_piece(empty_board, "a1", PieceType.ROOK, GameTurn.WHITE)
        place_piece(empty_board, "a4", PieceType.PAWN, GameTurn.WHITE)

        assert not move_validator.is_valid_move(
            board=empty_board,
            start_position="a1",
            end_position="a4",
            current_turn=GameTurn.WHITE,
        )

    @pytest.mark.parametrize(
        "piece_type, start_position, end_position",
        [
            (PieceType.ROOK, "a1", "a4"),
            (PieceType.KNIGHT, "b1", "c3"),
            (PieceType.BISHOP, "c1", "h6"),
            (PieceType.QUEEN, "d1", "d5"),
            (PieceType.QUEEN, "d1", "h5"),
            (PieceType.KING, "e1", "e2"),
            (PieceType.PAWN, "e2", "e4"),
        ],
    )
    def test_is_valid_move_accepts_piece_legal_move(
        self, empty_board, piece_type, start_position, end_position
    ):
        place_piece(empty_board, start_position, piece_type, GameTurn.WHITE)

        assert move_validator.is_valid_move(
            board=empty_board,
            start_position=start_position,
            end_position=end_position,
            current_turn=GameTurn.WHITE,
        )

    @pytest.mark.parametrize(
        "piece_type, start_position, end_position",
        [
            (PieceType.ROOK, "a1", "b2"),
            (PieceType.KNIGHT, "b1", "b3"),
            (PieceType.BISHOP, "c1", "c4"),
            (PieceType.QUEEN, "d1", "e3"),
            (PieceType.KING, "e1", "e3"),
            (PieceType.PAWN, "e2", "e5"),
        ],
    )
    def test_is_valid_move_rejects_piece_illegal_move(
        self, empty_board, piece_type, start_position, end_position
    ):
        place_piece(empty_board, start_position, piece_type, GameTurn.WHITE)

        assert not move_validator.is_valid_move(
            board=empty_board,
            start_position=start_position,
            end_position=end_position,
            current_turn=GameTurn.WHITE,
        )

    def test_is_valid_move_rejects_blocked_sliding_piece(self, empty_board):
        place_piece(empty_board, "a1", PieceType.ROOK, GameTurn.WHITE)
        place_piece(empty_board, "a3", PieceType.PAWN, GameTurn.WHITE)

        assert not move_validator.is_valid_move(
            board=empty_board,
            start_position="a1",
            end_position="a4",
            current_turn=GameTurn.WHITE,
        )

    def test_is_valid_move_allows_knight_to_jump_over_piece(self, board):
        assert move_validator.is_valid_move(
            board=board,
            start_position="b1",
            end_position="c3",
            current_turn=GameTurn.WHITE,
        )


class TestValidatePawnMove:
    def test_validate_pawn_move_allows_white_diagonal_capture(self, empty_board):
        place_piece(empty_board, "e2", PieceType.PAWN, GameTurn.WHITE)
        place_piece(empty_board, "f3", PieceType.KNIGHT, GameTurn.BLACK)

        assert move_validator.validate_pawn_move(
            board=empty_board,
            start_position=empty_board.position_to_index("e2"),
            end_position=empty_board.position_to_index("f3"),
        )

    def test_validate_pawn_move_allows_black_diagonal_capture(self, empty_board):
        place_piece(empty_board, "e7", PieceType.PAWN, GameTurn.BLACK)
        place_piece(empty_board, "d6", PieceType.KNIGHT, GameTurn.WHITE)

        assert move_validator.validate_pawn_move(
            board=empty_board,
            start_position=empty_board.position_to_index("e7"),
            end_position=empty_board.position_to_index("d6"),
        )

    def test_validate_pawn_move_rejects_forward_capture(self, empty_board):
        place_piece(empty_board, "e2", PieceType.PAWN, GameTurn.WHITE)
        place_piece(empty_board, "e3", PieceType.KNIGHT, GameTurn.BLACK)

        assert not move_validator.validate_pawn_move(
            board=empty_board,
            start_position=empty_board.position_to_index("e2"),
            end_position=empty_board.position_to_index("e3"),
        )


class TestPathClear:
    def test_is_path_clear_returns_true_for_empty_path(self, empty_board):
        place_piece(empty_board, "a1", PieceType.ROOK, GameTurn.WHITE)

        assert move_validator.is_path_clear(
            board=empty_board,
            start_position=empty_board.position_to_index("a1"),
            end_position=empty_board.position_to_index("a4"),
        )

    def test_is_path_clear_returns_false_for_blocked_path(self, empty_board):
        place_piece(empty_board, "a1", PieceType.ROOK, GameTurn.WHITE)
        place_piece(empty_board, "a3", PieceType.PAWN, GameTurn.WHITE)

        assert not move_validator.is_path_clear(
            board=empty_board,
            start_position=empty_board.position_to_index("a1"),
            end_position=empty_board.position_to_index("a4"),
        )


class TestKingState:
    def test_get_king_position_returns_position_for_colour(self, empty_board):
        place_piece(empty_board, "e1", PieceType.KING, GameTurn.WHITE)

        assert move_validator.get_king_position(
            board=empty_board, current_turn=GameTurn.WHITE
        ) == (0, 4)

    def test_get_king_position_returns_none_when_king_missing(self, empty_board):
        assert (
            move_validator.get_king_position(
                board=empty_board, current_turn=GameTurn.WHITE
            )
            is None
        )

    def test_is_king_in_check_returns_true_when_attacked(self, empty_board):
        place_piece(empty_board, "e1", PieceType.KING, GameTurn.WHITE)
        place_piece(empty_board, "e8", PieceType.ROOK, GameTurn.BLACK)

        assert move_validator.is_king_in_check(
            board=empty_board, king_turn=GameTurn.WHITE
        )

    def test_is_king_in_check_returns_false_when_attack_is_blocked(self, empty_board):
        place_piece(empty_board, "e1", PieceType.KING, GameTurn.WHITE)
        place_piece(empty_board, "e2", PieceType.PAWN, GameTurn.WHITE)
        place_piece(empty_board, "e8", PieceType.ROOK, GameTurn.BLACK)

        assert not move_validator.is_king_in_check(
            board=empty_board, king_turn=GameTurn.WHITE
        )

    def test_is_legal_move_rejects_move_that_leaves_king_in_check(self, empty_board):
        game = Game(turn=GameTurn.WHITE)
        game.set_board(empty_board)
        place_piece(empty_board, "e1", PieceType.KING, GameTurn.WHITE)
        place_piece(empty_board, "e2", PieceType.ROOK, GameTurn.WHITE)
        place_piece(empty_board, "e8", PieceType.ROOK, GameTurn.BLACK)

        assert not move_validator.is_legal_move(
            game=game,
            start_position="e2",
            end_position="f2",
        )

    def test_is_legal_move_allows_move_that_blocks_check(self, empty_board):
        game = Game(turn=GameTurn.WHITE)
        game.set_board(empty_board)
        place_piece(empty_board, "e1", PieceType.KING, GameTurn.WHITE)
        place_piece(empty_board, "d2", PieceType.ROOK, GameTurn.WHITE)
        place_piece(empty_board, "e8", PieceType.ROOK, GameTurn.BLACK)

        assert move_validator.is_legal_move(
            game=game,
            start_position="d2",
            end_position="e2",
        )

    @pytest.mark.parametrize(
        "in_check, has_legal_move, expected",
        [
            (True, False, True),
            (True, True, False),
            (False, False, False),
        ],
    )
    def test_is_king_in_check_mate_uses_check_and_legal_moves(
        self, monkeypatch, empty_board, in_check, has_legal_move, expected
    ):
        game = Game(turn=GameTurn.WHITE)
        game.set_board(empty_board)
        monkeypatch.setattr(
            move_validator, "is_king_in_check", lambda board, king_turn: in_check
        )
        monkeypatch.setattr(
            move_validator, "is_any_move_legal", lambda game: has_legal_move
        )

        assert (
            move_validator.is_king_in_check_mate(
                game=game, current_turn=GameTurn.WHITE
            )
            is expected
        )
