from chess.bot.client import get_active_bot_game_ids_call
from chess.bot.bot_service import bot_play_move
from chess.utils.chess_logger import logger
import time


def bot_loop() -> None:
    while True:
        bot_games = get_active_bot_game_ids_call()
        for game_id in bot_games:
            initial_time = time.perf_counter()
            bot_play_move(game_id=game_id)
            logger.info('Bot move played successfully')
            logger.info(time.perf_counter() - initial_time)
        time.sleep(2)


if __name__ == "__main__":
    bot_loop()
