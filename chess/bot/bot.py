from chess.services.move_validator import is_legal_move, split_opponents
from chess.models.board import ALLOWED_POSITIONS
from chess.models.game import Game
import copy


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
                    legal_moves.append(bot_p, end)
        return legal_moves

    def kill_piece_points(self, game: Game, end) -> list[list]:
        """Gives points for if kills piece"""
        end_position = game.board.get_piece(end)
        points = 0
        if end_position is not None:
            if end_position.type == "queen":
                points = 5
            elif end_position.type == "knight":
                points = 4
            elif end_position.type == "bishop":
                points = 3
            elif end_position.type == "rook":
                points = 2
            elif end_position.type == "pawn":
                points = 1
        return points

    def expose_piece_points(self, game: Game, start, end) -> list[list]:
        """Removes points for exposing pieces"""
        temp_game = copy.deepcopy(game)
        temp_game.board.move_piece(start, end)
        temp_game.switch_turn()
        possible_opponent_moves = self.possible_moves(temp_game)
        for el in possible_opponent_moves:
            end_position = temp_game.board.get_piece(el[1])
            points = 0
            if end_position is not None:
                if end_position.type == "queen":
                    points -= 5
                elif end_position.type == "knight":
                    points -= 4
                elif end_position.type == "bishop":
                    points -= 3
                elif end_position.type == "rook":
                    points -= 2
                elif end_position.type == "pawn":
                    points -= 1
        return points

    def free_path_points(self, game: Game, start, end) -> int:
        """Returns the number of possible moves"""
        temp_game = copy.deepcopy(game)
        temp_game.board.move_piece(start, end)
        return len(self.possible_moves(temp_game))

    def score_move(self, game: Game) -> list[list]:
        """Scores bot move"""
        bot_moves = self.possible_moves(game)
        for move in bot_moves:
            move_score = 1 # w1 * kill_points +  w2 * points + w3 * points
            move["score"] = move_score
        return bot_moves

    def chose_move(self, bot_moves: list) -> tuple[str, str]:
        best_move = max(bot_moves, key=lambda move: move["score"])
        return best_move["start_square"], best_move["end_square"]
