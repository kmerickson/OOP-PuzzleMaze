"""
"""
from abc import ABC, abstractmethod
from typing_extensions import override
from interactive_drawable_states import State, Events, IdleText, IdleButton
from text import Text
from text_decorators import Outline, Button
import pygame


class InteractiveDrawable(ABC):
    """Interface for classes that will employ
       the state pattern
    """

    def __init__(self) -> None:
        """Constructor for Interactive Drawable class
        """
        self._state: State | None = None

    @property
    def state(self) -> State | None:
        """Getter for state variable

        Returns:
            _state: The current state the
            class is in
        """
        return self._state

    @state.setter
    def state(self, state: State) -> None:
        """Setter for state variable

        Args:
            state (State): state to change to
        """
        self._state = state

    def draw(self) -> None:
        """Draws UI element based on current state
        """
        if self._state is not None:
            self._state.draw()

    def handle_event(self, event: Events) -> None:
        """Change needed attributes depending
           on state

        Args:
            event (Events): Event that will determine state
        """
        if self._state is not None:
            self._state.handle_event(self, event)

    @abstractmethod
    def handle_mouse_position(self) -> None:
        """Method that will determine which state
           the UI element is current is in depending
           on user's mouse position
        """
        pass


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
                super().handle_event(Events.HOVER)
            else:
                super().handle_event(Events.IDLE)


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
                super().handle_event(Events.HOVER)
            else:
                super().handle_event(Events.IDLE)


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
