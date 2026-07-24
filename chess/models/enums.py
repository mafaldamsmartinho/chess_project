from enum import Enum

from pydantic import BaseModel


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


class PieceState(BaseModel):
    colour: str
    type: str
    index: int


class BoardState(BaseModel):
    board: list[list[PieceState | None]]
