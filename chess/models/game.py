from chess.models.board import Board


class Game:

    def __init__(self) -> None:
        """Initialises the game"""
        self.board = Board()
        self.turn = 'white'
        self.status = 'ongoing'

    def switch_turn(self) -> None:
        """Switch game turn"""
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'