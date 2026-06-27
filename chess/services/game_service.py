from chess.models.game import Game
from chess.services.move_validator import is_legal_move
from chess.models.piece import Piece
from chess.database.repositories import get_game, deserialize_board, update_game, save_move, get_moves


def play_move(start: str, end: str, game_id: int):
    game_data = get_game(game_id)
    game = Game()
    game.status = game_data[3]
    game.turn = game_data[4]
    game.board = deserialize_board(game_data[5])

    piece: Piece = game.board.get_piece(start)
    captured_piece: Piece = game.board.get_piece(end)
    move_data = get_moves(game_id)

    if captured_piece is not None:
        captured_piece = f'{captured_piece.colour}_{captured_piece.type}'
        if captured_piece == 'white_king':
            game.status = 'black_wins'
            game.turn = 'finished'
            return
        elif captured_piece == 'black_king':
            game.status = 'white_wins'
            game.turn = 'finished'
            return

    if not move_data:
        move_number = 1
    else:
        move_number = max(row[2] for row in move_data) + 1

    if is_legal_move(game, start, end): # Checks if user wants to perform a valid move according with all rules.
        game.board.move_piece(start, end)
        game.switch_turn()  # Switch player turn
        save_move(game_id, move_number, start, end, f'{piece.colour}_{piece.type}', captured_piece)
        update_game(game_id, game.turn, game.status, game.board.to_dict())
        return {"board": game.board.to_dict()}
    return None