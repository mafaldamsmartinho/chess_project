from chess.models.game import Game
from chess.services.move_validator import is_legal_move


def play_move(game: Game, start: str, end: str):

    if is_legal_move(game.board, start, end, game.turn): # Checks if user wants to perform a valid move according with all rules.
        game.board.move_piece(start, end)
        success = True
        message = 'Move played successfully'
        game.switch_turn()  # Switch player turn
        next_turn = game.turn
    else:
        success = False
        message = 'Invalid. Wrong turn or move.'
        next_turn = game.turn

    play_info: dict = {  # creates a dictionary to store play move.
        "success": success,
        "message": message,
        "board": game.board.to_dict(),
        "next_turn": next_turn
    }
    return play_info