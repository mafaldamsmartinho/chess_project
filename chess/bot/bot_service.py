from chess.models.game import Game
from chess.bot.bot import Bot
from chess.utils.serialization import deserialize_board
from chess.bot.client import get_game_by_id_call, play_move_call
from api.schemas import MessageResponse


def bot_play_move(game_id: int) -> MessageResponse:
    """Executes Bot move"""
    game_data_bot = get_game_by_id_call(game_id=game_id)
    game = Game(turn=game_data_bot["turn"],
                status=game_data_bot["status"])
    game.set_board(board=deserialize_board(data=game_data_bot["board"]))

    bot = Bot()
    bot_start, bot_end = bot.choose_move(game=game)
    play_move_call(game_id=game_id, start=bot_start, end=bot_end)
    return
