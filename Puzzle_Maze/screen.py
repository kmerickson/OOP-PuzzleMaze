"""Modules containing various screens that will
  for different states within the game
"""

__author__ = "Jessica Story"
__date__ = "5/2/25"
__license__ = "MIT"

from abc import ABC, abstractmethod
import pygame


class Screen(ABC):
    """Class acting as common interface for screens
    """

    def __init__(self, screen: pygame.Surface) -> None:
        """Constructor for screen class

        Args:
            screen (pygame.Surface): screen to draw on
        """
        self._screen: pygame.Surface = screen
        self._screen_width: float = self._screen.get_size()[0]
        self._screen_height: float = self._screen.get_size()[1]

    @abstractmethod
    def draw_screen(self) -> None:
        """Draw screen for a single iteration
        """

    @abstractmethod
    def adjust_to_screen(self) -> None:
        """Adjust variables to a size change
        """

    def main_loop(self) -> None:
        """Display screen on its own
        """
        while True:
            self.draw_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.display.update()

    @property
    def screen(self) -> pygame.Surface:
        """Getter for screen variable

        Returns:
            _screen (pygame.Surface): surface that is drawn on
        """
        return self._screen

    @property
    def screen_width(self) -> float:
        """Getter for screen width variable

        Returns:
            _self_width (float): width of screen
            variable
        """
        return self._screen_width

    @property
    def screen_height(self) -> float:
        """Getter for screen height variable

        Returns:
            _self_height: height of screen
            variable
        """
        return self._screen_height

    def resize_screen_variables(self) -> None:
        """Resize size variables after screen change
        """
        self._screen_width, self._screen_height = self._screen.get_size()
