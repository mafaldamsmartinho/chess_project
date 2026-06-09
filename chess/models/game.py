from chess.models.board import Board

moves_history: list = []


class Game:

    def __init__(self):
        self.turn = 'white'
        self.board = Board()
        self.board.setup_board()
        self.white_king = self.board.board[0][4]
        self.black_king = self.board.board[7][4]

    def switch_turn(self):
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

    def add_move(self, move_data):
        moves_history.append(move_data)