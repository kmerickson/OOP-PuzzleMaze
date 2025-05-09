"""
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from enum import Enum
from interactive_drawable_state import InteractiveDrawableState
from drawable import Drawable

if TYPE_CHECKING:
    from interactive_text import InteractiveText


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

    def handle_event(self, outer_class: 'InteractiveText', event: TextEvents) -> None:
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

    def handle_event(self, outer_class: 'InteractiveText', event: TextEvents) -> None:
        """Switches state depending on given event

        Args:
            outer_class (Any): Object to change state of
            event (Events): Event that determines state
        """
        if event == TextEvents.IDLE:
            outer_class.text.color = outer_class.color
            outer_class.state = IdleText(outer_class.text)
