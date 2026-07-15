from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from chess.api.schemas import (
    CreateGameRequest,
    GameResponse,
    MessageResponse,
    MoveRequest,
    MoveResponse,
)
from chess.database.connection import get_session
from chess.database.games_repository import (
    create_game,
    get_active_bot_game_ids,
    get_game_by_id,
)
from chess.database.moves_repository import get_moves_by_game_id
from chess.database.players_repository import (
    create_player,
    get_player_id_by_name_and_bot,
    get_players_by_game_id,
)
from chess.exceptions import GameNotFoundError, InvalidMoveError
from chess.models.game import Game
from chess.services.game_service import play_move
from chess.utils.chess_logger import logger

router = APIRouter()


@router.post("/games")
def start_new_game_router(
    request: CreateGameRequest, session: Session = Depends(get_session)
) -> GameResponse:
    white_id = get_player_id_by_name_and_bot(
        name=request.white_player, bot=request.is_bot_white, session=session
    )
    black_id = get_player_id_by_name_and_bot(
        name=request.black_player, bot=request.is_bot_black, session=session
    )
    try:
        # Create white or/and black id player in table
        if white_id is None:
            white_id = create_player(
                name=request.white_player, bot=request.is_bot_white,
                session=session)
        if black_id is None:
            black_id = create_player(
                name=request.black_player, bot=request.is_bot_black,
                session=session)
        game = Game()

        game_id = create_game(
            white_id=white_id,
            black_id=black_id,
            board_state=game.board,
            session=session,
        )  # Create new game
        game = get_game_by_id(game_id=game_id, session=session)
        session.commit()
        return GameResponse(
            game_id=game.id,
            white_id=game.white_id,
            black_id=game.black_id,
            status=game.status,
            turn=game.turn,
            board=game.board,
        )
    except Exception:
        session.rollback()
        raise


@router.get("/games/{game_id}/players")
def get_players_by_game_id_router(
    game_id: int, session: Session = Depends(get_session)
) -> tuple[str, str, bool, bool]:
    """Get players names based on game_id."""
    players = get_players_by_game_id(game_id=game_id, session=session)
    if players is None:
        raise HTTPException(status_code=404,
                            detail=f"Game with id {game_id} not found")
    return players


@router.get("/bot/games")
def get_bot_active_games_router(session: Session = Depends(get_session)
                                ) -> list[int]:
    """Get bot games awaiting move."""
    bot_games = get_active_bot_game_ids(session=session)
    if not bot_games:
        logger.info("No Game bot games found")
    return bot_games


@router.get("/games/{game_id}")
def get_game_by_game_id_router(
    game_id: int, session: Session = Depends(get_session)
) -> GameResponse:
    """Get game data based on game id."""
    game_data = get_game_by_id(game_id=game_id, session=session)
    if game_data is None:
        logger.warning(f"No Game {game_id} found")
        raise HTTPException(status_code=404,
                            detail=f"Game with id {game_id} not found")

    logger.info(f"Succesfully loaded game {game_id}")
    return GameResponse(
        game_id=game_data.id,
        white_id=game_data.white_id,
        black_id=game_data.black_id,
        status=game_data.status,
        turn=game_data.turn,
        board=game_data.board,
    )


@router.post("/games/{game_id}/move")
def play_move_router(
    request: MoveRequest, game_id: int, session: Session = Depends(get_session)
) -> MessageResponse:
    """Execute move, save into DB and update game."""
    try:
        play_move(
            start=request.start_square,
            end=request.end_square,
            game_id=game_id,
            session=session,
        )
        logger.info("Human move played successfully")
        return MessageResponse(message="Move played successfully")

    except GameNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except InvalidMoveError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="DB operation failed")


@router.get("/games/{game_id}/moves")
def get_moves_by_game_id_router(
    game_id: int, session: Session = Depends(get_session)
) -> list[MoveResponse]:
    """Presents list of moves from a game."""
    moves = get_moves_by_game_id(game_id=game_id, session=session)
    return [
        MoveResponse(
            id=move.id,
            game_id=move.game_id,
            move_number=move.move_number,
            start_square=move.start_square,
            end_square=move.end_square,
            piece=move.piece,
            captured_piece=move.captured_piece,
        )
        for move in moves
    ]
