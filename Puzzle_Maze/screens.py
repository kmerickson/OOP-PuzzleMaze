import pygame
from interactive_ui_elements import GameText, GameButton, Text
from abc import ABC, abstractmethod

class Screen(ABC):
    def __init__(self, screen: pygame.Surface):
        self._screen: pygame.Surface = screen
        self._screen_width: float = self._screen.get_size()[0] 
        self._screen_height: float = self._screen.get_size()[1]

    @abstractmethod
    def draw_screen(self):
        pass

    @abstractmethod
    def adjust_to_screen(self):
        pass

    def main_loop(self):
        while True:
            self.draw_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.display.update()

    @property
    def screen(self):
        return self._screen
    
    @property
    def screen_height(self):
        return self._screen_height
    
    @screen_height.setter
    def screen_height(self, screen_height):
        self._screen_height = screen_height
    
    @property
    def screen_width(self):
        return self._screen_width

    @screen_width.setter
    def screen_width(self, screen_width):
        self._screen_width = screen_width

class MainMenu(Screen):
    X_FACTOR: float = 0.5
    Y_FACTOR_PLAY_BUTTON: float = 0.35
    Y_FACTOR_OPTIONS_BUTTON: float = 0.60
    Y_FACTOR_QUIT_BUTTON: float = .85
    Y_FACTOR_MENU_TEXT: float = 0.1
    FACTOR_FOR_MAIN_TEXT: float = 0.1
    BACKGROUND_PICTURE_DIRECTORY: str = "assets/green_space.jpg"

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self._background_picture: pygame.Surface = pygame.image.load(self.BACKGROUND_PICTURE_DIRECTORY)
        self._scaled_picture: pygame.Surface = pygame.transform.scale(self._background_picture,
                                                      (self.screen_width, self.screen_height))
        self._play_button: GameButton = GameButton(screen, "Play", self.X_FACTOR, self.Y_FACTOR_PLAY_BUTTON,
                                       0)
        self._options_button: GameButton = GameButton(screen, "Info", self.X_FACTOR, self.Y_FACTOR_OPTIONS_BUTTON,
                                       0)
        self._quit_button: GameButton = GameButton(screen, "Quit", self.X_FACTOR, self.Y_FACTOR_QUIT_BUTTON,
                                       0)
        self._menu_text = GameText(
            self._screen, "Chip's Core Escape", self.X_FACTOR, self.Y_FACTOR_MENU_TEXT, (self.screen_width * self.FACTOR_FOR_MAIN_TEXT))

    def adjust_to_screen(self):
        self.screen_width = self._screen.get_size()[0]
        self.screen_height = self._screen.get_size()[1]
        self._scaled_picture = pygame.transform.scale(self._background_picture,
                                                      (self.screen_width, self.screen_height))
        self._menu_text.text.size = self._screen_width  * self.FACTOR_FOR_MAIN_TEXT

    def draw_screen(self):
        self.adjust_to_screen()
        self._screen.blit(self._scaled_picture, (0, 0))
        self._menu_text.draw()
        self._play_button.draw()
        self._options_button.draw()
        self._quit_button.draw()
    
    @property
    def main_text(self):
        return self._menu_text
    
    @property
    def play_button(self):
        return self._play_button
    @property
    def options_button(self):
        return self._options_button
    @property
    def quit_button(self):
        return self._quit_button


class OptionsScreen(Screen):
    BACKGROUND_COLOR = "White"
    X_FACTOR_1 = 0.5
    X_FACTOR_2 = 0.75
    Y_FACTOR_MAIN_TEXT = 0.08
    FACTOR_FOR_TEXT_SIZE = 0.3
    Y_FACTOR_1 = 0.33
    Y_FACTOR_2 = 0.66
    SMALL_SCREEN = 800, 600
    LARGE_SCREEN = 1280, 720

    def __init__(self, screen):
        super().__init__(screen)
        self._main_text = GameText(screen, "Chip's Core Escape:", self.X_FACTOR_1,
                             self.Y_FACTOR_MAIN_TEXT, self.screen_width * self.FACTOR_FOR_TEXT_SIZE)
        self._body_text_line1 = GameText(screen," is a basic puzzle maze game.", 0.5, 0.25, 70)
        self._body_text_line2 = GameText(screen,"It features the player going through a maze", 0.5, 0.35, 70)
        self._body_text_line3 = GameText(screen,"having to avoid enemies while needing items", 0.5, 0.45, 70)
        self._body_text_line4 = GameText(screen,"to advance. \nIt was developed as our final project.", 0.5, 0.55, 70)
        self._back_button = GameButton(screen, "Back", self.X_FACTOR_1, 0.85, 0)   

    @property
    def back_button(self):
        return self._back_button
    
    def adjust_to_screen(self):
        self.screen_width = self._screen.get_size()[0]
        self.screen_height = self._screen.get_size()[1]
        self._main_text.size = self.screen_width * self.FACTOR_FOR_TEXT_SIZE

    def draw_screen(self):
        self.adjust_to_screen()
        self.screen.fill("Black")
        self._main_text.draw()
        self._body_text_line1.draw()
        self._body_text_line2.draw()
        self._body_text_line3.draw()
        self._body_text_line4.draw()
        self._back_button.draw()