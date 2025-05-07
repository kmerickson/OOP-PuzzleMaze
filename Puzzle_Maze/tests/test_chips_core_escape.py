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
from game_states import MainMenuState, PlayState, InfoState
from game_state import GameEvents

class TestChipsCoreEscape(unittest.TestCase):
    def tearDown(self) -> None:
        """Tear down method to avoid
            issues with singleton
            property
        """
        ChipsCoreEscape.reset_instance()
        return super().tearDown()

    def test_singleton(self) -> None:
        """Tests singleton property
        """
        _ = ChipsCoreEscape()
        with self.assertRaises(NameError):
            _ = ChipsCoreEscape()

    def test_get_instance(self) -> None:
        """Tests get_instance method
        """
        instance1 = ChipsCoreEscape()
        instance2 = ChipsCoreEscape.get_instance()
        self.assertIs(instance1, instance2)

    def test_set_instance(self) -> None:
        """Tests set_instance method
        """
        instance1 = ChipsCoreEscape()
        instance2 = ChipsCoreEscape.get_instance()
        self.assertIs(instance1, instance2)
        ChipsCoreEscape.reset_instance()
        self.assertIsNone(ChipsCoreEscape._instance)
    
    def test__set_screen_calls_pygame(self) -> None: 
        game: ChipsCoreEscape = ChipsCoreEscape()
        with patch("pygame.init") as mock_init:
            game._set_screen()
            mock_init.assert_called()
    
    def test__set_screen_correct_size(self) -> None: 
        game: ChipsCoreEscape = ChipsCoreEscape()
        game._set_screen()
        self.assertEqual((game.DEFAULT_WIDTH, game.DEFUALT_HEIGHT),
                         game.screen.get_size())

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


    def test_handle_event_wrong_pos(self) -> None: 
        game: ChipsCoreEscape = ChipsCoreEscape()
        with patch("pygame.mouse.get_pos", return_value=(0, 0)):
            game.state.handle_event(game, GameEvents.USER_CLICK)
            self.assertTrue(isinstance(game.state, MainMenuState))

    def test_handle_event_main_to_game(self) -> None:
        game: ChipsCoreEscape = ChipsCoreEscape()
        with patch("pygame.mouse.get_pos",
                   return_value=game.menu.play_button.button.rect.center):
            game.state.handle_event(game, GameEvents.USER_CLICK)
            self.assertTrue(isinstance(game.state, PlayState))

    def test_handle_event_main_to_info(self) -> None:
        game: ChipsCoreEscape = ChipsCoreEscape()
        with patch("pygame.mouse.get_pos",
                   return_value=game.menu.info_button.button.rect.center):
            game.state.handle_event(game, GameEvents.USER_CLICK)
            self.assertTrue(isinstance(game.state, InfoState))

    def test_handle_event_main_to_quit(self) -> None:
        game: ChipsCoreEscape = ChipsCoreEscape()
        with patch("pygame.mouse.get_pos",
                   return_value=game.menu.quit_button.button.rect.center):
            with patch("sys.exit") as mock_exit:
                game.state.handle_event(game, GameEvents.USER_CLICK)
                mock_exit.assert_called_once()

    def test_handle_event_play_to_main(self) -> None:
        game: ChipsCoreEscape = ChipsCoreEscape()
        game.state = PlayState()
        game.state.handle_event(game, GameEvents.ESCAPE)
        self.assertTrue(isinstance(game.state, MainMenuState))

    @patch('pygame.event.get')
    def test_chips_core_escape1(self, mock_event_queue) -> None:
        game: ChipsCoreEscape = ChipsCoreEscape()
        with patch.object(game.state, 'display_screen', autospec=True) as mock_display_screen:

            mock_event_queue.side_effect = [
                [],
                [pygame.event.Event(pygame.QUIT)]
            ]
            with self.assertRaises(SystemExit):
                game.chips_core_escape()
            mock_display_screen.assert_called()
    
    @patch('pygame.event.get')
    def test_chips_core_escape2(self, mock_event_queue) -> None:
        game: ChipsCoreEscape = ChipsCoreEscape()
        with patch.object(game.state, 'handle_event', autospec=True) as mock_handle_event:

            mock_event_queue.side_effect = [
                [pygame.event.Event(pygame.MOUSEBUTTONDOWN)],
                [pygame.event.Event(pygame.QUIT)]
            ]
            with self.assertRaises(SystemExit):
                game.chips_core_escape()
            mock_handle_event.assert_called()

    @patch('pygame.event.get')
    def test_chips_core_escape3(self, mock_event_queue) -> None:
        game: ChipsCoreEscape = ChipsCoreEscape()
        with patch.object(game.state, 'handle_event', autospec=True) as mock_handle_event:

            mock_event_queue.side_effect = [
                [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)],
                [pygame.event.Event(pygame.QUIT)]
            ]
            with self.assertRaises(SystemExit):
                game.chips_core_escape()
            mock_handle_event.assert_called()

    @patch.object(ChipsCoreEscape, 'chips_core_escape')
    def test_main(self, mock_chips_core_escape):
        ChipsCoreEscape.main()
        mock_chips_core_escape.assert_called_once()

    def test_new_game_instance(self):
        game: ChipsCoreEscape = ChipsCoreEscape()
        first_game_object: Game = game.play
        game.play = Game()
        self.assertIsNot(first_game_object, game.play)

