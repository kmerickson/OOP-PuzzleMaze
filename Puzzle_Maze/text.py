from abc import ABC, abstractmethod
from typing_extensions import override
import pygame


class Drawable(ABC):
    """The base component for the decorator design pattern.
        Intended to also be useful outside of text and decorators
    """

    def __init__(self, screen: pygame.Surface, factor_of_x_pos: float,
                 factor_of_y_pos: float, image_dir: str,
                 size: float, data: str) -> None:
        """Constructor for Drawable class

        Args:
            screen (pygame.Surface): Surface that will be drawn on
            factor_of_x_pos (float): Position to place object on x-axis
            factor_of_y_pos (float): Position to place object on y-axis
            image_dir (str): Directory to find image that be drawn on screen
            size (float): Size of object
            data (str): data for given object
        """
        self._screen: pygame.Surface = screen
        self._screen_width: float = self._screen.get_size()[0]
        self._screen_height: float = self._screen.get_size()[1]
        self._factor_of_x_pos: float = factor_of_x_pos
        self._factor_of_y_pos: float = factor_of_y_pos
        self._rect: pygame.Rect | None = None
        self._surface: pygame.Surface | None = None
        self._image_dir: str = image_dir
        self._size: float = size
        self._data: str = data

    @abstractmethod
    def draw(self) -> None:
        """Method to draw object on the screen.
        """
        pass

    @abstractmethod
    def dynamically_draw(self) -> None:
        """Method to accommodate players resizing the screen
        """
        pass

    @abstractmethod
    def _adjust_to_changes(self) -> None:
        """Method to adjust to changed instance variables
           (such as user resizing the screen) prior to
           drawing the object
        """
        pass

    def resize_screen(self) -> None:
        """Sets screen width and screen height variables
            based on given surface
        """
        self._screen_width, self._screen_height = self._screen.get_size()

    @property
    def screen(self) -> pygame.Surface:
        """Getter for the screen variable

        Returns:
            _screen (pygame.Surface)
            the surface the game is being drawn on
        """
        return self._screen

    @screen.setter
    def screen(self, screen: pygame.Surface) -> None:
        """Setter for the screen variable

        Args:
            screen (pygame.Surface)
            the surface the game will be drawn on
        """
        self._screen = screen

    @property
    def screen_width(self) -> float:
        """Getter for the screen width variable

        Returns:
            _width (float):
            the width of the surface the game is being drawn on
        """
        return self._screen_width

    @property
    def screen_height(self) -> float:
        """Getter for the screen height variable

        Returns:
            _height (float):
            the width of the surface the game is being drawn on
        """
        return self._screen_height

    @property
    def x_pos(self) -> float:
        """Getter for the x (horizontal) coordinate
            object will be drawn on

        Returns:
            x_pos (float): Result of multiplying the current
            screen width by idealized position on screen
        """
        return self._screen_width * self._factor_of_x_pos

    @property
    def factor_of_x_pos(self) -> float:
        """Getter for the factor of x pos variable

        Returns:
            _factor_of_x_pos (float):
            determines where the object
            will be on the screen horizontally
        """
        return self._factor_of_x_pos

    @factor_of_x_pos.setter
    def factor_of_x_pos(self, factor_of_x_pos: float) -> None:
        """Setter for the factor of x pos variable

        Args:
            factor_of_x_pos (float):
            determines where the object
            will be on the screen horizontally
        """
        self._factor_of_x_pos = factor_of_x_pos

    @property
    def factor_of_y_pos(self) -> float:
        """Getter for the factor of y pos variable

        Returns:
            _factor_of_y_pos (float):
            determines where the object
            will be on the screen vertically
        """
        return self._factor_of_y_pos

    @factor_of_y_pos.setter
    def factor_of_y_pos(self, factor_of_y_pos: float) -> None:
        """Setter for the factor of y pos variable

        Args:
            factor_of_y_pos (float):
            determines where the object
            will be on the screen vertically
        """
        self._factor_of_y_pos = factor_of_y_pos

    @property
    def y_pos(self) -> float:
        """Getter for the y (vertical) coordinate
            object will be drawn on

        Returns:
            y_pos (float): Result of multiplying the current
            screen height by idealized position on screen
        """
        return self._screen_height * self._factor_of_y_pos

    @property
    def rect(self) -> pygame.Rect | None:
        """Getter for pygame's rect variable
            for drawing an object

        Returns:
            _rect (pygame.Rect): The rect
            to be used to draw the object
        """
        return self._rect

    @rect.setter
    def rect(self, rect: pygame.Rect) -> None:
        """Setter for the rect variable

        Args:
            rect (pygame.Rect): the rect that will
            be used while drawing the object
        """
        self._rect = rect

    @property
    def surface(self) -> pygame.Surface | None:
        """Getter for the surface variable

        Returns:
            _surface (pygame.Surface)
            the surface that the
            image from the image_dir directory
            will be drawn on
        """
        return self._surface

    @surface.setter
    def surface(self, surface: pygame.Surface) -> None:
        """Setter for the surface variable

        Ars:
            surface (pygame.Surface)
            the surface that the
            image from the image_dir directory
            will be drawn on
        """
        self._surface = surface

    @property
    def image_dir(self) -> str:
        """Getter for the image_dir variable

        Returns:
            _image_dir (str): The string of the
            directory of the image to be used while
            drawing object
        """
        return self._image_dir

    @image_dir.setter
    def image_dir(self, image_dir: str) -> None:
        """Setter for the image_dir variable

        Args:
            image_dir (str): the directory of the
            image to be used to draw object
        """
        self._image_dir = image_dir

    @property
    def size(self) -> float:
        """Getter for the size variable

        Returns:
            _size (float)
            size to be used while drawing
            object
        """
        return self._size

    @size.setter
    def size(self, size: float) -> None:
        """Setter for the size variable

        Args:
            size (float)
            the new size to be used while drawing
            object
        """
        self._size = size

    @property
    def data(self) -> str:
        """Getter for the data variable

        Returns:
            _data (str)
            data needed for the specific object
        """
        return self._data

    @data.setter
    def data(self, data: str) -> None:
        """Setter for the data variable

        Args:
            data (str)
            the new size to be used while drawing
            object
        """
        self._data = data


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