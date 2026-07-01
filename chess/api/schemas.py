from pydantic import BaseModel
from typing import Any


class PieceData(BaseModel):
    colour: str
    type: str
    index: int


class CreateGameRequest(BaseModel):
    white_player: str
    is_bot_white: bool
    black_player: str
    is_bot_black: bool


class MoveRequest(BaseModel):
    start_square: str
    end_square: str


class SaveMoveRequest(BaseModel):
    move_number: int
    start_square: str
    end_square: str
    piece: str
    captured_piece: str | None


class UpdateGameRequest(BaseModel):
    current_turn: str
    status: str
    board_state: Any


class MessageResponse(BaseModel):
    message: str


class GameResponse(BaseModel):
    game_id: int
    white_id: int
    black_id: int
    status: str
    turn: str
    board: Any


class LoadGameResponse(BaseModel):
    game_response: GameResponse | None
    message: str


class MoveResponse(BaseModel):
    id: int
    game_id: int
    move_number: int
    start_square: str
    end_square: str
    piece: str
    captured_piece: str | None


class PlayerResponse(BaseModel):
    name: str
    bot: bool


class GamePlayersResponse(BaseModel):
    white: PlayerResponse
    black: PlayerResponse
