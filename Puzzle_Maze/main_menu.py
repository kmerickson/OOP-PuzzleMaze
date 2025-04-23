import pygame
from interactive_ui_elements import GameText, GameButton


class MainMenu:
    X_FACTOR: float = 0.5
    Y_FACTOR_PLAY_BUTTON: float = 0.45
    Y_FACTOR_OPTIONS_BUTTON: float = 0.65
    Y_FACTOR_QUIT_BUTTON: float = 0.85
    Y_FACTOR_MENU_TEXT: float = 0.167
    FACTOR_FOR_MAIN_TEXT: float = 0.1
    BACKGROUND_PICTURE_DIRECTORY: str = "assets/green_space.jpg"

    def __init__(self, screen: pygame.Surface):
        self._screen: pygame.Surface = screen
        self._background_picture: pygame.Surface = pygame.image.load(self.BACKGROUND_PICTURE_DIRECTORY)
        self._screen_width: float = self._screen.get_size()[0]
        self._screen_height: float = self._screen.get_size()[1]
        self._scaled_picture: pygame.Surface = pygame.transform.scale(self._background_picture,
                                                      (self._screen_width, self._screen_height))
        self._play_button: GameButton = GameButton(screen, "Play", self.X_FACTOR, self.Y_FACTOR_PLAY_BUTTON,
                                       0)
        self._options_button: GameButton = GameButton(screen, "Options", self.X_FACTOR, self.Y_FACTOR_OPTIONS_BUTTON,
                                       0)
        self._quit_button: GameButton = GameButton(screen, "Quit", self.X_FACTOR, self.Y_FACTOR_QUIT_BUTTON,
                                       0)
        self._menu_text = GameText(
            self._screen, "Chip's Core Escape", self.X_FACTOR, self.Y_FACTOR_MENU_TEXT, (self._screen_width * self.FACTOR_FOR_MAIN_TEXT))
        self._break = False

    def adjust_screen(self):
        self._screen_width = self._screen.get_size()[0]
        self._screen_height = self._screen.get_size()[1]
        self._scaled_picture = pygame.transform.scale(self._background_picture,
                                                      (self._screen_width, self._screen_height))
        self._menu_text.text.size = self._screen_width  * self.FACTOR_FOR_MAIN_TEXT

    def draw_screen(self):
        self.adjust_screen()
        self._screen.blit(self._scaled_picture, (0, 0))
        self._menu_text.draw()
        self._play_button.draw()
        self._options_button.draw()
        self._quit_button.draw()
    
    @property
    def play_button(self):
        return self._play_button
    @property
    def options_button(self):
        return self._options_button
    @property
    def quit_button(self):
        return self._quit_button
    
    def main_loop(self):
        while True:
            self.draw_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.display.update()