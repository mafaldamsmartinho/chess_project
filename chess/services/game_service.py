from chess.models.piece import Piece
from chess.models.game import Game
from chess.services.move_validator import is_legal_move, is_king_in_check_mate
from chess.database.repositories import get_game, deserialize_board, update_game, save_move, get_moves


def play_move(start: str, end: str, game_id: int) -> None | dict[str, dict]:
    game_data = get_game(game_id)
    game = Game()
    game.status = game_data[3]
    game.turn = game_data[4]
    game.board = deserialize_board(game_data[5])
    piece: Piece = game.board.get_piece(start)
    captured_piece: Piece = game.board.get_piece(end)
    move_number = next_move_number(game_id)

    if is_legal_move(game, start, end):  # Checks if user wants to perform a valid move according with all rules.
        game.board.move_piece(start, end)
        game.switch_turn()  # Switch player turn
        if is_king_in_check_mate(game, game.turn):  # Check if next player king is in check mate
            if game.turn == 'white':
                game.status = 'black_wins'
            else:
                game.status = 'white_wins'
            game.turn = 'finished'
        save_move(game_id, move_number, start, end, f'{piece.colour}_{piece.type}', captured_piece)
        update_game(game_id, game.turn, game.status, game.board.to_dict())
        return {"board": game.board.to_dict()}
    return None


def next_move_number(game_id: int) -> int:
    """Checks next move number"""
    move_data = get_moves(game_id)
    if not move_data:
        move_number = 1
    else:
        move_number = max(row[2] for row in move_data) + 1
    return move_number
