import unittest
import pygame
from unittest import mock
from hypothesis import given, strategies as st

from GameObjects import (
    GameObject,
    Player,
    Enemy,
    Door,
    LockedDoorState,
    UnlockedDoorState,
    TILE_SIZE,
    PLAYER_MOVE_DELAY,
    ENEMY_MOVE_DELAY,
    TILE_EMPTY,
    TILE_WALL,
    TILE_GOAL,
    TILE_DOOR,
    TILE_KEY,
    TILE_UNLOCKED
)


class DummySurface(pygame.Surface):
    def __init__(self):
        # Minimal surface for testing
        super().__init__((1, 1))


class DummyScreen:
    def __init__(self):
        self.blit_calls = []

    def blit(self, image, topleft):
        self.blit_calls.append((image, topleft))


class Pressed:
    """Emulates pygame.key.get_pressed() for arbitrary key constants."""
    def __init__(self, key):
        self.key = key

    def __getitem__(self, idx):
        return idx == self.key


class TestGameObject(unittest.TestCase):
    @given(name=st.text(), x=st.integers(-100, 100), y=st.integers(-100, 100))
    def test_init_move_and_collision(self, name, x, y):
        img = DummySurface()
        go = GameObject(name, (x, y), img)
        self.assertEqual(go.name, name)
        self.assertIs(go.image, img)
        self.assertEqual(go.rect.topleft, (x, y))

        # move_to
        go.move_to(x + 5, y - 3)
        self.assertEqual(go.rect.topleft, (x + 5, y - 3))

        # draw
        screen = DummyScreen()
        go.draw(screen)
        self.assertEqual(len(screen.blit_calls), 1)
        self.assertIs(screen.blit_calls[0][0], img)

        # collision
        other = GameObject("other", (x + 5, y - 3), img)
        self.assertTrue(go.collides_with(other))
        other.move_to(x + 1000, y + 1000)
        self.assertFalse(go.collides_with(other))

    def test_update_noop_and_change_img(self):
        img1 = DummySurface()
        img2 = DummySurface()
        go = GameObject("go", (0, 0), img1)
        # update should do nothing
        go.update()
        # change_img
        go.change_img(img2)
        self.assertIs(go.image, img2)


class TestPlayer(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))
        self.surface = DummySurface()
        self.maze = [[TILE_EMPTY] * 5 for _ in range(5)]

    def tearDown(self):
        pygame.quit()

    @given(px=st.integers(0, 4), py=st.integers(0, 4))
    def test_constructor_and_draw(self, px, py):
        pos = (px * TILE_SIZE, py * TILE_SIZE)
        p = Player(pos, image=self.surface)
        self.assertEqual(p.name, "Player")
        self.assertEqual(p.rect.topleft, pos)
        self.assertEqual(p.key_count, 0)
        self.assertEqual(p.last_move_time, 0)

        screen = DummyScreen()
        p.draw(screen)
        self.assertEqual(len(screen.blit_calls), 1)

    def simulate(self, key, before, after, start, mod):
        p = Player(start, image=self.surface)
        p.last_move_time = before
        maze = [row.copy() for row in self.maze]
        for (r, c), v in mod.items():
            maze[r][c] = v
        with mock.patch('pygame.key.get_pressed', return_value=Pressed(key)), \
             mock.patch('pygame.time.get_ticks', return_value=after):
            p.update(maze, [])
        return p, maze

    def test_move_delay(self):
        p, _ = self.simulate(pygame.K_UP, 1000, 1000 + PLAYER_MOVE_DELAY - 1, (0, 0), {})
        self.assertEqual(p.rect.topleft, (0, 0))

    def test_move_empty(self):
        p, _ = self.simulate(pygame.K_RIGHT, 0, PLAYER_MOVE_DELAY + 1, (0, 0), {})
        self.assertEqual(p.rect.topleft, (TILE_SIZE, 0))

    def test_block_wall(self):
        p, _ = self.simulate(pygame.K_RIGHT, 0, PLAYER_MOVE_DELAY + 1, (0, 0), {(0, 1): TILE_WALL})
        self.assertEqual(p.rect.topleft, (0, 0))

    def test_block_locked_door(self):
        p, _ = self.simulate(pygame.K_RIGHT, 0, PLAYER_MOVE_DELAY + 1, (0, 0), {(0, 1): TILE_DOOR})
        self.assertEqual(p.rect.topleft, (0, 0))
        self.assertEqual(p.key_count, 0)

    def test_move_goal(self):
        p, _ = self.simulate(pygame.K_DOWN, 0, PLAYER_MOVE_DELAY + 1, (0, 0), {(1, 0): TILE_GOAL})
        self.assertEqual(p.rect.topleft, (0, TILE_SIZE))

    def test_move_unlocked(self):
        p, _ = self.simulate(pygame.K_RIGHT, 0, PLAYER_MOVE_DELAY + 1, (0, 0), {(0, 1): TILE_UNLOCKED})
        self.assertEqual(p.rect.topleft, (TILE_SIZE, 0))

    def test_pickup_and_open(self):
        p, _ = self.simulate(pygame.K_DOWN, 0, PLAYER_MOVE_DELAY + 1, (0, 0), {(1, 0): TILE_KEY})
        self.assertEqual(p.key_count, 1)
        door_maze = [[TILE_DOOR if (r, c) == (2, 0) else TILE_EMPTY for c in range(5)] for r in range(5)]
        p2 = Player((0, 3 * TILE_SIZE), image=self.surface)
        p2.key_count = 1
        door = Door((0, 2 * TILE_SIZE), LockedDoorState())
        with mock.patch('pygame.key.get_pressed', return_value=Pressed(pygame.K_UP)), \
             mock.patch('pygame.time.get_ticks', return_value=PLAYER_MOVE_DELAY + 1):
            p2.update(door_maze, [door])
        self.assertEqual(p2.key_count, 0)
        self.assertEqual(door_maze[2][0], TILE_UNLOCKED)


class TestDoorStates(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))
        self.maze = [[TILE_EMPTY] * 3 for _ in range(3)]

    def tearDown(self):
        pygame.quit()

    def test_passability(self):
        self.assertFalse(LockedDoorState().is_passable())
        self.assertTrue(UnlockedDoorState().is_passable())

    def test_locked_transition(self):
        p = Player((0, 0), image=DummySurface())
        p.key_count = 1
        d = Door((TILE_SIZE, TILE_SIZE), LockedDoorState())
        d.interact(p, self.maze)
        self.assertEqual(p.key_count, 0)
        self.assertEqual(self.maze[1][1], TILE_UNLOCKED)
        self.assertIsInstance(d._state, UnlockedDoorState)

    def test_unlocked_noop(self):
        p = Player((0, 0), image=DummySurface())
        d = Door((TILE_SIZE, TILE_SIZE), UnlockedDoorState())
        d.interact(p, self.maze)
        self.assertEqual(self.maze[1][1], TILE_EMPTY)

    def test_draw_and_update(self):
        screen = DummyScreen()
        d = Door((0, 0), LockedDoorState())
        d.draw(screen)
        self.assertEqual(len(screen.blit_calls), 1)
        d._state.update = mock.MagicMock()
        d.update()
        d._state.update.assert_called()


class TestEnemy(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))
        self.surface = DummySurface()
        self.maze = [[TILE_EMPTY] * 3 for _ in range(5)]

    def tearDown(self):
        pygame.quit()

    def test_move_success(self):
        e = Enemy((0, 0), image=self.surface, velocity=1)
        e.last_move_time = 0
        with mock.patch('pygame.time.get_ticks', return_value=ENEMY_MOVE_DELAY + 1):
            e.update(self.maze, GameObject("x", (100, 100), self.surface))
        self.assertEqual(e.rect.topleft, (0, TILE_SIZE))

    def test_reverse_out_of_bounds(self):
        e = Enemy((0, 4 * TILE_SIZE), image=self.surface, velocity=1)
        e.last_move_time = 0
        with mock.patch('pygame.time.get_ticks', return_value=ENEMY_MOVE_DELAY + 1):
            e.update(self.maze, GameObject("x", (100, 100), self.surface))
        self.assertEqual(e.velocity, -1)

    def test_reverse_on_wall(self):
        maze = [row.copy() for row in self.maze]
        maze[1][0] = TILE_WALL
        e = Enemy((0, 0), image=self.surface, velocity=1)
        e.last_move_time = 0
        with mock.patch('pygame.time.get_ticks', return_value=ENEMY_MOVE_DELAY + 1):
            e.update(maze, GameObject("x", (100, 100), self.surface))
        self.assertEqual(e.velocity, -1)

    def test_no_move_before_delay(self):
        e = Enemy((0, 0), image=self.surface, velocity=1)
        e.last_move_time = 1000
        with mock.patch('pygame.time.get_ticks', return_value=1000 + ENEMY_MOVE_DELAY - 1):
            e.update(self.maze, GameObject("x", (0, 0), self.surface))
        self.assertEqual(e.rect.topleft, (0, 0))

    def test_print_on_collision(self):
        # place enemy and player at same position to trigger collision
        pos = (0, 0)
        player = GameObject("p", pos, self.surface)
        e = Enemy(pos, image=self.surface, velocity=0)
        e.last_move_time = 0
        pygame.event.clear()
        with mock.patch('pygame.time.get_ticks', return_value=ENEMY_MOVE_DELAY + 1), \
             mock.patch('builtins.print') as mock_print:
            e.update([[TILE_EMPTY]], player)
        mock_print.assert_called_with("You Died!")

class TestDefaultImageLoading(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))

    def tearDown(self):
        pygame.quit()

    @mock.patch('pygame.image.load')
    def test_player_default_image_scaling(self, mock_load):
        # Ensure Player loads and scales its default image
        mock_surf = DummySurface()
        mock_load.return_value = mock_surf
        with mock.patch('pygame.transform.scale') as mock_scale:
            p = Player((0, 0))
        mock_load.assert_called_once_with("assets/player.png")
        self.assertTrue(mock_scale.called)
        # verify scale called with correct size
        posargs = mock_scale.call_args[0]
        self.assertEqual(posargs[1], (TILE_SIZE, TILE_SIZE))

    @mock.patch('pygame.image.load')
    def test_enemy_default_image_scaling(self, mock_load):
        # Ensure Enemy loads and scales its default image
        mock_surf = DummySurface()
        mock_load.return_value = mock_surf
        with mock.patch('pygame.transform.scale') as mock_scale:
            e = Enemy((0, 0))
        mock_load.assert_called_once_with("assets/enemy.png")
        self.assertTrue(mock_scale.called)
        posargs = mock_scale.call_args[0]
        self.assertEqual(posargs[1], (TILE_SIZE, TILE_SIZE))
