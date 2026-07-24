import logging

from chess.utils.chess_logger import logger


def test_logger_uses_uvicorn_error_logger():
    assert logger is logging.getLogger("uvicorn.error")
    assert logger.name == "uvicorn.error"
