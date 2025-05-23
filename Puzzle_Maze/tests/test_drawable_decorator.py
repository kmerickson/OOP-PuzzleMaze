"""Tests for the Drawable Decorator class
"""

__author__ = "Jessica Story"
__date__ = "5/13/25"
__license__ = "MIT"

import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict
import pygame
from text import Text
from drawable_decorator import DrawableDecorator
from drawable_decorators import Outline
from hypothesis import given
from hypothesis.strategies import floats


class TestDrawableDecorator(unittest.TestCase):
    """Tests the Drawable Decorator class
    """

    def setUp(self) -> None:
        """Set up function
        """
        pygame.init()
        pygame.font.init()
        self._mock_screen = MagicMock()
        self._mock_screen.get_size.return_value = (1024, 768)
        self._text_parameters: Dict[str, Any] = {
            "screen": self._mock_screen,
            "factor_of_x_pos": 0.5,
            "factor_of_y_pos": 0.5,
            "image_dir": "image_dir",
            "size": 30,
            "text": "text",
            "color": "black"
        }
        self._outline_color: str = "black"
        self._outline_size: int = 2

    @patch('pygame.font.Font')
    def test_draw(self, mock_font_obj: unittest.mock.MagicMock) -> None:
        """Tests the draw function


        """
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen

        text = Text(**self._text_parameters)

        with patch.object(text, 'draw', wraps=text.draw) as mock_draw:
            decorator = DrawableDecorator(text)
            decorator.draw()
            mock_draw.assert_called()

    @patch('pygame.font.Font')
    def test_dynamically_draw(self, mock_font_obj: unittest.mock.MagicMock) -> None:
        """Tests the dynamically draw function
        """
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen

        text = Text(**self._text_parameters)

        with patch.object(text, 'dynamically_draw', wraps=text.draw) as mock_draw:
            decorator = DrawableDecorator(text)
            decorator.dynamically_draw()
            mock_draw.assert_called()

    @patch('pygame.font.Font')
    def test_adjust_to_changes(self, mock_font_obj: unittest.mock.MagicMock) -> None:
        """Tests the adjust to changes function
        """
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen

        text = Text(**self._text_parameters)

        with patch.object(text, '_adjust_to_changes', wraps=text.draw) as mock_draw:
            decorator = DrawableDecorator(text)
            decorator._adjust_to_changes()
            mock_draw.assert_called()

    @patch('pygame.font.Font')
    def test_drawable_setter_getter(self, mock_font_obj: unittest.mock.MagicMock) -> None:
        """Tests the setter and getter for drawable attribute
        """
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen

        text = Text(**self._text_parameters)
        decorator = DrawableDecorator(text)
        text2 = Text(**self._text_parameters)

        with patch.object(text2, 'resize_screen', wraps=text.draw) as mock_resize:
            decorator.drawable = text2
            self.assertIs(decorator.drawable, text2)
            mock_resize.assert_called()

    @patch('pygame.font.Font')
    def test_drawable_setter_getter2(self, mock_font_obj: unittest.mock.MagicMock) -> None:
        """Tests the setter and getter for drawable attribute
        """
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen

        text = Text(**self._text_parameters)
        decorator = DrawableDecorator(text)
        outline = Outline(text, self._outline_color, self._outline_size)
        decorator.drawable = outline

        self.assertIs(decorator.drawable, outline)

    @patch('pygame.font.Font')
    def test_original_size_getter(self, mock_font_obj: unittest.mock.MagicMock) -> None:
        """Tests the getter for original size attribute
        """
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen

        text = Text(**self._text_parameters)
        outline = Outline(text, self._outline_color, self._outline_size)
        decorator = DrawableDecorator(outline)

        self.assertEqual(decorator.original_size, text.size)

    @patch('pygame.font.Font')
    @given(floats(min_value=1, max_value=100))
    def test_original_size_setter(
        self, mock_font_obj: unittest.mock.MagicMock,
            new_size: int) -> None:
        """Tests the setter for original size attribute
        """
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen

        text = Text(**self._text_parameters)
        outline = Outline(text, self._outline_color, self._outline_size)
        decorator = DrawableDecorator(outline)
        decorator.original_size = new_size

        self.assertEqual(new_size, text.size)
