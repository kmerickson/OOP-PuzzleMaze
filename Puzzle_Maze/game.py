from typing import List, Dict, Tuple
import pygame
import sys
import os
from pygame.locals import QUIT
from GameObjects import Player, Enemy, Door, TILE_SIZE, LockedDoorState
from GameObjects import TILE_EMPTY, TILE_WALL, TILE_GOAL, TILE_KEY
# Constants
GRID_WIDTH: int = 12
GRID_HEIGHT: int = 12
WIDTH: int = TILE_SIZE * GRID_WIDTH
HEIGHT: int = TILE_SIZE * GRID_HEIGHT
FPS: int = 60
ASSET_DIR: str = "assets"

# Tile management


class TileSet:
    def __init__(self) -> None:
        self.tiles: List[str] = ['empty', 'wall', 'goal', 'door', 'key', 'door_unlocked']
        self.images: Dict[str, pygame.Surface] = self._load_images()

    def _load_images(self) -> Dict[str, pygame.Surface]:
        images: Dict[str, pygame.Surface] = {}

        def load_or_color(name: str, fallback_color: Tuple[int, int, int]) -> pygame.Surface:
            path: str = os.path.join(ASSET_DIR, f"{name}.png")
            if os.path.exists(path):
                img: pygame.Surface = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                if name in {"key", "goal", "door", "door_unlocked"}:
                    base: pygame.Surface = images["empty"].copy()
                    base.blit(img, (0, 0))
                    return base
                return img
            surf: pygame.Surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
            surf.fill(fallback_color)
            return surf

        images["empty"] = load_or_color("empty", (50, 50, 50))
        images["wall"] = load_or_color("wall", (100, 100, 100))
        images["goal"] = load_or_color("goal", (0, 255, 0))
        images["door"] = load_or_color("door", (150, 75, 0))
        images["key"] = load_or_color("key", (255, 215, 0))
        images["player"] = load_or_color("player", (0, 0, 255))
        images["enemy"] = load_or_color("enemy", (255, 0, 0))
        images["door_unlocked"] = load_or_color("door_unlocked", (0, 200, 255))

        return images

    def get_image(self, tile_index: int) -> pygame.Surface:
        return self.images[self.tiles[tile_index]]

    def get_tile_name(self, tile_index: int) -> str:
        return self.tiles[tile_index]


# Game logic


class Game:
    def __init__(self) -> None:
        self.screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tile Puzzle")
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.tileset: TileSet = TileSet()
        self.levels: List[List[List[int]]] = self.load_levels()
        self.level_index: int = 0

        ###############################
        # added to hold a list of doors
        self.doors: List[Door] = []
        # if an object class is created for keys and goals as well, could
        # create an object array in the same way and simplify updates
        ###############################
        self.door_unlock_time: int | None = None
        self.load_level(self.level_index)

    def load_levels(self) -> List[List[List[int]]]:
        return [
            [
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
            ],
            [
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
            ],
            [
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
        ]

    def load_level(self, index: int) -> None:
        self.maze: List[List[int]] = self.levels[index]
        ###############################
        self.doors = []  # reset list of doors for the level
        self.player: Player = Player((1 * TILE_SIZE, 1 * TILE_SIZE))

        if index == 2:
            self.enemies = [
                Enemy((1 * TILE_SIZE, 10 * TILE_SIZE), velocity=-1),
                Enemy((10 * TILE_SIZE, 1 * TILE_SIZE), velocity=1)
            ]
        else:
            self.enemies = [
                Enemy((6 * TILE_SIZE, 3 * TILE_SIZE), velocity=-1),
                Enemy((1 * TILE_SIZE, 6 * TILE_SIZE), velocity=1)
            ]

        ###############################
        # initialize the position of all the doors on the level:
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                if self.maze[row][col] == 3:
                    door_pos: Tuple[int, int] = (col * TILE_SIZE, row * TILE_SIZE)
                    door: Door = Door(door_pos, LockedDoorState())
                    self.doors.append(door)

        self.door_unlock_time = None

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))
        for row in range(len(self.maze)):
            for col in range(len(self.maze[row])):
                tile_value: int = self.maze[row][col]
                ###################################
                # need to add in the empty tile image behind doors:
                if tile_value in {TILE_WALL, TILE_GOAL, TILE_KEY}:
                    tile_img: pygame.Surface = self.tileset.get_image(tile_value)
                else:
                    # filles in the empty and tilespots behind doors:
                    tile_img = self.tileset.get_image(TILE_EMPTY)
                # tile_img = self.tileset.images['door_unlocked']
                # if tile_value == 5 else self.tileset.get_image(tile_value)
                self.screen.blit(tile_img, (col * TILE_SIZE, row * TILE_SIZE))

        #####################################
        # draw all the doors after tiles and walls drawn
        for door in self.doors:
            door.draw(self.screen)
        ####################################

        # maybe in future add an array of all objects to be drawn on top of empty tiles

        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        pygame.display.flip()

    def update(self) -> None:
        if self.door_unlock_time and pygame.time.get_ticks() - self.door_unlock_time > 300:
            for r in range(len(self.maze)):
                for c in range(len(self.maze[r])):
                    if self.maze[r][c] == 5:
                        self.maze[r][c] = 0
            self.door_unlock_time = None

        row: int = self.player.rect.top // TILE_SIZE
        col: int = self.player.rect.left // TILE_SIZE
        tile_name: str = self.tileset.get_tile_name(self.maze[row][col])
        ######################################
        for door in self.doors:
            if self.player.collides_with(door):
                door.interact(self.player, self.maze)

        if tile_name == 'goal':
            print("Level complete!")
            self.level_index += 1
            if self.level_index < len(self.levels):
                self.load_level(self.level_index)
            else:
                print("You won all levels!")
                pygame.quit()
                sys.exit()

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            self.single_iteration()

    def single_iteration(self) -> None:
        self.player.update(self.maze, self.doors)
        for enemy in self.enemies:
            enemy.update(self.maze, self.player)
        self.update()
        self.draw()
        self.clock.tick(FPS)

    @staticmethod
    def game_loop() -> None:
        game_iteration = Game()
        game_iteration.run()
