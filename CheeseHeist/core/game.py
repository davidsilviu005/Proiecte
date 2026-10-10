"""Bucla principala si integrarea tuturor modurilor de joc."""

from __future__ import annotations

from typing import Optional

import pygame

from config import settings
from core.game_logic import GameLogic
from core.game_state import GameState
from difficulty.difficulty_metrics import (
    calculate_difficulty_score,
    get_level_difficulty,
)
from difficulty.genetic_algorithm import (
    EvolutionResult,
    GeneticAlgorithm,
    LevelIndividual,
    save_evolution_result,
)
from entities.entity_manager import EntityManager
from generation.level_manager import LevelManager
from generation.level_validator import LevelValidator
from generation.maze_generator import MazeGenerator
from graphics.asset_manager import AssetManager
from graphics.renderer import Renderer
from graphics.ui import (
    AGENT_MODE,
    EVOLVE_MODE,
    HUMAN_MODE,
    MODE_LABELS,
    RANDOM_MODE,
    GameUI,
)
from learning.environment import QLearningEnvironment, State
from learning.q_learning_agent import QLearningAgent
from learning.training import (
    TrainingStats,
    extract_policy_path,
    save_training_results,
    train_agent,
)


class Game:
    """Controleaza jocul, meniul si modurile algoritmice."""

    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(
            (
                settings.WINDOW_WIDTH,
                settings.WINDOW_HEIGHT,
            )
        )
        pygame.display.set_caption(settings.WINDOW_TITLE)

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.has_started = False

        self.last_move_time = 0
        self.move_delay = settings.MOVE_DELAY
        self.last_agent_move_time = 0

        self.cheese_message_until = 0
        self.previous_cheese_state = False

        self.current_mode = HUMAN_MODE
        self.target_difficulty = settings.DEFAULT_DIFFICULTY
        self.difficulty_score: Optional[float] = None
        self.difficulty_name: Optional[str] = None

        self.evolution_result: Optional[EvolutionResult] = None
        self.evolution_initial_score: Optional[float] = None

        self.agent: Optional[QLearningAgent] = None
        self.agent_environment: Optional[
            QLearningEnvironment
        ] = None
        self.agent_state: Optional[State] = None
        self.training_stats: Optional[TrainingStats] = None
        self.learned_path: list[tuple[int, int]] = []
        self.agent_success = False
        self.agent_comparison: dict[str, int | bool] = {}

        self.assets = AssetManager()
        self.renderer = Renderer(self.screen, self.assets)
        self.ui = GameUI(self.screen)

        self.maze_generator = MazeGenerator(
            rows=settings.GRID_ROWS,
            columns=settings.GRID_COLUMNS,
            seed=settings.DEFAULT_MAZE_SEED,
        )

        self.level = self.generate_valid_level()
        self.update_level_components()
        self.print_level_information()

    def generate_valid_level(self) -> LevelManager:
        """Genereaza niveluri pana cand unul este jucabil."""

        maximum_attempts = 100

        for attempt in range(1, maximum_attempts + 1):
            generated_level = self.maze_generator.generate_maze()
            validator = LevelValidator(generated_level)

            if validator.is_level_playable():
                print(
                    "Labirint valid generat dupa "
                    f"{attempt} incercari."
                )
                return generated_level

        raise RuntimeError(
            "Nu s-a putut genera un labirint jucabil."
        )

    def generate_level_for_difficulty(
        self,
        difficulty: str,
    ) -> LevelManager:
        """Cauta un nivel din categoria de dificultate ceruta."""

        if difficulty not in settings.DIFFICULTY_LEVELS:
            raise ValueError("Dificultatea nu este valida.")

        generation_options = {
            "easy": (2, 0.24),
            "medium": (5, 0.12),
            "hard": (8, 0.05),
        }
        trap_count, passage_ratio = generation_options[difficulty]
        target = settings.DIFFICULTY_TARGET_SCORES[difficulty]

        closest_level: Optional[LevelManager] = None
        closest_difference = float("inf")

        for _ in range(settings.DIFFICULTY_GENERATION_ATTEMPTS):
            generator = MazeGenerator(
                rows=settings.GRID_ROWS,
                columns=settings.GRID_COLUMNS,
                trap_count=trap_count,
                extra_passage_ratio=passage_ratio,
            )
            level = generator.generate_maze()
            score = calculate_difficulty_score(level)

            if score is None:
                continue

            difference = abs(score - target)
            if difference < closest_difference:
                closest_level = level
                closest_difference = difference

            if get_level_difficulty(level) == difficulty:
                return level

        if closest_level is not None:
            return closest_level

        raise RuntimeError(
            "Nu s-a putut genera nivelul cerut."
        )

    def update_level_components(self) -> None:
        """Recreeaza obiectele care depind de nivelul curent."""

        self.level_validator = LevelValidator(self.level)
        self.bfs_path = (
            self.level_validator.get_home_to_cheese_path()
        )
        self.shortest_path_length = (
            self.level_validator.get_shortest_path_length()
            or 0
        )
        self.entity_manager = EntityManager.from_level(self.level)
        self.game_logic = GameLogic(
            self.level,
            self.entity_manager,
        )

        self.difficulty_score = calculate_difficulty_score(
            self.level
        )
        self.difficulty_name = get_level_difficulty(self.level)

        self.last_move_time = 0
        self.cheese_message_until = 0
        self.previous_cheese_state = False
        self.show_bfs_path = settings.SHOW_BFS_PATH_BY_DEFAULT

    def _handle_progress_events(self) -> None:
        """Pastreaza fereastra activa in timpul calculelor."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _show_evolution_progress(
        self,
        generation: int,
        best: LevelIndividual,
        history: list[float],
    ) -> None:
        score_text = "--"
        if best.difficulty_score is not None:
            score_text = f"{best.difficulty_score:.2f}"

        self.ui.draw_progress(
            "EVOLVING LEVEL",
            [
                f"Target: {self.target_difficulty.upper()}",
                (
                    "Initial score: "
                    f"{self.evolution_initial_score:.2f}"
                    if self.evolution_initial_score is not None
                    else "Initial score: --"
                ),
                (
                    f"Generation: {generation} / "
                    f"{settings.GA_GENERATIONS}"
                ),
                (
                    f"Fitness: {history[0]:.2f}"
                    f" -> {best.fitness:.2f}"
                ),
                f"Difficulty score: {score_text}",
            ],
            generation / max(1, settings.GA_GENERATIONS),
        )
        pygame.display.flip()
        self._handle_progress_events()

    def evolve_level(self) -> LevelManager:
        """Evolueaza un nivel spre dificultatea selectata."""

        initial_level = self.generate_valid_level()
        self.evolution_initial_score = (
            calculate_difficulty_score(initial_level)
        )

        algorithm = GeneticAlgorithm(
            target_difficulty=self.target_difficulty,
        )
        result = algorithm.evolve(
            initial_level=initial_level,
            progress_callback=self._show_evolution_progress,
        )

        self.evolution_result = result
        save_evolution_result(result)

        return result.best_individual.level

    def _show_training_progress(
        self,
        episode: int,
        stats: TrainingStats,
    ) -> None:
        if (
            episode != 1
            and episode % 50 != 0
            and episode != settings.Q_LEARNING_EPISODES
        ):
            return

        recent_successes = sum(stats.successes[-100:])
        recent_total = len(stats.successes[-100:])
        recent_rate = (
            recent_successes / max(1, recent_total) * 100
        )

        self.ui.draw_progress(
            "TRAINING AGENT",
            [
                (
                    f"Episode: {episode} / "
                    f"{settings.Q_LEARNING_EPISODES}"
                ),
                f"Success rate: {stats.success_rate:.1f}%",
                f"Last 100 episodes: {recent_rate:.1f}%",
                f"Epsilon: {stats.epsilon_history[-1]:.3f}",
                f"Episode reward: {stats.rewards[-1]:.0f}",
            ],
            episode / settings.Q_LEARNING_EPISODES,
        )
        pygame.display.flip()
        self._handle_progress_events()

    def setup_agent(self) -> None:
        """Antreneaza agentul pentru nivelul curent."""

        environment = QLearningEnvironment(self.level)
        agent = QLearningAgent()
        untrained_path, untrained_success = extract_policy_path(
            environment,
            agent,
        )
        stats = train_agent(
            environment,
            agent,
            progress_callback=self._show_training_progress,
        )

        agent.save_q_table(settings.DEFAULT_Q_TABLE_PATH)
        learned_path, success = extract_policy_path(
            environment,
            agent,
        )
        bfs_steps = len(
            environment.get_optimal_round_trip_path()
        ) - 1
        comparison = {
            "untrained_success": untrained_success,
            "untrained_steps": len(untrained_path) - 1,
            "trained_success": success,
            "trained_steps": len(learned_path) - 1,
            "bfs_steps": bfs_steps,
        }
        save_training_results(
            stats,
            settings.RESULTS_DIRECTORY / "q_learning.json",
            comparison,
        )

        self.agent_environment = environment
        self.agent = agent
        self.training_stats = stats
        self.learned_path = learned_path
        self.agent_success = success
        self.agent_comparison = comparison
        self.agent_state = environment.reset()
        self.last_agent_move_time = 0

        print(
            "Q-learning:",
            len(learned_path) - 1,
            "pasi; BFS:",
            bfs_steps,
            "pasi; succes:",
            success,
        )

    def start_selected_mode(
        self,
        mode: str,
        difficulty: str,
    ) -> None:
        """Pregateste nivelul pentru optiunile alese in meniu."""

        self.current_mode = mode
        self.target_difficulty = difficulty
        self.evolution_result = None
        self.evolution_initial_score = None
        self.agent = None
        self.agent_environment = None
        self.agent_state = None
        self.training_stats = None
        self.learned_path = []
        self.agent_success = False
        self.agent_comparison = {}

        if mode == RANDOM_MODE:
            self.maze_generator = MazeGenerator(
                rows=settings.GRID_ROWS,
                columns=settings.GRID_COLUMNS,
            )
            self.level = self.generate_valid_level()

        elif mode == EVOLVE_MODE:
            self.level = self.evolve_level()

        else:
            self.level = self.generate_level_for_difficulty(
                difficulty
            )

        self.update_level_components()

        if mode == AGENT_MODE:
            self.setup_agent()

        self.has_started = True
        self.print_level_information()

    def generate_new_level(self) -> None:
        """Reporneste modul curent cu un nivel nou."""

        self.start_selected_mode(
            self.current_mode,
            self.target_difficulty,
        )

    def print_level_information(self) -> None:
        """Afiseaza in consola informatii despre nivel."""

        print()
        print(self.level.to_text())
        print("Traseu minim:", self.shortest_path_length)
        print("Numar capcane:", len(self.entity_manager.traps))
        print(
            "Dificultate:",
            self.difficulty_name,
            self.difficulty_score,
        )

    def handle_events(self) -> None:
        """Proceseaza evenimentele de la tastatura si mouse."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                continue

            if not self.has_started:
                if (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    self.is_running = False
                    continue

                selection = self.ui.handle_menu_event(event)
                if selection is not None:
                    self.start_selected_mode(*selection)
                continue

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE:
                self.is_running = False

            elif event.key == pygame.K_m:
                self.has_started = False
                self.entity_manager.mouse.stop_moving()

            elif event.key == pygame.K_r:
                self.generate_new_level()

            elif event.key == pygame.K_b:
                self.show_bfs_path = not self.show_bfs_path

    def get_pressed_movement(
        self,
    ) -> Optional[tuple[int, int]]:
        """Returneaza directia tinuta apasata de jucator."""

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            return -1, 0

        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            return 1, 0

        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            return 0, -1

        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            return 0, 1

        return None

    def update_mouse_animation_state(
        self,
        current_time: int,
    ) -> None:
        """Actualizeaza animatia soricelului controlat de om."""

        mouse = self.entity_manager.mouse
        movement = self.get_pressed_movement()
        can_move = (
            self.game_logic.is_playing()
            and not self.game_logic.is_stunned(current_time)
        )

        if movement is None or not can_move:
            mouse.stop_moving()
            return

        row_change, col_change = movement
        mouse.set_direction_from_movement(
            row_change,
            col_change,
        )
        mouse.start_moving()

    def handle_continuous_movement(
        self,
        current_time: int,
    ) -> None:
        """Muta jucatorul cat timp o directie este apasata."""

        if self.current_mode == AGENT_MODE:
            return

        if not self.game_logic.is_playing():
            return

        if self.game_logic.is_stunned(current_time):
            return

        movement = self.get_pressed_movement()
        if movement is None:
            return

        if current_time - self.last_move_time < self.move_delay:
            return

        row_change, col_change = movement
        self.game_logic.move_mouse(
            row_change,
            col_change,
            current_time,
        )
        self.last_move_time = current_time

    def update_agent(self, current_time: int) -> None:
        """Executa urmatoarea actiune a politicii invatate."""

        if (
            self.agent is None
            or self.agent_environment is None
            or self.agent_state is None
        ):
            return

        mouse = self.entity_manager.mouse

        if self.agent_environment.done:
            mouse.stop_moving()
            return

        elapsed = current_time - self.last_agent_move_time
        if elapsed < settings.AGENT_MOVE_DELAY:
            if elapsed > settings.AGENT_MOVE_DELAY // 2:
                mouse.stop_moving()
            return

        valid_actions = self.agent_environment.get_valid_actions(
            self.agent_state
        )
        action = self.agent.choose_action(
            self.agent_state,
            training=False,
            valid_actions=valid_actions,
        )
        row_change, col_change = (
            self.agent_environment.ACTIONS[action]
        )
        old_position = mouse.position

        next_state, _, done, info = (
            self.agent_environment.step(action)
        )

        mouse.set_direction_from_movement(
            row_change,
            col_change,
        )
        mouse.start_moving()

        if self.agent_environment.mouse_position != old_position:
            mouse.set_position(
                self.agent_environment.mouse_position
            )
            mouse.register_move()

        if info["collected_cheese"]:
            self.entity_manager.cheese.collect()
            mouse.collect_cheese()
            self.cheese_message_until = (
                current_time
                + settings.CHEESE_MESSAGE_DURATION
            )

        if info["hit_trap"]:
            for trap in self.entity_manager.traps:
                if trap.position == mouse.position:
                    trap.trigger()
                    break

        if done and info["success"]:
            self.game_logic.state = GameState.WON

        self.agent_state = next_state
        self.last_agent_move_time = current_time

    def update_cheese_message(self, current_time: int) -> None:
        """Afiseaza temporar mesajul de colectare."""

        has_cheese = self.entity_manager.mouse.has_cheese

        if has_cheese and not self.previous_cheese_state:
            self.cheese_message_until = (
                current_time
                + settings.CHEESE_MESSAGE_DURATION
            )

        self.previous_cheese_state = has_cheese

    def update(self) -> None:
        """Actualizeaza starea jocului."""

        if not self.has_started:
            return

        current_time = pygame.time.get_ticks()

        if self.current_mode == AGENT_MODE:
            self.update_agent(current_time)
        else:
            self.game_logic.update(current_time)
            self.update_mouse_animation_state(current_time)
            self.handle_continuous_movement(current_time)

        self.update_cheese_message(current_time)

    def get_game_status(self, current_time: int) -> str:
        """Returneaza textul starii curente."""

        if self.game_logic.state == GameState.WON:
            return "YOU WON"

        if (
            self.current_mode == AGENT_MODE
            and self.agent_environment is not None
            and self.agent_environment.done
        ):
            return "AGENT STOPPED"

        if self.game_logic.is_stunned(current_time):
            return "STUNNED"

        if self.game_logic.is_release_message_visible(current_time):
            return "FREE AGAIN"

        return "PLAYING"

    def _get_evolution_text(self) -> Optional[str]:
        if (
            self.evolution_initial_score is None
            or self.difficulty_score is None
        ):
            return None

        return (
            f"{self.evolution_initial_score:.1f}"
            f" -> {self.difficulty_score:.1f}"
        )

    def draw_game(self, current_time: int) -> None:
        """Deseneaza nivelul si informatiile lui."""

        self.screen.fill(settings.BACKGROUND_COLOR)
        self.renderer.draw_title()
        self.renderer.draw_level(self.level)

        if self.show_bfs_path:
            path = self.bfs_path

            if self.agent_environment is not None:
                path = (
                    self.agent_environment
                    .get_optimal_round_trip_path()
                )

            self.renderer.draw_debug_path(path)

            if self.learned_path:
                self.renderer.draw_agent_path(self.learned_path)

        self.renderer.draw_entities(
            self.entity_manager.get_active_entities(),
            current_time,
        )

        if settings.SHOW_GRID_LINES:
            self.renderer.draw_grid_lines(self.level)

        stun_seconds = (
            self.game_logic.get_stun_seconds_remaining(
                current_time
            )
        )
        active_traps = sum(
            1
            for trap in self.entity_manager.traps
            if trap.is_active
        )

        success_rate = None
        if self.training_stats is not None:
            success_rate = self.training_stats.success_rate

        self.renderer.draw_sidebar(
            shortest_path_length=self.shortest_path_length,
            moves=self.entity_manager.mouse.number_of_moves,
            has_cheese=self.entity_manager.mouse.has_cheese,
            active_traps=active_traps,
            status=self.get_game_status(current_time),
            stun_seconds=stun_seconds,
            has_won=self.game_logic.has_won(),
            mode=MODE_LABELS[self.current_mode],
            difficulty_name=self.difficulty_name or "invalid",
            difficulty_score=self.difficulty_score,
            success_rate=success_rate,
            evolution_text=self._get_evolution_text(),
        )

        self.renderer.draw_mouse_countdown(
            self.entity_manager.mouse,
            stun_seconds,
        )

        if (
            current_time < self.cheese_message_until
            and not self.game_logic.has_won()
        ):
            self.renderer.draw_cheese_message()

        if self.game_logic.has_won():
            self.renderer.draw_victory_overlay()

    def draw(self) -> None:
        """Deseneaza cadrul curent."""

        if not self.has_started:
            self.ui.draw_menu()
        else:
            self.draw_game(pygame.time.get_ticks())

        pygame.display.flip()

    def run(self) -> None:
        """Ruleaza jocul pana la inchiderea ferestrei."""

        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)

        pygame.quit()
