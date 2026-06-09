from chess.models.piece import Piece

NUM_ROWS: int = 8
NUM_COLS: int = 8
MAJOUR_PIECES: list = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop',
                       'knight', 'rook']
INDEX_MAJOUR_PIECES: list = [1, 1, 1, 1, 1, 2, 2, 2]
SQUARE_TO_INDEX: dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5,
                         'g': 6, 'h': 7}
LAST_ROW: list = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
PIECES_SIMPLE: dict = {'pawn': 'P', 'rook': 'R', 'knight': 'K', 'bishop': 'B', 'queen': 'Q', 'king': 'K'}
COLOUR_SIMPLE: dict = {'black': 'B', 'white': 'W'}

class Board:

    def __init__(self):
        self.board = [[None for col in range(NUM_COLS)]
                      for row in range(NUM_ROWS)]

    def setup_board(self):
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if row == 7:
                    self.board[row][col] = Piece('black', MAJOUR_PIECES[col],
                                                 INDEX_MAJOUR_PIECES[col])
                if row == 6:
                    self.board[row][col] = Piece('black', 'pawn', col)
                if row == 1:
                    self.board[row][col] = Piece('white', 'pawn', col)
                if row == 0:
                    self.board[row][col] = Piece('white', MAJOUR_PIECES[col],
                                                 INDEX_MAJOUR_PIECES[col])

    def is_valid_position(self, position: str):
        ALLOWED_POSITIONS = {'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
                             'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8',
                             'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8',
                             'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8',
                             'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8',
                             'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8',
                             'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8',
                             'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8'}
        return position in ALLOWED_POSITIONS

    def position_to_index(self, position: str):
        index = list(position)
        index_char = SQUARE_TO_INDEX.get(index[0])
        index_num = int(index[1]) - 1
        return (index_num, index_char)

    def get_piece(self, position: str):
        sq_index = self.position_to_index(position)
        return self.board[int(sq_index[0])][int(sq_index[1])]

    def set_piece(self, position: str, piece):
        position_index: list = self.position_to_index(position)
        self.board[position_index[0]][position_index[1]] = piece

    def move_piece(self, start, end):
        piece = self.get_piece(start)
        if piece is not None:
            self.set_piece(start, None)
            self.set_piece(end, piece)

    def to_dict(self):
        board: list = []
        rows: list = []
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if self.board[row][col] is not None:
                    rows.append(self.board[row][col].to_dict())
                else:
                    rows.append(None)
            board.append(rows)
            rows = []
        return board

    def to_display(self):
        board: list = []
        rows: list = []
        row_count = 8
        for row in range(NUM_ROWS - 1, -1, -1):
            rows.append(str(row_count))
            for col in range(NUM_COLS):
                if self.board[row][col] is not None:
                    piece: dict = self.board[row][col].to_dict()
                    short_name = COLOUR_SIMPLE.get(piece.get("colour")) + PIECES_SIMPLE.get(piece.get("type"))
                    rows.append(short_name)
                else:
                    rows.append('--')
            board.append(rows)
            print(' '.join(rows))
            rows = []
            row_count -= 1
        print('  '.join(LAST_ROW))