from chess.models.game import Game
from chess.services.move_validator import is_valid_move


def play_move(game: Game, start: str, end: str):

    found_white_king: bool = False
    found_black_king: bool = False

    if is_valid_move(game.board, start, end, game.turn):
        game.board.move_piece(start, end)
        success = True
        message = 'Move played successfully'
        game.switch_turn()
        next_turn = game.turn
    else:
        success = False
        message = 'Invalid. Wrong turn or move.'
        next_turn = game.turn

    for row in game.board.board:
        if game.white_king in row:
            found_white_king |= True
        if game.black_king in row:
            found_black_king |= True

    if found_white_king and not found_black_king:
        message = 'GAME OVER!!! WHITE WINS.'
        next_turn = None
    elif found_black_king and not found_white_king:
        message = 'GAME OVER!!! BLACK WINS.'
        next_turn = None

    play_info: dict = {
        "success": success,
        "message": message,
        "board": game.board.to_dict(),
        "next_turn": next_turn
    }
    return play_info