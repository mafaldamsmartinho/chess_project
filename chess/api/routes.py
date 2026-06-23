from fastapi import APIRouter, HTTPException
from chess.database.repositories import create_game, create_player, get_game, deserialize_board, update_game, save_move, get_moves, get_games
from chess.api.schemas import CreateGameRequest, MoveRequest, GameResponse
from chess.models.game import Game
from chess.models.piece import Piece
from chess.services.game_service import play_move


router = APIRouter()


@router.post('/games')
def start_game_router(request: CreateGameRequest):
    white_id = create_player(request.white_player)  # Create white id player in table
    black_id = create_player(request.black_player)  # Create white id player in table
    game = Game()
    board = game.board

    game_id = create_game(white_id, black_id, board)  # Create new game
    game = get_game(game_id)
    return {
        "game_id": game[0],
        "white_id": game[1],
        "black_id": game[2],
        "status": game[3],
        "turn": game[4],
        "board": game[5],
        }


@router.get('/games/{game_id}', response_model=GameResponse)
def get_game_router(game_id: int):  # Get game data based on game id
    game = get_game(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail=f"Game id {game_id} not found")

    return {
        "game_id": game[0],
        "white_id": game[1],
        "black_id": game[2],
        "status": game[3],
        "turn": game[4],
        "board": game[5],
        }


@router.post('/games/{game_id}/move')
def play_move_router(request: MoveRequest, game_id: int):
    game_data = get_game(game_id)
    if game_data is None:
        raise HTTPException(status_code=404, detail=f"Game id {game_id} not found")

    game = Game()
    game.status = game_data[3]
    game.turn = game_data[4]
    game.board = deserialize_board(game_data[5])

    if not game.board.is_valid_position(request.start_square):
        raise HTTPException(status_code=400, detail='Invalid request. Start move not valid.')
    elif not game.board.is_valid_position(request.end_square):
        raise HTTPException(status_code=400, detail='Invalid request. End move not valid.')

    piece: Piece = game.board.get_piece(request.start_square)
    captured_piece: Piece = game.board.get_piece(request.end_square)
    move_data = get_moves(game_id)
    result = play_move(game, request.start_square, request.end_square)

    if piece is None:
        raise HTTPException(status_code=400, detail="No piece found on start square.")

    if captured_piece is not None:
        captured_piece = f'{captured_piece.colour}_{captured_piece.type}'

    if not move_data:
        move_number = 1
    else:
        move_number = max(row[2] for row in move_data) + 1

    if result["success"] is True:
        save_move(game_id, move_number, request.start_square, request.end_square, f'{piece.colour}_{piece.type}', captured_piece)
        update_game(game_id, game.turn, game.status, game.board.to_dict())
    return result


@router.get('/games/{game_id}/moves')
def get_moves_router(game_id):
    move_data = get_moves(game_id)
    present_moves = []
    for row in move_data:
        present_moves.append({
            "id": row[0],
            "game_id": row[1],
            "move_number": row[2],
            "start_square": row[3],
            "end_square": row[4],
            "piece": row[5],
            "captured_piece": row[6]
        })
    return present_moves


@router.get('/games')
def get_games_router():
    games_data = get_games()
    present_games = []
    for row in games_data:
        present_games.append({
            "id": row[0],
            "white_id": row[1],
            "black_number": row[2],
            "status": row[3],
            "turn": row[4]
            })
    return present_games