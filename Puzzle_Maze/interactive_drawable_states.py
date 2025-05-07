"""
"""
from abc import ABC, abstractmethod
from enum import Enum
from text import Drawable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from interactive_drawables import InteractiveText, InteractiveDrawable, InteractiveButton


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

    def __init__(self, drawable: Drawable):
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
    def handle_event(self, outer_class: 'InteractiveDrawable', event: Events) -> None:
        """Sets state depending on given event

        Args:
            outer_class (Any): Class that will use state class
            event (Events): Event that will determine state
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

    def handle_event(self, outer_class: 'InteractiveText', event: Events) -> None:
        """Switches state depending on given event

        Args:
            outer_class (Any): Object to change state of
            event (Events): Event that determines state
        """
        if event == Events.HOVER:
            outer_class.text.color = outer_class.hover_color
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

    def handle_event(self, outer_class: 'InteractiveText', event: Events) -> None:
        """Switches state depending on given event

        Args:
            outer_class (Any): Object to change state of
            event (Events): Event that determines state
        """
        if event == Events.IDLE:
            outer_class.text.color = outer_class.color
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

    def handle_event(self, outer_class: 'InteractiveButton', event: Events) -> None:
        """Switches state depending on given event

        Args:
            outer_class (Any): Object to change state of
            event (Events): Event that determines state
        """
        if event == Events.HOVER:
            outer_class.button.drawable = outer_class.outline
            outer_class.text.color = outer_class.hover_color
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

    def handle_event(self, outer_class: 'InteractiveButton', event: Events) -> None:
        """Switches state depending on given event

        Args:
            outer_class (Any): Object to change state of
            event (Events): Event that determines state
        """
        if event == Events.IDLE:
            outer_class.button.drawable = outer_class.text
            outer_class.text.color = outer_class.color
            outer_class.state = IdleButton(outer_class.button)

