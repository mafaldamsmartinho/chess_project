from psycopg2.extras import Json
from chess.models.board import Board
from chess.models.piece import Piece
from chess.api.schemas import PieceData


def serialize_board(board: Board) -> Json:
    """Converts board dict into a json"""
    return Json(board.to_dict())


def deserialize_board(data: list[list[dict[str, str | int] | None]]) -> Board:
    """Converts json board into a board list of el None or Piece"""
    board = Board()
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            piece_data = PieceData(**el)  # pydantic instantiation
            if el is not None:
                board.board[i][j] = Piece(colour=piece_data.colour,
                                          type=piece_data.type,
                                          index=piece_data.index)
            else:
                board.board[i][j] = None
    return board
