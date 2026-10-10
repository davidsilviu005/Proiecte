"""Teste pentru mediul si agentul Q-learning."""

import pytest

from generation.level_manager import LevelManager
from generation.tile_type import TileType
from learning.environment import QLearningEnvironment
from learning.q_learning_agent import QLearningAgent
from learning.training import compare_with_bfs, train_agent


def create_training_level() -> LevelManager:
    """Creeaza un coridor simplu pentru antrenare."""

    wall = TileType.WALL

    return LevelManager(
        [
            [wall, wall, wall, wall, wall],
            [
                wall,
                TileType.HOME,
                TileType.FLOOR,
                TileType.CHEESE,
                wall,
            ],
            [wall, wall, wall, wall, wall],
        ]
    )


def test_environment_reset_returns_initial_state() -> None:
    environment = QLearningEnvironment(create_training_level())

    assert environment.reset() == (1, 1, False)


def test_wall_hit_keeps_position_and_gives_penalty() -> None:
    environment = QLearningEnvironment(create_training_level())

    state, reward, done, info = environment.step(0)

    assert state == (1, 1, False)
    assert reward == -5
    assert not done
    assert info["hit_wall"]


def test_cheese_and_home_rewards_finish_episode() -> None:
    environment = QLearningEnvironment(create_training_level())

    environment.step(3)
    state, reward, done, _ = environment.step(3)

    assert state == (1, 3, True)
    assert reward == 30
    assert not done

    environment.step(2)
    state, reward, done, info = environment.step(2)

    assert state == (1, 1, True)
    assert reward == 100
    assert done
    assert info["success"]


def test_q_value_uses_classic_update_formula() -> None:
    agent = QLearningAgent(
        learning_rate=0.5,
        discount_factor=0.9,
        epsilon=0.0,
    )
    state = (1, 1, False)
    next_state = (1, 2, False)
    agent.get_q_values(next_state)[3] = 10

    value = agent.update_q_value(
        state,
        action=3,
        reward=-1,
        next_state=next_state,
    )

    assert value == pytest.approx(4.0)


def test_epsilon_does_not_drop_below_minimum() -> None:
    agent = QLearningAgent(
        epsilon=0.1,
        epsilon_min=0.05,
        epsilon_decay=0.1,
    )

    assert agent.decay_epsilon() == 0.05
    assert agent.decay_epsilon() == 0.05


def test_training_learns_optimal_round_trip() -> None:
    environment = QLearningEnvironment(create_training_level())
    agent = QLearningAgent(seed=4)

    stats = train_agent(
        environment,
        agent,
        episodes=300,
    )
    comparison = compare_with_bfs(environment, agent)

    assert stats.success_rate > 90
    assert comparison["success"]
    assert comparison["q_learning_steps"] == comparison["bfs_steps"]


def test_q_table_can_be_saved_and_loaded(tmp_path) -> None:
    agent = QLearningAgent(seed=2)
    state = (1, 1, False)
    agent.get_q_values(state)[3] = 12.5
    path = tmp_path / "q_table.json"

    agent.save_q_table(path)
    loaded_agent = QLearningAgent()
    loaded_agent.load_q_table(path)

    assert loaded_agent.get_q_values(state)[3] == 12.5
