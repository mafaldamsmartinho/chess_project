from chess.models.piece import Piece
from chess.models.game import Game
from chess.models.enums import GameStatus, GameTurn
from chess.services.move_validator import is_legal_move, is_king_in_check_mate
from chess.database.games_repository import get_game_by_id, update_game
from chess.database.moves_repository import get_moves_by_game_id, save_move
from chess.utils.serialization import deserialize_board
from fastapi import HTTPException


def play_move(start: str, end: str, game_id: int) -> dict[str, list[list[dict[str, str | int] | None]]]:
    game_data = get_game_by_id(game_id=game_id)
    game = Game(turn=game_data[4],
                status=game_data[3])
    game.set_board(board=deserialize_board(data=game_data[5]))

    piece: Piece = game.board.get_piece(position=start)
    if piece is None:
        raise HTTPException(status_code=400, detail='No piece found on start square.')

    captured_piece = game.board.get_piece(position=end)
    move_number = next_move_number(game_id=game_id)

    if captured_piece is not None:
        captured_piece = f'{captured_piece.colour}_{captured_piece.type.value}'

    if game.status != GameStatus.ONGOING:
        raise HTTPException(status_code=400, detail='This game has ended.')

    if is_legal_move(game=game, start_position=start, end_position=end):  # Checks if user wants to perform a valid move according with all rules.
        start_position = game.board.position_to_index(position=start)
        end_position = game.board.position_to_index(position=end)
        game.board.move_piece(start=start_position, end=end_position)
        game.switch_turn()  # Switch player turn
        if is_king_in_check_mate(game=game, current_turn=game.turn) or move_number > 100:  # Check if next player king is in check mate
            if game.turn == GameTurn.WHITE:
                game.status = GameStatus.BLACK_WIN
            else:
                game.status = GameStatus.WHITE_WIN
            game.turn = GameTurn.FINISHED
        save_move(game_id=game_id,
                  move_number=move_number,
                  start=start,
                  end=end,
                  piece=f'{piece.colour}_{piece.type.value}',
                  captured_piece=captured_piece)
        update_game(game_id=game_id,
                    current_turn=game.turn,
                    status=game.status,
                    board_state=game.board.to_dict())
        return {"board": game.board.to_dict()}
    else:
        raise HTTPException(status_code=400, detail="Ilegal move.")


def next_move_number(game_id: int) -> int:
    """Checks next move number"""
    move_data = get_moves_by_game_id(game_id=game_id)
    if not move_data:
        move_number = 1
    else:
        move_number = max(row[2] for row in move_data) + 1
    return move_number

