from chess.models.piece import Piece
from chess.models.game import Game
from chess.models.enums import GameStatus, GameTurn
from chess.services.move_validator import is_legal_move, is_king_in_check_mate
from chess.database.games_repository import get_game_by_id, update_game
from chess.database.models import Moves
from chess.database.moves_repository import save_move
from chess.utils.serialization import deserialize_board
from chess.exceptions import GameNotFoundError, InvalidMoveError
from sqlalchemy import func, select
from sqlalchemy.orm import Session


def play_move(start: str, end: str, game_id: int, session: Session) -> dict:
    try:
        game_data = get_game_by_id(game_id=game_id, session=session)

        if game_data is None:
            raise GameNotFoundError(f"Game with id {game_id} does not exist.")
        
        game = Game(turn=game_data.turn, status=game_data.status)
        game.set_board(board=deserialize_board(boardstate=game_data.board))

        piece: Piece = game.board.get_piece(position=start)
        
        if piece is None:
            raise InvalidMoveError("No piece found on start square.")

        if game.status != GameStatus.ONGOING:
            raise InvalidMoveError("This game has ended.")

        if not is_legal_move(game=game, start_position=start, end_position=end):  # Checks if user wants to perform a valid move according with all rules.
            raise InvalidMoveError("Ilegal Move.")
        
        captured_piece = game.board.get_piece(position=end)
        move_number = next_move_number(game_id=game_id, session=session)

        game.board.move_piece(start=game.board.position_to_index(position=start), end=game.board.position_to_index(position=end))
        game.switch_turn()  # Switch player turn
        if is_king_in_check_mate(game=game, current_turn=game.turn) or move_number > 100:  # Check if next player king is in check mate
            if game.turn == GameTurn.WHITE:
                game.status = GameStatus.BLACK_WIN
            else:
                game.status = GameStatus.WHITE_WIN
            game.turn = GameTurn.FINISHED
        save_move(game_id=game_id, move_number=move_number, start=start, end=end, piece=f'{piece.colour}_{piece.type.value}',
                  captured_piece=f'{captured_piece.colour}_{captured_piece.type.value}' if captured_piece else None,
                  session=session)
        update_game(game_id=game_id, current_turn=game.turn, status=game.status, board_state=game.board.to_dict(), session=session)
        session.commit()
        return {"board": game.board.to_dict()}

    except Exception:
        session.rollback()
        raise


def next_move_number(game_id: int, session: Session) -> int:
    """Checks next move number"""
    last_move_number = session.scalar(
        select(func.max(Moves.move_number)).where(Moves.game_id == game_id)
    )
    return 1 if last_move_number is None else last_move_number + 1

