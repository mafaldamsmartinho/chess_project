from chess.bot.client import get_bot_games_call
from chess.bot.bot_service import bot_play_move
from chess.models.chess_logger import logger
import time


def bot_loop():
    while True:
        bot_games = get_bot_games_call()
        for game_id in bot_games:
            bot_play_move(game_id)
            logger.info('Bot move played successfully')
        time.sleep(2)


if __name__ == "__main__":
    bot_loop()