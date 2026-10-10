"""Functii pentru antrenarea si evaluarea agentului."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Optional

from config import settings
from learning.environment import QLearningEnvironment
from learning.q_learning_agent import QLearningAgent


TrainingCallback = Callable[[int, "TrainingStats"], None]


@dataclass
class TrainingStats:
    """Pastreaza progresul obtinut in timpul antrenarii."""

    rewards: list[float] = field(default_factory=list)
    steps: list[int] = field(default_factory=list)
    successes: list[bool] = field(default_factory=list)
    epsilon_history: list[float] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Returneaza procentul episoadelor reusite."""

        if not self.successes:
            return 0.0

        return (
            sum(self.successes)
            / len(self.successes)
            * 100
        )


def train_agent(
    environment: QLearningEnvironment,
    agent: QLearningAgent,
    episodes: int = settings.Q_LEARNING_EPISODES,
    max_steps: Optional[int] = None,
    progress_callback: Optional[TrainingCallback] = None,
) -> TrainingStats:
    """Antreneaza agentul pentru numarul cerut de episoade."""

    if episodes <= 0:
        raise ValueError(
            "Numarul de episoade trebuie sa fie pozitiv."
        )

    episode_limit = (
        environment.max_steps
        if max_steps is None
        else max_steps
    )

    if episode_limit <= 0:
        raise ValueError(
            "Limita de pasi trebuie sa fie pozitiva."
        )

    stats = TrainingStats()

    for episode in range(episodes):
        state = environment.reset()
        total_reward = 0.0
        success = False

        for step_number in range(1, episode_limit + 1):
            action = agent.choose_action(
                state,
                training=True,
            )

            next_state, reward, done, info = (
                environment.step(action)
            )

            agent.update_q_value(
                state,
                action,
                reward,
                next_state,
                done,
            )

            state = next_state
            total_reward += reward

            if done:
                success = bool(info["success"])
                break

        stats.rewards.append(round(total_reward, 4))
        stats.steps.append(step_number)
        stats.successes.append(success)
        stats.epsilon_history.append(agent.epsilon)
        agent.decay_epsilon()

        if progress_callback is not None:
            progress_callback(episode + 1, stats)

    return stats


def extract_policy_path(
    environment: QLearningEnvironment,
    agent: QLearningAgent,
    max_steps: Optional[int] = None,
) -> tuple[list[tuple[int, int]], bool]:
    """Ruleaza politica invatata si intoarce traseul gasit."""

    limit = max_steps or environment.max_steps
    state = environment.reset()
    path = [environment.mouse_position]

    for _ in range(limit):
        valid_actions = environment.get_valid_actions(state)
        action = agent.choose_action(
            state,
            training=False,
            valid_actions=valid_actions,
        )

        state, _, done, info = environment.step(action)
        path.append(environment.mouse_position)

        if done:
            return path, bool(info["success"])

    return path, False


def compare_with_bfs(
    environment: QLearningEnvironment,
    agent: QLearningAgent,
) -> dict[str, int | bool]:
    """Compara traseul invatat cu traseul optim BFS."""

    bfs_path = environment.get_optimal_round_trip_path()
    learned_path, success = extract_policy_path(
        environment,
        agent,
    )

    return {
        "success": success,
        "bfs_steps": max(0, len(bfs_path) - 1),
        "q_learning_steps": max(
            0,
            len(learned_path) - 1,
        ),
    }


def save_training_results(
    stats: TrainingStats,
    path: Path,
    comparison: Optional[dict[str, int | bool]] = None,
) -> Path:
    """Salveaza statisticile antrenarii in format JSON."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = asdict(stats)
    data["success_rate"] = stats.success_rate

    if comparison is not None:
        data["comparison"] = comparison

    path.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )

    return path
