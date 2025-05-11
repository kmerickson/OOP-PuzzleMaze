"""Tests text and drawable
"""

import unittest
from unittest.mock import patch, MagicMock
import pygame
from text import Text
from typing import Any
from hypothesis import given
from hypothesis.strategies import integers, floats


class TestText(unittest.TestCase):
    def setUp(self) -> None:
        self._mock_screen = MagicMock()
        self._mock_screen.get_size.return_value = (1024, 768)
        self._text_parameters = {
            "screen": self._mock_screen,
            "factor_of_x_pos": 0.5,
            "factor_of_y_pos": 0.5,
            "image_dir": "image_dir",
            "size": 30,
            "text": "text",
            "color": "black"
    }
    
    @patch('pygame.font.Font')
    def test_draw(self, mock_font_obj) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen
        text = Text(**self._text_parameters)
        text.draw()

        self._mock_screen.blit.assert_called()

    @patch('pygame.font.Font')
    def test_resize_screen(self, mock_font_obj):
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen

        text = Text(**self._text_parameters)
        
        before_screen_width = text.screen_width
        before_screen_height = text.screen_height
        
        self._mock_screen.get_size.return_value = (800, 600)
        text.resize_screen()

        self.assertNotEqual(before_screen_width, text.screen_width)
        self.assertNotEqual(before_screen_height, text.screen_height)

    @patch('pygame.font.Font')
    def test_dynamically_draw(self, mock_font_obj) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen
        text = Text(**self._text_parameters)
        with patch.object(text, '_adjust_to_changes') as mock_adjust:
            text.dynamically_draw()
            mock_adjust.assert_called_once()
        self._mock_screen.blit.assert_called()

    @patch('pygame.font.Font')
    def test_adjust_to_changes_changed_screen(self, mock_font_obj) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen
        text = Text(**self._text_parameters)

        before_x_pos: float = text.x_pos
        before_y_pos: float = text.y_pos

        self._mock_screen.get_size.return_value = (800, 600)
        text._adjust_to_changes()

        self.assertNotEqual(before_x_pos, text.x_pos)
        self.assertNotEqual(before_y_pos, text.y_pos)

    @patch('pygame.font.Font')
    def test_adjust_to_changes_changed_size(self, mock_font_obj) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        text = Text(**self._text_parameters)
        new_font_size: float = 40
        text.size = new_font_size
        text._adjust_to_changes()
        self.assertTrue(text.font.size, new_font_size)

    @patch('pygame.font.Font')
    def test_adjust_to_changes_changed_color(self, mock_font_obj) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font

        text = Text(**self._text_parameters)
        new_color: str = "green"
        text.color = new_color
        text._adjust_to_changes()
        mock_font.render.assert_called_with(text.data, True, new_color)
    
    @patch('pygame.font.Font')
    def test_data_getter(self, mock_font_obj) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font

        text = Text(**self._text_parameters)
        self.assertEqual(text.data, self._text_parameters['text'])

    @patch('pygame.font.Font')
    def test_data_getter2(self, mock_font_obj) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font

        text = Text(**self._text_parameters)
        before_text: str = text.data
        new_text: str = "new_text"
        text.data = new_text
        self.assertNotEqual(text.data, before_text)

    @patch('pygame.font.Font')
    def test_data_getter3(self, mock_font_obj) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font

        text = Text(**self._text_parameters)
        new_text: str = "new_text"
        text.data = new_text
        text._adjust_to_changes()
        mock_font.render.assert_called_with(new_text, True, self._text_parameters['color'])

    @patch('pygame.font.Font')
    def test_data_color(self, mock_font_obj) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font

        text = Text(**self._text_parameters)
        self.assertEqual(text.color, self._text_parameters['color'])

    @patch('pygame.font.Font')
    def test_data_color2(self, mock_font_obj) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font

        text = Text(**self._text_parameters)
        before_color: str = text.color
        new_color: str = "green"
        text.color = new_color
        self.assertNotEqual(text.color, before_color)

    @patch('pygame.font.Font')
    def test_data_color3(self, mock_font_obj) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font

        text = Text(**self._text_parameters)
        new_color: str = "green"
        text.color = new_color
        text._adjust_to_changes()
        mock_font.render.assert_called_with(text.data, True, new_color)

    @patch('pygame.font.Font')
    def test_font_getter(self, MockFont) -> None:
        text = Text(**self._text_parameters)
        mock_font = MockFont()
        text.font = mock_font
        self.assertIs(text.font, mock_font)

    @patch('pygame.font.Font')
    @given(new_size=integers(min_value=1, max_value=100))
    def test_font_getter2(self, mock_font_obj, new_size) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font

        text = Text(**self._text_parameters)
        text.size = new_size
        text._adjust_to_changes()
        mock_font_obj.assert_called_with(text.image_dir, new_size)

    @patch('pygame.font.Font')
    @given(integers(min_value=1, max_value=100))
    def test_font_getter3(self, mock_font_obj, new_size) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font

        text = Text(**self._text_parameters)

        text.size = new_size
        new_image_dir = "new_font_path"
        text.image_dir = new_image_dir
        text._adjust_to_changes()
        mock_font_obj.assert_called_with(new_image_dir, new_size) 

    @patch('pygame.font.Font')
    def test_screen_getter_setter(self, mock_font_obj) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen
        text = Text(**self._text_parameters)
        self.assertIs(text.screen, self._mock_screen)

    @patch('pygame.font.Font')
    def test_factor_of_x_pos(self, mock_font_obj) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen
        text = Text(**self._text_parameters)
        self.assertEqual(text.factor_of_x_pos, self._text_parameters['factor_of_x_pos'])

    @patch('pygame.font.Font')
    @given(floats(min_value=0, max_value=1)) 
    def test_factor_of_x_pos2(self, mock_font_obj, new_factor) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font 

        text = Text(**self._text_parameters)

        text.factor_of_x_pos = new_factor
        self.assertEqual(text.factor_of_x_pos, new_factor)

    @patch('pygame.font.Font')
    def test_factor_of_y_pos(self, mock_font_obj) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen
        text = Text(**self._text_parameters)
        self.assertEqual(text.factor_of_y_pos, self._text_parameters['factor_of_y_pos'])

    @patch('pygame.font.Font')
    @given(floats(min_value=0, max_value=1)) 
    def test_factor_of_y_pos2(self, mock_font_obj, new_factor) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font 

        text = Text(**self._text_parameters)

        text.factor_of_y_pos = new_factor
        self.assertEqual(text.factor_of_y_pos, new_factor)

    @patch('pygame.font.Font')
    def test_image_dir(self, mock_font_obj) -> None:
        mock_font = MagicMock()
        mock_font.name = self._text_parameters['image_dir']
        mock_font_obj.return_value = mock_font
        text = Text(**self._text_parameters)
        new_file_dir: str = "new_direct"
        text.image_dir = new_file_dir
        mock_font.name = new_file_dir
        self.assertEqual(text.image_dir, new_file_dir)
        text._adjust_to_changes()
        self.assertEqual(text.font.name, new_file_dir)

    @patch('pygame.font.Font')
    def test_screen_setter(self, mock_font_obj) -> None:
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen
        text = Text(**self._text_parameters)
        new_mock_screen = MagicMock()
        text.screen = new_mock_screen
        self.assertIs(text.screen, new_mock_screen)