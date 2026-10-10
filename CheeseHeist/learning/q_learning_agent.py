"""Agentul care invata folosind un tabel Q."""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Optional

from config import settings
from learning.environment import State


class QLearningAgent:
    """Implementeaza strategia epsilon-greedy si actualizarea Q."""

    def __init__(
        self,
        action_count: int = 4,
        learning_rate: float = settings.Q_LEARNING_RATE,
        discount_factor: float = settings.Q_DISCOUNT_FACTOR,
        epsilon: float = settings.Q_INITIAL_EPSILON,
        epsilon_min: float = settings.Q_MIN_EPSILON,
        epsilon_decay: float = settings.Q_EPSILON_DECAY,
        seed: Optional[int] = None,
    ) -> None:
        if action_count <= 0:
            raise ValueError(
                "Numarul de actiuni trebuie sa fie pozitiv."
            )

        self.action_count = action_count
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.q_table: dict[State, list[float]] = {}
        self.rng = random.Random(seed)

    def get_q_values(self, state: State) -> list[float]:
        """Creeaza la nevoie si returneaza valorile unei stari."""

        if state not in self.q_table:
            self.q_table[state] = [
                0.0 for _ in range(self.action_count)
            ]

        return self.q_table[state]

    def choose_action(
        self,
        state: State,
        training: bool = True,
        valid_actions: Optional[list[int]] = None,
    ) -> int:
        """Alege o actiune aleatoare sau cea mai buna actiune."""

        actions = (
            list(range(self.action_count))
            if valid_actions is None
            else valid_actions
        )

        if not actions:
            raise ValueError("Nu exista actiuni disponibile.")

        if training and self.rng.random() < self.epsilon:
            return self.rng.choice(actions)

        q_values = self.get_q_values(state)
        best_value = max(q_values[action] for action in actions)
        best_actions = [
            action
            for action in actions
            if q_values[action] == best_value
        ]

        return self.rng.choice(best_actions)

    def update_q_value(
        self,
        state: State,
        action: int,
        reward: float,
        next_state: State,
        done: bool = False,
    ) -> float:
        """Actualizeaza o valoare folosind formula Q-learning."""

        current_values = self.get_q_values(state)
        old_value = current_values[action]

        future_value = 0.0
        if not done:
            future_value = max(
                self.get_q_values(next_state)
            )

        target = reward + self.discount_factor * future_value
        new_value = old_value + self.learning_rate * (
            target - old_value
        )
        current_values[action] = new_value

        return new_value

    def decay_epsilon(self) -> float:
        """Reduce explorarea fara a cobori sub limita minima."""

        self.epsilon = max(
            self.epsilon_min,
            self.epsilon * self.epsilon_decay,
        )

        return self.epsilon

    def save_q_table(
        self,
        path: Path = settings.DEFAULT_Q_TABLE_PATH,
    ) -> Path:
        """Salveaza tabelul Q si parametrii agentului in JSON."""

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        entries = [
            {
                "state": [row, col, has_cheese],
                "values": values,
            }
            for (row, col, has_cheese), values
            in sorted(self.q_table.items())
        ]

        data = {
            "action_count": self.action_count,
            "learning_rate": self.learning_rate,
            "discount_factor": self.discount_factor,
            "epsilon": self.epsilon,
            "epsilon_min": self.epsilon_min,
            "epsilon_decay": self.epsilon_decay,
            "q_table": entries,
        }

        path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

        return path

    def load_q_table(
        self,
        path: Path = settings.DEFAULT_Q_TABLE_PATH,
    ) -> None:
        """Incarca un tabel Q salvat anterior."""

        path = Path(path)
        data = json.loads(path.read_text(encoding="utf-8"))

        self.action_count = int(data["action_count"])
        self.learning_rate = float(data["learning_rate"])
        self.discount_factor = float(data["discount_factor"])
        self.epsilon = float(data["epsilon"])
        self.epsilon_min = float(data["epsilon_min"])
        self.epsilon_decay = float(data["epsilon_decay"])
        self.q_table = {}

        for entry in data["q_table"]:
            row, col, has_cheese = entry["state"]
            state = (
                int(row),
                int(col),
                bool(has_cheese),
            )
            self.q_table[state] = [
                float(value)
                for value in entry["values"]
            ]


def save_q_table(
    agent: QLearningAgent,
    path: Path = settings.DEFAULT_Q_TABLE_PATH,
) -> Path:
    """Salveaza tabelul unui agent."""

    return agent.save_q_table(path)


def load_q_table(
    path: Path = settings.DEFAULT_Q_TABLE_PATH,
    seed: Optional[int] = None,
) -> QLearningAgent:
    """Creeaza un agent si incarca tabelul salvat."""

    agent = QLearningAgent(seed=seed)
    agent.load_q_table(path)
    return agent
