"""Module containing classes
   directly associated with program run.
   Done via state pattern
"""

from __future__ import annotations
from typing_extensions import override
from typing import TYPE_CHECKING
import sys
import pygame
from game import Game
from game_state import GameEvents, GameState

if TYPE_CHECKING:
    from chips_core_escape import ChipsCoreEscape

__author__ = "Jessica Story"
__date__ = "5/2/25"
__license__ = "MIT"


class PlayState(GameState):
    """The concrete state class of play
    """
    @override
    def display_screen(self, outer_class: "ChipsCoreEscape") -> None:
        """Method to display screen in the play state

        Args:
            outer_class (ChipsCoreEscape): the class that
            will contain states
        """
        outer_class.play.single_iteration()

    @override
    def handle_event(self, outer_class: "ChipsCoreEscape",
                     event: GameEvents) -> None:
        """Method to that decides which events to deal with it and how
           to deal with them in the play state

        Args:
            outer_class (ChipsCoreEscape): the class that
            will contain states
            event (GameEvents): the event to react to
        """
        if event == GameEvents.ESCAPE:
            outer_class.state = MainMenuState()


class InfoState(GameState):
    """The concrete state class of info
    """
    @override
    def display_screen(self, outer_class: "ChipsCoreEscape") -> None:
        """Method to display screen in the info state

        Args:
            outer_class (ChipsCoreEscape): the class that
            will contain states
        """
        outer_class.info.draw_screen()

    @override
    def handle_event(self, outer_class: "ChipsCoreEscape",
                     event: GameEvents) -> None:
        """Method to that decides which events to deal with it and how
           to deal with them in the info state

        Args:
            outer_class (ChipsCoreEscape): the class that
            will contain states
            event (GameEvents): the event to react to
        """
        if event == GameEvents.ESCAPE:
            outer_class.state = MainMenuState()
        if event == GameEvents.USER_CLICK:
            mouse_position = pygame.mouse.get_pos()
            if (
                outer_class.info.back_button.button.rect is not None and
                outer_class.info.back_button.button.rect.collidepoint(mouse_position)
            ):
                outer_class.state = MainMenuState()


class MainMenuState(GameState):
    """The concrete state class of main menu
    """
    @override
    def display_screen(self, outer_class: "ChipsCoreEscape") -> None:
        """Method to display screen in the main menu state

        Args:
            outer_class (ChipsCoreEscape): the class that
            will contain states
        """
        outer_class.menu.draw_screen()

    def handle_event(self, outer_class: "ChipsCoreEscape",
                     event: GameEvents) -> None:
        """Method to that decides which events to deal with it and how
           to deal with them in the main menu state

        Args:
            outer_class (ChipsCoreEscape): the class that
            will contain states
            event (GameEvents): the event to react to
        """
        if event == GameEvents.USER_CLICK:
            mouse_position = pygame.mouse.get_pos()
            if (
                outer_class.menu.play_button.button.rect is not None and
                outer_class.menu.play_button.button.rect.collidepoint(mouse_position)
            ):
                outer_class.play = Game()
                outer_class.state = PlayState()
            elif (
                    outer_class.menu.info_button.button.rect is not None and
                    outer_class.menu.info_button.button.rect.collidepoint(mouse_position)
            ):
                outer_class.state = InfoState()
            elif (
                    outer_class.menu.quit_button.button.rect is not None and
                    outer_class.menu.quit_button.button.rect.collidepoint(mouse_position)
            ):
                pygame.quit()
                sys.exit()
        if event == GameEvents.ESCAPE:
            pygame.quit()
            sys.exit()