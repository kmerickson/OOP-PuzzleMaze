"""Testing with unittest for game module
"""

__author__ = "Jessica Story"
__date__ = "5/2/25"
__license__ = "MIT"

from unittest.mock import patch, MagicMock
from typing import List, Tuple
import unittest
import sys
from io import StringIO
from hypothesis import given
from hypothesis.strategies import integers, sampled_from
from game import TileSet, Game
from GameObjects import Enemy
import pygame
from text import Drawable, Text

class TestDrawable(unittest.TestCase):
    def setUp(self) -> None:
        """Setup method
        """
        pygame.init()

    @patch.object(Drawable, '__abstractmethods__', set())
    def test_display_screen_base_class(self):
        class IncompleteDrawable(Drawable):
            pass
        state = IncompleteDrawable()
        with self.assertRaises(NotImplementedError):
            state.display_screen(None)

    @patch.object(Drawable, '__abstractmethods__', set())
    def test_handle_event_base_class(self):
        class IncompleteGameState(GameState):
            pass
        state = IncompleteGameState()
        with self.assertRaises(NotImplementedError):
            state.handle_event(None, None)