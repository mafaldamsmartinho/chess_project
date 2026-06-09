from chess.models.board import Board

moves_history: list = []


class Game:

    def __init__(self):
        self.turn = 'white'
        self.board = Board()
        self.board.setup_board()

    def switch_turn(self):
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

    def add_move(self, move_data):
        moves_history.append(move_data)