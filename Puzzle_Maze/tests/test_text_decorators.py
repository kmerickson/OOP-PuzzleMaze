"""Testing with unittest for Outline and Button
    classes (Decorators of Text class)
"""

__author__ = "Jessica Story"
__date__ = "5/13/25"
__license__ = "MIT"

import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict
import pygame
from text import Text
from text_decorators import Outline, Button


class TestOutline(unittest.TestCase):
    """Test class for Outline class
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
        """Tests draw function

        Args:
            mock_font_obj (unittest.mock.MagicMock): Mocks
            font object to avoid issues with rendering
        """
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen

        text = Text(**self._text_parameters)
        outline = Outline(text, self._outline_color, self._outline_size)

        with patch.object(text.screen, 'blit') as mock_blit, \
                patch.object(text, 'draw') as mock_draw:
            outline.draw()

            mock_blit.assert_called_once_with(outline.surface, outline.rect)
            mock_draw.assert_called_once()

    @patch('pygame.font.Font')
    def test_dynamically_draw(self, mock_font_obj: unittest.mock.MagicMock) -> None:
        """Tests dynamically draw function

        Args:
            mock_font_obj (unittest.mock.MagicMock): Mocks
            font object to avoid issues with rendering
        """
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen

        text = Text(**self._text_parameters)
        outline = Outline(text, self._outline_color, self._outline_size)

        with patch.object(outline, '_adjust_to_changes') as mock_adjust_changes, \
            patch.object(text, '_adjust_to_changes') as mock_text_adjust_changes, \
                patch.object(outline, 'draw') as mock_draw:
            outline.dynamically_draw()

            mock_adjust_changes.assert_called_once()
            mock_text_adjust_changes.assert_called_once()
            mock_draw.assert_called_once()

    @patch('pygame.font.Font')
    def test_adjust_to_changes(self, mock_font_obj: unittest.mock.MagicMock) -> None:
        """Tests adjust to changes function

        Args:
            mock_font_obj (unittest.mock.MagicMock): Mocks
            font object to avoid issues with rendering
        """
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen

        text = Text(**self._text_parameters)
        outline = Outline(text, self._outline_color, self._outline_size)

        with patch.object(outline.drawable, 'resize_screen') as mock_resize_screen, \
            patch.object(outline.drawable, '_adjust_to_changes') as mock_text_adjust_changes, \
            patch('pygame.font.Font') as mock_font_class, \
                patch.object(mock_font_class.return_value, 'render') as mock_render:
            mock_render.return_value = MagicMock()

            outline._adjust_to_changes()

            mock_resize_screen.assert_called_once()
            mock_text_adjust_changes.assert_called_once()
            mock_font_class.assert_called_once_with(
                text.image_dir, int(
                    outline.original_size + self._outline_size))
            mock_render.assert_called_once_with(text.data, True, self._outline_color)


class TestButton(unittest.TestCase):
    def setUp(self) -> None:
        """Set up function
        """
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
        self._image_dir: str = "image_dir"

    @patch('pygame.image.load')
    @patch('pygame.font.Font')
    def test_draw(
        self, mock_font_obj: unittest.mock.MagicMock,
            mock_load: unittest.mock.MagicMock) -> None:
        """Tests draw function

        Args:
            mock_font_obj (unittest.mock.MagicMock): Mocks font
            object to avoid issues with rendering
            mock_load (unittest.mock.MagicMock): Mocks loading
            button image to avoid issues
        """
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen

        text = Text(**self._text_parameters)
        mock_surface = MagicMock(spec=pygame.Surface)
        mock_load.return_value = mock_surface
        button = Button(text, self._image_dir)

        with patch.object(text.screen, 'blit') as mock_blit, \
                patch.object(text, 'draw') as mock_draw:
            button.draw()
            mock_blit.assert_called_once_with(button.surface, button.rect)
            mock_draw.assert_called_once()

    @patch('pygame.image.load')
    @patch('pygame.font.Font')
    def test_dynamically_draw(
        self, mock_font_obj: unittest.mock.MagicMock,
            mock_load: unittest.mock.MagicMock) -> None:
        """Tests dynamically draw function

        Args:
            mock_font_obj (unittest.mock.MagicMock): Mocks font
            object to avoid issues with rendering
            mock_load (unittest.mock.MagicMock): Mocks loading
            button image to avoid issues
        """
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen

        text = Text(**self._text_parameters)
        mock_surface = MagicMock(spec=pygame.Surface)
        mock_load.return_value = mock_surface
        button = Button(text, self._image_dir)
        
        with patch.object(button, '_adjust_to_changes') as mock_adjust_changes, \
            patch.object(text, '_adjust_to_changes') as mock_text_adjust_changes, \
                patch.object(button, 'draw') as mock_draw:
            button.dynamically_draw()
            mock_adjust_changes.assert_called_once()
            mock_text_adjust_changes.assert_called_once()
            mock_draw.assert_called_once()
            self.assertEqual(text.size, button._button_height)

    @patch('pygame.transform.scale')
    @patch('pygame.image.load')
    @patch('pygame.font.Font')
    def test_adjust_to_changes(
        self, mock_font_obj: unittest.mock.MagicMock,
        mock_load: unittest.mock.MagicMock,
            mock_scale: unittest.mock.MagicMock) -> None:
        """Tests draw function

        Args:
            mock_font_obj (unittest.mock.MagicMock): Mocks font
            object to avoid issues with rendering
            mock_load (unittest.mock.MagicMock): Mocks loading
            button image to avoid issues
            mock_scale (mock_scale: unittest.mock.MagicMock) Mocks
            the scale of the button issue to avoid issues
        """
        mock_font = MagicMock()
        mock_font_obj.return_value = mock_font
        mock_font.render.return_value = self._mock_screen
        text = Text(**self._text_parameters)
        mock_surface = MagicMock(spec=pygame.Surface)
        mock_load.return_value = mock_surface
        button = Button(text, self._image_dir)

        with patch.object(button.drawable, 'resize_screen') as mock_resize_screen:
            button._adjust_to_changes()
            mock_resize_screen.assert_called()