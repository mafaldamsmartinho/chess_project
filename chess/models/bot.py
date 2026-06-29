from chess.services.move_validator import is_legal_move
from chess.models.board import Board, ALLOWED_POSITIONS
from chess.models.game import Game


class Bot:

    def __init__(self):
        pass

    def possible_moves(self, game: Game) -> list[list]:
        """Possible bot moves"""
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
                    legal_moves.append([bot_p, end])
        return legal_moves

    def score_move(self, game: Game):
        """Scores bot move"""
        possible_moves = self.possible_moves(game)
        for move in possible_moves:
            end_position = game.board.get_piece(move[1])
            if end_position is not None and end_position.type == "queen":
                points = 5
            elif end_position is not None and end_position.type == "knight":
                points = 4
            elif end_position is not None and end_position.type == "bishop":
                points = 3
            elif end_position is not None and end_position.type == "rook":
                points = 2
            elif end_position is not None and end_position.type == "pawn":
                points = 1
            move.append(points)
        return

    def chose_move(self, game: Game):
        return self.possible_moves(game)[1]
