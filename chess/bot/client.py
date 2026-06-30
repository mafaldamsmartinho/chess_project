import requests

BASE_URL = "http://127.0.0.1:8000"


def get_game_call(game_id: int) -> list:
    response = requests.get(f"{BASE_URL}/games/{game_id}")
    response.raise_for_status()
    return response.json()


def get_bot_games_call() -> list:
    response = requests.get(f"{BASE_URL}/bot/games")
    response.raise_for_status()
    return response.json()


def get_moves_call(game_id: int) -> None:
    response = requests.get(f"{BASE_URL}/games/{game_id}/moves")
    response.raise_for_status()
    return response.json()


def save_move_call(game_id, move_number, start_square, end_square, piece, captured_piece) -> None:
    response = requests.post(
        f"{BASE_URL}/moves/{game_id}",
        json={
            "move_number": move_number,
            "start_square": start_square,
            "end_square": end_square,
            "piece": piece,
            "captured_piece": captured_piece,
        })
    response.raise_for_status()
    return response.json()


def update_game_call(game_id, current_turn, status, board_state) -> None:
    response = requests.put(
        f"{BASE_URL}/games/{game_id}",
        json={
            "current_turn": current_turn,
            "status": status,
            "board_state": board_state,
        })
    response.raise_for_status()
    return response.json()
