from chess.models.board import Board
from chess.models.enums import GameStatus, GameTurn


class Game:

    def __init__(self, turn: GameTurn | str = GameTurn.WHITE, status: GameStatus | str = GameStatus.ONGOING) -> None:
        """Initialises the game"""
        self.board = Board()
        self.turn = GameTurn(turn)
        self.status = GameStatus(status)

    def set_board(self, board: Board) -> None:
        self.board = board

    def switch_turn(self) -> None:
        """Switch game turn"""
        if self.turn == GameTurn.WHITE:
            self.turn = GameTurn.BLACK
        else:
            self.turn = GameTurn.WHITE
