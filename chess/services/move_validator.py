from chess.models.board import Board
from chess.models.piece import Piece
from chess.models.game import Game


def is_valid_move(board: Board, start: str, end: str, current_turn: str):
    valid_mode: bool = True

    if not board.is_valid_position(start):
        print(f'{start} square not valid')
        valid_mode = False
    if not board.is_valid_position(end):
        print(f'{end} square not valid')
        valid_mode = False

    start_sq_piece: Piece = board.get_piece(start)
    end_sq_piece: Piece = board.get_piece(end)

    if end_sq_piece is not None:
        if end_sq_piece.colour == current_turn:
            print(f'{current_turn} piece own end square piece')
            valid_mode = False
    if start_sq_piece is None:
        print(f'{start} not valid. Empty start square.')
        valid_mode = False
    elif start_sq_piece.colour != current_turn:
        print(f'{start} not valid. Wrong turn.')
        valid_mode = False
    if not is_path_clear(board, start, end):
        print('Path is not clear')
        valid_mode = False

    if start_sq_piece.type == 'pawn':
        valid_mode = validate_pawn_move(board, start, end)
    elif start_sq_piece.type == 'rook':
        valid_mode = validate_rook_move(board, start, end)
    elif start_sq_piece.type == 'knight':
        pass
        # validate_knight_move(...)
    elif start_sq_piece.type == 'bishop':
        valid_mode = validate_bishop_move(board, start, end)
    elif start_sq_piece.type == 'queen':
        valid_mode = validate_queen_move(board, start, end)
    elif start_sq_piece.type == 'king':
        # validate_king_move(...)
    return valid_mode


def is_path_clear(board: Board, start: str, end: str):
    start_position: list = board.position_to_index(start)
    end_position: list = board.position_to_index(end)
    path_clear = True

    if start_position[0] == end_position[0]:  # Same row
        row_step = 0
        row = start_position[0]
        if start_position[1] < end_position[1]:
            col_step = 1
            col = start_position[1] + 1
        else:
            col_step = -1
            col = start_position[1] - 1
    elif start_position[1] == end_position[1]:  # Same col
        col_step = 0
        col = start_position[1]
        if start_position[0] < end_position[0]:
            row_step = 1
            row = start_position[0] + 1
        else:
            row_step = -1
            row = start_position[0] - 1
    else:  # diagonal
        if start_position[0] < end_position[0]:
            row_step = 1
            row = start_position[0] + 1
        else:
            row_step = -1
            row = start_position[0] - 1
        if start_position[1] < end_position[1]:
            col_step = 1
            col = start_position[1] + 1
        else:
            col_step = -1
            col = start_position[1] - 1

    square = (row, col)

    while square != end_position:
        if board.board[row][col] is None:
            row = row + row_step
            col = col + col_step
            square = (row, col)
        else:
            path_clear = False
            break
    return path_clear


def validate_pawn_move(board: Board, start: str, end: str):
    start_position = board.position_to_index(start)
    end_position = board.position_to_index(end)
    valid_move = True
    if abs(start_position[0] - end_position[0]) == 1 and abs(start_position[1] - end_position[1]) == 0:
        return valid_move
    elif board.get_piece(end) is not None and abs(start_position[0] - end_position[0]) == 1 and abs(start_position[1] - end_position[1]) == 1:
        return valid_move
    else:
        valid_move = False
        return valid_move


def validate_rook_move(board: Board, start: str, end: str):
    start_position = board.position_to_index(start)
    end_position = board.position_to_index(end)
    valid_move = True
    if abs(start_position[0] - end_position[0]) != 0 and abs(start_position[1] - end_position[1]) == 0:
        return valid_move
    elif abs(start_position[0] - end_position[0]) == 0 and abs(start_position[1] - end_position[1]) != 0:
        return valid_move
    else:
        valid_move = False
        return valid_move


def validate_bishop_move(board: Board, start: str, end: str):
    start_position = board.position_to_index(start)
    end_position = board.position_to_index(end)
    return abs(start_position[0] - end_position[0]) == abs(start_position[1] - end_position[1])


def  validate_queen_move(board: Board, start: str, end: str):
    start_position = board.position_to_index(start)
    end_position = board.position_to_index(end)
    valid_move = True
    if abs(start_position[0] - end_position[0]) == abs(start_position[1] - end_position[1]):
        return valid_move
    elif abs(start_position[0] - end_position[0]) != 0 and abs(start_position[1] - end_position[1]) == 0:
        return valid_move
    elif abs(start_position[0] - end_position[0]) == 0 and abs(start_position[1] - end_position[1]) != 0:
        return valid_move
    else:
        valid_move = False
        return valid_move