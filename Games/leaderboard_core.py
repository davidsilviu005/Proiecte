# leaderboard_core.py
import json
import os
from datetime import datetime

FILE_NAME = "scores.json"


def _load_data():
    if not os.path.exists(FILE_NAME):
        return {}
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def add_score(game_name, player_name, score, extra=None):
    """
    game_name: string, e.g. "flappy_bird", "2048"
    player_name: string
    score: number (higher = better)
    extra: dict with extra info (time, attempts, accuracy, etc.)
    """
    data = _load_data()
    if game_name not in data:
        data[game_name] = []

    entry = {
        "player": player_name,
        "score": score,
        "extra": extra or {},
        "time": datetime.now().isoformat(timespec="seconds"),
    }

    data[game_name].append(entry)
    # sort by score descending and keep only top 20
    data[game_name].sort(key=lambda e: e["score"], reverse=True)
    data[game_name] = data[game_name][:20]

    _save_data(data)


def get_leaderboard(game_name, limit=10):
    data = _load_data()
    entries = data.get(game_name, [])
    return entries[:limit]


def get_all_games():
    """Return list of all game names that have scores."""
    data = _load_data()
    return list(data.keys())
