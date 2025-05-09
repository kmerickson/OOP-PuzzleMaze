"""
"""
import pygame
from typing_extensions import override
from ui_elements.text_decorators import Button
from interactive_ui_elements.interactive_text import InteractiveText
from interactive_ui_elements.interactive_button_states import ButtonEvents, IdleButton


class InteractiveButton(InteractiveText):
    """Context class for state pattern
    """

    def __init__(self, screen: pygame.Surface, factor_of_x_pos: float,
                 factor_of_y_pos: float, image_dir: str, size: float,
                 text_to_place: str, color: str, hover_color: str,
                 outline_color: str, outline_size: float,
                 button_image_dir: str) -> None:
        """Constructor for InteractiveButton class

        Args:
            screen (pygame.Surface): Surface element will be drawn on
            factor_of_x_pos (float): X axis position of button
            factor_of_y_pos (float): Y axis position of button
            image_dir (str): Directory of font file
            size (float): Font size
            text_to_draw (str): The actual text to use
            color (str): Color of text
            hover_color (str): Color of hovered over text
            outline_color (str): Color of outline when users hover over text
            outline_size (str): Size of outline when users hover over text
            button_image_dir (str): Directory of picture to use as button
        """
        super().__init__(screen, factor_of_x_pos, factor_of_y_pos, image_dir, size,
                         text_to_place, color, hover_color, outline_color,
                         outline_size)
        self._button = Button(self._text, button_image_dir)
        self.state = IdleButton(self._button)

    @property
    def button(self) -> Button:
        """Getter for button variable

        Returns:
            _button (Button): button object to alter depending on current
            state
        """
        return self._button

    @override
    def handle_mouse_position(self) -> None:
        """Determines when text is in a hover and idle state
           based on user's mouse position in relation to
           instance variables
        """
        if self._button.rect is not None:
            mouse_pos = pygame.mouse.get_pos()
            if (self._button.rect.collidepoint(mouse_pos)):
                super().handle_event(ButtonEvents.HOVER)
            else:
                super().handle_event(ButtonEvents.IDLE)
