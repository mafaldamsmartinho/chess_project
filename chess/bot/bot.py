from chess.services.move_validator import is_legal_move
from chess.utils.game_state import split_opponents
from chess.models.enums import PieceType
from chess.models.game import Game
import copy
import time


class Bot:

    def __init__(self) -> None:
        pass



    def list_possible_moves(self, game: Game) -> list[dict]:
        """Possible bot moves"""
        legal_moves: list = []

        bot_positions, end_positions = split_opponents(game=game)

        for bot_p in bot_positions:
            for end in end_positions:
                if is_legal_move(game=game, start_position=bot_p, end_position=end):
                    legal_moves.append({"start_square": bot_p, "end_square": end})
        return legal_moves

    def kill_piece_points(self, game: Game, end: tuple[int, int]) -> int:
        """Gives points for if kills piece"""
        end_position = game.board.get_piece_by_index(index_position=end)
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
        game.switch_turn()
        possible_opponent_moves = self.list_possible_moves(game=game)
        for el in possible_opponent_moves:
            end_position = game.board.get_piece_by_index(index_position=el["end_square"])
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
        game.switch_turn()
        return exposed_points

    def pieces_protected(self, game: Game) -> int:
        """Checks if end square is protected"""
        protected_points = 0
        start_squares, end_squares = split_opponents(game=game)
        for protected in start_squares:
            temp_game = copy.deepcopy(game)
            temp_game.board.set_piece(index_position=protected, piece=None)
            for start in start_squares:
                if is_legal_move(game=game, start_position=start, end_position=protected):
                    protected_points += 1
                    # In future, points can be atributed according to piece type
        return protected_points

    def add_score_move_to_dict(self, game: Game) -> list[dict]:
        """Adds the calculated score to each move dictionary"""
        bot_moves = self.list_possible_moves(game=game)
        for move in bot_moves:
            kill_points = self.kill_piece_points(game=game, end=move["end_square"])
            game.board.move_piece(start=move["start_square"],
                                  end=move["end_square"])
            move["score"] = self.score_move(game=game, kill_points=kill_points)
            game.board.move_piece(start=move["end_square"],
                                  end=move["start_square"])
        return bot_moves

    def score_move(self, game: Game, kill_points: int):
        """Scores bot move"""
        initial_time = time.perf_counter()
        no_possible_moves = len(self.list_possible_moves(game=game))
        t_possible_moves = time.perf_counter()
        # print("no of possible moves: ",t_possible_moves - initial_time)
        no_pieces_protected = self.pieces_protected(game=game)
        t_protected = time.perf_counter()
        # print("no protected: ",t_protected - t_possible_moves)
        no_exposed_pieces = self.expose_pieces_points(game=game)
        t_expo = time.perf_counter()
        # print("no exposed: ", t_expo - t_protected)
        score = (no_possible_moves/30) * 0.2 + no_pieces_protected * 0.2 + no_exposed_pieces * 0.2 + kill_points * 0.4
        return score

    def choose_move(self, game: Game) -> tuple[tuple[int, int], tuple[int, int]]:
        bot_moves = self.add_score_move_to_dict(game=game)
        best_move = max(bot_moves, key=lambda move: move["score"])
        return best_move["start_square"], best_move["end_square"]
