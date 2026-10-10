"""Mediul discret in care invata agentul Q-learning."""

from __future__ import annotations

from typing import Any, Optional

from config import settings
from generation.level_manager import LevelManager
from generation.level_validator import LevelValidator
from generation.tile_type import TileType


State = tuple[int, int, bool]


class QLearningEnvironment:
    """Transforma un nivel intr-un mediu cu stari si recompense."""

    ACTIONS = {
        0: (-1, 0),
        1: (1, 0),
        2: (0, -1),
        3: (0, 1),
    }

    ACTION_NAMES = {
        0: "up",
        1: "down",
        2: "left",
        3: "right",
    }

    def __init__(
        self,
        level: LevelManager,
        max_steps: Optional[int] = None,
    ) -> None:
        self.level = level
        self.validator = LevelValidator(level)

        home = level.find_tile(TileType.HOME)
        cheese = level.find_tile(TileType.CHEESE)

        if home is None or cheese is None:
            raise ValueError(
                "Nivelul trebuie sa contina casa si branza."
            )

        if not self.validator.is_level_playable():
            raise ValueError("Nivelul trebuie sa fie jucabil.")

        self.home_position = home
        self.cheese_position = cheese
        self.trap_positions = set(
            level.find_all_tiles(TileType.TRAP)
        )

        default_max_steps = (
            level.rows
            * level.columns
            * settings.Q_MAX_STEPS_MULTIPLIER
        )

        if max_steps is not None and max_steps <= 0:
            raise ValueError(
                "Limita de pasi trebuie sa fie pozitiva."
            )

        self.max_steps = (
            default_max_steps
            if max_steps is None
            else max_steps
        )
        self.mouse_position = self.home_position
        self.has_cheese = False
        self.steps = 0
        self.done = False
        self.success = False

    def get_state(self) -> State:
        """Returneaza starea curenta a agentului."""

        row, col = self.mouse_position
        return row, col, self.has_cheese

    def reset(self) -> State:
        """Reseteaza episodul si returneaza starea initiala."""

        self.mouse_position = self.home_position
        self.has_cheese = False
        self.steps = 0
        self.done = False
        self.success = False

        return self.get_state()

    def get_valid_actions(
        self,
        state: Optional[State] = None,
    ) -> list[int]:
        """Returneaza actiunile care nu lovesc un perete."""

        if state is None:
            row, col = self.mouse_position
        else:
            row, col, _ = state

        valid_actions = []

        for action, (row_change, col_change) in (
            self.ACTIONS.items()
        ):
            target = (
                row + row_change,
                col + col_change,
            )

            if self.level.is_walkable(target):
                valid_actions.append(action)

        return valid_actions

    def step(
        self,
        action: int,
    ) -> tuple[State, int, bool, dict[str, Any]]:
        """Executa o actiune si returneaza rezultatul ei."""

        if self.done:
            raise RuntimeError(
                "Episodul s-a terminat. Apeleaza reset()."
            )

        if action not in self.ACTIONS:
            raise ValueError("Actiunea nu este valida.")

        row_change, col_change = self.ACTIONS[action]
        row, col = self.mouse_position
        target = (
            row + row_change,
            col + col_change,
        )

        self.steps += 1
        hit_wall = not self.level.is_walkable(target)
        hit_trap = False
        collected_cheese = False

        if hit_wall:
            reward = -5
        else:
            self.mouse_position = target
            reward = -1

            if target in self.trap_positions:
                reward = -15
                hit_trap = True

            if (
                target == self.cheese_position
                and not self.has_cheese
            ):
                self.has_cheese = True
                collected_cheese = True
                reward = 30

            if (
                target == self.home_position
                and self.has_cheese
            ):
                reward = 100
                self.done = True
                self.success = True

        if self.steps >= self.max_steps:
            self.done = True

        info = {
            "success": self.success,
            "hit_wall": hit_wall,
            "hit_trap": hit_trap,
            "collected_cheese": collected_cheese,
            "steps": self.steps,
        }

        return self.get_state(), reward, self.done, info

    def get_optimal_round_trip_path(
        self,
    ) -> list[tuple[int, int]]:
        """Returneaza traseul BFS pana la branza si inapoi."""

        outward_path = (
            self.validator.get_home_to_cheese_path()
        )

        if not outward_path:
            return []

        return outward_path + list(
            reversed(outward_path[:-1])
        )
