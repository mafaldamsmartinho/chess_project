from chess.api.schemas import PieceData
from chess.models.board import Board
from chess.models.piece import Piece
from typing import TypedDict


class SerializedPiece(TypedDict):
    colour: str
    type: str
    index: int


SerializedBoard = list[list[SerializedPiece | None]]


def serialize_board(board: Board) -> SerializedBoard:
    """Converts board dict into a json."""
    return board.to_dict()


def deserialize_board(boardstate: SerializedBoard) -> Board:
    """Converts json board into a board list of el None or Piece."""
    board = Board()
    for i, row in enumerate(boardstate):
        for j, el in enumerate(row):
            if el is not None:
                piece_data = PieceData(**el)  # pydantic instantiation
                board.board[i][j] = Piece(
                    colour=piece_data.colour,
                    type=piece_data.type,
                    index=piece_data.index,
                )
            else:
                board.board[i][j] = None
    return board
