"""Teste pentru algoritmul genetic si operatorii sai."""

import random

from difficulty.genetic_algorithm import (
    GeneticAlgorithm,
    LevelIndividual,
    create_next_generation,
    crossover_levels,
    is_valid_level,
    mutate_level,
    preserve_elite,
    select_parent,
)
from generation.maze_generator import MazeGenerator
from generation.tile_type import TileType


def create_individual(seed: int) -> LevelIndividual:
    """Creeaza un individ jucabil si repetabil."""

    level = MazeGenerator(
        rows=9,
        columns=9,
        seed=seed,
        trap_count=2,
    ).generate_maze()
    individual = LevelIndividual(level)
    individual.evaluate("medium")
    return individual


def test_individual_copy_has_independent_grid() -> None:
    original = create_individual(1)
    copied = original.copy()
    old_tile = original.level.get_tile((1, 1))

    copied.level.set_tile((1, 1), TileType.FLOOR)

    assert original.level.get_tile((1, 1)) == old_tile


def test_tournament_selects_best_when_all_compete() -> None:
    population = [create_individual(seed) for seed in range(3)]
    population[0].fitness = 1
    population[1].fitness = 5
    population[2].fitness = 3

    parent = select_parent(
        population,
        tournament_size=3,
        rng=random.Random(2),
    )

    assert parent is population[1]


def test_crossover_creates_valid_child() -> None:
    child = crossover_levels(
        create_individual(1),
        create_individual(2),
        rng=random.Random(3),
    )

    assert is_valid_level(child.level)
    assert len(
        child.level.find_all_tiles(TileType.HOME)
    ) == 1
    assert len(
        child.level.find_all_tiles(TileType.CHEESE)
    ) == 1


def test_mutation_preserves_closed_border() -> None:
    mutated = mutate_level(
        create_individual(4),
        mutation_rate=0.5,
        rng=random.Random(5),
    )

    assert is_valid_level(mutated.level)

    for col in range(mutated.level.columns):
        assert mutated.level.get_tile((0, col)) == TileType.WALL
        assert mutated.level.get_tile(
            (mutated.level.rows - 1, col)
        ) == TileType.WALL


def test_elite_is_copied_in_fitness_order() -> None:
    population = [create_individual(seed) for seed in range(3)]
    population[0].fitness = 2
    population[1].fitness = 9
    population[2].fitness = 4

    elite = preserve_elite(population, elite_count=2)

    assert [individual.fitness for individual in elite] == [9, 4]
    assert elite[0] is not population[1]


def test_next_generation_has_requested_size() -> None:
    population = [create_individual(seed) for seed in range(6)]

    next_generation = create_next_generation(
        population,
        target_difficulty="medium",
        population_size=6,
        rng=random.Random(8),
    )

    assert len(next_generation) == 6
    assert all(
        is_valid_level(individual.level)
        for individual in next_generation
    )


def test_evolution_records_each_generation() -> None:
    algorithm = GeneticAlgorithm(
        target_difficulty="hard",
        rows=9,
        columns=9,
        population_size=6,
        generations=2,
        seed=9,
    )

    result = algorithm.evolve()

    assert len(result.fitness_history) == 3
    assert is_valid_level(result.best_individual.level)
    assert result.fitness_history == sorted(
        result.fitness_history
    )
