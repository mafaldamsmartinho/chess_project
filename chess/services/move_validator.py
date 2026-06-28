from chess.models.board import Board, ALLOWED_POSITIONS
from chess.models.piece import Piece
from chess.models.game import Game
import copy
from fastapi import HTTPException


def is_legal_move(game: Game, start: str, end: str):
    temp_game = copy.deepcopy(game)
    if not is_valid_move(temp_game.board, start, end, game.turn):
        return False
    # Checks if king will be in check after this move
    temp_game.board.move_piece(start, end)
    if is_king_in_check(temp_game.board, game.turn):
        return False
    return True


def is_king_in_check_mate(game: Game, current_turn: str):
    # Check if king is in check
    if is_king_in_check(game.board, current_turn) and is_move_possible(game):
        return True
    return False


def get_king_position(board: Board, current_turn: str):
    # Check where current turn king is
    for el in ALLOWED_POSITIONS:
        piece = board.get_piece(el)
        if piece is not None and piece.type == 'king' and piece.colour == current_turn:
            return el


def is_king_in_check(board: Board, king_turn: str):
    king_position = get_king_position(board, king_turn)
    next_turn = 'white'
    if king_turn == 'white':
        next_turn = 'black'
    for el in ALLOWED_POSITIONS:
        piece = board.get_piece(el)
        if piece is not None and piece.colour == next_turn:  # Check if king is threaten
            if is_valid_move(board, el, king_position, next_turn):
                return True
    return False


def is_move_possible(game: Game):
    start_positions: list = []
    end_positions: list = []

    for el in ALLOWED_POSITIONS:
        piece = game.board.get_piece(el)
        if piece is not None and piece.colour == game.turn:
            start_positions.append(el)
        else:
            end_positions.append(el)

    for start in start_positions:
        for end in end_positions:
            if is_legal_move(game, start, end):
                return True
    return False


def is_valid_move(board: Board, start: str, end: str, current_turn: str):
    start_sq_piece: Piece = board.get_piece(start)
    end_sq_piece: Piece = board.get_piece(end)

    if end_sq_piece is not None:
        if end_sq_piece.colour == current_turn:
            print(f'{current_turn} piece own end square piece')
            return False
    if start_sq_piece is None:
        print(f'{start} not valid. Empty start square.')
        return False
    elif start_sq_piece.colour != current_turn:
        print(f'{start} not valid. Wrong turn.')
        raise HTTPException(status_code=400, detail=f'{start} not valid. Wrong turn patata.')

    if start_sq_piece.type == 'pawn' and not validate_pawn_move(board, start, end):
        return False
    elif start_sq_piece.type == 'rook' and not validate_rook_move(board, start, end):
        return False
    elif start_sq_piece.type == 'knight' and not validate_knight_move(board, start, end):
        return False
    elif start_sq_piece.type == 'bishop' and not validate_bishop_move(board, start, end):
        return False
    elif start_sq_piece.type == 'queen' and not validate_queen_move(board, start, end):
        return False
    elif start_sq_piece.type == 'king' and not validate_king_move(board, start, end):
        return False
    if start_sq_piece.type == 'knight':
        return True
    if not is_path_clear(board, start, end):
        print(f'Path between {start} and {end} is not clear')
        return False
    return True


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

