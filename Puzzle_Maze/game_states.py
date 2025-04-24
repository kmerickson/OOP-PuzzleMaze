from entry_point import MainMenu, OptionsScreen
from abc import ABC, abstractmethod
from enum import Enum
import pygame
from game import Game

class GameEvents(Enum):
    """Enum containing 
        all the states UI
        elements can be in
    """
    USER_CLICK = 0,
    ESCAPE = 1

class GameState(ABC):
    @abstractmethod
    def display_screen(self, outer_class: "ChipsCoreEscape"):
        pass

    @abstractmethod
    def handle_event(self, outer_class: "ChipsCoreEscape", event: GameEvents):
        pass


class PlayState(GameState):
    def display_screen(self, outer_class):
        outer_class._game.single_iteration()
    def handle_event(self, outer_class, event):
        if event == GameEvents.ESCAPE:
            outer_class._state = MainMenuState()


class OptionsState(GameState):
    def display_screen(self, outer_class):
        outer_class._options.draw_screen()
    def handle_event(self, outer_class, event):
        if event == GameEvents.ESCAPE:
            outer_class._state = MainMenuState()
        if event == GameEvents.USER_CLICK:
            mouse_position = pygame.mouse.get_pos()
            if (outer_class._options.small_button.button.rect.collidepoint(mouse_position)):
                outer_class.screen = pygame.display.set_mode((outer_class._options.SMALL_SCREEN), pygame.RESIZABLE)
                outer_class._state = MainMenuState()
                outer_class.display_screen()
            elif(outer_class._options.large_button.button.rect.collidepoint(mouse_position)):
                outer_class.screen = pygame.display.set_mode((outer_class._options.LARGE_SCREEN), pygame.RESIZABLE)
                outer_class._state = MainMenuState()
                outer_class.display_screen()
            elif(outer_class._options.full_button.button.rect.collidepoint(mouse_position)):
                #outer_class.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                outer_class._state = MainMenuState()

class MainMenuState(GameState):
    def display_screen(self, outer_class: "ChipsCoreEscape"):
        outer_class._menu.draw_screen()
    
    def handle_event(self, outer_class: "ChipsCoreEscape", event: GameEvents):
        if event == GameEvents.USER_CLICK:
            mouse_position = pygame.mouse.get_pos()
            if (outer_class._menu.play_button.button.rect.collidepoint(mouse_position)):
                outer_class._game = Game()
                outer_class._state = PlayState() 
            elif(outer_class._menu.options_button.button.rect.collidepoint(mouse_position)):
                outer_class._state = OptionsState()
            elif(outer_class._menu.quit_button.button.rect.collidepoint(mouse_position)):
                pygame.quit()
        if event == GameEvents.ESCAPE:
            pygame.quit()

class ChipsCoreEscape:
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        self._game = Game()
        self._menu = MainMenu(self._screen)
        self._options = OptionsScreen(self._screen)
        self._state: GameState = MainMenuState()
        

    def display_screen(self):
        self._state.display_screen(self)

    def handle_user(self, events):
            self._state.handle_event(self, events)

    def game(self):
        
        while True:
            self.display_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_user(GameEvents.USER_CLICK)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.handle_user(GameEvents.ESCAPE)
            pygame.display.update()