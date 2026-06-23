from pydantic import BaseModel
from typing import Any


class CreateGameRequest(BaseModel):
    white_player: str
    black_player: str


class MoveRequest(BaseModel):
    start_square: str
    end_square: str


class GameResponse(BaseModel):
    game_id: int
    white_id: int
    black_id: int
    status: str
    turn: str
    board: Any


class MoveResponse(BaseModel):
    id: int
    game_id: int
    move_number: int
    start_square: str
    end_square: str
    piece: str
    captured_piece: str