"""Tests for Chips Core Escape class
"""

__author__ = "Jessica Story"
__date__ = "5/13/25"
__license__ = "MIT"

from unittest.mock import patch
import unittest
import pygame
from chips_core_escape import ChipsCoreEscape
from game_states import MainMenuState, PlayState


class TestChipsCoreEscape(unittest.TestCase):
    """Tests class for ChipsCoreEscape class
    """
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
        """Tests set screen function
        """
        game: ChipsCoreEscape = ChipsCoreEscape()
        with patch("pygame.init") as mock_init:
            game._set_screen()
            mock_init.assert_called()
            self.assertTrue(isinstance(game.screen, pygame.Surface))

    @patch('pygame.event.get')
    def test_chips_core_escape1(self, mock_event_queue) -> None:
        """Tests quitting the chips core escape function
            by pressing X on screen
        """
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
        """Tests quitting the chips core escape function
            by pressing QUIT button
        """
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
        """Tests quitting the chips core escape function
            by pressing escape button
        """
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
        """Tests main function
        """
        ChipsCoreEscape.main()
        mock_chips_core_escape.assert_called_once()

    def test_new_game_instance(self):
        """Tests whether game can be restarted
        """
        game: ChipsCoreEscape = ChipsCoreEscape()
        first_game_object: Game = game.play
        game.play = Game()
        self.assertIsNot(first_game_object, game.play)

    def test_state_property(self):
        """Tests whether game starts out in main menu state
        """
        game: ChipsCoreEscape = ChipsCoreEscape()
        self.assertTrue(isinstance, (game.state, MainMenuState))

    def test_state_setter(self):
        """Tests that state can be set
        """
        game: ChipsCoreEscape = ChipsCoreEscape()
        game.state = PlayState()
        self.assertTrue(isinstance, (game.state, PlayState))

        
