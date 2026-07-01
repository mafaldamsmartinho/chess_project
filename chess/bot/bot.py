from chess.services.move_validator import is_legal_move
from chess.utils.game_state import split_opponents
from chess.models.board import ALLOWED_POSITIONS
from chess.models.enums import PieceType
from chess.models.game import Game
import copy


class Bot:

    def __init__(self) -> None:
        pass

    def list_possible_moves(self, game: Game) -> list[dict[str, str]]:
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

    def expose_pieces_points(self, game: Game) -> int:
        """Removes points for exposing pieces"""
        temp_game = copy.deepcopy(game)
        temp_game.switch_turn()
        possible_opponent_moves = self.list_possible_moves(game=temp_game)
        for el in possible_opponent_moves:
            end_position = temp_game.board.get_piece(position=el["end_square"])
            exposed_points = 0
            if end_position is not None:
                if end_position.type == PieceType.QUEEN:
                    exposed_points -= 5
                elif end_position.type == PieceType.KNIGHT:
                    exposed_points -= 4
                elif end_position.type == PieceType.BISHOP:
                    exposed_points -= 3
                elif end_position.type == PieceType.ROOK:
                    exposed_points -= 2
                elif end_position.type == PieceType.PAWN:
                    exposed_points -= 1
        return exposed_points

    def pieces_protected(self, game: Game) -> int:
        """Checks if end square is protected"""
        protected_points = 0
        start_squares, end_squares = split_opponents(game=game)
        for protected in start_squares:
            temp_game = copy.deepcopy(game)
            temp_game.board.set_piece(position=protected, piece=None)
            for start in start_squares:
                if is_legal_move(game=game, start=start, end=protected):
                    protected_points += 1
                    # In future, points can be atributed according to piece type
        return protected_points

    def add_score_move_to_dict(self, game: Game) -> list[dict[str, str, int]]:
        """Adds the calculated score to each move dictionary"""
        bot_moves = self.list_possible_moves(game=game)
        for move in bot_moves:
            kill_points = self.kill_piece_points(game=game, end=move["end_square"])
            temp_game = copy.deepcopy(game)
            temp_game.board.move_piece(start=move["start_square"],
                                            end=move["end_square"])
            move["score"] = self.score_move(game=temp_game, kill_points=kill_points)
        return bot_moves

    def score_move(self, game: Game, kill_points: int):
        """Scores bot move"""
        no_possible_moves = len(self.list_possible_moves(game=game))
        no_pieces_protected = self.pieces_protected(game=game)
        no_exposed_pieces = self.expose_pieces_points(game=game)
        score = (no_possible_moves/30) * 0.2 + no_pieces_protected * 0.2 + no_exposed_pieces * 0.2 + kill_points * 0.4
        return score

    def choose_move(self, game: Game) -> tuple[str, str]:
        bot_moves = self.add_score_move_to_dict(game=game)
        best_move = max(bot_moves, key=lambda move: move["score"])
        return best_move["start_square"], best_move["end_square"]
