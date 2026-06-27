from chess.services.move_validator import is_legal_move
from chess.models.board import Board, ALLOWED_POSITIONS
from chess.models.game import Game


class Bot:

    def __init__(self):
        print('init bot')

    def possible_moves(self, game: Game):  # returns a list of tuples 
        bot_positions: list = []
        end_positions: list = []
        legal_moves: list = []

        for el in ALLOWED_POSITIONS:
            piece = game.board.get_piece(el)
            if piece is not None and piece.colour == game.turn:
                bot_positions.append(el)
            else:
                end_positions.append(el)

        for bot_p in bot_positions:
            for end in end_positions:
                if is_legal_move(game, bot_p, end):
                    legal_moves.append((bot_p, end))
        return legal_moves

    def chose_move(self, game: Game):
        return self.possible_moves(game)[5]

