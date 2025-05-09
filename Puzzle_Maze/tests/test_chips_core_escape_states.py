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
from chips_core_escape import ChipsCoreEscape
from chips_core_escape_states import PlayState, MainMenuState, InfoState, ChipsCoreEscapeEvents
from typing import Any
import pytest

class TestChipsCoreEscape(unittest.TestCase):
    def tearDown(self) -> None:
        """Tear down method to avoid
            issues with singleton
            property
        """
        ChipsCoreEscape.reset_instance()
        return super().tearDown()

    def test_handle_event_wrong_pos(self) -> None: 
        game: ChipsCoreEscape = ChipsCoreEscape()
        with patch("pygame.mouse.get_pos", return_value=(0, 0)):
            game.state.handle_event(game, ChipsCoreEscapeEvents.USER_CLICK)
            self.assertTrue(isinstance(game.state, MainMenuState))

    def test_handle_event_main_to_game(self) -> None:
        game: ChipsCoreEscape = ChipsCoreEscape()
        with patch("pygame.mouse.get_pos",
                   return_value=game.menu.play_button.button.rect.center):
            game.state.handle_event(game, ChipsCoreEscapeEvents.USER_CLICK)
            self.assertTrue(isinstance(game.state, PlayState))

    def test_handle_event_main_to_info(self) -> None:
        game: ChipsCoreEscape = ChipsCoreEscape()
        with patch("pygame.mouse.get_pos",
                   return_value=game.menu.info_button.button.rect.center):
            game.state.handle_event(game, ChipsCoreEscapeEvents.USER_CLICK)
            self.assertTrue(isinstance(game.state, InfoState))

    def test_handle_event_main_to_quit1(self) -> None:
        game: ChipsCoreEscape = ChipsCoreEscape()
        with patch("sys.exit") as mock_exit:
            game.state.handle_event(game, ChipsCoreEscapeEvents.ESCAPE)
            mock_exit.assert_called_once()

    def test_handle_event_main_to_quit2(self) -> None:
        game: ChipsCoreEscape = ChipsCoreEscape()
        with patch("pygame.mouse.get_pos",
                   return_value=game.menu.quit_button.button.rect.center):
            with patch("sys.exit") as mock_exit:
         
                game.state.handle_event(game, ChipsCoreEscapeEvents.USER_CLICK)
                mock_exit.assert_called_once()
                
    def test_handle_event_play_to_main(self) -> None:
        game: ChipsCoreEscape = ChipsCoreEscape()
        game.state = PlayState()
        game.state.handle_event(game, ChipsCoreEscapeEvents.ESCAPE)
        self.assertTrue(isinstance(game.state, MainMenuState))

    def test_handle_event_info_to_main1(self) -> None:
        game: ChipsCoreEscape = ChipsCoreEscape()
        game.state = InfoState()
        with patch("pygame.mouse.get_pos",
                   return_value=game.info.back_button.button.rect.center):
            game.state.handle_event(game, ChipsCoreEscapeEvents.USER_CLICK)
            self.assertTrue(isinstance(game.state, MainMenuState))

    def test_handle_event_info_to_main2(self) -> None:
        game: ChipsCoreEscape = ChipsCoreEscape()
        game.state = InfoState()
        game.state.handle_event(game, ChipsCoreEscapeEvents.ESCAPE)
        self.assertTrue(isinstance(game.state, MainMenuState))

    def test_display_screen_main_menu(self) -> None: 
        game: ChipsCoreEscape = ChipsCoreEscape()
        with patch.object(game.menu, "draw_screen") as mock_draw:
            game.state.display_screen(game)
            mock_draw.assert_called_once()

    def test_display_screen_game(self) -> None: 
        game: ChipsCoreEscape = ChipsCoreEscape()
        with patch.object(game.play, "single_iteration") as mock_draw:
            game.state = PlayState()
            game.state.display_screen(game)
            mock_draw.assert_called_once()
        
    def test_display_screen_info(self) -> None: 
        game: ChipsCoreEscape = ChipsCoreEscape()
        with patch.object(game.info, "draw_screen") as mock_draw:
            game.state = InfoState()
            game.state.display_screen(game)
            mock_draw.assert_called_once()