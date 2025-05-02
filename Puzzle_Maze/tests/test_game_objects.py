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
    TILE_SIZE,
    PLAYER_MOVE_DELAY,
    ENEMY_MOVE_DELAY,
    TILE_EMPTY,
    TILE_WALL,
    TILE_DOOR,
    TILE_KEY,
    TILE_UNLOCKED
)


class DummySurface(pygame.Surface):
    def __init__(self):
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

        go.move_to(x + 5, y - 3)
        self.assertEqual(go.rect.topleft, (x + 5, y - 3))

        screen = DummyScreen()
        go.draw(screen)
        self.assertEqual(len(screen.blit_calls), 1)
        self.assertIs(screen.blit_calls[0][0], img)
        self.assertEqual(screen.blit_calls[0][1], go.rect.topleft)

        other = GameObject("other", (x + 5, y - 3), img)
        self.assertTrue(go.collides_with(other))
        other.move_to(x + 1000, y + 1000)
        self.assertFalse(go.collides_with(other))


class TestPlayer(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))  # needed for convert_alpha()
        self.surface = DummySurface()
        self.maze = [[TILE_EMPTY] * 5 for _ in range(5)]

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
        self.assertIs(screen.blit_calls[0][0], p.image)
        self.assertEqual(screen.blit_calls[0][1], p.rect.topleft)

    def simulate_key_and_time(self, key, start_time, tick_time, start_pos, maze_mod):
        p = Player(start_pos, image=self.surface)
        p.last_move_time = start_time
        maze = [row.copy() for row in self.maze]
        for (r, c), val in maze_mod.items():
            maze[r][c] = val

        with mock.patch('pygame.key.get_pressed', return_value=Pressed(key)), \
                mock.patch('pygame.time.get_ticks', return_value=tick_time):
            p.update(maze, [])
        return p, maze

    def test_move_into_empty(self):
        p, _ = self.simulate_key_and_time(
            pygame.K_RIGHT,
            0,
            PLAYER_MOVE_DELAY + 1,
            (0, 0),
            {}
        )
        self.assertEqual(p.rect.topleft, (TILE_SIZE, 0))

    def test_pickup_key_and_door(self):
        # pickup key
        p, maze_after = self.simulate_key_and_time(
            pygame.K_DOWN,
            0,
            PLAYER_MOVE_DELAY + 1,
            (0, 0),
            {(1, 0): TILE_KEY}
        )
        self.assertEqual(p.key_count, 1)
        self.assertEqual(maze_after[1][0], TILE_EMPTY)

        # open door: start below door and press up
        maze_with_door = [
            [TILE_DOOR if (r, c) == (2, 0) else TILE_EMPTY for c in range(5)]
            for r in range(5)
        ]
        p2 = Player((0, 3 * TILE_SIZE), image=self.surface)
        door = Door((0, 2 * TILE_SIZE), LockedDoorState())
        p2.key_count = 1
        p2.last_move_time = 0
        with mock.patch('pygame.key.get_pressed', return_value=Pressed(pygame.K_UP)), \
                mock.patch('pygame.time.get_ticks', return_value=PLAYER_MOVE_DELAY + 1):
            p2.update(maze_with_door, [door])
        self.assertEqual(p2.key_count, 0)
        self.assertEqual(maze_with_door[2][0], TILE_UNLOCKED)

    def tearDown(self):
        pygame.quit()


class TestEnemy(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))
        self.surface = DummySurface()
        self.maze = [[TILE_EMPTY] * 3 for _ in range(5)]

    def tearDown(self):
        pygame.quit()

    def test_enemy_moves_and_reverses_on_wall(self):
        maze = [row.copy() for row in self.maze]
        maze[1][0] = TILE_WALL
        e = Enemy((0, 0), image=self.surface, velocity=1)
        e.last_move_time = 0
        with mock.patch('pygame.time.get_ticks', return_value=ENEMY_MOVE_DELAY + 1):
            e.update(maze, GameObject("x", (100, 100), self.surface))
        self.assertEqual(e.velocity, -1)
        self.assertEqual(e.rect.topleft, (0, 0))

    def test_collision_posts_escape_event(self):
        player = GameObject("p", (0, TILE_SIZE), self.surface)
        e = Enemy((0, 0), image=self.surface, velocity=1)
        e.last_move_time = 0
        pygame.event.clear()
        with mock.patch('pygame.time.get_ticks', return_value=ENEMY_MOVE_DELAY + 1):
            e.update(self.maze, player)
        events = pygame.event.get()
        self.assertTrue(
            any(evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE for evt in events)
        )
