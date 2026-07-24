from types import SimpleNamespace
from unittest.mock import Mock
import pytest

from chess.exceptions import GameNotFoundError, InvalidMoveError
from chess.models.board import Board
from chess.models.game import Game
from chess.models.enums import GameStatus, GameTurn
from chess.services import game_service


@pytest.fixture
def session():
    return Mock()


@pytest.fixture
def board():
    return Board()


@pytest.fixture
def game_data(board):
    return SimpleNamespace(
        turn=GameTurn.WHITE,
        status=GameStatus.ONGOING,
        board=board.to_dict(),
    )


class TestPlayMove:
    def test_play_move_passes_session_to_dependencies(
        self, monkeypatch, game_data, session
    ):
        get_game_by_id = Mock(return_value=game_data)
        next_move_number = Mock(return_value=1)
        is_legal_move = Mock(return_value=True)
        is_king_in_check_mate = Mock(return_value=False)
        save_move = Mock()
        update_game = Mock()

        monkeypatch.setattr(game_service, "get_game_by_id", get_game_by_id)
        monkeypatch.setattr(game_service, "next_move_number", next_move_number)
        monkeypatch.setattr(game_service, "is_legal_move", is_legal_move)
        monkeypatch.setattr(
            game_service, "is_king_in_check_mate", is_king_in_check_mate
        )
        monkeypatch.setattr(game_service, "save_move", save_move)
        monkeypatch.setattr(game_service, "update_game", update_game)

        result = game_service.play_move(
            start="e2", end="e4", game_id=1, session=session
        )

        get_game_by_id.assert_called_once_with(game_id=1, session=session)
        next_move_number.assert_called_once_with(game_id=1, session=session)
        save_move.assert_called_once_with(
            game_id=1,
            move_number=1,
            start="e2",
            end="e4",
            piece="white_pawn",
            captured_piece=None,
            session=session,
        )
        update_game.assert_called_once()
        assert update_game.call_args.kwargs["session"] == session
        session.commit.assert_called_once()
        session.rollback.assert_not_called()
        assert result["board"][1][4] is None
        assert result["board"][3][4]["type"] == "pawn"

    def test_play_move_saves_captured_piece(self, monkeypatch, game_data, session):
        board = Board()
        board.move_piece(
            start=board.position_to_index(position="d7"),
            end=board.position_to_index(position="e4"),
        )
        game_data.board = board.to_dict()
        get_game_by_id = Mock(return_value=game_data)
        next_move_number = Mock(return_value=3)
        save_move = Mock()
        update_game = Mock()

        monkeypatch.setattr(game_service, "get_game_by_id", get_game_by_id)
        monkeypatch.setattr(game_service, "next_move_number", next_move_number)
        monkeypatch.setattr(game_service, "is_legal_move", Mock(return_value=True))
        monkeypatch.setattr(
            game_service, "is_king_in_check_mate", Mock(return_value=False)
        )
        monkeypatch.setattr(game_service, "save_move", save_move)
        monkeypatch.setattr(game_service, "update_game", update_game)

        result = game_service.play_move(
            start="e2", end="e4", game_id=1, session=session
        )

        save_move.assert_called_once_with(
            game_id=1,
            move_number=3,
            start="e2",
            end="e4",
            piece="white_pawn",
            captured_piece="black_pawn",
            session=session,
        )
        update_game.assert_called_once()
        session.commit.assert_called_once()
        session.rollback.assert_not_called()
        assert result["board"][3][4]["colour"] == GameTurn.WHITE

    def test_play_move_updates_winner_when_checkmate(
        self, monkeypatch, game_data, session
    ):
        get_game_by_id = Mock(return_value=game_data)
        update_game = Mock()

        monkeypatch.setattr(game_service, "get_game_by_id", get_game_by_id)
        monkeypatch.setattr(game_service, "next_move_number", Mock(return_value=8))
        monkeypatch.setattr(game_service, "is_legal_move", Mock(return_value=True))
        monkeypatch.setattr(
            game_service, "is_king_in_check_mate", Mock(return_value=True)
        )
        monkeypatch.setattr(game_service, "save_move", Mock())
        monkeypatch.setattr(game_service, "update_game", update_game)

        game_service.play_move(start="e2", end="e4", game_id=1, session=session)

        update_game.assert_called_once()
        assert update_game.call_args.kwargs["current_turn"] == GameTurn.FINISHED
        assert update_game.call_args.kwargs["status"] == GameStatus.WHITE_WIN
        session.commit.assert_called_once()
        session.rollback.assert_not_called()

    def test_play_move_raises_when_game_not_found(self, monkeypatch, session):
        game_data = None
        get_game_by_id = Mock(return_value=game_data)
        save_move = Mock()
        update_game = Mock()
        monkeypatch.setattr(game_service, "get_game_by_id", get_game_by_id)
        monkeypatch.setattr(game_service, "save_move", save_move)
        monkeypatch.setattr(game_service, "update_game", update_game)
        with pytest.raises(GameNotFoundError):
            game_service.play_move(start="e2", end="e4", game_id=1, session=session)
        get_game_by_id.assert_called_once_with(game_id=1, session=session)
        save_move.assert_not_called()
        update_game.assert_not_called()
        session.commit.assert_not_called()
        session.rollback.assert_called_once()

    def test_play_move_invalid_move_raises_invalid_move_error(
        self, monkeypatch, game_data, session
    ):
        get_game_by_id = Mock(return_value=game_data)
        save_move = Mock()
        update_game = Mock()
        monkeypatch.setattr(game_service, "get_game_by_id", get_game_by_id)
        monkeypatch.setattr(game_service, "save_move", save_move)
        monkeypatch.setattr(game_service, "update_game", update_game)
        with pytest.raises(InvalidMoveError):
            game_service.play_move(start="e4", end="e5", game_id=1, session=session)
        get_game_by_id.assert_called_once_with(game_id=1, session=session)
        save_move.assert_not_called()
        update_game.assert_not_called()
        session.commit.assert_not_called()
        session.rollback.assert_called_once()

    def test_play_move_invalid_status_finished_raises_invalid_move_error(
        self, monkeypatch, board, session
    ):
        game_data = SimpleNamespace(
            turn=GameTurn.WHITE,
            status=GameStatus.WHITE_WIN,
            board=board.to_dict(),
        )
        get_game_by_id = Mock(return_value=game_data)
        is_legal_move = Mock()
        save_move = Mock()
        update_game = Mock()
        monkeypatch.setattr(game_service, "get_game_by_id", get_game_by_id)
        monkeypatch.setattr(game_service, "is_legal_move", is_legal_move)
        monkeypatch.setattr(game_service, "save_move", save_move)
        monkeypatch.setattr(game_service, "update_game", update_game)
        with pytest.raises(InvalidMoveError):
            game_service.play_move(start="e2", end="e4", game_id=1, session=session)
        get_game_by_id.assert_called_once_with(game_id=1, session=session)
        is_legal_move.assert_not_called()
        save_move.assert_not_called()
        update_game.assert_not_called()
        session.commit.assert_not_called()
        session.rollback.assert_called_once()

    def test_play_move_ilegal_move_raises_invalid_move_error(
        self, monkeypatch, game_data, session
    ):
        get_game_by_id = Mock(return_value=game_data)
        is_legal_move = Mock(return_value=False)
        save_move = Mock()
        update_game = Mock()
        monkeypatch.setattr(game_service, "get_game_by_id", get_game_by_id)
        monkeypatch.setattr(game_service, "is_legal_move", is_legal_move)
        monkeypatch.setattr(game_service, "save_move", save_move)
        monkeypatch.setattr(game_service, "update_game", update_game)
        with pytest.raises(InvalidMoveError):
            game_service.play_move(start="e2", end="f3", game_id=1, session=session)
        get_game_by_id.assert_called_once_with(game_id=1, session=session)
        is_legal_move.assert_called_once()
        save_move.assert_not_called()
        update_game.assert_not_called()
        session.commit.assert_not_called()
        session.rollback.assert_called_once()


class TestNextMoveNumber:
    @pytest.mark.parametrize("last_move_number, expected", [(7, 8), (None, 1)])
    def test_next_move_number_uses_session_scalar(
        self, last_move_number, expected, session
    ):
        session.scalar.return_value = last_move_number

        move_number = game_service.next_move_number(game_id=1, session=session)

        assert move_number == expected
        session.scalar.assert_called_once()


class TestGameWinner:
    @pytest.mark.parametrize(
        "game_turn, expected_status",
        [
            (GameTurn.BLACK, GameStatus.WHITE_WIN),
            (GameTurn.WHITE, GameStatus.BLACK_WIN),
        ],
    )
    def test_game_winners(self, game_turn, expected_status):
        game = Game(turn=game_turn)
        game_service.game_winner(game=game)
        assert game.turn == GameTurn.FINISHED and game.status == expected_status

    def test_game_winner_status_is_ongoing(self):
        game = Game(turn=GameTurn.WHITE, status=GameStatus.BLACK_WIN)
        with pytest.raises(ValueError):
            game_service.game_winner(game=game)
