from chess.database.repositories import get_game, deserialize_board
from chess.models.game import Game
from chess.models.bot import Bot
from chess.services.game_service import play_move
from fastapi import HTTPException


def bot_play_move(game_id: int) -> dict[str, dict]:
    """Executes Bot move"""
    game = Game()
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