"""Module containing the decorators for a text object
"""

__author__ = "Jessica Story"
__date__ = "5/13/25"
__license__ = "MIT"

from typing_extensions import override
import pygame
from drawable import Drawable
from text import Text
from drawable_decorator import DrawableDecorator


class Outline(DrawableDecorator):
    """Decorator for Drawable objects. Creates
        outline behind object.
    """

    def __init__(self, drawable: Text, outline_color: str,
                 outline_size: float) -> None:
        """Constructor for Outline class

        Args:
            drawable (Text): object to draw outline for
            outline_color (str): color of the outline
            outline_size (_type_): size of the extension of the
            outline from original text
        """
        super().__init__(drawable)
        self._outline_color: str = outline_color
        self._outline_size: float = outline_size
        self._font: pygame.font.Font = pygame.font.Font(
            self.drawable.image_dir, int(
                self.original_size + self._outline_size
            )
        )
        self._surface: pygame.Surface = self._font.render(
            self.drawable.data, True, self._outline_color)

        self._rect: pygame.Rect = self._surface.get_rect(
            center=(
                self.drawable.x_pos, self.drawable.y_pos
            )
        )

    @override
    def draw(self) -> None:
        """Implementation of the draw function from base class
        """
        self.drawable.screen.blit(self._surface, self._rect)
        self.drawable.draw()

    @override
    def dynamically_draw(self) -> None:
        """Implementation of the dynamically_draw function from base class
        """
        self._adjust_to_changes()
        self.drawable._adjust_to_changes()
        self.draw()

    @override
    def _adjust_to_changes(self) -> None:
        """Implementation of the _adjust_to_changes function from base class
        """
        self.drawable.resize_screen()
        self.drawable._adjust_to_changes()

        self._font = pygame.font.Font(
            self.drawable.image_dir, int(
                self.original_size + self._outline_size
            )
        )
        self.surface = self._font.render(self.drawable.data, True,
                                         self._outline_color)
        self.rect = self.surface.get_rect(
            center=(
                self.drawable.x_pos, self.drawable.y_pos
            )
        )


class Button(DrawableDecorator):
    """Decorator for Drawable objects. Creates
        a button behind the object.
    """

    def __init__(self, drawable: Drawable, image_dir: str) -> None:
        """Constructor for the Button Class

        Args:
            drawable (Drawable): Object to place button behind
            image_dir (str): Directory of button image
        """
        super().__init__(drawable)
        self._button_image_dir: str = image_dir
        self._surface: pygame.Surface = pygame.image.load(
            self._button_image_dir)

        self._button_width: float = self._surface.get_size()[0]
        self._button_height: float = self._surface.get_size()[1]
        self._rect: pygame.Rect = self._surface.get_rect(
            center=(
                self.drawable.x_pos, self.drawable.y_pos))
        self.original_size = self._button_height

    def draw(self) -> None:
        """Implementation of the draw function from base class
        """
        self.drawable.screen.blit(self._surface, self._rect)
        self.drawable.draw()

    def dynamically_draw(self) -> None:
        """Implementation of the dynamically_draw function from base class
        """
        self._adjust_to_changes()
        self.original_size = self._button_height
        self.drawable._adjust_to_changes()
        self.draw()

    def _adjust_to_changes(self) -> None:
        """Implementation of the _adjust_to_changes function from base class
        """
        screen_width, screen_height = self.drawable.screen.get_size()
        change_in_screen_width, change_in_screen_height = (
            screen_width / self.drawable.screen_width,
            screen_height / self.drawable.screen_height
        )
        self._button_width = change_in_screen_width * self._button_width
        self._button_height = change_in_screen_height * self._button_height
        self.drawable.resize_screen()

        self._surface = pygame.transform.scale(
            self._surface,
            (self._button_width, self._button_height))
        self._rect = self._surface.get_rect(
            center=(
                self.drawable.x_pos, self.drawable.y_pos
            )
        )
