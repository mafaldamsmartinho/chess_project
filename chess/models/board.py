from chess.models.piece import Piece

NUM_ROWS = 8
NUM_COLS = 8
MAJOUR_PIECES = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
INDEX_MAJOUR_PIECES = [1, 1, 1, 1, 1, 2, 2, 2]

class Board:

    def __init__(self):
        self.board = [[None for col in range(NUM_COLS)] 
                      for row in range(NUM_ROWS)]

    def setup_board(self):
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if row == 0:    
                    self.board[row][col] = Piece('black', MAJOUR_PIECES[col], INDEX_MAJOUR_PIECES[col])
                if row == 1:
                    self.board[row][col] = Piece('black', 'pawn', col) 
                if row == 7:
                    self.board[row][col] = Piece('white', 'pawn', col) 
                if row == 8:    
                    self.board[row][col] = Piece('white', MAJOUR_PIECES[col], INDEX_MAJOUR_PIECES[col])

    def is_valid_position(position: str):
        ALLOWED_POSITIONS = {'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8',
                            'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8',
                            'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8',
                            'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8'}
        return position in ALLOWED_POSITIONS

    def position_to_index(position: str):
        return list(position)



