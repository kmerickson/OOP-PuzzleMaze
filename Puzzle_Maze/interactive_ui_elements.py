"""Module containing classes related
    to adding hover effects to buttons
    and texts. Uses the state design
    pattern
"""
from abc import ABC, abstractmethod
from typing import Any
from enum import Enum
from typing_extensions import override
import pygame
from ui_elements import Text, Outline, Button, Drawable


class Events(Enum):
    """Enum containing
        all the states UI
        elements can be in
    """
    IDLE = 0
    HOVER = 1


class State(ABC):
    """Base state class for state design pattern
    """

    def __init__(self, drawable: Drawable) -> None:
        """Constructor for State class

        Args:
            drawable (Drawable): UI element
            to use to draw and handle events with
        """
        self._drawable = drawable

    @property
    def drawable(self) -> Drawable:
        """Getter for drawable variable

        Returns:
            _drawable (Drawable): UI element
            to use to draw and handle events with
        """
        return self._drawable

    def draw(self) -> None:
        """Draws UI element
        """
        self._drawable.dynamically_draw()

    @abstractmethod
    def handle_event(self, outer_class: Any, event: Events) -> None:
        """Sets state depending on given event

        Args:
            outer_class (Any): Class that will use state class
            event (Events): Event that will determine state
        """
        pass


class InteractiveDrawable:
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
        if not isinstance(self._state, State):
            raise TypeError("State has not been initialized")
        self._state.draw()

    def handle_event(self, event: Events) -> None:
        """Change needed attributes depending
           on state

        Args:
            event (Events): Event that will determine state
        """
        if not isinstance(self._state, State):
            raise TypeError("State has not been initialized")
        self._state.handle_event(self, event)

    @abstractmethod
    def handle_mouse_position(self) -> None:
        """Method that will determine which state
           the UI element is current is in depending
           on user's mouse position
        """
        pass


class IdleText(State):
    """Deals with text when it's in an idle state
    """

    def __init__(self, drawable: Drawable) -> None:
        """Constructor for IdleText class

        Args:
            drawable (Drawable): The drawable
            object to use while drawing and event handling
        """
        super().__init__(drawable)

    def handle_event(self, outer_class: Any, event: Events) -> None:
        """Switches state depending on given event

        Args:
            outer_class (Any): Object to change state of
            event (Events): Event that determines state
        """
        if event == Events.HOVER:
            outer_class.state = HoverText(outer_class.outline)


class HoverText(State):
    """Deals with text when it's in a hover state
    """

    def __init__(self, drawable: Drawable) -> None:
        """Constructor for HoverText class

        Args:
            drawable (Drawable): The drawable
            object to use while drawing and event handling
        """
        super().__init__(drawable)

    def handle_event(self, outer_class: Any, event: Events) -> None:
        """Switches state depending on given event

        Args:
            outer_class (Any): Object to change state of
            event (Events): Event that determines state
        """
        if event == Events.IDLE:
            outer_class.state = IdleText(outer_class.text)


class IdleButton(State):
    """Deals with buttons when they're in an idle state
    """

    def __init__(self, drawable: Drawable) -> None:
        """Constructor for IdleButton class

        Args:
            drawable (Drawable): The drawable
            object to use while drawing and event handling
        """
        super().__init__(drawable)

    def handle_event(self, outer_class: Any, event: Events) -> None:
        """Switches state depending on given event

        Args:
            outer_class (Any): Object to change state of
            event (Events): Event that determines state
        """
        if event == Events.HOVER:
            outer_class.button.drawable = outer_class.outline
            outer_class.state = HoverButton(outer_class.button)


class HoverButton(State):
    """Deals with buttons when they're in a hover state
    """

    def __init__(self, drawable: Drawable) -> None:
        """Constructor for HoverButton class

        Args:
            drawable (Drawable): The drawable
            object to use while drawing and event handling
        """
        super().__init__(drawable)

    def handle_event(self, outer_class: Any, event: Events) -> None:
        """Switches state depending on given event

        Args:
            outer_class (Any): Object to change state of
            event (Events): Event that determines state
        """
        if event == Events.IDLE:
            outer_class.button.drawable = outer_class.text
            outer_class.state = IdleButton(outer_class.button)


class InteractiveText(InteractiveDrawable):
    """Context class for state pattern
    """

    def __init__(
        self, screen: pygame.Surface, factor_of_x_pos: float,
        factor_of_y_pos: float, image_dir: str, size: float,
        text_to_draw: str, color: str, outline_color: str, outline_size: float
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
            outline_color (str): Color of outline when users hover over text
            outline_size (float): Size of outline when users hover over text
        """
        super().__init__()
        self._text = Text(screen, factor_of_x_pos, factor_of_y_pos,
                          image_dir, size, text_to_draw, color)
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

    @override
    def handle_mouse_position(self) -> None:
        """Determines when text is in a hover and idle state
           based on user's mouse position in relation to
           instance variables
        """
        if not isinstance(self._text.rect, pygame.Rect):
            raise TypeError("Text not drawn. Collision point does not exist")
        mouse_pos = pygame.mouse.get_pos()
        if (self._text.rect.collidepoint(mouse_pos)):
            super().handle_event(Events.HOVER)
        else:
            super().handle_event(Events.IDLE)


class InteractiveButton(InteractiveDrawable):
    """Context class for state pattern
    """

    def __init__(self, screen: pygame.Surface, factor_of_x_pos: float,
                 factor_of_y_pos: float, image_dir: str, size: float,
                 text_to_place: str, color: str, outline_color: str,
                 outline_size: float, button_image_dir: str) -> None:
        """Constructor for InteractiveButton class

        Args:
            screen (pygame.Surface): Surface element will be drawn on
            factor_of_x_pos (float): X axis position of button
            factor_of_y_pos (float): Y axis position of button
            image_dir (str): Directory of font file
            size (float): Font size
            text_to_draw (str): The actual text to use
            color (str): Color of text
            outline_color (str): Color of outline when users hover over text
            outline_size (str): Size of outline when users hover over text
            button_image_dir (str): Directory of picture to use as button
        """
        super().__init__()
        self._text = Text(screen, factor_of_x_pos, factor_of_y_pos,
                          image_dir, size, text_to_place, color)
        self._outline = Outline(self._text, outline_color, outline_size)
        self._button = Button(self._text, button_image_dir)
        self.state = IdleButton(self._button)

    @property
    def text(self) -> Text:
        """Getter for text variable

        Returns:
            _text (Text): Text object that contains text on button
            in idle state
        """
        return self._text

    @property
    def outline(self) -> Outline:
        """Getter for outline variable

        Returns:
            _outline (Outline): Outline object that contains text on button
            in hover state
        """
        return self._outline

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
        if not isinstance(self._button.rect, pygame.Rect):
            raise TypeError("Button not drawn. Collision point does not exist")
        mouse_pos = pygame.mouse.get_pos()
        if (self._button.rect.collidepoint(mouse_pos)):
            super().handle_event(Events.HOVER)
        else:
            super().handle_event(Events.IDLE)


class GameText(InteractiveText):
    """Class to avoid large parameter lists while
       using text
    """

    def __init__(self, screen: pygame.Surface, text_to_place: str,
                 factor_of_x_pos: float, factor_of_y_pos: float,
                 size: float) -> None:
        """Constructor for GameText class

        Args:
            screen (pygame.Surface): Surface to draw on
            text_to_place (str): Text that will be drawn
            factor_of_x_pos (float): X-axis position of text
            factor_of_y_pos (_type_): Y-axis position of text
            size (float): Size of font
        """
        super().__init__(screen, factor_of_x_pos, factor_of_y_pos,
                         "assets/Cyberpunks.ttf", size, text_to_place,
                         "Light Green", "Black", 10)


class GameButton(InteractiveButton):
    """Class to avoid large parameter lists while
       using buttons
    """

    def __init__(self, screen: pygame.Surface, text_to_place: str,
                 factor_of_x_pos: float, factor_of_y_pos: float,
                 size: float) -> None:
        """Constructor for GameButton class

        Args:
            screen (pygame.Surface): Surface to draw on
            text_to_place (str): Text that will be drawn
            factor_of_x_pos (float): X-axis position of text
            factor_of_y_pos (_type_): Y-axis position of text
            size (float): Size of font
        """
        super().__init__(screen, factor_of_x_pos, factor_of_y_pos,
                         "assets/Cyberpunks.ttf", size, text_to_place,
                         "Light Green", "Black", 15, "assets/button.png")
