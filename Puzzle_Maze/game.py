# file: puzzle.py
import pygame
import sys
import time
from random import randint
from pygame.locals import *

# Initialize
pygame.init()

# Constants
TILE_SIZE = 128
WIDTH = TILE_SIZE * 8
HEIGHT = TILE_SIZE * 8
FPS = 60

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tile Puzzle")
clock = pygame.time.Clock()

# Load images
tiles_images = {
    'empty': pygame.Surface((TILE_SIZE, TILE_SIZE)),
    'wall': pygame.Surface((TILE_SIZE, TILE_SIZE)),
    'goal': pygame.Surface((TILE_SIZE, TILE_SIZE)),
    'door': pygame.Surface((TILE_SIZE, TILE_SIZE)),
    'key': pygame.Surface((TILE_SIZE, TILE_SIZE)),
    'player': pygame.Surface((TILE_SIZE, TILE_SIZE)),
    'enemy': pygame.Surface((TILE_SIZE, TILE_SIZE)),
}

# Simple colors for placeholder visuals
tiles_images['empty'].fill((50, 50, 50))
tiles_images['wall'].fill((100, 100, 100))
tiles_images['goal'].fill((0, 255, 0))
tiles_images['door'].fill((150, 75, 0))
tiles_images['key'].fill((255, 215, 0))
tiles_images['player'].fill((0, 0, 255))
tiles_images['enemy'].fill((255, 0, 0))

tiles = ['empty', 'wall', 'goal', 'door', 'key']
unlock = 0

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 2, 0, 1],
    [1, 0, 1, 0, 1, 1, 3, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 4, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

class Actor:
    def __init__(self, name, pos):
        self.image = tiles_images[name]
        self.rect = self.image.get_rect(topleft=pos)
        self.name = name
        self.yv = 0

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def move_to(self, pos):
        self.rect.topleft = pos

    def colliderect(self, other):
        return self.rect.colliderect(other.rect)

player = Actor("player", (1 * TILE_SIZE, 1 * TILE_SIZE))
enemy = Actor("enemy", (6 * TILE_SIZE, 3 * TILE_SIZE))
enemy.yv = -1

def draw():
    screen.fill((0, 0, 0))
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            tile = tiles[maze[row][column]]
            screen.blit(tiles_images[tile], (x, y))
    player.draw()
    enemy.draw()
    pygame.display.flip()

def handle_input():
    global unlock
    keys_pressed = pygame.key.get_pressed()
    dx = dy = 0

    if keys_pressed[K_UP]: dy = -1
    elif keys_pressed[K_DOWN]: dy = 1
    elif keys_pressed[K_LEFT]: dx = -1
    elif keys_pressed[K_RIGHT]: dx = 1

    if dx == 0 and dy == 0:
        return

    row = player.rect.top // TILE_SIZE + dy
    col = player.rect.left // TILE_SIZE + dx

    if not (0 <= row < 8 and 0 <= col < 8):
        return

    tile = tiles[maze[row][col]]

    if tile in ['empty', 'goal', 'key', 'door']:
        if tile == 'goal':
            print("Well done")
            pygame.quit()
            sys.exit()
        elif tile == 'key':
            unlock += 1
            maze[row][col] = 0
        elif tile == 'door' and unlock > 0:
            unlock -= 1
            maze[row][col] = 0
        player.move_to((col * TILE_SIZE, row * TILE_SIZE))

def update_enemy():
    row = enemy.rect.top // TILE_SIZE + enemy.yv
    col = enemy.rect.left // TILE_SIZE

    if 0 <= row < 8:
        tile = tiles[maze[row][col]]
        if tile != 'wall':
            time.sleep(0.5)
            enemy.move_to((col * TILE_SIZE, row * TILE_SIZE))
        else:
            enemy.yv *= -1

    if enemy.colliderect(player):
        print("You died")
        pygame.quit()
        sys.exit()

def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        handle_input()
        update_enemy()
        draw()
        clock.tick(FPS)

if __name__ == "__main__":
    game_loop()