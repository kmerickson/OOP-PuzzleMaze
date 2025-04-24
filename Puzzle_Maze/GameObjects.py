""" Game objects classes such as player, enemies,
and other """

import sys
# import os
from typing import Type, Tuple
import pygame
from pygame.locals import *

TILE_SIZE = 64
PLAYER_MOVE_DELAY = 200
ENEMY_MOVE_DELAY = 500
TILE_EMPTY = 0
TILE_WALL = 1
TILE_GOAL = 2
TILE_DOOR = 3
TILE_KEY = 4
TILE_UNLOCKED = 5

class GameObject:
    """Game object class from which objects such as player and enemy are derived"""
    
    def __init__(self, name: str, pos: tuple[int, int], image: pygame.Surface) -> None:
        """ Initialization Function, replaced the Actor class in game.py """
        self.name = name
        self.image = image
        # set the top left corner as the point of reference:
        self.rect = image.get_rect(topleft=pos) 

    def draw(self, screen) -> None:
        """draws the position of the object relative to the top left corner"""
        screen.blit(self.image, self.rect.topleft)

    def update(self) -> None:
        """Place holder update function"""
        pass

    def move_to(self, x: int, y: int) -> None:
        """used to move game objects, upon update, moves object to new coords"""
        print(f"[DEBUG] Setting self.rect.topleft = ({x}, {y})")
        self.rect.topleft = (x, y)

    def collides_with(self, other: 'GameObject') -> bool:
        """Checks for collision between this object and input object.
        Incorporates the colliderect() function."""
        return self.rect.colliderect(other.rect)

class Player(GameObject):
    """Player GameObject class"""
    
    # want there to be a default image
    def __init__(self, position: tuple[int, int],
                 image: pygame.Surface | None = None) -> None:
        """init function that sets a default image and requires the starting position"""
        if image is None:
            # load image
            # convert_alpha converts to same pixel format as display
            # and supports transparency
            default_image = pygame.image.load("assets/player.png").convert_alpha()
            # set the correct scale
            default_image = pygame.transform.scale(default_image,
                                                   (TILE_SIZE, TILE_SIZE))
        else:  # allow for the player image to change
            default_image = image

        # pull all functionality from the GameObject init function
        super().__init__("Player", position, default_image)

        self.unlock_count = 0
        self.last_move_time = 0
        # self.level_index = 0  # no longer needed
    
    def draw(self, screen):
        print(f"[DEBUG] Drawing player at {self.rect.topleft}")
        super().draw(screen)

    # handle movement
    def update(self, maze: list[list[int]]) -> None:
        """Handles player input, basically copied handle_player_input()
        from previous version of game.py
        This version requires passing in the 'maze' which are the matrices
        created in the load_levels() function."""

        print("[DEBUG] Player.update() CALLED")
        keys = pygame.key.get_pressed()
        print("Keys pressed:", [i for i, key in enumerate(keys) if key])

        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < PLAYER_MOVE_DELAY:
            return

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[K_UP]:
            dy = -1
            print("Up pressed")
        elif keys[K_DOWN]:
            dy = 1
            print("Down pressed")
        elif keys[K_LEFT]:
            dx = -1
            print("Left pressed")
        elif keys[K_RIGHT]:
            dx = 1
            print("Right pressed")
        else:
            return

        new_row = self.rect.top // TILE_SIZE + dy
        new_col = self.rect.left // TILE_SIZE + dx
        print("Trying to move to:", new_row, new_col)
        if not (0 <= new_row < len(maze) and 0 <= new_col < len(maze[0])):
            return

        # utilize the maze matrix used to draw the level to
        # decide what the player can do: 
        tile_index = maze[new_row][new_col]
        print("Tile at target:", tile_index)

        # if tile_name == 'goal':
        # 	print("Level Complete") # I don't think this actually shows up
        # 	self.level_index += 1 """

        # 	"""section below not applicable in this class,
        # 	keeping as reminder of what to do: figure out level changes
        # 	if self.level_index < len(self.levels):
        # 		self.load_level(self.level_index)
        # 	else:
        # 		print("You won all levels!")
        # 		pygame.quit()
        # 		sys.exit()
        # 	return
        if tile_index == TILE_KEY:
            self.unlock_count += 1
            maze[new_row][new_col] = 0
        elif tile_index == TILE_DOOR:
            if self.unlock_count > 0:
                self.unlock_count -= 1
                maze[new_row][new_col] = 5 # 5 is temporarily unlocked
            else:
                return
        elif tile_index not in (TILE_EMPTY, TILE_GOAL):
            return  # do nothing if wall
                
        print(f"Moving player to: ({new_col * TILE_SIZE}, {new_row * TILE_SIZE})")
        self.move_to(new_col * TILE_SIZE, new_row * TILE_SIZE)
        self.last_move_time = current_time

class Enemy(GameObject):
    """Enemy GameObject class"""
    def __init__(self, position: tuple[int, int],
                 image: pygame.Surface | None = None, velocity: int = 1) -> None:
        if image is None:
            default_image = pygame.image.load("assets/enemy.png").convert_alpha()
            default_image = pygame.transform.scale(default_image, (TILE_SIZE, TILE_SIZE))
        else:
            default_image = image

        super().__init__("Enemy", position, default_image)

        self.velocity = velocity
        self.last_move_time = 0

    def update(self, maze: list[list[int]], player: GameObject) -> None:
        """Update logic for the enemy class, pass in the maze 2D array and 
        the player game object."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < ENEMY_MOVE_DELAY:
            return
        
        new_row = self.rect.top // TILE_SIZE + self.velocity
        col = self.rect.left // TILE_SIZE # doesn't actually move from column

        if 0 <= new_row < len(maze):
            tile_index = maze[new_row][col]
            if tile_index != TILE_WALL:
                self.move_to(col * TILE_SIZE, new_row * TILE_SIZE)
            else:
                self.velocity *= -1
        else:
            self.velocity *= -1 # added to reverse if it goes out of bounds as well

        self.last_move_time = current_time

        if self.collides_with(player):
            print("You Died!")
            #Added to make return to main menu with player death
            #Will return if player presses escape or dies, as an escape key click is mocked
            mock_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
            pygame.event.post(mock_event)

#class Key(GameObject):
#class Door(GameObject):
#class Goal(GameObject):