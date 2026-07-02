from fastapi import APIRouter, HTTPException
from chess.database.games_repository import create_game, get_active_bot_game_ids, get_game_by_id
from chess.database.moves_repository import get_moves_by_game_id
from chess.database.players_repository import create_player, get_player_id_by_name_and_bot, get_players_by_game_id
from chess.api.schemas import CreateGameRequest, MoveRequest, GameResponse, MessageResponse
from chess.models.game import Game
from chess.services.game_service import play_move
from chess.utils.chess_logger import logger

router = APIRouter()


@router.post('/games')
def start_new_game_router(request: CreateGameRequest) -> GameResponse:
    white_id = get_player_id_by_name_and_bot(name=request.white_player, bot=request.is_bot_white)
    black_id = get_player_id_by_name_and_bot(name=request.black_player, bot=request.is_bot_black)

    if white_id is None:
        white_id = create_player(name=request.white_player, bot=request.is_bot_white)  # Create white id player in table
    if black_id is None:
        black_id = create_player(name=request.black_player, bot=request.is_bot_black)  # Create black id player in table
    game = Game()

    game_id = create_game(white_id=white_id, black_id=black_id, board_state=game.board)  # Create new game
    game = get_game_by_id(game_id=game_id)
    return GameResponse(
        game_id=game[0],
        white_id=game[1],
        black_id=game[2],
        status=game[3],
        turn=game[4],
        board=game[5])


@router.get('/games/{game_id}/players')
def get_players_by_game_id_router(game_id: int) -> tuple[str, str, bool, bool]:
    """Get players names based on game_id"""
    white_player, black_player, white_player_bot, black_player_bot = get_players_by_game_id(game_id=game_id)
    return white_player, black_player, white_player_bot, black_player_bot


@router.get('/bot/games')
def get_bot_active_games_router() -> list[int] | None:
    """Get bot games awaiting move."""
    bot_games = get_active_bot_game_ids()
    if not bot_games:
        logger.info("No Game bot games found")
    return bot_games


@router.get('/games/{game_id}')
def get_game_by_game_id_router(game_id: int) -> GameResponse:
    """Get game data based on game id"""
    try:
        game = get_game_by_id(game_id=game_id)
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
def play_move_router(request: MoveRequest, game_id: int) -> MessageResponse:
    """Execute move, save into DB and update game"""
    play_move(start=request.start_square, end=request.end_square, game_id=game_id)
    logger.info('Human move played successfully')

    return MessageResponse(message='Human move played successfully.')


@router.get('/games/{game_id}/moves')
def get_moves_by_game_id_router(game_id: int) -> list[dict[str, int | str | None]]:
    """Presents list of moves from a game"""
    move_data = get_moves_by_game_id(game_id=game_id)
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

