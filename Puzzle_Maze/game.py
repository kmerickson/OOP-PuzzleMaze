# file: game.py
import pygame
import sys
import os
from pygame.locals import *
from GameObjects import Player, Enemy


# Initialize pygame
# pygame.init()  # not needed if done in main.py

# Constants
TILE_SIZE = 64  # also defined again in GameObjects.py,
                # Maybe move to a constants.py file
GRID_WIDTH = 8
GRID_HEIGHT = 8
WIDTH = TILE_SIZE * GRID_WIDTH
HEIGHT = TILE_SIZE * GRID_HEIGHT
FPS = 60
PLAYER_MOVE_DELAY = 200
ENEMY_MOVE_DELAY = 500
ASSET_DIR = "assets"

# Tile management
class TileSet:
    def __init__(self):
        ###################
        # added door_unlocked to array"
        self.tiles = ['empty', 'wall', 'goal', 'door', 'key', 'door_unlocked']
        ##################
        self.images = self._load_images()

    def _load_images(self):
        images = {}

        def load_or_color(name, fallback_color):
            path = os.path.join(ASSET_DIR, f"{name}.png")
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                if name in {"key", "goal", "door", "door_unlocked"}:
                    base = images["empty"].copy()
                    base.blit(img, (0, 0))
                    return base
                return img
            surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
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

    def get_image(self, tile_index):
        return self.images[self.tiles[tile_index]]

    def get_tile_name(self, tile_index):
        return self.tiles[tile_index]

# Actor base
class Actor:
    def __init__(self, name, position, image):
        self.name = name
        self.image = image
        self.rect = image.get_rect(topleft=position)
        self.y_velocity = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def move_to(self, position):
        self.rect.topleft = position

    def collides_with(self, other):
        return self.rect.colliderect(other.rect)

# Game logic
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tile Puzzle")
        self.clock = pygame.time.Clock()

        self.tileset = TileSet()
        self.levels = self.load_levels()
        self.level_index = 0

        self.door_unlock_time = None
        self.load_level(self.level_index)

    def load_levels(self):
        return [
            [
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 1, 2, 1],
                [1, 0, 1, 1, 1, 1, 3, 1],
                [1, 0, 1, 4, 0, 1, 0, 1],
                [1, 0, 1, 1, 0, 0, 0, 1],
                [1, 0, 0, 1, 1, 1, 0, 1],
                [1, 1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]
            ],
            [
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 3, 1, 0, 1],
                [1, 0, 1, 0, 0, 1, 0, 1],
                [1, 0, 1, 2, 0, 1, 4, 1],
                [1, 0, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]
            ]
        ]

    def load_level(self, index):
        self.maze = self.levels[index]
        # New player and enemy class only requires the starting position
        # to be added as an arguemnt. A second argument can be added to
        # change the image. Enemy class requires velocity as well.
        #############################################################
        self.player = Player((1 * TILE_SIZE, 1 * TILE_SIZE))
        self.enemy = Enemy((6 * TILE_SIZE, 3 * TILE_SIZE), velocity = -1) 
        ############################################################
        self.door_unlock_time = None

    def draw(self):
        self.screen.fill((0, 0, 0))
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                tile_value = self.maze[row][col]
                if tile_value == 5:
                    tile_img = self.tileset.images['door_unlocked']
                else:
                    tile_img = self.tileset.get_image(tile_value)
                self.screen.blit(tile_img, (col * TILE_SIZE, row * TILE_SIZE))
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)
        pygame.display.flip()

        # No longer needed 
        # def handle_player_input(self):
        # current_time = pygame.time.get_ticks()
        # if current_time - self.last_player_move < PLAYER_MOVE_DELAY:
        #     return

        # keys = pygame.key.get_pressed()
        # dx = dy = 0
        # if keys[K_UP]: dy = -1
        # elif keys[K_DOWN]: dy = 1
        # elif keys[K_LEFT]: dx = -1
        # elif keys[K_RIGHT]: dx = 1
        # else: return

        # new_row = self.player.rect.top // TILE_SIZE + dy
        # new_col = self.player.rect.left // TILE_SIZE + dx
        # if not (0 <= new_row < GRID_HEIGHT and 0 <= new_col < GRID_WIDTH): return

        # tile_name = self.tileset.get_tile_name(self.maze[new_row][new_col])
        # if tile_name == 'goal':
        #     print("Level complete!")
        #     self.level_index += 1
        #     if self.level_index < len(self.levels):
        #         self.load_level(self.level_index)
        #     else:
        #         print("You won all levels!")
        #         pygame.quit()
        #         sys.exit()
        #     return
        # elif tile_name == 'key':
        #     self.unlock_count += 1
        #     self.maze[new_row][new_col] = 0
        # elif tile_name == 'door':
        #     if self.unlock_count > 0:
        #         self.unlock_count -= 1
        #         self.maze[new_row][new_col] = 5  # 5 is temporary unlocked state
        #         self.door_unlock_time = pygame.time.get_ticks()
        #     else:
        #         return
        # elif tile_name != 'empty':
        #     return

        # self.player.move_to((new_col * TILE_SIZE, new_row * TILE_SIZE))
        # self.last_player_move = current_time

        #  def update_enemy(self):
        # current_time = pygame.time.get_ticks()
        # if current_time - self.last_enemy_move < ENEMY_MOVE_DELAY:
        #     return

        # row = self.enemy.rect.top // TILE_SIZE + self.enemy.y_velocity
        # col = self.enemy.rect.left // TILE_SIZE
        # if 0 <= row < GRID_HEIGHT:
        #     tile_name = self.tileset.get_tile_name(self.maze[row][col])
        #     if tile_name != 'wall':
        #         self.enemy.move_to((col * TILE_SIZE, row * TILE_SIZE))
        #     else:
        #         self.enemy.y_velocity *= -1

        # self.last_enemy_move = current_time

        # if self.enemy.collides_with(self.player):
        #     print("You died")
        #     pygame.quit()
        #     sys.exit()

    def update(self):
        if self.door_unlock_time:
            if pygame.time.get_ticks() - self.door_unlock_time > 300:
                for r in range(GRID_HEIGHT):
                    for c in range(GRID_WIDTH):
                        if self.maze[r][c] == 5:
                            self.maze[r][c] = 0
                self.door_unlock_time = None

        ###############################################
        # Added to check if player is on goal tile
        row = self.player.rect.top // TILE_SIZE
        col = self.player.rect.left // TILE_SIZE
        tile_name = self.tileset.get_tile_name(self.maze[row][col])

        if tile_name == 'goal':
            print("Level complete!")
            self.level_index += 1
            if self.level_index < len(self.levels):
                # makes sure haven't completed all levels
                self.load_level(self.level_index) # load next level
            else:
                print(" You won all levels!")
                # put in logic to display message until a key is pressed
                # ! want to replace this to go back to menu
                pygame.quit()
                sys.exit()
        #############################################

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            ##########################################################
            # new player and enemy classes require the maze as an input    
            self.player.update(self.maze)
            # the enemy class also requires player information as an input
            self.enemy.update(self.maze, self.player)
            ##########################################################
            self.update()
            self.draw()
            self.clock.tick(FPS)

def game_loop():
    Game().run()

if __name__ == "__main__":
    game_loop()
