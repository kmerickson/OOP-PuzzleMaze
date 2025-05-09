"""
"""
from typing_extensions import override
import pygame
from ui_elements.drawable import Drawable


class Text(Drawable):
    """Concrete component for the decorator design pattern.
    """

    def __init__(self, screen: pygame.Surface, factor_of_x_pos: float,
                 factor_of_y_pos: float, image_dir: str, size: float,
                 text: str, color: str) -> None:
        """Constructor for the Text class

        Args:
            screen (pygame.Surface): Surface that will be drawn on
            factor_of_x_pos (float): Position to place text on x-axis
            factor_of_y_pos (float): Position to place text on y-axis
            image_dir (str): Directory to find font that will be used
            size (float): Size of font
            text (str): Text to be drawn on screen
            color (str): Color of text
        """
        super().__init__(screen, factor_of_x_pos, factor_of_y_pos,
                         image_dir, size, text)
        self._color: str = color
        self._font: pygame.font.Font = pygame.font.Font(
            self.image_dir, int(self.size)
        )

        self.surface = self._font.render(self.data, True, self._color)
        self.rect = self.surface.get_rect(
            center=(
                self.x_pos, self.y_pos
            )
        )

    @override
    def draw(self) -> None:
        """Implementation of draw function from base class
        """
        if self.surface is not None and self.rect is not None:
            self.screen.blit(self.surface, self.rect)

    @override
    def dynamically_draw(self) -> None:
        """Implementation of dynamically_draw function from base class
        """
        self._adjust_to_changes()
        self.draw()

    @override
    def _adjust_to_changes(self) -> None:
        """Implementation of _adjust_to_changes function from base class
        """
        self.resize_screen()
        self._font = pygame.font.Font(
            self.image_dir, int(self.size)
        )
        self.surface = self._font.render(self.data, True, self._color)
        self.rect = self.surface.get_rect(
            center=(
                self.x_pos, self.y_pos
            )
        )

    @property
    def color(self) -> str:
        """Getter for the color variable

        Returns:
            _color (str)
            color of the text that will be drawn
        """
        return self._color

    @color.setter
    def color(self, color: str) -> None:
        """Setter for the color variable

        Args:
            color (float):
            new color of the text to be drawn
        """
        self._color = color

    @property
    def font(self) -> pygame.font.Font:
        """Getter for the font variable

        Returns:
            _font (pygame.font)
            pygame font object
        """
        return self._font

    @font.setter
    def font(self, font: pygame.font.Font) -> None:
        """Setter for the font variable

        Args:
            font (pygame.font):
            new pygame font object that be
            used while drawing object
        """
        self._font = font
