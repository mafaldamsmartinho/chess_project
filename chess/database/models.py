from sqlalchemy import Boolean, Integer, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

from chess.models.enums import GameStatus, GameTurn
from chess.utils.serialization import SerializedBoard


class Base(MappedAsDataclass, DeclarativeBase):
    # Classes that inherit from this represent DB
    pass


class Players(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    bot: Mapped[bool] = mapped_column(Boolean)


class Games(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    white_id: Mapped[int] = mapped_column(Integer)
    black_id: Mapped[int] = mapped_column(Integer)
    board: Mapped[SerializedBoard] = mapped_column(JSONB)
    status: Mapped[GameStatus] = mapped_column(
        SQLEnum(
            GameStatus,
            name="game_status_enum",
            values_callable=lambda enum: [item.value for item in enum],
        ),
        nullable=False,
        default=GameStatus.ONGOING,
    )
    turn: Mapped[GameTurn] = mapped_column(
        SQLEnum(
            GameTurn,
            name="game_turn_enum",
            values_callable=lambda enum: [item.value for item in enum],
        ),
        nullable=False,
        default=GameTurn.WHITE,
    )


class Moves(Base):
    __tablename__ = "moves"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    game_id: Mapped[int] = mapped_column(Integer)
    move_number: Mapped[int] = mapped_column(Integer)
    start_square: Mapped[str] = mapped_column(Text, nullable=False)
    end_square: Mapped[str] = mapped_column(Text, nullable=False)
    piece: Mapped[str] = mapped_column(Text, nullable=False)
    captured_piece: Mapped[str | None] = mapped_column(Text)
