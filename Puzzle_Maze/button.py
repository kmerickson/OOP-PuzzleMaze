"""Module containing the button class
"""
import pygame
import sys
from text import Text


class Button():
    """Class representing a button within the context of
    pygame use
    """
    NON_HOVER_TRANSPARENCY_VALUE: int = 128
    FACTOR_OF_X_POS: float = 0.5

    def draw_button(self):
        self._screen.blit(self._button, self._button_rect)

    def _set_up_button_shape_change(self):
        self._button = pygame.transform.scale(
            self._button,
            (self._button_width, self._button_height))
        self._button_rect = self._button.get_rect(
            center=(
                self._screen_width * self.FACTOR_OF_X_POS,
                self._screen_height * self._factor_of_y_pos
            )
        )

    def __init__(self, image_dir: str, factor_of_y_pos: float,
                 text_to_place: str, font_dir: str, color: str,
                 screen: pygame.Surface, screen_width: int,
                 screen_height: int):
        """_summary_

        Args:
            image_dir (str): Location of image to be used as
            button for button

            x_pos (int): x position of button
            y_pos (int): y position of button

            text_to_place (str): text that will be placed
            on top of button
            font_dir (str): Location of ttf file for font
            color (str): intended color for text on button

            screen (pygame.Surface): the surface that button
            will be placed on
            screen_width (int): the width of the surface
            button will be placed on
            screen_height (int): the height of the surface
            button will be placed on
        """
        self._screen = screen
        self._screen_width = screen_width
        self._screen_height = screen_height

        self._image_dir = image_dir
        self._button: pygame.Surface = pygame.image.load(image_dir)
        self._x_pos: float = self.FACTOR_OF_X_POS * self._screen_width
        self._factor_of_y_pos = factor_of_y_pos
        self._y_pos: int = self._factor_of_y_pos * self._screen_height
        self._button_rect: pygame.Rect = self._button.get_rect(
            center=(
                self._x_pos, self._y_pos))

        self._button_width: float = self._button.get_size()[0]
        self._button_height: float = self._button.get_size()[1]

        self._text_to_place: str = text_to_place
        self._font_dir = font_dir
        self._text = Text(
            "assets/Cyberpunks.ttf",
            self._screen,
            self._screen_width,
            self._screen_height,
            self.FACTOR_OF_X_POS,
            self._factor_of_y_pos,
            color,
            self._button_height,
            self._text_to_place,
            False,
            15,
            "Light Green",
            True)
        self._text_hover = Text(
            "assets/Cyberpunks.ttf",
            self._screen,
            self._screen_width,
            self._screen_height,
            self.FACTOR_OF_X_POS,
            self._factor_of_y_pos,
            "Light Green",
            self._button_height,
            self._text_to_place,
            True,
            15,
            "Light Green",
            True)
        self._text.draw_button()

        self._screen.blit(self._button, self._button_rect)
        self._text.draw_button()

    def update(self, screen_width, screen_height):
        change_in_screen_width: float = screen_width / self._screen_width
        change_in_screen_height: float = screen_height / self._screen_height

        self._button_width = change_in_screen_width * self._button_width
        self._button_height = change_in_screen_height * self._button_height

        self._screen_width = screen_width
        self._screen_height = screen_height

        self._set_up_button_shape_change()
        self._text.update_on_screen_resize(
            self._button_height,
            self._screen_width,
            self._screen_height)

    def user_clicked_button(self, mouse_position):
        if self._button_rect.collidepoint(mouse_position):
            return True
        return False

    def react_to_user_position(self, mouse_position):
        self.draw_button()
        if self._button_rect.collidepoint(mouse_position):
            self._text.draw_hover_state()
        if not self._button_rect.collidepoint(mouse_position):
            self._text.draw_button()
