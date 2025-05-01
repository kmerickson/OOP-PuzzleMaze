""" Game objects classes such as player, enemies,
and other"""

from __future__ import annotations
from typing import Type, Tuple
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
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
        """ Initialization Function"""
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
        # # print(f"[DEBUG] Setting self.rect.topleft = ({x}, {y})")
        self.rect.topleft = (x,  y)

    def collides_with(self, other: 'GameObject') -> bool:
        """Checks for collision between this object and input object.
        Incorporates the colliderect() function."""
        return self.rect.colliderect(other.rect)

    def change_img(self, new_img: pygame.Surface) -> None:
        """changes the image for a state transition or animation"""
        self.image = new_img


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

        self.key_count = 0
        self.last_move_time = 0
        # self.level_index = 0  # no longer needed

    def draw(self, screen) -> None:
        # print(f"[DEBUG] Drawing player at {self.rect.topleft}")
        super().draw(screen)

    # handle movement
    def update(self, maze: list[list[int]], doors: list[Door]) -> None:
        """Handles player input, basically copied handle_player_input()
        from previous version of game.py
        This version requires passing in the 'maze' which are the matrices
        created in the load_levels() function."""

        # # print("[DEBUG] Player.update() CALLED")
        keys = pygame.key.get_pressed()
        # # print("Keys pressed:", [i for i, key in enumerate(keys) if key])

        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < PLAYER_MOVE_DELAY:
            return

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[K_UP]:
            dy = -1
            # # print("Up pressed")
        elif keys[K_DOWN]:
            dy = 1
            # # print("Down pressed")
        elif keys[K_LEFT]:
            dx = -1
            # # print("Left pressed")
        elif keys[K_RIGHT]:
            dx = 1
            # # print("Right pressed")
        else:
            return

        new_row = self.rect.top // TILE_SIZE + dy
        new_col = self.rect.left // TILE_SIZE + dx
        # print("Trying to  move to:", new_row, new_col)
        if not (0 <= new_row < len(maze) and 0 <= new_col < len(maze[0])):
            return

        for door in doors:
            if door.rect.collidepoint(new_col * TILE_SIZE, new_row * TILE_SIZE):
                door.interact(self, maze)
                tile_index = maze[new_row][new_col]
                break

        # utilize the maze matrix used to draw the level to
        # decide what the player can do:
        tile_index = maze[new_row][new_col]
        # print("Tile at target:", tile_index)

        if tile_index == TILE_KEY:
            self.key_count += 1
            print("Key Count: ", self.key_count)
            maze[new_row][new_col] = TILE_EMPTY
        elif tile_index == TILE_WALL:
            return  # do nothing if wall
        elif tile_index == TILE_DOOR:
            return

        # print(f"Moving player to: ({new_col * TILE_SIZE}, {new_row * TILE_SIZE})")
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
        col = self.rect.left // TILE_SIZE   # doesn't actually move from column

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
            # ADDED to make return to main menu with player death
            # Will return if player presses escape or dies, as an escape key click is mocked
            mock_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
            pygame.event.post(mock_event)


T = TypeVar('T', bound=GameObject)


class ObjectState(ABC, Generic[T]):
    """Base abstract state class. Declares methods that all concrete states
    should implement. Designed to take in any object class with state implementations"""

    @property
    def context(self) -> T:
        """returns the game object which is this class's context"""
        return self._context

    @context.setter
    def context(self, context: T) -> None:
        """Setter function for the context, which is the object class"""
        self._context = context

    @abstractmethod
    def handle(self, player, maze: list[list[int]]) -> None:
        """handle interactions with the player"""
        pass

    @abstractmethod
    def update(self):
        """Update variables"""
        pass


class Door(GameObject):
    """Door GameObject class. Functions based off different states managed
    by the ObjectState class. The two states are the LockedDoorState and 
    UnlockedDoorState classes."""
    def __init__(self, position: tuple[int, int], state: ObjectState['Door']) -> None:

        default_image = pygame.image.load("assets/door.png").convert_alpha()
        default_image = pygame.transform.scale(default_image, (TILE_SIZE, TILE_SIZE))

        super().__init__("Door", position, default_image)

        self._state = None  # variable to hold the object state
        self.transition_to(state)

    def transition_to(self, state: ObjectState) -> None:
        """Handles state transitions"""
        # might be a better function to handle image transitions
        # maybe by storing the default image in the state
        self._state = state
        self._state.context = self

    def interact(self, player: Player, maze: list[list[int]]) -> None:
        """Passes the player object in to state object to handle behavior.
        Maze is passed in to update images."""
        self._state.handle(player, maze)

    def update(self) -> None:
        """Delegates updating to the state class."""
        self._state.update()

    def draw(self, screen) -> None:
        """Utilizes basic drawing operation from GameObject class"""
        super().draw(screen)


class LockedDoorState(ObjectState['Door']):
    """class for simple functionality of a locked door (can't pass)"""
    def handle(self, player: Player, maze: list[list[int]]) -> None:
        if player.key_count > 0:
            player.key_count -= 1
            print("key used, new key count: ", player.key_count)

            # change image to unlocked:
            new_img = pygame.image.load("assets/door_unlocked.png").convert_alpha()
            new_img = pygame.transform.scale(new_img, (TILE_SIZE, TILE_SIZE))
            self.context.change_img(new_img)

            # update the maze array door position with new value:
            door_row = self.context.rect.top // TILE_SIZE
            door_col = self.context.rect.left // TILE_SIZE
            maze[door_row][door_col] = TILE_UNLOCKED

            self.context.transition_to(UnlockedDoorState())

    def update(self) -> None:
        """"has no added functionality"""
        pass

    def is_passable(self) -> bool:
        """checks if the player can pass through"""
        return False


class UnlockedDoorState(ObjectState['Door']):
    """State for door object that allows open door to be treated as an empty tile"""
    def handle(self, player: Player, maze: list[list[int]]) -> None:
        # print("door is still unlocked.")
        pass

    def update(self) -> None:
        """has no functionality"""
        pass

    def is_passable(self) -> bool:
        """checks if the player can pass through"""
        return True

# not sure I want to add these, probably won't be able to make use of the added modularity
# class Key(GameObject):
# 	"""Key object class"""
# 	def __init__(self, position: tuple[int, int],
# 			image: pygame.Surface | None = None) -> None:
# 		if image is None:
# 			default_image = pygame.image.load("assets/key.png").convert_alpha()
# 			default_image = pygame.transform.scale(default_image, (TILE_SIZE, TILE_SIZE))
# 		else:
# 			default_image = image

# 		super().__init__("Key", position, default_image)


# class Goal(GameObject):
#     """Goal GameObject class"""
#     def __init__(self, position: tuple[int, int], image: pygame.Surface | None = None) -> None:
#         if image is None:
#             default_image = pygame.image.load("assets/goal.png").convert_alpha()
#             default_image = pygame.transform.scale(default_image, (TILE_SIZE, TILE_SIZE))
#         else:
#             default_image = image

#         super().__init__("Goal", position, default_image)
