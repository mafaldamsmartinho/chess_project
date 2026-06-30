from chess.database.repositories import get_bot_games
from chess.services.bot_service import bot_play_move
from chess.models.chess_logger import logger
from chess.api.schemas import MessageResponse
import time


def bot_loop():
    while True:
        bot_games = get_bot_games()
        for game_id in bot_games:
            bot_play_move(game_id)
            logger.info('Bot move played successfully')
            MessageResponse(message='Bot move played successfully.')
        time.sleep(2)


if __name__ == "__main__":
    bot_loop()