from chess.models.game import Game
from chess.services.move_validator import is_valid_move


def play_move(game: Game, start: str, end: str):

    if is_valid_move(game.board, start, end, game.turn):
        game.board.move_piece(start, end)
        success = True
        message = 'Move played successfully'
        next_turn = str(game.switch_turn())
    else:
        success = False
        message = 'Invalid. Wrong turn or move.'
        next_turn = str(game.turn)

    play_info: dict = {
        "success": success,
        "message": message,
        "board": game.board,
        "next_turn": next_turn
    }
    return play_info
