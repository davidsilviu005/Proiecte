"""Teste pentru metricile si categoriile de dificultate."""

import pytest

from config import settings
from difficulty.difficulty_metrics import (
    calculate_difficulty_score,
    calculate_path_length,
    calculate_trap_risk,
    calculate_wall_density,
    classify_difficulty,
    count_dead_ends,
    count_intersections,
)
from generation.level_manager import LevelManager
from generation.tile_type import TileType


def create_cross_level() -> LevelManager:
    """Creeaza un nivel mic cu o intersectie centrala."""

    wall = TileType.WALL
    floor = TileType.FLOOR

    return LevelManager(
        [
            [wall, wall, wall, wall, wall],
            [wall, wall, floor, wall, wall],
            [wall, TileType.HOME, floor, TileType.CHEESE, wall],
            [wall, wall, floor, wall, wall],
            [wall, wall, wall, wall, wall],
        ]
    )


def test_structural_metrics_are_correct() -> None:
    level = create_cross_level()

    assert calculate_path_length(level) == 2
    assert count_dead_ends(level) == 4
    assert count_intersections(level) == 1
    assert calculate_wall_density(level) == pytest.approx(0.8)


def test_trap_on_optimal_path_has_maximum_risk() -> None:
    wall = TileType.WALL
    level = LevelManager(
        [
            [wall, wall, wall, wall, wall],
            [
                wall,
                TileType.HOME,
                TileType.TRAP,
                TileType.CHEESE,
                wall,
            ],
            [wall, wall, wall, wall, wall],
        ]
    )

    assert calculate_trap_risk(level) == 1.0


def test_score_stays_in_expected_range() -> None:
    score = calculate_difficulty_score(create_cross_level())

    assert score is not None
    assert 0 <= score <= 100


def test_numeric_score_is_classified() -> None:
    assert classify_difficulty(
        settings.EASY_SCORE_LIMIT - 0.1
    ) == "easy"
    assert classify_difficulty(
        settings.EASY_SCORE_LIMIT
    ) == "medium"
    assert classify_difficulty(
        settings.MEDIUM_SCORE_LIMIT
    ) == "hard"
