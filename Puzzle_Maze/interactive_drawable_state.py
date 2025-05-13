"""Module containing interactive drawable state class
"""

__author__ = "Jessica Story"
__date__ = "5/13/25"
__license__ = "MIT"
from typing import Any
from abc import ABC, abstractmethod
from drawable import Drawable


class InteractiveDrawableState(ABC):
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
    def handle_event(self, outer_class: Any, event: Any) -> None:
        """Sets state depending on given event

        Args:
            outer_class (Any): Class that will use state class
            event (Events): Event that will determine state
        """
