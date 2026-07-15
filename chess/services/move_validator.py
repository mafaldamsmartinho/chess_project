import copy

from chess.models.board import NUM_COLS, NUM_ROWS, Board
from chess.models.enums import GameTurn, PieceType
from chess.models.game import Game
from chess.models.piece import Piece
from chess.utils.game_state import split_opponents


def get_position_index(
    board: Board, position: str | tuple[int, int]
) -> tuple[int, int]:
    """Returns a board index from either a string square or index tuple."""
    if isinstance(position, str):
        return board.position_to_index(position=position)
    return position


def is_legal_move(
    game: Game,
    start_position: str | tuple[int, int],
    end_position: str | tuple[int, int],
) -> bool:
    """Checks if king will be in check after this move."""
    temp_game = copy.deepcopy(game)
    start_position = get_position_index(board=temp_game.board, position=start_position)
    end_position = get_position_index(board=temp_game.board, position=end_position)
    if not is_valid_move(
        board=temp_game.board,
        start_position=start_position,
        end_position=end_position,
        current_turn=game.turn,
    ):
        return False
    temp_game.board.move_piece(start=start_position, end=end_position)
    if is_king_in_check(board=temp_game.board, king_turn=game.turn):
        return False
    return True


def is_king_in_check_mate(game: Game, current_turn: GameTurn | str) -> bool:
    """Check if king is in check and no piece move is valid."""
    if is_king_in_check(
        board=game.board, king_turn=current_turn
    ) and not is_any_move_legal(game=game):
        return True
    return False


def get_king_position(
    board: Board, current_turn: GameTurn | str
) -> tuple[int, int] | None:
    """Check where current turn king is and return its index position."""
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            el = (row, col)
            piece = board.get_piece_by_index(index_position=el)
            if (
                piece is not None
                and piece.type == PieceType.KING
                and piece.colour == current_turn
            ):
                return el


def is_king_in_check(board: Board, king_turn: GameTurn | str) -> bool:
    """Checks if king turn is in check."""
    king_turn = GameTurn(king_turn)
    king_position = get_king_position(board=board, current_turn=king_turn)
    if king_position is None:
        return False
    next_turn = GameTurn.WHITE
    if king_turn == GameTurn.WHITE:
        next_turn = GameTurn.BLACK
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            el = (row, col)
            piece = board.get_piece_by_index(index_position=el)
            if piece is not None and piece.colour == next_turn:
                if is_valid_move(
                    board=board,
                    start_position=el,
                    end_position=king_position,
                    current_turn=next_turn,
                ):
                    return True
    return False


def is_any_move_legal(game: Game) -> bool:
    """Checks if any current turn pieces can be moved."""
    start_positions, end_positions = split_opponents(game=game)
    for start_position in start_positions:
        for end_position in end_positions:
            if is_legal_move(
                game=game, start_position=start_position, end_position=end_position
            ):
                return True
    return False


def is_valid_move(
    board: Board,
    start_position: str | tuple[int, int],
    end_position: str | tuple[int, int],
    current_turn: GameTurn | str,
) -> bool:
    """Global check if move is valid accosding with piece rules."""
    current_turn = GameTurn(current_turn)
    start_position = get_position_index(board=board, position=start_position)
    end_position = get_position_index(board=board, position=end_position)
    start_sq_piece: Piece | None = board.get_piece_by_index(
        index_position=start_position
    )
    end_sq_piece: Piece | None = board.get_piece_by_index(index_position=end_position)

    if end_sq_piece is not None:  # Check if captured piece is opposite turn
        if end_sq_piece.colour == current_turn:
            return False
    if start_sq_piece is None:  # Check if start square not empty
        return False
    if start_sq_piece.colour != current_turn:  # Check if correct turn
        return False

    match start_sq_piece.type:
        case PieceType.PAWN:
            if not validate_pawn_move(
                board=board, start_position=start_position, end_position=end_position
            ):
                return False
        case PieceType.ROOK:
            if not validate_rook_move(
                board=board, start_position=start_position, end_position=end_position
            ):
                return False
        case PieceType.KNIGHT:
            if not validate_knight_move(
                board=board, start_position=start_position, end_position=end_position
            ):
                return False
            return True
        case PieceType.BISHOP:
            if not validate_bishop_move(
                board=board, start_position=start_position, end_position=end_position
            ):
                return False
        case PieceType.QUEEN:
            if not validate_queen_move(
                board=board, start_position=start_position, end_position=end_position
            ):
                return False
        case PieceType.KING:
            if not validate_king_move(
                board=board, start_position=start_position, end_position=end_position
            ):
                return False
    return is_path_clear(
        board=board, start_position=start_position, end_position=end_position
    )


def is_path_clear(
    board: Board, start_position: tuple[int, int], end_position: tuple[int, int]
) -> bool:
    """Check if path between start and end is clear."""
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
    return check_squares(
        board=board,
        start_position=start_position,
        end_position=end_position,
        row_step=row_step,
        col_step=col_step,
    )


def check_squares(
    board: Board,
    start_position: tuple[int, int],
    end_position: tuple[int, int],
    row_step: int,
    col_step: int,
) -> bool:
    """Checks if squares from start to end and specific direction are empty."""
    row = start_position[0] + row_step
    col = start_position[1] + col_step
    square = (row, col)
    while square != end_position:
        if (
            row < 0
            or row >= len(board.board)
            or col < 0
            or col >= len(board.board[row])
        ):
            return False
        if board.board[row][col] is None:
            row += row_step
            col += col_step
            square = (row, col)
        else:
            return False
    return True


def validate_pawn_move(
    board: Board, start_position: tuple[int, int], end_position: tuple[int, int]
) -> bool:
    """ "Check if pawn move is valid according with colour."""
    start_piece: Piece = board.get_piece_by_index(index_position=start_position)
    if start_piece.colour == GameTurn.WHITE:
        if (
            board.get_piece_by_index(index_position=end_position) is None
            and end_position[0] - start_position[0] == 1
            and abs(start_position[1] - end_position[1]) == 0
        ):  # checks if pawn is moving one square on the same column.
            return True
        elif (
            board.get_piece_by_index(index_position=end_position) is None
            and end_position[0] - start_position[0] == 2
            and abs(start_position[1] - end_position[1]) == 0
            and (start_position[0] == 1 or start_position[0] == 6)
        ):  # checks if pawn is moving for first time. 2 squares on the same column.
            return True
        elif (
            board.get_piece_by_index(index_position=end_position) is not None
            and end_position[0] - start_position[0] == 1
            and abs(end_position[1] - start_position[1]) == 1
        ):  # checks if pawn has opponent piece in diagonal.
            return True
        else:
            return False
    elif start_piece.colour == GameTurn.BLACK:
        if (
            board.get_piece_by_index(index_position=end_position) is None
            and start_position[0] - end_position[0] == 1
            and abs(start_position[1] - end_position[1]) == 0
        ):  # checks if pawn is moving one square on the same column.
            return True
        elif (
            board.get_piece_by_index(index_position=end_position) is None
            and start_position[0] - end_position[0] == 2
            and abs(start_position[1] - end_position[1]) == 0
            and (start_position[0] == 1 or start_position[0] == 6)
        ):  # checks if pawn is moving for first time. 2 squares on the same column.
            return True
        elif (
            board.get_piece_by_index(index_position=end_position) is not None
            and start_position[0] - end_position[0] == 1
            and abs(start_position[1] - end_position[1]) == 1
        ):  # checks if pawn has opponent piece in diagonal.
            return True
        else:
            return False
    return False


def validate_rook_move(
    board: Board, start_position: tuple[int, int], end_position: tuple[int, int]
) -> bool:
    """Checks if rook move is valid."""
    if (
        abs(start_position[0] - end_position[0]) != 0
        and abs(start_position[1] - end_position[1]) == 0
    ):  # Horizontal move
        return True
    elif (
        abs(start_position[0] - end_position[0]) == 0
        and abs(start_position[1] - end_position[1]) != 0
    ):  # Vertical move
        return True
    else:
        return False


def validate_knight_move(
    board: Board, start_position: tuple[int, int], end_position: tuple[int, int]
) -> bool:
    """Checks if Knigth move is valid."""
    if (
        abs(start_position[0] - end_position[0]) == 2
        and abs(start_position[1] - end_position[1]) == 1
    ):
        return True
    elif (
        abs(start_position[0] - end_position[0]) == 1
        and abs(start_position[1] - end_position[1]) == 2
    ):
        return True
    else:
        return False


def validate_bishop_move(
    board: Board, start_position: tuple[int, int], end_position: tuple[int, int]
) -> bool:
    """Checks if bishop move is valid."""
    return abs(start_position[0] - end_position[0]) == abs(
        start_position[1] - end_position[1]
    )


def validate_queen_move(
    board: Board, start_position: tuple[int, int], end_position: tuple[int, int]
) -> bool:
    """Checks if queen move is valid."""
    if abs(start_position[0] - end_position[0]) == abs(
        start_position[1] - end_position[1]
    ):
        return True
    elif (
        abs(start_position[0] - end_position[0]) != 0
        and abs(start_position[1] - end_position[1]) == 0
    ):
        return True
    elif (
        abs(start_position[0] - end_position[0]) == 0
        and abs(start_position[1] - end_position[1]) != 0
    ):
        return True
    else:
        return False


def validate_king_move(
    board: Board, start_position: tuple[int, int], end_position: tuple[int, int]
) -> bool:
    """Checks if king move is valid."""
    if (
        abs(start_position[0] - end_position[0]) == 1
        and abs(start_position[1] - end_position[1]) == 0
    ):
        return True
    elif (
        abs(start_position[0] - end_position[0]) == 1
        and abs(start_position[1] - end_position[1]) == 1
    ):
        return True
    elif (
        abs(start_position[0] - end_position[0]) == 0
        and abs(start_position[1] - end_position[1]) == 1
    ):
        return True
    else:
        return False
