from chess.models.enums import PieceType
from chess.models.game import Game
from chess.models.piece import Piece
from chess.services.move_validator import (
    is_king_in_check,
    is_legal_move,
    validate_bishop_move,
    validate_king_move,
    validate_knight_move,
    validate_pawn_move,
    validate_queen_move,
    validate_rook_move,
)
from chess.utils.game_state import split_opponents


class Bot:
    def __init__(self) -> None:
        pass

    def list_possible_scored_moves(self, game: Game) -> list[dict]:
        """Possible scored bot moves."""
        scored_moves: list = []
        kill_points_dict: dict = {}

        bot_positions, end_positions = split_opponents(game=game)

        for i, start_p in enumerate(bot_positions):
            piece = game.board.get_piece_by_index(index_position=start_p)
            for j, end_p in enumerate(end_positions):
                valid_piece_move = self.is_valid_piece_move(
                    game=game, piece=piece, start_p=start_p, end_p=end_p
                )
                if valid_piece_move and is_legal_move(
                    game=game, start_position=start_p, end_position=end_p
                ):
                    if (
                        end_p not in kill_points_dict
                    ):  # Avoid duplicate checks of same piece in repeted end positions
                        kill_points_dict[end_p] = self.kill_piece_points(
                            game=game, end=end_p
                        )
                    move_score = self.score_move(
                        game=game,
                        start_position=start_p,
                        end_position=end_p,
                        kill_points=kill_points_dict[end_p],
                    )
                    scored_moves.append(
                        {
                            "start_square": start_p,
                            "end_square": end_p,
                            "score": move_score,
                        }
                    )
        return scored_moves

    def number_of_possible_piece_moves(
        self, game: Game, piece_position: tuple, end_positions: list
    ) -> int:
        moves = 0
        moved_piece = game.board.get_piece_by_index(piece_position)
        for end_p in end_positions:
            valid_piece_move = self.is_valid_piece_move(
                game=game, piece=moved_piece, start_p=piece_position,
                end_p=end_p)
            if valid_piece_move and is_legal_move(
                game=game, start_position=piece_position, end_position=end_p
            ):
                moves += 1
        return moves

    def is_valid_piece_move(
        self, game: Game, piece: Piece, start_p: tuple, end_p: tuple
    ) -> bool:
        match piece.type:
            case PieceType.KING:
                valid_piece_move = validate_king_move(
                    board=game.board, start_position=start_p, end_position=end_p
                )
            case PieceType.QUEEN:
                valid_piece_move = validate_queen_move(
                    board=game.board, start_position=start_p, end_position=end_p
                )
            case PieceType.KNIGHT:
                valid_piece_move = validate_knight_move(
                    board=game.board, start_position=start_p, end_position=end_p
                )
            case PieceType.BISHOP:
                valid_piece_move = validate_bishop_move(
                    board=game.board, start_position=start_p, end_position=end_p
                )
            case PieceType.ROOK:
                valid_piece_move = validate_rook_move(
                    board=game.board, start_position=start_p, end_position=end_p
                )
            case PieceType.PAWN:
                valid_piece_move = validate_pawn_move(
                    board=game.board, start_position=start_p, end_position=end_p
                )
        return valid_piece_move

    def kill_piece_points(self, game: Game, end: tuple[int, int]) -> int:
        """Gives points for if kills piece."""
        end_position_piece = game.board.get_piece_by_index(index_position=end)
        points = 0
        if end_position_piece is not None:
            match end_position_piece.type:
                case PieceType.QUEEN:
                    points = 8
                case PieceType.KNIGHT:
                    points = 6
                case PieceType.BISHOP:
                    points = 5
                case PieceType.ROOK:
                    points = 3
                case PieceType.PAWN:
                    points = 1
        return points

    def expose_pieces_points(
        self, game: Game, bot_virtual_position: tuple, end_positions: list
    ) -> int:
        """Removes points for exposing pieces."""
        game.switch_turn()
        bot_virtual_piece = game.board.get_piece_by_index(
            index_position=bot_virtual_position
        )
        exposed_points = 0
        for opponent_p in end_positions:
            opponent_piece = game.board.get_piece_by_index(opponent_p)
            if opponent_piece is not None:
                valid_piece_move = self.is_valid_piece_move(
                    game=game,
                    piece=opponent_piece,
                    start_p=opponent_p,
                    end_p=bot_virtual_position,
                )
                if valid_piece_move and is_legal_move(
                    game=game,
                    start_position=opponent_p,
                    end_position=bot_virtual_position,
                ):
                    if bot_virtual_piece.type != PieceType.KING:
                        match bot_virtual_piece.type:
                            case PieceType.QUEEN:
                                exposed_points -= 8
                            case PieceType.KNIGHT:
                                exposed_points -= 6
                            case PieceType.BISHOP:
                                exposed_points -= 5
                            case PieceType.ROOK:
                                exposed_points -= 3
                            case PieceType.PAWN:
                                exposed_points -= 1
        game.switch_turn()
        return exposed_points

    def check_opponent_king_points(self, game: Game) -> int:
        points_check_opponent_king = 0
        game.switch_turn()
        if is_king_in_check(board=game.board, king_turn=game.turn):
            points_check_opponent_king = 8
        game.switch_turn()
        return points_check_opponent_king

    def pieces_protected(
        self, game: Game, bot_positions: list, end_positions: list
    ) -> int:
        """Checks if end square is protected."""
        protected_points = 0
        # Loop through bot virtual positions and check if protected
        for protected_square in bot_positions:
            protected_piece = game.board.get_piece_by_index(
                index_position=protected_square
            )
            game.board.set_piece(index_position=protected_square, piece=None)
            for start in bot_positions:
                if start != protected_square and protected_piece.type != PieceType.KING:
                    piece = game.board.get_piece_by_index(index_position=start)
                    valid_piece_move = self.is_valid_piece_move(
                        game=game, piece=piece, start_p=start, end_p=protected_square
                    )
                    if valid_piece_move and is_legal_move(
                        game=game, start_position=start, end_position=protected_square
                    ):
                        match protected_piece.type:
                            case PieceType.QUEEN:
                                protected_points += 8
                            case PieceType.KNIGHT:
                                protected_points += 6
                            case PieceType.BISHOP:
                                protected_points += 5
                            case PieceType.ROOK:
                                protected_points += 3
                            case PieceType.PAWN:
                                protected_points += 1
            game.board.set_piece(index_position=protected_square, piece=protected_piece)
        return protected_points

    def score_move(
        self, game: Game, start_position: tuple, end_position: tuple, kill_points: int
    ) -> float:
        """Adds the calculated score to each move dictionary."""
        captured_piece = game.board.get_piece_by_index(index_position=end_position)
        game.board.move_piece(start=start_position, end=end_position)
        move_score = self.score_move_function(
            game=game,
            start_position=start_position,
            end_position=end_position,
            kill_points=kill_points,
        )
        game.board.move_piece(start=end_position, end=start_position)
        game.board.set_piece(index_position=end_position, piece=captured_piece)
        return move_score

    def score_move_function(
        self, game: Game, start_position: tuple, end_position: tuple, kill_points: int
    ) -> float:
        """Scores bot move."""
        bot_positions, end_positions = split_opponents(game=game)
        points_possible_moves = self.number_of_possible_piece_moves(
            game=game, piece_position=end_position, end_positions=end_positions
        )
        points_pieces_protected = self.pieces_protected(
            game=game, bot_positions=bot_positions, end_positions=end_positions
        )
        points_exposed_pieces = self.expose_pieces_points(
            game=game, bot_virtual_position=end_position, end_positions=end_positions
        )
        points_check_opponent_king = self.check_opponent_king_points(game=game)
        score = (
            (points_possible_moves / 20) * 0.2
            + points_pieces_protected * 0.2
            + points_exposed_pieces * 0.2
            + kill_points * 0.2
            + points_check_opponent_king * 0.2
        )
        return score

    def choose_move(self, game: Game) -> tuple[tuple[int, int], tuple[int, int]]:
        bot_moves = self.list_possible_scored_moves(game=game)
        print(bot_moves)
        best_move = max(bot_moves, key=lambda move: move["score"])
        return best_move["start_square"], best_move["end_square"]
