"""Testing with unittest for game module
"""

__author__ = "Jessica Story"
__date__ = "5/13/25"
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


class TestGame(unittest.TestCase):
    """Unittesting Game and Tileset class
    """
    TILE_SIZE: int = 64
    LEVEL_1: List[List[int]] = [
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
    LEVEL_2: List[List[int]] = [
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
    LEVEL_3: List[List[int]] = [
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
    LEVELS: List[List[List[int]]] = [LEVEL_1, LEVEL_2, LEVEL_3]

    def setUp(self) -> None:
        """Setup method
        """
        pygame.init()
        self._game: Game = Game()

    @given(integers(min_value=0, max_value=2))
    def test_load_levels(self, index: int) -> None:
        """Tests load levels funtion of Game class

        Args:
            index (int): Goes through all level indexes
        """
        returnValue: List[List[int]] = self._game.load_levels()
        self.assertEqual(returnValue[index], self.LEVELS[index])

    @given(integers(min_value=0, max_value=2))
    def test_load_level(self, index: int) -> None:
        """Tests load level funtion of Game class

        Args:
            index (int): Goes through all level indexes
        """
        self._game.load_level(index)
        self.assertEqual(self._game.maze, self.LEVELS[index])

    @patch('pygame.image.load')
    @patch("pygame.transform.scale")
    def test_load_level_index_1_enemies(
        self, mock_image: unittest.mock.Mock,
            mock_transform: unittest.mock.Mock) -> None:
        """Tests that the first level generates enemies
           correctly. Test load level of Game class

        Args:
            mock_image (unittest.mock.Mock): As Enemy constructor
            loads an image, it needs to be mockied
            mock_transform (unittest.mock.Mock): As Enemy constructor
            transform an image, it needs to be mockied
        """

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
    def test_load_level_index_2_enemies(
        self, mock_image: unittest.mock.Mock,
            mock_transform: unittest.mock.Mock) -> None:
        """Tests that the second level generates enemies
           correctly. Test load level of Game class

        Args:
            mock_image (unittest.mock.Mock): As Enemy constructor
            loads an image, it needs to be mockied
            mock_transform (unittest.mock.Mock): As Enemy constructor
            transform an image, it needs to be mockied
        """
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
        """Tests that the player is set correctly
           correctly. Test load level of Game class
        """
        self._game.load_level(0)
        expected_player_key_count: int = 0
        expected_player_last_move_time: int = 0

        self.assertEqual(self._game.player.key_count, expected_player_key_count)
        self.assertEqual(self._game.player.last_move_time, expected_player_last_move_time)

    def test_door_logic(self) -> None:
        """Tests that the doors are set correctly
           correctly. Test load level of Game class
        """
        test_maze: List[List[int]] = [[
            [1, 0, 1, 0],
            [3, 3, 3, 1],
        ]]

        expected_size: int = 3
        self._game.levels = test_maze
        self._game.load_level(0)
        self.assertEqual(len(self._game.doors), expected_size)
        self.assertEqual(self._game.door_unlock_time, None)

    def test_draw(self) -> None:
        """Tests draw function of Game class
        """
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
    def test_update_level_complete(self, mock_stdout: StringIO) -> None:
        """Test update function of Game class. Verifies
            winning condition when there's a level
            to advance to
        Args:
            mock_stdout (StringIO): Output displayed on console
        """
        test_tile = [[2, 2], [2, 2]]
        self._game.maze = test_tile
        self._game.level_index = 0
        self._game.maze = test_tile
        self._game.player.rect.topleft = (0, 0)

        self._game.update()
        expected_output = "Level complete!"
        self.assertIn(expected_output, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_level_end_game(self, mock_stdout: StringIO) -> None:
        """Test update function of Game class. Verifies
            winning condition when thereis not a level
            to advance to
        Args:
            mock_stdout (StringIO): Output displayed on console
        """
        test_tile: List[List[int]] = [[2, 2], [2, 2]]
        self._game.maze = test_tile
        self._game.level_index = 4
        self._game.maze = test_tile
        self._game.player.rect.topleft = (0, 0)

        self._game.update()
        expected_output = "You won all levels!"
        self.assertIn(expected_output, mock_stdout.getvalue())

    @patch('pygame.image.load')
    @patch("pygame.transform.scale")
    def test_update_game_unlocked_key(
        self, mock_image: unittest.mock.Mock,
            mock_transform: unittest.mock.Mock) -> None:
        """Test update function of Game class. Tests
           when player unlocks a door
        Args:
            mock_image (unittest.mock.Mock): To load
            images associated with doors and keys
            mock_transform (unittest.mock.Mock): To
            transform images associated with doors and keys
        """
        mock_surface = MagicMock(spec=pygame.Surface)
        mock_image.return_value = mock_surface
        mock_transform.return_value = mock_surface
        mock_exit = MagicMock()
        sys.exit = mock_exit

        self._game = Game()
        test_tile: List[List[int]] = [[5, 5], [5, 5]]
        self._game.maze = test_tile
        self._game.level_index = 0
        self._game.door_unlock_time = -1000
        self._game.update()
        self.assertEqual(0, self._game.maze[0][0])

    def test_single_iteration(self) -> None:
        """Test single iteration function of Game class
        """
        mock_game_update = MagicMock()
        mock_enemy_update = MagicMock()
        mock_player_update = MagicMock()
        mock_draw = MagicMock()

        with patch.object(self._game, 'update', mock_game_update), \
                patch.object(self._game.player, 'update', mock_player_update), \
                patch.object(self._game.enemies[0], 'update', mock_enemy_update), \
                patch.object(self._game, 'draw', mock_draw):
            self._game.maze = self.LEVEL_1
            self._game.single_iteration()
            mock_game_update.assert_called()
            mock_enemy_update.assert_called()
            mock_player_update.assert_called()
            mock_draw.assert_called()

    @patch('pygame.event.get')
    @patch('sys.exit', side_effect=SystemExit)
    def test_run_quit(
        self, mock_exit: unittest.mock.Mock,
            mock_event_get: unittest.mock.Mock) -> None:
        """Test quitting in run function of Game class
        """
        mock_event_get.return_value = [pygame.event.Event(pygame.QUIT)]

        with self.assertRaises(SystemExit):
            self._game.run()
        mock_exit.assert_called()

    @patch('pygame.event.get')
    @patch('sys.exit', side_effect=SystemExit)
    def test_run_functions(
        self, mock_exit: unittest.mock.Mock,
            mock_event_queue: unittest.mock.Mock) -> None:
        """Test calling of other functions in run function of Game class
        """
        with patch.object(self._game, 'single_iteration', autospec=True) as mock_single_iteration:

            mock_event_queue.side_effect = [
                [],
                [pygame.event.Event(pygame.QUIT)]
            ]

            with self.assertRaises(SystemExit):
                self._game.run()
            mock_single_iteration.assert_called_once()
            mock_exit.assert_called_once()

    @patch.object(Game, 'run')
    def test_game_loop(self, mock_run: MagicMock) -> None:
        """Test game_loop function of Game class
        """
        Game.game_loop()
        mock_run.assert_called_once()


class TestTileSet(unittest.TestCase):
    def setUp(self) -> None:
        """Setup method
        """
        pygame.init()
        self._game = Game()
        self._tile_class: TileSet = TileSet()

    @patch('os.path.exists', return_value=False)
    @patch('pygame.Surface')
    def test_fallback_when_file_missing(
        self, mock_surface_class: unittest.mock.Mock,
            mock_exists: unittest.mock.Mock) -> None:
        """Test load images and load or color function of Tileset class
        """
        self._tile_class = TileSet()
        mock_surface = MagicMock()
        mock_surface_class.return_value = mock_surface
        self._tile_class._load_images()

        mock_exists.assert_called()
        mock_surface_class.assert_called()
        mock_surface.fill.assert_called()

    @given(sampled_from(
        [(0, "empty"), (1, "wall"), (2, "goal"),
         (3, "door"), (4, "key"), (5, "door_unlocked")]))
    def test_get_tile_name(self, tile_data: Tuple[int, str]) -> None:
        """Test get tile name of Tileset class with valid inputs
        """
        tile_index: int = tile_data[0]
        tile_name: str = tile_data[1]
        self.assertEqual(self._tile_class.get_tile_name(tile_index), tile_name)

    @given(integers(min_value=6))
    def test_get_tile_name_invalid(self, tile: int) -> None:
        """Test get tile name of Tileset class with invalid inputs
        """
        with self.assertRaises(IndexError):
            self._tile_class.get_tile_name(tile)
