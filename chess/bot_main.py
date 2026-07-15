import cProfile
import datetime
import signal
import sys
import time

from chess.bot.bot_service import bot_play_move
from chess.bot.client import get_active_bot_game_ids_call
from chess.utils.chess_logger import logger

pr = cProfile.Profile()
pr.enable()


def handle_sigterm(signum, frame):
    pr.disable()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pr.dump_stats(f"snakeviz/{timestamp}_example_profiling.prof")
    print("Received SIGTERM...")
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)


def bot_loop() -> None:
    while True:
        bot_games = get_active_bot_game_ids_call()
        if bot_games is not None:
            for game_id in bot_games:
                initial_time = time.perf_counter()
                bot_play_move(game_id=game_id)
                logger.info("Bot move played successfully")
                logger.info(time.perf_counter() - initial_time)


if __name__ == "__main__":
    bot_loop()
