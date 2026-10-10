"""Algoritmul genetic folosit pentru evolutia nivelurilor."""

from __future__ import annotations

import json
import random
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from config import settings
from difficulty.difficulty_metrics import (
    calculate_difficulty_score,
    classify_difficulty,
)
from generation.level_manager import LevelManager
from generation.level_validator import LevelValidator
from generation.maze_generator import MazeGenerator
from generation.tile_type import TileType


Position = tuple[int, int]
ProgressCallback = Callable[
    [int, "LevelIndividual", list[float]],
    None,
]


def copy_level(level: LevelManager) -> LevelManager:
    """Copiaza nivelul fara a pastra referinte la grila veche."""

    grid = [row.copy() for row in level.grid]
    return LevelManager(grid)


def is_valid_level(level: LevelManager) -> bool:
    """Verifica obiectivele si existenta unui traseu complet."""

    homes = level.find_all_tiles(TileType.HOME)
    cheeses = level.find_all_tiles(TileType.CHEESE)

    if len(homes) != 1 or len(cheeses) != 1:
        return False

    return LevelValidator(level).is_level_playable()


def _get_level(
    value: LevelIndividual | LevelManager,
) -> LevelManager:
    if isinstance(value, LevelIndividual):
        return value.level

    return value


def _clean_grid(level: LevelManager) -> list[list[TileType]]:
    grid = [row.copy() for row in level.grid]

    for row in range(level.rows):
        for col in range(level.columns):
            if grid[row][col] in {
                TileType.HOME,
                TileType.CHEESE,
                TileType.TRAP,
            }:
                grid[row][col] = TileType.FLOOR

    return grid


def _walkable_neighbors(
    grid: list[list[TileType]],
    pos: Position,
) -> list[Position]:
    row, col = pos
    rows = len(grid)
    columns = len(grid[0])

    possible = [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1),
    ]

    return [
        neighbor
        for neighbor in possible
        if 0 <= neighbor[0] < rows
        and 0 <= neighbor[1] < columns
        and grid[neighbor[0]][neighbor[1]]
        != TileType.WALL
    ]


def _get_component(
    grid: list[list[TileType]],
    start: Position,
) -> set[Position]:
    queue = deque([start])
    visited = {start}

    while queue:
        current = queue.popleft()

        for neighbor in _walkable_neighbors(grid, current):
            if neighbor in visited:
                continue

            visited.add(neighbor)
            queue.append(neighbor)

    return visited


def _largest_component(
    grid: list[list[TileType]],
) -> list[Position]:
    remaining = {
        (row, col)
        for row in range(len(grid))
        for col in range(len(grid[0]))
        if grid[row][col] != TileType.WALL
    }

    largest: set[Position] = set()

    while remaining:
        start = next(iter(remaining))
        component = _get_component(grid, start)
        remaining.difference_update(component)

        if len(component) > len(largest):
            largest = component

    return sorted(largest)


def _get_distances(
    grid: list[list[TileType]],
    start: Position,
) -> dict[Position, int]:
    queue = deque([start])
    distances = {start: 0}

    while queue:
        current = queue.popleft()

        for neighbor in _walkable_neighbors(grid, current):
            if neighbor in distances:
                continue

            distances[neighbor] = distances[current] + 1
            queue.append(neighbor)

    return distances


def _prepare_grid(
    grid: list[list[TileType]],
) -> None:
    rows = len(grid)
    columns = len(grid[0])

    for col in range(columns):
        grid[0][col] = TileType.WALL
        grid[rows - 1][col] = TileType.WALL

    for row in range(rows):
        grid[row][0] = TileType.WALL
        grid[row][columns - 1] = TileType.WALL

    if len(_largest_component(grid)) >= 2:
        return

    middle_row = rows // 2
    middle_col = columns // 2
    grid[middle_row][middle_col] = TileType.FLOOR
    grid[middle_row][middle_col + 1] = TileType.FLOOR


def _add_special_tiles(
    grid: list[list[TileType]],
    trap_count: int,
    rng: random.Random,
) -> LevelManager:
    _prepare_grid(grid)
    component = _largest_component(grid)

    home = rng.choice(component)
    distances = _get_distances(grid, home)
    cheese = max(
        distances,
        key=distances.get,
    )

    home_row, home_col = home
    cheese_row, cheese_col = cheese

    grid[home_row][home_col] = TileType.HOME
    grid[cheese_row][cheese_col] = TileType.CHEESE

    free_positions = [
        pos
        for pos in component
        if pos not in {home, cheese}
    ]

    trap_count = min(
        max(0, trap_count),
        len(free_positions),
    )

    for trap_row, trap_col in rng.sample(
        free_positions,
        trap_count,
    ):
        grid[trap_row][trap_col] = TileType.TRAP

    return LevelManager(grid)


@dataclass
class LevelIndividual:
    """Un nivel impreuna cu valorile folosite la evolutie."""

    level: LevelManager
    fitness: float = float("-inf")
    difficulty_score: Optional[float] = None
    valid: bool = False

    def copy(self) -> LevelIndividual:
        """Returneaza o copie independenta a individului."""

        return LevelIndividual(
            level=copy_level(self.level),
            fitness=self.fitness,
            difficulty_score=self.difficulty_score,
            valid=self.valid,
        )

    def evaluate(self, target_difficulty: str) -> float:
        """Calculeaza fitness-ul pentru dificultatea ceruta."""

        self.valid = is_valid_level(self.level)

        if not self.valid:
            self.difficulty_score = None
            self.fitness = -10000.0
            return self.fitness

        score = calculate_difficulty_score(self.level)

        if score is None:
            self.difficulty_score = None
            self.fitness = -10000.0
            return self.fitness

        target = settings.DIFFICULTY_TARGET_SCORES[
            target_difficulty
        ]

        closeness = max(
            0.0,
            100.0 - abs(score - target) * 8.0,
        )

        category_bonus = 20.0
        if classify_difficulty(score) != target_difficulty:
            category_bonus = 0.0

        walkable = sum(
            1
            for row in self.level.grid
            for tile in row
            if tile != TileType.WALL
        )

        home = self.level.find_tile(TileType.HOME)
        connected = 0

        if home is not None:
            clean_grid = _clean_grid(self.level)
            connected = len(_get_component(clean_grid, home))

        balance_bonus = 20.0 * connected / max(1, walkable)
        playability_bonus = 50.0

        self.difficulty_score = score
        self.fitness = round(
            closeness
            + category_bonus
            + balance_bonus
            + playability_bonus,
            4,
        )

        return self.fitness


@dataclass
class EvolutionResult:
    """Rezultatul complet al unei rulari genetice."""

    target_difficulty: str
    initial_individual: LevelIndividual
    best_individual: LevelIndividual
    fitness_history: list[float] = field(
        default_factory=list
    )


def calculate_fitness(
    individual: LevelIndividual,
    target_difficulty: str,
) -> float:
    """Evalueaza un individ si returneaza fitness-ul lui."""

    return individual.evaluate(target_difficulty)


def select_parent(
    population: list[LevelIndividual],
    tournament_size: int = settings.GA_TOURNAMENT_SIZE,
    rng: Optional[random.Random] = None,
) -> LevelIndividual:
    """Alege un parinte prin selectie de tip turneu."""

    if not population:
        raise ValueError("Populatia nu poate fi goala.")

    rng = rng or random.Random()
    size = min(max(1, tournament_size), len(population))
    candidates = rng.sample(population, size)

    return max(
        candidates,
        key=lambda individual: individual.fitness,
    )


def crossover_levels(
    first_parent: LevelIndividual | LevelManager,
    second_parent: LevelIndividual | LevelManager,
    rng: Optional[random.Random] = None,
) -> LevelIndividual:
    """Combina doua grile si regenereaza elementele speciale."""

    rng = rng or random.Random()
    first_level = _get_level(first_parent)
    second_level = _get_level(second_parent)

    if (
        first_level.rows != second_level.rows
        or first_level.columns != second_level.columns
    ):
        raise ValueError(
            "Parintii trebuie sa aiba aceeasi dimensiune."
        )

    first_grid = _clean_grid(first_level)
    second_grid = _clean_grid(second_level)
    child_grid = [row.copy() for row in first_grid]

    if rng.random() < 0.5:
        cut = rng.randint(1, first_level.rows - 2)

        for row in range(cut, first_level.rows - 1):
            child_grid[row] = second_grid[row].copy()
    else:
        cut = rng.randint(1, first_level.columns - 2)

        for row in range(1, first_level.rows - 1):
            for col in range(cut, first_level.columns - 1):
                child_grid[row][col] = second_grid[row][col]

    first_traps = len(
        first_level.find_all_tiles(TileType.TRAP)
    )
    second_traps = len(
        second_level.find_all_tiles(TileType.TRAP)
    )
    trap_count = round((first_traps + second_traps) / 2)

    child_level = _add_special_tiles(
        child_grid,
        trap_count,
        rng,
    )

    return LevelIndividual(child_level)


def mutate_level(
    individual: LevelIndividual | LevelManager,
    mutation_rate: float = settings.GA_MUTATION_RATE,
    rng: Optional[random.Random] = None,
) -> LevelIndividual:
    """Muta pereti, coridoare, branza si capcane."""

    if not 0 <= mutation_rate <= 1:
        raise ValueError(
            "Rata de mutatie trebuie sa fie intre 0 si 1."
        )

    rng = rng or random.Random()
    level = _get_level(individual)
    grid = _clean_grid(level)

    for row in range(1, level.rows - 1):
        for col in range(1, level.columns - 1):
            if rng.random() >= mutation_rate:
                continue

            if grid[row][col] == TileType.WALL:
                grid[row][col] = TileType.FLOOR
            else:
                grid[row][col] = TileType.WALL

    trap_count = len(
        level.find_all_tiles(TileType.TRAP)
    )

    if rng.random() < 0.5:
        trap_count += rng.choice((-1, 1))

    mutated_level = _add_special_tiles(
        grid,
        trap_count,
        rng,
    )

    return LevelIndividual(mutated_level)


def preserve_elite(
    population: list[LevelIndividual],
    elite_count: int = settings.GA_ELITE_COUNT,
) -> list[LevelIndividual]:
    """Pastreaza copii ale celor mai buni indivizi."""

    elite_count = min(
        max(0, elite_count),
        len(population),
    )

    ordered = sorted(
        population,
        key=lambda individual: individual.fitness,
        reverse=True,
    )

    return [
        individual.copy()
        for individual in ordered[:elite_count]
    ]


def create_next_generation(
    population: list[LevelIndividual],
    target_difficulty: str,
    population_size: Optional[int] = None,
    elite_count: int = settings.GA_ELITE_COUNT,
    tournament_size: int = settings.GA_TOURNAMENT_SIZE,
    mutation_rate: float = settings.GA_MUTATION_RATE,
    rng: Optional[random.Random] = None,
) -> list[LevelIndividual]:
    """Creeaza o generatie noua folosind toti operatorii."""

    if not population:
        raise ValueError("Populatia nu poate fi goala.")

    rng = rng or random.Random()
    if population_size is None:
        population_size = len(population)

    if population_size <= 0:
        raise ValueError(
            "Dimensiunea populatiei trebuie sa fie pozitiva."
        )

    next_generation = preserve_elite(
        population,
        elite_count,
    )

    while len(next_generation) < population_size:
        first_parent = select_parent(
            population,
            tournament_size,
            rng,
        )
        second_parent = select_parent(
            population,
            tournament_size,
            rng,
        )

        child = crossover_levels(
            first_parent,
            second_parent,
            rng,
        )
        child = mutate_level(
            child,
            mutation_rate,
            rng,
        )
        child.evaluate(target_difficulty)
        next_generation.append(child)

    return next_generation


class GeneticAlgorithm:
    """Coordoneaza populatia si generatiile algoritmului."""

    def __init__(
        self,
        target_difficulty: str,
        rows: int = settings.GRID_ROWS,
        columns: int = settings.GRID_COLUMNS,
        population_size: int = settings.GA_POPULATION_SIZE,
        generations: int = settings.GA_GENERATIONS,
        mutation_rate: float = settings.GA_MUTATION_RATE,
        elite_count: int = settings.GA_ELITE_COUNT,
        tournament_size: int = settings.GA_TOURNAMENT_SIZE,
        seed: Optional[int] = None,
    ) -> None:
        if target_difficulty not in settings.DIFFICULTY_LEVELS:
            raise ValueError("Dificultatea ceruta nu este valida.")

        if population_size < 2:
            raise ValueError(
                "Populatia trebuie sa aiba cel putin doi indivizi."
            )

        if generations < 0:
            raise ValueError(
                "Numarul de generatii nu poate fi negativ."
            )

        if not 0 <= mutation_rate <= 1:
            raise ValueError(
                "Rata de mutatie trebuie sa fie intre 0 si 1."
            )

        self.target_difficulty = target_difficulty
        self.rows = rows
        self.columns = columns
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elite_count = elite_count
        self.tournament_size = tournament_size
        self.rng = random.Random(seed)

    def _generate_individual(self) -> LevelIndividual:
        trap_count = self.rng.randint(0, 9)
        passage_ratio = self.rng.uniform(0.0, 0.30)

        generator = MazeGenerator(
            rows=self.rows,
            columns=self.columns,
            seed=self.rng.randrange(1_000_000_000),
            trap_count=trap_count,
            extra_passage_ratio=passage_ratio,
        )

        return LevelIndividual(generator.generate_maze())

    def create_initial_population(
        self,
        initial_level: Optional[LevelManager] = None,
    ) -> list[LevelIndividual]:
        """Creeaza si evalueaza prima populatie."""

        population: list[LevelIndividual] = []

        if initial_level is not None:
            population.append(
                LevelIndividual(copy_level(initial_level))
            )

        while len(population) < self.population_size:
            population.append(self._generate_individual())

        for individual in population:
            individual.evaluate(self.target_difficulty)

        return population

    def evolve(
        self,
        initial_level: Optional[LevelManager] = None,
        progress_callback: Optional[ProgressCallback] = None,
    ) -> EvolutionResult:
        """Ruleaza evolutia si returneaza cel mai bun nivel."""

        population = self.create_initial_population(
            initial_level
        )
        initial = population[0].copy()
        best = max(
            population,
            key=lambda individual: individual.fitness,
        ).copy()
        history = [best.fitness]

        if progress_callback is not None:
            progress_callback(0, best.copy(), history.copy())

        for generation in range(1, self.generations + 1):
            population = create_next_generation(
                population=population,
                target_difficulty=self.target_difficulty,
                population_size=self.population_size,
                elite_count=self.elite_count,
                tournament_size=self.tournament_size,
                mutation_rate=self.mutation_rate,
                rng=self.rng,
            )

            generation_best = max(
                population,
                key=lambda individual: individual.fitness,
            )

            if generation_best.fitness > best.fitness:
                best = generation_best.copy()

            history.append(best.fitness)

            if progress_callback is not None:
                progress_callback(
                    generation,
                    best.copy(),
                    history.copy(),
                )

        return EvolutionResult(
            target_difficulty=self.target_difficulty,
            initial_individual=initial,
            best_individual=best,
            fitness_history=history,
        )


def save_level(
    level: LevelManager,
    path: Path,
) -> Path:
    """Salveaza grila unui nivel in format JSON."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "rows": level.rows,
        "columns": level.columns,
        "grid": [
            [tile.name for tile in row]
            for row in level.grid
        ],
    }

    path.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )

    return path


def save_evolution_result(
    result: EvolutionResult,
    generated_directory: Path = (
        settings.GENERATED_LEVELS_DIRECTORY
    ),
    results_directory: Path = settings.RESULTS_DIRECTORY,
) -> tuple[Path, Path]:
    """Salveaza nivelul final si istoricul fitness-ului."""

    level_path = Path(generated_directory) / (
        f"evolved_{result.target_difficulty}.json"
    )
    result_path = Path(results_directory) / (
        f"evolution_{result.target_difficulty}.json"
    )

    save_level(result.best_individual.level, level_path)
    result_path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "target_difficulty": result.target_difficulty,
        "initial_score": (
            result.initial_individual.difficulty_score
        ),
        "final_score": (
            result.best_individual.difficulty_score
        ),
        "best_fitness": result.best_individual.fitness,
        "fitness_history": result.fitness_history,
    }

    result_path.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )

    return level_path, result_path
