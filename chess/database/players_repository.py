from chess.database.models import Players, Games

from sqlalchemy import select
from sqlalchemy.orm import aliased, Session


def create_player(name: str, bot: bool, session: Session) -> int:
    """Creates new player in DB and returns id"""
    player = Players(name=name, bot=bot)
    session.add(player)
    session.flush()
    return player.id


def get_player_id_by_name_and_bot(name: str, bot: bool, session: Session) -> int | None:
    """Checks if player already exists"""
    statement = (
        select(Players.id)
        .where(Players.name == name)
        .where(Players.bot == bot)
    )
    return session.scalar(statement)


def get_players_by_game_id(game_id: int, session: Session) -> tuple[str, str, bool, bool] | None:
    """Get player ids from a game id"""
    white = aliased(Players)
    black = aliased(Players)

    statement = (
        select(white.name, white.bot, black.name, black.bot)
        .select_from(Games)
        .join(white, Games.white_id == white.id)
        .join(black, Games.black_id == black.id)
        .where(Games.id == game_id)
    )

    result = session.execute(statement).one_or_none()

    if result is None:
        return None

    white_player, white_player_bot, black_player, black_player_bot = result

    return (white_player, black_player, white_player_bot, black_player_bot)
