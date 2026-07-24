import pytest

from chess.models.board import Board
from chess.models.enums import GameStatus, GameTurn
from chess.models.game import Game


@pytest.fixture
def game():
    return Game()


class TestGameInit:
    def test_init_has_board(self, game):
        assert isinstance(game.board, Board)

    def test_init_has_default_turn(self, game):
        assert game.turn == GameTurn.WHITE

    def test_init_has_default_status(self, game):
        assert game.status == GameStatus.ONGOING

    def test_init_accepts_string_turn(self):
        game = Game(turn="black")

        assert game.turn == GameTurn.BLACK

    def test_init_accepts_string_status(self):
        game = Game(status="white_wins")

        assert game.status == GameStatus.WHITE_WIN

    def test_init_invalid_turn(self):
        with pytest.raises(ValueError):
            Game(turn="blue")

    def test_init_invalid_status(self):
        with pytest.raises(ValueError):
            Game(status="paused")


class TestSetBoard:
    def test_set_board_replaces_board(self, game):
        board = Board()
        board.set_piece(index_position=(0, 0), piece=None)

        game.set_board(board=board)

        assert game.board == board
        assert game.board.get_piece_by_index(index_position=(0, 0)) is None


class TestSwitchTurn:
    def test_switch_turn_from_white_to_black(self, game):
        game.switch_turn()

        assert game.turn == GameTurn.BLACK

    def test_switch_turn_from_black_to_white(self):
        game = Game(turn=GameTurn.BLACK)

        game.switch_turn()

        assert game.turn == GameTurn.WHITE

    def test_switch_turn_twice_returns_to_original_turn(self, game):
        game.switch_turn()
        game.switch_turn()

        assert game.turn == GameTurn.WHITE
