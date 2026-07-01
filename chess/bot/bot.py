from chess.services.move_validator import is_legal_move, split_opponents
from chess.models.board import ALLOWED_POSITIONS
from chess.models.enums import PieceType
from chess.models.game import Game
import copy


class Bot:

    def __init__(self) -> None:
        pass

    def possible_moves(self, game: Game) -> list[dict[str, str]]:
        """Possible bot moves"""
        bot_positions: list = []
        end_positions: list = []
        legal_moves: list = []

        for el in ALLOWED_POSITIONS:
            piece = game.board.get_piece(position=el)
            if piece is not None and piece.colour == game.turn:
                bot_positions.append(el)
            else:
                end_positions.append(el)

        for bot_p in bot_positions:
            for end in end_positions:
                if is_legal_move(game=game, start=bot_p, end=end):
                    legal_moves.append({"start_square": bot_p, "end_square": end})
        return legal_moves

    def kill_piece_points(self, game: Game, end: str) -> int:
        """Gives points for if kills piece"""
        end_position = game.board.get_piece(position=end)
        points = 0
        if end_position is not None:
            if end_position.type == PieceType.QUEEN:
                points = 5
            elif end_position.type == PieceType.KNIGHT:
                points = 4
            elif end_position.type == PieceType.BISHOP:
                points = 3
            elif end_position.type == PieceType.ROOK:
                points = 2
            elif end_position.type == PieceType.PAWN:
                points = 1
        return points

    def expose_piece_points(self, game: Game, start: str, end: str) -> int:
        """Removes points for exposing pieces"""
        temp_game = copy.deepcopy(game)
        temp_game.board.move_piece(start=start, end=end)
        temp_game.switch_turn()
        possible_opponent_moves = self.possible_moves(game=temp_game)
        for el in possible_opponent_moves:
            end_position = temp_game.board.get_piece(position=el["end_square"])
            points = 0
            if end_position is not None:
                if end_position.type == PieceType.QUEEN:
                    points -= 5
                elif end_position.type == PieceType.KNIGHT:
                    points -= 4
                elif end_position.type == PieceType.BISHOP:
                    points -= 3
                elif end_position.type == PieceType.ROOK:
                    points -= 2
                elif end_position.type == PieceType.PAWN:
                    points -= 1
        return points

    def free_path_points(self, game: Game, start: str, end: str) -> int:
        """Returns the number of possible moves"""
        temp_game = copy.deepcopy(game)
        temp_game.board.move_piece(start=start, end=end)
        return len(self.possible_moves(game=temp_game))

    def score_move(self, game: Game) -> list[dict[str, str | int]]:
        """Scores bot move"""
        bot_moves = self.possible_moves(game=game)
        for move in bot_moves:
            move_score = 1  # w1 * kill_points +  w2 * points + w3 * points
            move["score"] = move_score
        return bot_moves

    def choose_move(self, game: Game) -> tuple[str, str]:
        bot_moves = self.score_move(game=game)
        best_move = max(bot_moves, key=lambda move: move["score"])
        return best_move["start_square"], best_move["end_square"]
