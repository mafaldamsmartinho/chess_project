from fastapi import APIRouter, HTTPException
from chess.database.repositories import create_game, create_player, get_game, deserialize_board, get_moves, check_player, get_players
from chess.api.schemas import CreateGameRequest, MoveRequest, GameResponse, MessageResponse
from chess.models.game import Game
from chess.models.bot import Bot
from chess.services.game_service import play_move
from chess.models.chess_logger import logger
from chess.services.bot_service import bot_play_move


router = APIRouter()


@router.post('/games')
def start_game_router(request: CreateGameRequest) -> GameResponse:
    white_id = check_player(request.white_player, request.is_bot_white)
    black_id = check_player(request.black_player, request.is_bot_black)

    if white_id is None:
        white_id = create_player(request.white_player, request.is_bot_white)  # Create white id player in table
    if black_id is None:
        black_id = create_player(request.black_player, request.is_bot_black)  # Create black id player in table
    game = Game()

    game_id = create_game(white_id, black_id, game.board)  # Create new game
    game = get_game(game_id)
    return GameResponse(
        game_id=game[0],
        white_id=game[1],
        black_id=game[2],
        status=game[3],
        turn=game[4],
        board=game[5])


@router.get('/games/{game_id}/players')
def get_players_router(game_id: int):  # Get players names based on game_id
    white_player, black_player = get_players(game_id)
    return white_player, black_player


@router.get('/games/{game_id}')
def get_game_router(game_id: int):
    """Get game data based on game id"""
    try:
        game = get_game(game_id)
    except HTTPException as e:
        logger.warning(f"No Game {game_id} found")
        raise HTTPException(status_code=400, detail=e.detail)

    logger.info(f"Succesfully loaded game {game_id}")
    return GameResponse(
        game_id=game[0],
        white_id=game[1],
        black_id=game[2],
        status=game[3],
        turn=game[4],
        board=game[5],
        )


@router.post('/games/{game_id}/move')
def play_turn_router(request: MoveRequest, game_id: int) -> MessageResponse:
    play_move(request.start_square, request.end_square, game_id)
    logger.info('Human move played successfully')

    return MessageResponse(message='Human move played successfully.')


@router.get('/games/{game_id}/moves')
def get_moves_router(game_id) -> list:
    """Presents list of moves from a game"""
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
