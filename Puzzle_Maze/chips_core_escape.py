"""Module containing Chip's Core Escape class
"""

__author__ = "Jessica Story"
__date__ = "5/13/25"
__license__ = "MIT"

from typing import Optional
import sys
import pygame
from game_states import MainMenuState, ChipsCoreEscapeEvents
from screen_state import ScreenState
from game_screens import MainMenu, InfoScreen
from game import Game


class ChipsCoreEscape:
    """Singelton class that's the main entry point of
      program
    """
    _instance: Optional['ChipsCoreEscape'] = None

    DEFAULT_WIDTH: int = 1280
    DEFAULT_HEIGHT: int = 720

    def __init__(self) -> None:
        """Constructor for the ChipsCoreEscape class
        """
        if ChipsCoreEscape._instance:
            raise NameError(
                "Cannot create multiple instances of \
                a singleton class Solution")
        super().__init__()
        ChipsCoreEscape._instance = self
        self._screen: pygame.Surface = self._set_screen()
        self._play: Game = Game()
        self._menu: MainMenu = MainMenu(self._screen)
        self._info: InfoScreen = InfoScreen(self._screen)
        self._state: ScreenState = MainMenuState()

    def _set_screen(self) -> pygame.Surface:
        pygame.init()
        return pygame.display.set_mode(
            (self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT),
            pygame.RESIZABLE)

    def display_screen(self) -> None:
        """Display screen related to current state
        """
        self._state.display_screen(self)

    def handle_user(self, event: ChipsCoreEscapeEvents) -> None:
        """Handle user events based on current state

        Args:
            event (ChipsCoreEscapeEvents): event to consider
        """
        self._state.handle_event(self, event)

    def chips_core_escape(self) -> None:
        """Performs entire program
        """
        while True:
            self.display_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_user(ChipsCoreEscapeEvents.USER_CLICK)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.handle_user(ChipsCoreEscapeEvents.ESCAPE)
            pygame.display.update()

    @property
    def play(self) -> Game:
        """Getter for play attribute

        Returns:
            _play: object related to play state
        """
        return self._play

    @play.setter
    def play(self, game_obj: Game) -> None:
        """Setter for play attribute

        Args:
            game_obj: new game object
        """
        self._play = game_obj

    @property
    def info(self) -> InfoScreen:
        """Getter for info attribute

        Returns:
            _info: object related to info state
        """
        return self._info

    @property
    def menu(self) -> MainMenu:
        """Getter for menu attribute

        Returns:
            _menu: object related to main menu state
        """
        return self._menu

    @property
    def state(self) -> ScreenState:
        """Getter for state attribute

        Returns:
            _state: the state that the class
            is currently is in
        """
        return self._state

    @state.setter
    def state(self, state: ScreenState) -> None:
        """_Setter for state variable

        Args:
            state (GameState): state to
            change to
        """
        self._state = state

    @property
    def screen(self) -> pygame.Surface:
        """Getter for state attribute

        Returns:
            _screen: the surface game is drawn
            on
        """
        return self._screen

    @classmethod
    def get_instance(cls) -> Optional['ChipsCoreEscape']:
        """Returns the instance of the class

        Returns:
            WeatherApp: class instance
        """

        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Resets the instance
        """
        cls._instance = None

    @staticmethod
    def main() -> None:
        """main static method
        """
        game = ChipsCoreEscape()
        game.chips_core_escape()


if __name__ == "__main__":
    ChipsCoreEscape.main()  # pragma: no cover
