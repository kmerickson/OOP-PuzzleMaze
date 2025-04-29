import unittest
from unittest import mock
from hypothesis import given, strategies as st
import pygame

from game_objects import (
    GameObject,
    Player,
    Enemy,
    TILE_SIZE,
    PLAYER_MOVE_DELAY,
    ENEMY_MOVE_DELAY,
    TILE_EMPTY,
    TILE_WALL,
    TILE_DOOR,
    TILE_KEY
)


class DummySurface(pygame.Surface):
    def __init__(self):
        super().__init__((1, 1))


class DummyScreen:
    def __init__(self):
        self.blit_calls = []

    def blit(self, image, topleft):
        self.blit_calls.append((image, topleft))


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
        other.move_to((x + 1000, y + 1000))
        self.assertFalse(go.collides_with(other))


class TestPlayer(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.surface = DummySurface()
        self.maze = [[TILE_EMPTY] * 5 for _ in range(5)]

    @given(px=st.integers(0, 4), py=st.integers(0, 4))
    def test_constructor_and_draw(self, px, py):
        p = Player((px * TILE_SIZE, py * TILE_SIZE), image=self.surface)
        self.assertEqual(p.name, "Player")
        self.assertEqual(
            p.rect.topleft,
            (px * TILE_SIZE, py * TILE_SIZE)
        )
        self.assertEqual(p.unlock_count, 0)
        self.assertEqual(p.last_move_time, 0)

        screen = DummyScreen()
        with mock.patch('builtins.print') as pr:
            p.draw(screen)
            pr.assert_called_with(
                f"[DEBUG] Drawing player at {p.rect.topleft}"
            )
        self.assertEqual(len(screen.blit_calls), 1)

    def simulate_key_and_time(self, key, ticks_before, ticks_after, start_pos, maze_mod):
        p = Player(start_pos, image=self.surface)
        p.last_move_time = ticks_before
        maze = [row[:] for row in self.maze]
        for (r, c), val in maze_mod.items():
            maze[r][c] = val

        with mock.patch('pygame.key.get_pressed',
                        return_value=[1 if i == key else 0 for i in range(323)]), \
                mock.patch('pygame.time.get_ticks', return_value=ticks_after):
            p.update(maze)
        return p, maze

    def test_move_delay_prevents_movement(self):
        p = Player((0, 0), image=self.surface)
        p.last_move_time = 1000
        with mock.patch('pygame.key.get_pressed',
                        return_value=[1 if i == pygame.K_UP else 0 for i in range(323)]), \
            mock.patch('pygame.time.get_ticks',
                       return_value=1000 + PLAYER_MOVE_DELAY - 1):
            p.update(self.maze)
        self.assertEqual(p.rect.topleft, (0, 0))

    def test_move_into_empty(self):
        start = (0, 0)
        ticks = 1000
        p, _ = self.simulate_key_and_time(
            pygame.K_RIGHT,
            ticks,
            ticks + PLAYER_MOVE_DELAY + 1,
            start,
            {}
        )
        self.assertEqual(p.rect.topleft, (TILE_SIZE, 0))

    def test_pickup_key_and_door(self):
        start = (0, 0)
        maze_mod = {(1, 0): TILE_KEY}
        p, maze_after_key = self.simulate_key_and_time(
            pygame.K_DOWN,
            0,
            PLAYER_MOVE_DELAY + 1,
            start,
            maze_mod
        )
        self.assertEqual(p.unlock_count, 1)
        self.assertEqual(maze_after_key[1][0], TILE_EMPTY)

        maze_mod = {(2, 0): TILE_DOOR}
        p2 = Player((0, TILE_SIZE), image=self.surface)
        p2.unlock_count = 1
        p2.last_move_time = 0
        with mock.patch('pygame.key.get_pressed',
                        return_value=[1 if i == pygame.K_DOWN else 0 for i in range(323)]), \
            mock.patch('pygame.time.get_ticks',
                       return_value=PLAYER_MOVE_DELAY + 1):
            p2.update([[TILE_EMPTY] * 5 for _ in range(5)])

    def tearDown(self):
        pygame.quit()


class TestEnemy(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.surface = DummySurface()
        self.maze = [[TILE_EMPTY] * 3 for _ in range(5)]

    def tearDown(self):
        pygame.quit()

    def test_enemy_moves_and_reverses_on_wall(self):
        maze = [row[:] for row in self.maze]
        maze[1][0] = TILE_WALL
        e = Enemy((0, 0), image=self.surface, velocity=1)
        e.last_move_time = 0
        with mock.patch('pygame.time.get_ticks',
                        return_value=ENEMY_MOVE_DELAY + 1):
            e.update(maze, player=GameObject("x", (100, 100), self.surface))
        self.assertEqual(e.velocity, -1)
        self.assertEqual(e.rect.topleft, (0, 0))

        maze[1][0] = TILE_EMPTY
        e2 = Enemy((0, 0), image=self.surface, velocity=1)
        e2.last_move_time = 0
        with mock.patch('pygame.time.get_ticks',
                        return_value=ENEMY_MOVE_DELAY + 1):
            e2.update(maze, player=GameObject("x", (100, 100), self.surface))
        self.assertEqual(e2.rect.topleft, (0, TILE_SIZE))

    def test_collision_posts_escape_event(self):
        player = GameObject("p", (0, TILE_SIZE), self.surface)
        e = Enemy((0, 0), image=self.surface, velocity=1)
        e.last_move_time = 0
        pygame.event.clear()
        maze = [row[:] for row in self.maze]
        with mock.patch('pygame.time.get_ticks', return_value=ENEMY_MOVE_DELAY + 1):
            e.update(maze, player)
        events = pygame.event.get()
        escaped = any(
            evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE
            for evt in events
        )
        self.assertTrue(escaped)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
