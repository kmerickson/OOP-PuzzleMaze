"""Testing with unittest for the Movie Title class
"""

__author__ = "Jessica Story"
__date__ = "4/1/25"
__license__ = "MIT"

import unittest
from game import TileSet, Game
from hypothesis import given
from hypothesis.strategies import text, floats
from GameObjects import Enemy, Player
import pygame
from unittest.mock import patch, MagicMock
from typing import List, Tuple
from io import StringIO
import pytest
import sys
from hypothesis import given
from hypothesis.strategies import integers
import os 

class TestGame(unittest.TestCase):
    """Unittesting Movie Title class
    """
    TILE_SIZE = 64
    LEVEL_1 = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 1],
                [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 4, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
    LEVEL_2 = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
                [1, 0, 1, 2, 0, 1, 0, 1, 0, 1, 1, 1],
                [1, 0, 1, 1, 3, 1, 0, 1, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
    LEVEL_3 = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                [1, 0, 3, 4, 0, 0, 0, 0, 1, 0, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 4, 1],
                [1, 3, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                [1, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]

    def setUp(self) -> None:
        """Setup method
        """
        pygame.init()
        self._game = Game()
        self._tile_class = TileSet()

    def test_load_levels_level1(self) -> None:
        returnValue = self._game.load_levels()
        self.assertEqual(returnValue[0], self.LEVEL_1)

    def test_load_levels_level2(self) -> None:
        returnValue = self._game.load_levels()
        self.assertEqual(returnValue[1], self.LEVEL_2)
    
    def test_load_levels_level3(self) -> None:
        returnValue = self._game.load_levels()
        self.assertEqual(returnValue[2], self.LEVEL_3)

    def test_load_level_index_0_level_loaded(self) -> None:
        self._game.load_level(0)
        self.assertEqual(self._game.maze, self.LEVEL_1)

    def test_load_level_index_1_level_loaded(self) -> None:
        self._game.load_level(1)
        self.assertEqual(self._game.maze, self.LEVEL_2)

    def test_load_level_index_2_level_loaded(self) -> None:
        self._game.load_level(2)
        self.assertEqual(self._game.maze, self.LEVEL_3)
    
    @patch('pygame.image.load')
    @patch("pygame.transform.scale")
    def test_load_level_index_1_enemies(self, mock_image, mock_transform) -> None:
        mock_surface = MagicMock(spec=pygame.Surface)
        mock_image.return_value = mock_surface
        mock_transform.return_value = mock_surface
        self._game.load_level(1)
        enemies: List[Enemy] = [
            Enemy((6 * self.TILE_SIZE, 3 * self.TILE_SIZE), velocity=-1),
            Enemy((1 * self.TILE_SIZE, 6 * self.TILE_SIZE), velocity=1)
        ]
    
        for enemy, expected_enemy in zip(self._game.enemies, enemies):
            self.assertEqual(enemy.velocity, expected_enemy.velocity)
            self.assertEqual(enemy.image, expected_enemy.image)

    @patch('pygame.image.load')
    @patch("pygame.transform.scale")
    def test_load_level_index_2_enemies(self, mock_image, mock_transform) -> None:
        mock_surface = pygame.Surface((10, 10))
        mock_image.return_value = mock_surface
        mock_transform.return_value = mock_surface
        self._game.load_level(2)
        enemies: List[Enemy] = [
                Enemy((1 * self.TILE_SIZE, 10 * self.TILE_SIZE), velocity=-1),
                Enemy((10 * self.TILE_SIZE, 1 * self.TILE_SIZE), velocity=1)
            ]
        for enemy, expected_enemy in zip(self._game.enemies, enemies):
            self.assertEqual(enemy.velocity, expected_enemy.velocity)
            self.assertEqual(enemy.image, expected_enemy.image)

    def test_load_level_player(self) -> None:
        self._game.load_level(0)
        expected_player_key_count = 0
        expected_player_last_move_time = 0

        self.assertEqual(self._game.player.key_count, expected_player_key_count)
        self.assertEqual(self._game.player.last_move_time, expected_player_last_move_time)

    def test_door_logic(self) -> None:
        test_maze = [[
            [1, 0, 1, 0], 
            [3, 3, 3, 1],
            ]]
        expected_size: int = 3
        self._game.levels = test_maze
        self._game.load_level(0)
        self.assertEqual(len(self._game.doors), expected_size)
        self.assertEqual(self._game.door_unlock_time, None)

    def test_draw(self):
        mock_screen = MagicMock(spec=pygame.Surface)
        self._game.screen = mock_screen
        self._game.load_levels()
        self._game.load_level(0)
        self._game.draw()
        tile_count: int = sum(len(row) for row in self._game.maze)
        enemy_count: int = len(self._game.enemies)
        door_count: int = len(self._game.doors)
        player_count: int = 1
        total_call_count: int = tile_count + enemy_count + door_count + player_count
        self.assertEqual(mock_screen.blit.call_count, total_call_count)

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_level_complete(self, mock_stdout):
        test_tile = [[2, 2], [2, 2]]
        self._game.maze = test_tile
        self._game.level_index = 0
        self._game.maze = test_tile
        self._game.player.rect.topleft = (0, 0)

        self._game.update()
        expected_output = "Level complete!"
        self.assertIn(expected_output, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_level_end_game(self, mock_stdout):
        test_tile = [[2, 2], [2, 2]]
        self._game.maze = test_tile
        self._game.level_index = 4
        self._game.maze = test_tile
        self._game.player.rect.topleft = (0, 0)

        self._game.update()
        expected_output = "You won all levels!"
        self.assertIn(expected_output, mock_stdout.getvalue())

    @patch('pygame.image.load')
    @patch("pygame.transform.scale")
    def test_update_game_unlocked_key(self, mock_image, mock_transform):
        mock_surface = MagicMock(spec=pygame.Surface)
        mock_image.return_value = mock_surface
        mock_transform.return_value = mock_surface
        mock_exit = MagicMock()
        sys.exit = mock_exit
        self._game = Game()
        test_tile = [[5, 5], [5, 5]]
        self._game.maze = test_tile
        self._game.level_index = 0
        self._game.door_unlock_time = -1000
        self._game.update()
        self.assertEqual(0, self._game.maze[0][0])

    def test_single_iteration(self):
        mock_game_update = MagicMock()
        mock_enemy_update = MagicMock()
        mock_player_update = MagicMock()
        mock_draw = MagicMock()

        self._game.update = mock_game_update
        self._game.player.update = mock_player_update
        self._game.enemies[0].update = mock_enemy_update
        self._game.draw = mock_draw
        self._game.maze = self.LEVEL_1
        self._game.single_iteration()

        mock_game_update.assert_called()
        mock_enemy_update.assert_called()
        mock_player_update.assert_called()
        mock_draw.assert_called()

    def test_get_tile_name0(self) -> None:
        tile = 0
        tile_name = "empty"
        self.assertEqual(self._tile_class.get_tile_name(tile), tile_name)
    
    def test_get_tile_name1(self) -> None:
        tile = 1
        tile_name = "wall"
        self.assertEqual(self._tile_class.get_tile_name(tile), tile_name)
    
    def test_get_tile_name2(self) -> None:
        tile = 2
        tile_name = "goal"
        self.assertEqual(self._tile_class.get_tile_name(tile), tile_name)

    def test_get_tile_name3(self) -> None:
        tile = 3
        tile_name = "door"
        self.assertEqual(self._tile_class.get_tile_name(tile), tile_name)
    
    def test_get_tile_name4(self) -> None:
        tile = 4
        tile_name = "key"
        self.assertEqual(self._tile_class.get_tile_name(tile), tile_name)

    def test_get_tile_name5(self) -> None:
        tile = 5
        tile_name = "door_unlocked"
        self.assertEqual(self._tile_class.get_tile_name(tile), tile_name)

    @given(integers(min_value=6))
    def test_get_tile_name_invalid(self, tile):
        with self.assertRaises(IndexError):
            self._tile_class.get_tile_name(tile)

    @patch('pygame.event.get')
    @patch('sys.exit', side_effect=SystemExit)
    def test_run_quit(self, mock_exit, mock_event_get):

        mock_event_get.return_value = [pygame.event.Event(pygame.QUIT)]

        with self.assertRaises(SystemExit):
            self._game.run()
        mock_exit.assert_called_once()

    @patch('pygame.event.get')
    @patch('sys.exit', side_effect=SystemExit)
    def test_run_functions(self, mock_exit, mock_event_queue):
        self._game.single_iteration = MagicMock()

        mock_event_queue.side_effect = [
            [],
            [pygame.event.Event(pygame.QUIT)]
        ]

        with self.assertRaises(SystemExit):
            self._game.run()

        self._game.single_iteration.assert_called_once()
        mock_exit.assert_called_once()

    @patch.object(Game, 'run')
    def test_game_loop(self, mock_run: MagicMock) -> None:
        Game.game_loop()
        mock_run.assert_called_once()

    @patch('os.path.exists', return_value=False)
    @patch('pygame.Surface')
    def test_fallback_when_file_missing(self, mock_surface_class, mock_exists):
        self._tile_class = TileSet()
        mock_surface = MagicMock()
        mock_surface_class.return_value = mock_surface
        self._tile_class._load_images()

        mock_exists.assert_called()
        mock_surface_class.assert_called()
        mock_surface.fill.assert_called()