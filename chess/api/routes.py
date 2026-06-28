from fastapi import APIRouter, HTTPException
from chess.database.repositories import create_game, create_player, get_game, deserialize_board, get_moves, get_games, check_player, get_players
from chess.api.schemas import CreateGameRequest, MoveRequest, GameResponse, LoadGameResponse
from chess.models.game import Game
from chess.models.bot import Bot
from chess.services.game_service import play_move
import logging

router = APIRouter()

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(message)s"
)
logger = logging.getLogger("uvicorn.error")

@router.post('/games')
def start_game_router(request: CreateGameRequest):
    white_id = check_player(request.white_player)
    black_id = check_player(request.black_player)

    if white_id is None:
        white_id = create_player(request.white_player)  # Create white id player in table
    if black_id is None:
        black_id = create_player(request.black_player)  # Create black id player in table
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


@router.get('/games/{game_id}/players')
def get_players_router(game_id: int):  # Get players names based on game_id
    white_player, black_player = get_players(game_id)
    return white_player, black_player


@router.get('/games/{game_id}')
def get_game_router(game_id: int):  # Get game data based on game id
    try:
        game = get_game(game_id)
    except HTTPException as e:
        logger.warning(f"No Game {game_id} found")
        raise HTTPException(status_code=400, detail=e.detail)

    print(f"Succesfully loaded game {game_id}")
    return GameResponse(
        game_id=game[0],
        white_id=game[1],
        black_id=game[2],
        status=game[3],
        turn=game[4],
        board=game[5],
        )


@router.post('/games/{game_id}/move')
def play_turn_router(request: MoveRequest, game_id: int):
    game_data = get_game(game_id)
    if game_data is None:
        return HTTPException(status_code=404, detail=f"Game id {game_id} not found")

    game = Game()
    game.status = game_data[3]
    game.turn = game_data[4]
    game.board = deserialize_board(game_data[5])

    if game.status != 'ongoing':
        raise HTTPException(status_code=400, detail='This game has ended.')
    if not game.board.is_valid_position(request.start_square):
        raise HTTPException(status_code=400, detail='Invalid request. Start move not valid.')
    elif not game.board.is_valid_position(request.end_square):
        raise HTTPException(status_code=400, detail='Invalid request. End move not valid.')
    if game.board.get_piece(request.start_square) is None:
        raise HTTPException(status_code=400, detail="No piece found on start square.")

    result = play_move(request.start_square, request.end_square, game_id)
    if result is None:
        raise HTTPException(status_code=400, detail="Ilegal move.")

    if game_data[1] == 1 or game_data[2] == 1:  # We are playing with bot
        game_data_bot = get_game(game_id)
        game.status = game_data_bot[3]
        game.turn = game_data_bot[4]
        game.board = deserialize_board(game_data_bot[5])
        if game.status != 'ongoing':
            raise HTTPException(status_code=400, detail='This game has ended.')
        bot = Bot()
        bot_start, bot_end = bot.chose_move(game)
        bot_result = play_move(bot_start, bot_end, game_id)
        if bot_result is None:
            raise HTTPException(status_code=400, detail="Bot ilegal move.")
        return bot_result

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