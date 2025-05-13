"""Module containing text and button with the
    parameters used throughout the game
"""

__author__ = "Jessica Story"
__date__ = "5/13/25"
__license__ = "MIT"

import pygame
from interactive_text import InteractiveText
from interactive_button import InteractiveButton


class GameText(InteractiveText):
    """Class to avoid large parameter lists while
       using text
    """
    FONT_DIRECTORY: str = "assets/Cyberpunks.ttf"
    IDLE_COLOR: str = "White"
    HOVER_COLOR: str = "Light Green"
    OUTLINE_COLOR: str = "Black"
    OUTLINE_SIZE: int = 1

    def __init__(
            self, screen: pygame.Surface, text_to_place: str,
            factor_of_x_pos: float,
            factor_of_y_pos: float, size: float) -> None:
        """Constructor for GameText class

        Args:
            screen (pygame.Surface): Surface to draw on
            text_to_place (str): Text that will be drawn
            factor_of_x_pos (float): X-axis position of text
            factor_of_y_pos (_type_): Y-axis position of text
            size (float): Size of font
        """
        super().__init__(screen, factor_of_x_pos, factor_of_y_pos,
                         self.FONT_DIRECTORY, size, text_to_place,
                         self.IDLE_COLOR, self.HOVER_COLOR,
                         self.OUTLINE_COLOR, 1)


class GameButton(InteractiveButton):
    """Class to avoid large parameter lists while
       using buttons
    """
    FONT_DIRECTORY: str = "assets/Cyberpunks.ttf"
    IDLE_COLOR: str = "White"
    HOVER_COLOR: str = "Light Green"
    OUTLINE_COLOR: str = "Black"
    OUTLINE_SIZE: int = 15
    BUTTON_IMAGE_DIR: str = "assets/button.png"

    def __init__(self, screen: pygame.Surface, text_to_place: str,
                 factor_of_x_pos: float,
                 factor_of_y_pos: float) -> None:
        """Constructor for GameButton class

        Args:
            screen (pygame.Surface): Surface to draw on
            text_to_place (str): Text that will be drawn
            factor_of_x_pos (float): X-axis position of text
            factor_of_y_pos (_type_): Y-axis position of text
            size (float): Size of font
        """
        super().__init__(screen, factor_of_x_pos, factor_of_y_pos,
                         self.FONT_DIRECTORY, 0, text_to_place,
                         self.IDLE_COLOR, self.HOVER_COLOR,
                         self.OUTLINE_COLOR, 10, self.BUTTON_IMAGE_DIR)
