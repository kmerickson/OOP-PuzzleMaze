from typing import Optional
from game_states import MainMenuState, GameEvents, GameState
from screens import MainMenu, InfoScreen
import pygame
from game import Game
import sys


class ChipsCoreEscape:
    """Singelton class that's the main entry point of
      program
    """
    _instance: Optional['ChipsCoreEscape'] = None

    DEFAULT_WIDTH: int = 1280
    DEFUALT_HEIGHT: int = 720

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
        self._state: GameState = MainMenuState()

    def _set_screen(self) -> pygame.Surface:
        pygame.init()
        return pygame.display.set_mode(
            (self.DEFAULT_WIDTH, self.DEFUALT_HEIGHT),
            pygame.RESIZABLE)

    def display_screen(self) -> None:
        """Display screen related to current state
        """
        self._state.display_screen(self)

    def handle_user(self, event: GameEvents) -> None:
        """Handle user events based on current state

        Args:
            event (GameEvents): event to consider
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
                    self.handle_user(GameEvents.USER_CLICK)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.handle_user(GameEvents.ESCAPE)
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
    def state(self) -> GameState:
        """Getter for state attribute

        Returns:
            _state: the state that the class
            is currently is in
        """
        return self._state

    @state.setter
    def state(self, state: GameState) -> None:
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
