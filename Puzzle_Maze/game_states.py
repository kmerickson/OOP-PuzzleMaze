"""Module containing classes
   directly associated with program run.
   Done via state pattern
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional
from typing_extensions import override
import pygame
from game import Game
from screens import MainMenu, InfoScreen


class GameEvents(Enum):
    """Enum containing
        all the states the
        game can be in
    """
    USER_CLICK: int = 0,
    ESCAPE: int = 1


class GameState(ABC):
    """Base state class
    """
    @abstractmethod
    def display_screen(self, outer_class: "ChipsCoreEscape"):
        """Method to display screen dependent on current state

        Args:
            outer_class (ChipsCoreEscape): the class that
            will contain states
        """
        pass

    @abstractmethod
    def handle_event(self, outer_class: "ChipsCoreEscape", event: GameEvents):
        """Method to that decides which events to deal with it and how
           to deal with them depending on current state

        Args:
            outer_class (ChipsCoreEscape): the class that
            will contain states
            event (GameEvents): the event to react to
        """
        pass


class PlayState(GameState):
    """The concrete state class of play
    """
    @override
    def display_screen(self, outer_class: "ChipsCoreEscape"):
        """Method to display screen in the play state

        Args:
            outer_class (ChipsCoreEscape): the class that
            will contain states
        """
        outer_class.play.single_iteration()
    
    @override
    def handle_event(self, outer_class: "ChipsCoreEscape", event: GameEvents):
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
    def display_screen(self, outer_class: "ChipsCoreEscape"):
        """Method to display screen in the info state

        Args:
            outer_class (ChipsCoreEscape): the class that
            will contain states
        """
        outer_class.info.draw_screen()
    
    @override
    def handle_event(self, outer_class: "ChipsCoreEscape", event: GameEvents):
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
            if (outer_class.info.back_button.button.rect.collidepoint(mouse_position)):
                outer_class.state = MainMenuState()


class MainMenuState(GameState):
    """The concrete state class of main menu
    """
    @override
    def display_screen(self, outer_class: "ChipsCoreEscape"):
        """Method to display screen in the main menu state

        Args:
            outer_class (ChipsCoreEscape): the class that
            will contain states
        """
        outer_class.menu.draw_screen()
    
    def handle_event(self, outer_class: "ChipsCoreEscape", event: GameEvents):
        """Method to that decides which events to deal with it and how
           to deal with them in the main menu state

        Args:
            outer_class (ChipsCoreEscape): the class that
            will contain states
            event (GameEvents): the event to react to
        """
        if event == GameEvents.USER_CLICK:
            mouse_position = pygame.mouse.get_pos()
            if (outer_class.menu.play_button.button.rect.collidepoint(mouse_position)):
                outer_class.play = Game()
                outer_class.state = PlayState() 
            elif (outer_class.menu.info_button.button.rect.collidepoint(mouse_position)):
                outer_class.state = InfoState()
            elif (outer_class.menu.quit_button.button.rect.collidepoint(mouse_position)):
                pygame.quit()

        if event == GameEvents.ESCAPE:
            pygame.quit()


class ChipsCoreEscape:
    """Singelton class that's the main entry point of
      program
    """
    _instance: Optional['ChipsCoreEscape'] = None

    DEFAULT_WIDTH: int = 1280
    DEFUALT_HEIGHT: int = 720

    def __init__(self):
        """Constructor for the ChipsCoreEscape class
        """
        if ChipsCoreEscape._instance:
            raise NameError(
                "Cannot create multiple instances of \
                a singleton class Solution")
        super().__init__()
        ChipsCoreEscape._instance = self

        self._screen: pygame.Surface = self.__set_screen()
        self._play: Game = Game()
        self._menu: MainMenu = MainMenu(self._screen)
        self._info: InfoScreen = InfoScreen(self._screen)
        self._state: GameState = MainMenuState()

    def __set_screen(self) -> pygame.Surface:
        pygame.init()
        return pygame.display.set_mode(
            (self.DEFAULT_WIDTH, self.DEFUALT_HEIGHT),
            pygame.RESIZABLE)
    
    def display_screen(self) -> None:
        """Display screen related to current state
        """
        self._state.display_screen(self)

    def handle_user(self, event: GameEvents) -> None:
        """Handl user events based on current state

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
