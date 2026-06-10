from chess.models.board import Board
from chess.models.piece import Piece


def is_valid_move(board: Board, start: str, end: str, current_turn: str):
    valid_move: bool = True
    start_sq_piece: Piece = board.get_piece(start)
    end_sq_piece: Piece = board.get_piece(end)

    if end_sq_piece is not None:
        if end_sq_piece.colour == current_turn:
            valid_move &= False
            print(f'{current_turn} piece own end square piece')
    if start_sq_piece is None:
        valid_move &= False
        print(f'{start} not valid. Empty start square.')
    elif start_sq_piece.colour != current_turn:
        valid_move &= False
        print(f'{start} not valid. Wrong turn.')
    if not is_path_clear(board, start, end) and start_sq_piece.type != 'knight':
        valid_move &= False
        print(f'Path between {start} and {end} is not clear')
    if valid_move:
        if start_sq_piece.type == 'pawn':
            valid_move &= validate_pawn_move(board, start, end)
        elif start_sq_piece.type == 'rook':
            valid_move &= validate_rook_move(board, start, end)
        elif start_sq_piece.type == 'knight':
            valid_move &= validate_knight_move(board, start, end)
        elif start_sq_piece.type == 'bishop':
            valid_move &= validate_bishop_move(board, start, end)
        elif start_sq_piece.type == 'queen':
            valid_move &= validate_queen_move(board, start, end)
        elif start_sq_piece.type == 'king':
            valid_move &= validate_king_move(board, start, end)
    return valid_move


def is_path_clear(board: Board, start: str, end: str):
    start_position: list = board.position_to_index(start)
    end_position: list = board.position_to_index(end)
    row_diff = end_position[0] - start_position[0]
    col_diff = end_position[1] - start_position[1]

    if row_diff == 0:  # Same row
        row_step = 0
    elif row_diff > 0:
        row_step = 1
    else:
        row_step = -1
    if col_diff == 0:  # Same col
        col_step = 0
    elif col_diff > 0:
        col_step = 1
    else:
        col_step = -1
    return check_squares(board, start_position, end_position, row_step, col_step)


def check_squares(board, start_position, end_position, row_step, col_step):
    row = start_position[0] + row_step
    col = start_position[1] + col_step
    square = (row, col)
    while square != end_position:
        if board.board[row][col] is None:
            row += row_step
            col += col_step
            square = (row, col)
        else:
            return False
    return True

def validate_pawn_move(board: Board, start: str, end: str):
    start_position = board.position_to_index(start)
    end_position = board.position_to_index(end)
    start_piece: Piece = board.get_piece(start)
    if start_piece.colour == 'white':
        if end_position[0] - start_position[0] == 1 and abs(start_position[1] - end_position[1]) == 0: #checks if pawn is moving one square on the same column.
            return True
        elif end_position[0] - start_position[0] == 2 and abs(start_position[1] - end_position[1]) == 0 and (start_position[0] == 1 or start_position[0] == 6): #checks if pawn is moving for first time. 2 squares on the same column.
            return True
        elif board.get_piece(end) is not None and end_position[0] - start_position[0] == 1 and abs(end_position[1] - start_position[1]) == 1: #checks if pawn has opponent piece in diagonal.
            return True
        else:
            return False
    elif start_piece.colour == 'black':
        if start_position[0] - end_position[0] == 1 and abs(start_position[1] - end_position[1]) == 0: #checks if pawn is moving one square on the same column.
            return True
        elif start_position[0] - end_position[0] == 2 and abs(start_position[1] - end_position[1]) == 0 and (start_position[0] == 1 or start_position[0] == 6): #checks if pawn is moving for first time. 2 squares on the same column.
            return True
        elif board.get_piece(end) is not None and start_position[0] - end_position[0] == 1 and abs(start_position[1] - end_position[1]) == 1: #checks if pawn has opponent piece in diagonal.
            return True
        else:
            return False
        

def validate_rook_move(board: Board, start: str, end: str):
    start_position = board.position_to_index(start)
    end_position = board.position_to_index(end)
    valid_move: bool = True
    if abs(start_position[0] - end_position[0]) != 0 and abs(start_position[1] - end_position[1]) == 0:
        return valid_move
    elif abs(start_position[0] - end_position[0]) == 0 and abs(start_position[1] - end_position[1]) != 0:
        return valid_move
    else:
        valid_move = False
        return valid_move


def validate_knight_move(board: Board, start: str, end: str):
    start_position = board.position_to_index(start)
    end_position = board.position_to_index(end)
    valid_move: bool = True
    if abs(start_position[0] - end_position[0]) == 2 and abs(start_position[1] - end_position[1]) == 1:
        return valid_move
    elif abs(start_position[0] - end_position[0]) == 1 and abs(start_position[1] - end_position[1]) == 2:
        return valid_move
    else:
        valid_move = False
        return valid_move


def validate_bishop_move(board: Board, start: str, end: str):
    start_position = board.position_to_index(start)
    end_position = board.position_to_index(end)
    return abs(start_position[0] - end_position[0]) == abs(start_position[1] - end_position[1])


def validate_queen_move(board: Board, start: str, end: str):
    start_position = board.position_to_index(start)
    end_position = board.position_to_index(end)
    valid_move: bool = True
    if abs(start_position[0] - end_position[0]) == abs(start_position[1] - end_position[1]):
        return valid_move
    elif abs(start_position[0] - end_position[0]) != 0 and abs(start_position[1] - end_position[1]) == 0:
        return valid_move
    elif abs(start_position[0] - end_position[0]) == 0 and abs(start_position[1] - end_position[1]) != 0:
        return valid_move
    else:
        valid_move = False
        return valid_move


def validate_king_move(board: Board, start: str, end: str):
    start_position = board.position_to_index(start)
    end_position = board.position_to_index(end)
    valid_move: bool = True
    if abs(start_position[0] - end_position[0]) == 1 and abs(start_position[1] - end_position[1]) == 0:
        return valid_move
    elif abs(start_position[0] - end_position[0]) == 1 and abs(start_position[1] - end_position[1]) == 1:
        return valid_move
    elif abs(start_position[0] - end_position[0]) == 0 and abs(start_position[1] - end_position[1]) == 1:
        return valid_move
    else:
        valid_move = False
        return valid_move

