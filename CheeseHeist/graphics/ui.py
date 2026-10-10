"""Meniul si ecranele de progres ale jocului."""

from __future__ import annotations

from typing import Optional

import pygame

from config import settings


HUMAN_MODE = "human"
AGENT_MODE = "agent"
RANDOM_MODE = "random"
EVOLVE_MODE = "evolve"

MODE_OPTIONS = (
    (HUMAN_MODE, "Human Play"),
    (AGENT_MODE, "Watch Trained Agent"),
    (RANDOM_MODE, "Generate Random Level"),
    (EVOLVE_MODE, "Evolve Level"),
)

MODE_LABELS = dict(MODE_OPTIONS)


class GameUI:
    """Deseneaza meniul si gestioneaza selectiile lui."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.selected_mode = 0
        self.selected_difficulty = (
            settings.DIFFICULTY_LEVELS.index(
                settings.DEFAULT_DIFFICULTY
            )
        )

        self.title_font = pygame.font.Font(None, 58)
        self.heading_font = pygame.font.Font(None, 31)
        self.normal_font = pygame.font.Font(None, 24)

        self.mode_rectangles: list[pygame.Rect] = []
        self.difficulty_rectangles: list[
            pygame.Rect
        ] = []
        self.start_rectangle = pygame.Rect(0, 0, 0, 0)

    @property
    def mode(self) -> str:
        """Returneaza cheia modului selectat."""

        return MODE_OPTIONS[self.selected_mode][0]

    @property
    def difficulty(self) -> str:
        """Returneaza dificultatea selectata."""

        return settings.DIFFICULTY_LEVELS[
            self.selected_difficulty
        ]

    def get_selection(self) -> tuple[str, str]:
        """Returneaza modul si dificultatea curenta."""

        return self.mode, self.difficulty

    def handle_menu_event(
        self,
        event: pygame.event.Event,
    ) -> Optional[tuple[str, str]]:
        """Actualizeaza meniul si confirma selectia."""

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_mode = (
                    self.selected_mode - 1
                ) % len(MODE_OPTIONS)

            elif event.key == pygame.K_DOWN:
                self.selected_mode = (
                    self.selected_mode + 1
                ) % len(MODE_OPTIONS)

            elif event.key == pygame.K_LEFT:
                self.selected_difficulty = (
                    self.selected_difficulty - 1
                ) % len(settings.DIFFICULTY_LEVELS)

            elif event.key == pygame.K_RIGHT:
                self.selected_difficulty = (
                    self.selected_difficulty + 1
                ) % len(settings.DIFFICULTY_LEVELS)

            elif event.key in {
                pygame.K_RETURN,
                pygame.K_SPACE,
            }:
                return self.get_selection()

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            for index, rectangle in enumerate(
                self.mode_rectangles
            ):
                if rectangle.collidepoint(event.pos):
                    self.selected_mode = index

            for index, rectangle in enumerate(
                self.difficulty_rectangles
            ):
                if rectangle.collidepoint(event.pos):
                    self.selected_difficulty = index

            if self.start_rectangle.collidepoint(event.pos):
                return self.get_selection()

        return None

    def _draw_option(
        self,
        rectangle: pygame.Rect,
        text: str,
        selected: bool,
    ) -> None:
        color = (
            settings.PANEL_COLOR
            if selected
            else settings.BACKGROUND_COLOR
        )
        border_color = (
            settings.ACCENT_COLOR
            if selected
            else settings.GRID_LINE_COLOR
        )

        pygame.draw.rect(
            self.screen,
            color,
            rectangle,
            border_radius=6,
        )
        pygame.draw.rect(
            self.screen,
            border_color,
            rectangle,
            width=2,
            border_radius=6,
        )

        text_color = (
            settings.ACCENT_COLOR
            if selected
            else settings.TEXT_COLOR
        )
        surface = self.normal_font.render(
            text,
            True,
            text_color,
        )
        self.screen.blit(
            surface,
            surface.get_rect(center=rectangle.center),
        )

    def draw_menu(self) -> None:
        """Deseneaza meniul principal."""

        self.screen.fill(settings.BACKGROUND_COLOR)
        center_x = self.screen.get_width() // 2

        title = self.title_font.render(
            "CHEESE HEIST",
            True,
            settings.ACCENT_COLOR,
        )
        self.screen.blit(
            title,
            title.get_rect(center=(center_x, 65)),
        )

        mode_heading = self.heading_font.render(
            "MODE",
            True,
            settings.SECONDARY_TEXT_COLOR,
        )
        self.screen.blit(
            mode_heading,
            mode_heading.get_rect(center=(center_x, 120)),
        )

        self.mode_rectangles = []

        for index, (_, label) in enumerate(MODE_OPTIONS):
            rectangle = pygame.Rect(
                center_x - 220,
                145 + index * 57,
                440,
                47,
            )
            self.mode_rectangles.append(rectangle)
            self._draw_option(
                rectangle,
                label,
                index == self.selected_mode,
            )

        difficulty_heading = self.heading_font.render(
            "DIFFICULTY",
            True,
            settings.SECONDARY_TEXT_COLOR,
        )
        self.screen.blit(
            difficulty_heading,
            difficulty_heading.get_rect(
                center=(center_x, 405)
            ),
        )

        self.difficulty_rectangles = []
        option_width = 125
        total_width = option_width * 3 + 20
        start_x = center_x - total_width // 2

        for index, difficulty in enumerate(
            settings.DIFFICULTY_LEVELS
        ):
            rectangle = pygame.Rect(
                start_x + index * (option_width + 10),
                430,
                option_width,
                44,
            )
            self.difficulty_rectangles.append(rectangle)
            self._draw_option(
                rectangle,
                difficulty.upper(),
                index == self.selected_difficulty,
            )

        self.start_rectangle = pygame.Rect(
            center_x - 100,
            525,
            200,
            50,
        )
        pygame.draw.rect(
            self.screen,
            settings.SUCCESS_COLOR,
            self.start_rectangle,
            border_radius=6,
        )

        start_text = self.heading_font.render(
            "START",
            True,
            settings.BACKGROUND_COLOR,
        )
        self.screen.blit(
            start_text,
            start_text.get_rect(
                center=self.start_rectangle.center
            ),
        )

    def draw_progress(
        self,
        title: str,
        lines: list[str],
        progress: float,
    ) -> None:
        """Deseneaza progresul unei operatii mai lungi."""

        self.screen.fill(settings.BACKGROUND_COLOR)
        center_x = self.screen.get_width() // 2

        title_surface = self.title_font.render(
            title,
            True,
            settings.ACCENT_COLOR,
        )
        self.screen.blit(
            title_surface,
            title_surface.get_rect(center=(center_x, 145)),
        )

        for index, line in enumerate(lines):
            surface = self.normal_font.render(
                line,
                True,
                settings.TEXT_COLOR,
            )
            self.screen.blit(
                surface,
                surface.get_rect(
                    center=(center_x, 230 + index * 38)
                ),
            )

        bar_rectangle = pygame.Rect(
            center_x - 240,
            420,
            480,
            22,
        )
        pygame.draw.rect(
            self.screen,
            settings.GRID_LINE_COLOR,
            bar_rectangle,
            border_radius=4,
        )

        progress = min(max(progress, 0.0), 1.0)
        fill_rectangle = bar_rectangle.copy()
        fill_rectangle.width = round(
            bar_rectangle.width * progress
        )
        pygame.draw.rect(
            self.screen,
            settings.SUCCESS_COLOR,
            fill_rectangle,
            border_radius=4,
        )
