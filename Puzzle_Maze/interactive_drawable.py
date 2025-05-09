"""
"""
from abc import ABC, abstractmethod
from typing import Any
from interactive_drawable_state import InteractiveDrawableState


class InteractiveDrawable(ABC):
    """Interface for classes that will employ
       the state pattern
    """

    def __init__(self) -> None:
        """Constructor for Interactive Drawable class
        """
        self._state: InteractiveDrawableState | None = None

    @property
    def state(self) -> InteractiveDrawableState | None:
        """Getter for state variable

        Returns:
            _state: The current state the
            class is in
        """
        return self._state

    @state.setter
    def state(self, state: InteractiveDrawableState) -> None:
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

    def handle_event(self, event: Any) -> None:
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
