"""Module containing the base state for screens
"""

__author__ = "Jessica Story"
__date__ = "5/2/25"
__license__ = "MIT"
from abc import ABC, abstractmethod
from typing import Any


class ScreenState(ABC):
    """Base state class
    """
    @abstractmethod
    def display_screen(self, outer_class: Any) -> None:
        """Method to display screen dependent on current state

        Args:
            outer_class (ChipsCoreEscape): the class that
            will contain states
        """

    @abstractmethod
    def handle_event(self, outer_class: Any,
                     event: Any) -> None:
        """Method to that decides which events to deal with it and how
           to deal with them depending on current state

        Args:
            outer_class: the class that
            will contain states
            event (GameEvents): the event to react to
        """
