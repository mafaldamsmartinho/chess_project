from chess.models.piece import Piece
from chess.models.game import Game
from chess.services.game_service import deserialize_board
from chess.services.move_validator import is_legal_move, is_king_in_check_mate
from chess.bot.bot import Bot
from chess.bot.client import get_game_call, save_move_call, update_game_call, get_moves_call
from fastapi import HTTPException


def bot_play_move(game_id: int) -> dict[str, dict]:
    """Executes Bot move"""
    game = Game()
    game_data_bot = get_game_call(game_id)
    game.status = game_data_bot["status"]
    game.turn = game_data_bot["turn"]
    game.board = deserialize_board(game_data_bot["board"])

    bot = Bot()
    bot_start, bot_end = bot.chose_move(game)
    piece: Piece = game.board.get_piece(bot_start)
    captured_piece = game.board.get_piece(bot_end)
    move_number = next_move_number(game_id)

    if captured_piece is not None:
        captured_piece = f'{captured_piece.colour}_{captured_piece.type}'

    if is_legal_move(game, bot_start, bot_end):  # Checks if user wants to perform a valid move according with all rules.
        game.board.move_piece(bot_start, bot_end)
        game.switch_turn()  # Switch player turn
        if is_king_in_check_mate(game, game.turn):  # Check if next player king is in check mate
            if game.turn == 'white':
                game.status = 'black_wins'
            else:
                game.status = 'white_wins'
            game.turn = 'finished'
        save_move_call(game_id, move_number, bot_start, bot_end, f'{piece.colour}_{piece.type}', captured_piece)
        update_game_call(game_id, game.turn, game.status, game.board.to_dict())
        return {"board": game.board.to_dict()}
    else:
        raise HTTPException(status_code=400, detail="Bot ilegal move.")


def next_move_number(game_id: int) -> int:
    """Checks next move number"""
    move_data = get_moves_call(game_id)
    if not move_data:
        move_number = 1
    else:
        move_number = max(row["move_number"] for row in move_data) + 1
    return move_number
