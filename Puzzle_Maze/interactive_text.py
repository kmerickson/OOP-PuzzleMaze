"""
"""
import pygame
from typing_extensions import override
from interactive_drawable import InteractiveDrawable
from interactive_text_states import IdleText, TextEvents
from text import Text
from text_decorators import Outline


class InteractiveText(InteractiveDrawable):
    """Context class for state pattern
    """

    def __init__(
        self, screen: pygame.Surface, factor_of_x_pos: float,
        factor_of_y_pos: float, image_dir: str, size: float,
        text_to_draw: str, color: str, hover_color: str,
        outline_color: str, outline_size: float
    ) -> None:
        """Constructor for InteractiveText class

        Args:
            screen (pygame.Surface): Surface element will be drawn on
            factor_of_x_pos (float): X axis position of text
            factor_of_y_pos (float): Y axis position of text
            image_dir (str): Directory of font file
            size (float): Font size
            text_to_draw (str): The actual text to use
            color (str): Color of text
            color (str): Color of text when hovered over
            outline_color (str): Color of outline when users hover over text
            outline_size (str): Size of outline when users hover over text
        """
        super().__init__()
        self._text = Text(screen, factor_of_x_pos, factor_of_y_pos,
                          image_dir, size, text_to_draw, color)
        self._hover_color = hover_color
        self._color = color
        self._outline = Outline(self._text, outline_color, outline_size)
        self.state = IdleText(self._text)

    @property
    def text(self) -> Text:
        """Getter for text variable

        Returns:
            _text (Text): Text object that contains text in idle state
        """
        return self._text

    @property
    def outline(self) -> Outline:
        """Getter for outline variable

        Returns:
            _outline (Outline): Outline object that contains text in hover
            state
        """
        return self._outline

    @property
    def hover_color(self) -> str:
        """Getter for hover color variable

        Returns:
            _hover_color (str): Color text will be
            when hovered over
        """
        return self._hover_color

    @property
    def color(self) -> str:
        """Getter for color variable

        Returns:
            _color (str): Color of text in idle state
        """
        return self._color

    @override
    def draw(self) -> None:
        self.handle_mouse_position()
        super().draw()

    @override
    def handle_mouse_position(self) -> None:
        """Determines when text is in a hover and idle state
           based on user's mouse position in relation to
           instance variables
        """
        if self._text.rect is not None:
            mouse_pos = pygame.mouse.get_pos()
            if (self._text.rect.collidepoint(mouse_pos)):
                super().handle_event(TextEvents.HOVER)
            else:
                super().handle_event(TextEvents.IDLE)
