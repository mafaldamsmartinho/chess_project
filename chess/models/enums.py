from enum import Enum


class GameStatus(str, Enum):
    ONGOING = "ongoing"
    WHITE_WIN = "white_wins"
    BLACK_WIN = "black_wins"


class GameTurn(str, Enum):
    BLACK = "black"
    WHITE = "white"
    FINISHED = "finished"


class PieceType(str, Enum):
    KING = "king"
    QUEEN = "queen"
    ROOK = "rook"
    BISHOP = "bishop"
    KNIGHT = "knight"
    PAWN = "pawn"
