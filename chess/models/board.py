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





