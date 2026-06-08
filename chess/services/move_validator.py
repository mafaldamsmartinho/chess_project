from chess.models.board import Board
from chess.models.piece import Piece


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
    elif start_sq_piece.type == 'pawn':
        pass
        # is_path_clear(board, start, end)
        # validate_pawn_move(...)
    elif start_sq_piece.type == 'rook':
        pass
        # validate_rook_move(...)
    elif start_sq_piece.type == 'knight':
        pass
        # validate_knight_move(...)
    elif start_sq_piece.type == 'bishop':
        pass
        # validate_bishop_move(...)
    elif start_sq_piece.type == 'queen':
        pass
        # validate_queen_move(...)
    elif start_sq_piece.type == 'king':
        pass
        # validate_king_move(...)
    return valid_mode
