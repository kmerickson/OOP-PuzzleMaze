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


import unittest
from unittest.mock import MagicMock
import pygame
from text import Text


class TestTextClass(unittest.TestCase):
    def setUp(self):

        self.screen_mock = MagicMock(spec=pygame.Surface)
        self.screen_mock.blit = MagicMock()

        self.text = Text(
            screen=self.screen_mock,
            factor_of_x_pos=100.0,
            factor_of_y_pos=100.0,
            image_dir='path/to/font.ttf',
            size=30.0,
            text='Hello, World!',
            color='blue'
        )

    def test_draw_method(self):
        """Test if the draw method is called correctly"""
        # Call the draw method
        self.text.draw()

        # Verify if the `blit` method was called on the screen mock
        self.screen_mock.blit.assert_called_once()
