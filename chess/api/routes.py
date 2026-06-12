from fastapi import APIRouter, HTTPException
from chess.database.repositories import create_game, create_player, get_game, deserialize_board, update_game, save_move, get_moves
from chess.api.schemas import CreateGameRequest, MoveRequest
from chess.models.game import Game
from chess.services.game_service import play_move


router = APIRouter()


@router.post('/games')
def start_game_router(request: CreateGameRequest):
    white_id = create_player(request.white_player)
    black_id = create_player(request.black_player)
    game = Game()
    board_dict = game.board.to_dict()

    game_id = create_game(white_id, black_id, board_dict)
    game_data = get_game(game_id)
    return game_data

@router.get('/games/{game_id}')
def get_game_router(game_id: int):
    return get_game(game_id)


@router.post('/games/{game_id}/move')
def play_move_router(request: MoveRequest, game_id: int):
    game_data = get_game(game_id)
    game = Game()
    game.status = game_data[3]
    game.turn = game_data[4]
    game.board = deserialize_board(game_data[5])
    if not game.board.is_valid_position(request.start_square):
        raise HTTPException(status_code=400, detail='Invalid request. Start move not valid.')
    elif not game.board.is_valid_position(request.end_square):
        raise HTTPException(status_code=400, detail='Invalid request. End move not valid.')
    result = play_move(game, request.start_square, request.end_square)
    piece = game.board.get_piece(request.start_square)
    captured_piece = game.board.get_piece(request.end_square)
    move_data = get_moves(game_id)
    move_number = max(row[2] for row in move_data)
    if result["success"] is True:
        update_game(game_id, game.turn, game.status, game.board)
        save_move(game_id, move_number, request.start_square, request.end_square, piece, captured_piece)
    return result

