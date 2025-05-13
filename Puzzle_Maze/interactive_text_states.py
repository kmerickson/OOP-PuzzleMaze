"""Module containing the states for interactive text class
"""

__author__ = "Jessica Story"
__date__ = "5/13/25"
__license__ = "MIT"

from enum import Enum
from typing import Any
from interactive_drawable_state import InteractiveDrawableState
from drawable import Drawable


class TextEvents(Enum):
    """Enum containing
        all the states UI
        elements can be in
    """
    IDLE = 0
    HOVER = 1


class IdleText(InteractiveDrawableState):
    """Deals with text when it's in an idle state
    """

    def __init__(self, drawable: Drawable) -> None:
        """Constructor for IdleText class

        Args:
            drawable (Drawable): The drawable
            object to use while drawing and event handling
        """
        super().__init__(drawable)

    def handle_event(self, outer_class: Any, event: TextEvents) -> None:
        """Switches state depending on given event

        Args:
            outer_class (Any): Object to change state of
            event (Events): Event that determines state
        """
        if event == TextEvents.HOVER:
            outer_class.text.color = outer_class.hover_color
            outer_class.state = HoverText(outer_class.outline)


class HoverText(InteractiveDrawableState):
    """Deals with text when it's in a hover state
    """

    def __init__(self, drawable: Drawable) -> None:
        """Constructor for HoverText class

        Args:
            drawable (Drawable): The drawable
            object to use while drawing and event handling
        """
        super().__init__(drawable)

    def handle_event(self, outer_class: Any, event: TextEvents) -> None:
        """Switches state depending on given event

        Args:
            outer_class (Any): Object to change state of
            event (Events): Event that determines state
        """
        if event == TextEvents.IDLE:
            outer_class.text.color = outer_class.color
            outer_class.state = IdleText(outer_class.text)
