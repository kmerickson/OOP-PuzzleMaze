"""Tests for classes of game screens module
    Tests MainMenu and InfoScreen classes
"""

__author__ = "Jessica Story"
__date__ = "5/13/25"
__license__ = "MIT"

import unittest
from unittest.mock import patch, MagicMock
from typing import Tuple
import pygame
from game_screens import MainMenu, InfoScreen


class TestMainMenu(unittest.TestCase):
    """Tests MainMenu class
    """

    def setUp(self) -> None:
        """Set up function
        """
        pygame.init()
        pygame.font.init()
        self._valid_screen_size1: Tuple[int, int] = (1024, 768)
        self._valid_screen_size2: Tuple[int, int] = (800, 600)
        self._mock_screen = MagicMock()
        self._mock_screen.get_size.return_value = self._valid_screen_size1

    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    @patch.object(MainMenu, 'resize_screen_variables')
    def test_adjust_to_screen(
        self, mock_resize: unittest.mock.MagicMock,
            mock_scale: unittest.mock.MagicMock,
            mock_load: unittest.mock.MagicMock) -> None:
        """Tests the adjust to screen function

            Args:
            mock_resize (unittest.mock.MagicMock):
            mocks function
            mocks_scale: (unittest.mock.MagicMock):
            mocks pygame resizing an image
            mocks_load: (unittest.mock.MagicMock):
            mocks loading an image
        """
        menu = MainMenu(self._mock_screen)
        self._mock_screen.get_size.return_value = self._valid_screen_size2
        menu.adjust_to_screen()
        mock_resize.assert_called_once()
        mock_scale.assert_called()

    @patch('pygame.image.load')
    def test_background_picture_getter(
            self, mock_load: unittest.mock.MagicMock) -> None:
        """Mocks background picture getter

            Args:
            mocks_load: (unittest.mock.MagicMock):
            mocks loading an image
        """
        mock_background_surface = pygame.Surface(self._valid_screen_size2)
        mock_load.return_value = mock_background_surface

        screen = pygame.Surface(self._valid_screen_size2)
        menu = MainMenu(screen)

        mock_load.assert_any_call(menu.BACKGROUND_PICTURE_DIRECTORY)
        result: pygame.Surface = menu.background_picture

        self.assertIs(result, menu.background_picture)
        self.assertIs(result, mock_background_surface)

    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def test_scaled_picture_getter_and_image_path(
        self, mock_scale: unittest.mock.MagicMock,
            mock_load: unittest.mock.MagicMock) -> None:
        """Tests the scaled picture getter

            Args:
            mocks_scale: (unittest.mock.MagicMock):
            mocks pygame resizing an image
            mocks_load: (unittest.mock.MagicMock):
            mocks loading an image
        """
        mock_background_surface = MagicMock(spec=pygame.Surface)
        mock_load.return_value = mock_background_surface
        mock_scaled_surface = MagicMock(spec=pygame.Surface)
        mock_scale.return_value = mock_scaled_surface

        menu = MainMenu(self._mock_screen)

        mock_load.assert_any_call(menu.BACKGROUND_PICTURE_DIRECTORY)
        mock_scale.assert_any_call(mock_background_surface,
                                   (menu.screen_width, menu.screen_height))

        result: pygame.Surface = menu.scaled_picture

        self.assertIs(result, menu.scaled_picture)
        self.assertIs(result, mock_scaled_surface)

    @patch('pygame.image.load')
    @patch('pygame.transform.scale')
    def test_draw_screen(
        self, mock_scale: unittest.mock.MagicMock,
            mock_load: unittest.mock.MagicMock) -> None:
        """Tests the draw screen function

            Args:
            mocks_scale: (unittest.mock.MagicMock):
            mocks pygame resizing an image
            mocks_load: (unittest.mock.MagicMock):
            mocks loading an image
        """
        mock_screen = MagicMock()
        mock_screen.blit = MagicMock()
        mock_screen.get_size.return_value = self._valid_screen_size2

        mock_background_surface = MagicMock()
        mock_load.return_value = mock_background_surface

        mock_scaled_surface = MagicMock()
        mock_scale.return_value = mock_scaled_surface

        menu_screen = MainMenu(mock_screen)

        menu_screen.main_text.draw = MagicMock()
        menu_screen.play_button.draw = MagicMock()
        menu_screen.info_button.draw = MagicMock()
        menu_screen.quit_button.draw = MagicMock()

        menu_screen.draw_screen()

        mock_screen.blit.assert_called_once_with(mock_scaled_surface, (0, 0))

        menu_screen.main_text.draw.assert_called_once()
        menu_screen.play_button.draw.assert_called_once()
        menu_screen.info_button.draw.assert_called_once()
        menu_screen.quit_button.draw.assert_called_once()

    def test_main_text(self) -> None:
        """Tests main text getter
        """
        menu = MainMenu(self._mock_screen)
        text: str = menu.main_text.text.data
        self.assertIn("Chip's Core Escape", text)

    def test_play_button(self) -> None:
        """Tests play button getter
        """
        menu = MainMenu(self._mock_screen)
        text: str = menu.play_button.button.data
        self.assertIn("Play", text)

    def test_info_button(self) -> None:
        """Tests info button getter
        """
        menu = MainMenu(self._mock_screen)
        text: str = menu.info_button.button.data
        self.assertIn("Info", text)

    def test_quit_button(self) -> None:
        """Tests quit button getter
        """
        menu = MainMenu(self._mock_screen)
        text: str = menu.quit_button.button.data
        self.assertIn("Quit", text)


class TestInfoScreen(unittest.TestCase):
    """Tests class for the Info Screen class
    """

    def setUp(self) -> None:
        """Set up function
        """
        pygame.init()
        pygame.font.init()
        self._valid_screen_size: Tuple[int, int] = (800, 600)
        self._mock_screen = MagicMock()
        self._mock_screen.get_size.return_value = self._valid_screen_size
        self._main_text: str = "Chip's Core Escape"
        self._body1: str = " is a basic puzzle maze game."
        self._body2: str = "It features the player going through a maze"
        self._body3: str = "having to avoid enemies while needing items"
        self._body4: str = "to advance. It was developed as our final project."
        self._button: str = "Back"

    def test_draw_screen(self) -> None:
        """Tests draw screen function
        """
        mock_screen = MagicMock()
        mock_screen.fill = MagicMock()
        mock_screen.blit = MagicMock()
        mock_screen.get_size.return_value = self._valid_screen_size

        info_screen = InfoScreen(mock_screen)

        info_screen.main_text.draw = MagicMock()
        info_screen.body_text_line1.draw = MagicMock()
        info_screen.body_text_line_2.draw = MagicMock()
        info_screen.body_text_line_3.draw = MagicMock()
        info_screen.body_text_line_4.draw = MagicMock()
        info_screen.back_button.draw = MagicMock()

        info_screen.draw_screen()

        mock_screen.fill.assert_called_once_with(info_screen.BACKGROUND_COLOR)

        info_screen.main_text.draw.assert_called_once()
        info_screen.body_text_line1.draw.assert_called_once()
        info_screen.body_text_line_2.draw.assert_called_once()
        info_screen.body_text_line_3.draw.assert_called_once()
        info_screen.body_text_line_4.draw.assert_called_once()
        info_screen.back_button.draw.assert_called_once()

    @patch('pygame.image.load')
    @patch.object(InfoScreen, 'resize_screen_variables')
    def test_adjust_to_screen(
        self, mock_resize: unittest.mock.MagicMock,
            mock_load: unittest.mock.MagicMock) -> None:
        """Tests the adjust to screen function

            Args:
            mocks_resize: (unittest.mock.MagicMock):
            mocks function
            mocks_load: (unittest.mock.MagicMock):
            mocks loading an image
        """
        menu = InfoScreen(self._mock_screen)

        self._mock_screen.get_size.return_value = self._valid_screen_size
        menu.adjust_to_screen()
        mock_resize.assert_called_once()

    def test_main_text(self) -> None:
        """Tests main text getter
        """
        menu = InfoScreen(self._mock_screen)
        text: str = menu.main_text.text.data
        self.assertIn("Chip's Core Escape", text)

    def test_body1(self) -> None:
        """Tests line1 getter
        """
        menu = InfoScreen(self._mock_screen)
        text: str = menu.body_text_line1.text.data
        self.assertIn(self._body1, text)

    def test_body2(self) -> None:
        """Tests line2 getter
        """
        menu = InfoScreen(self._mock_screen)
        text: str = menu.body_text_line_2.text.data
        self.assertIn(self._body2, text)

    def test_body3(self) -> None:
        """Tests line3 getter
        """
        menu = InfoScreen(self._mock_screen)
        text: str = menu.body_text_line_3.text.data
        self.assertIn(self._body3, text)

    def test_body4(self) -> None:
        """Tests line4 getter
        """
        menu = InfoScreen(self._mock_screen)
        text: str = menu.body_text_line_4.text.data
        self.assertIn(self._body4, text)

    def test_quit_button(self) -> None:
        """Tests line5 getter
        """
        menu = InfoScreen(self._mock_screen)
        text: str = menu.back_button.button.data
        self.assertIn(self._button, text)
