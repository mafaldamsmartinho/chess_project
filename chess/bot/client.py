from typing import Any

import requests

BASE_URL = "http://127.0.0.1:8000"


def get_game_by_id_call(game_id: int) -> dict[str, Any]:
    response = requests.get(url=f"{BASE_URL}/games/{game_id}")
    response.raise_for_status()
    return response.json()


def get_active_bot_game_ids_call() -> list[int] | None:
    response = requests.get(url=f"{BASE_URL}/bot/games")
    response.raise_for_status()
    return response.json()


def play_move_call(game_id: int, start: str, end: str) -> dict[str, Any]:
    response = requests.post(
        url=f"{BASE_URL}/games/{game_id}/move",
        json={"start_square": start, "end_square": end},
    )
    response.raise_for_status()
    return response.json()
