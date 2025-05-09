"""
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from enum import Enum
from interactive_drawable_state import InteractiveDrawableState
from drawable import Drawable

if TYPE_CHECKING:
    from interactive_button import InteractiveButton


class ButtonEvents(Enum):
    """Enum containing
        all the states UI
        elements can be in
    """
    IDLE = 0
    HOVER = 1


class IdleButton(InteractiveDrawableState):
    """Deals with buttons when they're in an idle state
    """

    def __init__(self, drawable: Drawable) -> None:
        """Constructor for IdleButton class

        Args:
            drawable (Drawable): The drawable
            object to use while drawing and event handling
        """
        super().__init__(drawable)

    def handle_event(self, outer_class: 'InteractiveButton', event: ButtonEvents) -> None:
        """Switches state depending on given event

        Args:
            outer_class (Any): Object to change state of
            event (Events): Event that determines state
        """
        if event == ButtonEvents.HOVER:
            outer_class.button.drawable = outer_class.outline
            outer_class.text.color = outer_class.hover_color
            outer_class.state = HoverButton(outer_class.button)


class HoverButton(InteractiveDrawableState):
    """Deals with buttons when they're in a hover state
    """

    def __init__(self, drawable: Drawable) -> None:
        """Constructor for HoverButton class

        Args:
            drawable (Drawable): The drawable
            object to use while drawing and event handling
        """
        super().__init__(drawable)

    def handle_event(self, outer_class: 'InteractiveButton', event: ButtonEvents) -> None:
        """Switches state depending on given event

        Args:
            outer_class (Any): Object to change state of
            event (Events): Event that determines state
        """
        if event == ButtonEvents.IDLE:
            outer_class.button.drawable = outer_class.text
            outer_class.text.color = outer_class.color
            outer_class.state = IdleButton(outer_class.button)
