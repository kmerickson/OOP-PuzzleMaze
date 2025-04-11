"""Module containing the button class
"""
import pygame, sys


class Button():
    """Class representing a button within the context of
    pygame use
    """
    NON_HOVER_TRANSPARENCY_VALUE = 128
    #the value alpha will be set to allow for change while hovering
    #over the button
    FACTOR_OF_X_POS = 0.5
    #the value to multiply screen width by to get
    #x pos of button

    def __init__(self, image_dir: str, x_pos: int, y_pos: int,
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
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._button: pygame.Surface = pygame.image.load(image_dir)
        self._x_pos: int = x_pos
        self._y_pos: int = y_pos
        
        given_color: pygame.Color = pygame.Color(color)
        self._color_with_hover: pygame.Color = given_color
        given_color.a = self.NON_HOVER_TRANSPARENCY_VALUE
        self._color_without_hover: pygame.Color = given_color
        
        self._text_to_place: str = text_to_place
        self._font_dir = font_dir
        self._font_obj: pygame.font.Font = pygame.font.Font(font_dir, self._button.get_size()[1])
        self._text: pygame.Surface = self._font_obj.render(self._text_to_place, True, self._color_without_hover)

        self._button_rect: pygame.Rect = self._button.get_rect(center=(self._x_pos, self._y_pos))
        self._text_rect: pygame.Rect = self._text.get_rect(center=(self._x_pos, self._y_pos))

        self._button_width: float = self._button.get_size()[0]
        self._button_height: float = self._button.get_size()[1]
        self._aspect_ratio: float = self._button_width / self._button_height
    
        screen.blit(self._button, self._button_rect)
        screen.blit(self._text, self._text_rect)

    def update(self, screen, screen_width, screen_height, factor_of_y_pos):
        change_in_screen_width: float = screen_width / self._screen_width
        change_in_screen_height: float = screen_height / self._screen_height

        new_width_of_button: float = \
            change_in_screen_width * self._button_width

        new_height_of_button: float = \
            change_in_screen_height * self._button_height

        self._screen_width = new_width_of_button
        self._screen_height = new_height_of_button

        self._button = pygame.transform.scale(
            self._button,
            (new_width_of_button, new_height_of_button))
        self._button_rect = self._button.get_rect(
            center=(
                    screen_width * self.FACTOR_OF_X_POS,
                    screen_height * factor_of_y_pos
                    )
        )

        self._font_obj: pygame.font.Font = pygame.font.Font(self._font_dir, self._button_height)
        self._text: pygame.Surface = self_font_obj.render(self._text_to_place, True, self._color_without_hover)
        self._text_rect: pygame.Rect = self._text.get_rect(
            center=(
                    screen_width // 2, 
                    factor_of_y_pos * screen_height
                    )
         )

        screen.blit(self._button, self._button_rect)
        screen.blit(self._text, self._text_rect)

    def checkForInput(self, position):
        if position[0] in range(self._button_rect.left, self._button_rect.right) and position[1] in range(self._button_rect.top, self._button_rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self._button_rect.left, self._button_rect.right) and position[1] in range(self._button_rect.top, self._button_rect.bottom):
            self._text = self._font_obj.render(self._text_to_place, True, self._color_with_hover)
        else:
            self._text = self._font_obj.render(self._text_to_place, True, self._color_without_hover)