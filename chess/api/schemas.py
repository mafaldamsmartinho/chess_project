from pydantic import BaseModel


class CreateGameRequest(BaseModel):
    white_player: str
    black_player: str


class MoveRequest(BaseModel):
    start_square: str
    end_square: str