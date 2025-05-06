from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class GameEvents(Enum):
    """Enum containing
        all the states the
        game can be in
    """
    USER_CLICK = 0,
    ESCAPE = 1


class GameState(ABC):
    """Base state class
    """
    @abstractmethod
    def display_screen(self, outer_class: Any) -> None:
        """Method to display screen dependent on current state

        Args:
            outer_class (ChipsCoreEscape): the class that
            will contain states
        """
        pass

    @abstractmethod
    def handle_event(self, outer_class: Any,
                     event: GameEvents) -> None:
        """Method to that decides which events to deal with it and how
           to deal with them depending on current state

        Args:
            outer_class (ChipsCoreEscape): the class that
            will contain states
            event (GameEvents): the event to react to
        """
        pass
