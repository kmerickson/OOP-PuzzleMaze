"""Modules containing various screens that will
  for different states within the game
"""
from abc import ABC, abstractmethod
from typing_extensions import override
import pygame
from interactive_ui_elements import GameText, GameButton


class Screen(ABC):
    """Class acting as common interface for screens
    """
    def __init__(self, screen: pygame.Surface) -> None:
        """Constructor for screen class

        Args:
            screen (pygame.Surface): screen to draw on
        """
        self._screen: pygame.Surface = screen
        self._screen_width: float = self._screen.get_size()[0] 
        self._screen_height: float = self._screen.get_size()[1]

    @abstractmethod
    def draw_screen(self) -> None:
        """Draw screen for a single iteration
        """
        pass

    @abstractmethod
    def adjust_to_screen(self) -> None:
        """Adjust variables to a size change
        """
        pass

    def main_loop(self):
        """Display screen on its own
        """
        while True:
            self.draw_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.display.update()

    @property
    def screen(self) -> pygame.Surface:
        """Getter for screen variable

        Returns:
            _screen (pygame.Surface): surface that is drawn on
        """
        return self._screen
    
    @property
    def screen_width(self) -> float:
        """Getter for screen width variable

        Returns:
            _self_width (float): width of screen
            variable
        """
        return self._screen_width

    @property
    def screen_height(self) -> float:
        """Getter for screen height variable

        Returns:
            _self_height: height of screen
            variable
        """
        return self._screen_height
    
    def resize_screen_variables(self) -> None:
        """Resize size variables after screen change
        """
        self._screen_width, self._screen_height = self._screen.get_size()


class MainMenu(Screen):
    """Class that will create the main menu screen
    """
    X_FACTOR: float = 0.5
    FACTOR_FOR_MAIN_TEXT_SIZE: float = 0.1
    Y_FACTOR_MENU_TEXT: float = 0.1

    Y_FACTOR_PLAY_BUTTON: float = 0.35

    Y_FACTOR_OPTIONS_BUTTON: float = 0.60
    Y_FACTOR_QUIT_BUTTON: float = .85

    BACKGROUND_PICTURE_DIRECTORY: str = "assets/green_space.jpg"

    def __init__(self, screen: pygame.Surface) -> None:
        """Constructor for main menu class

        Args:
            screen (pygame.Surface): screen to draw on
        """
        super().__init__(screen)
        self._background_picture: pygame.Surface = pygame.image.load(
            self.BACKGROUND_PICTURE_DIRECTORY)
        self._scaled_picture: pygame.Surface = pygame.transform.scale(
            self._background_picture, (self.screen_width, self.screen_height))
        
        self._play_button: GameButton = GameButton(
            screen, "Play", self.X_FACTOR, self.Y_FACTOR_PLAY_BUTTON)
        self._info_button: GameButton = GameButton(
            screen, "Info", self.X_FACTOR, self.Y_FACTOR_OPTIONS_BUTTON)
        self._quit_button: GameButton = GameButton(
            screen, "Quit", self.X_FACTOR, self.Y_FACTOR_QUIT_BUTTON)
        self._menu_text: GameText = GameText(
            self._screen, "Chip's Core Escape", self.X_FACTOR, self.Y_FACTOR_MENU_TEXT,
            (self.screen_width * self.FACTOR_FOR_MAIN_TEXT_SIZE))

    @override
    def adjust_to_screen(self) -> None:
        """Changes necessary variables after screen change
        """
        self.resize_screen_variables()
        self._scaled_picture = pygame.transform.scale(self._background_picture,
                                                      (self.screen_width, self.screen_height))
        
        self._menu_text.text.size = self.screen_width * self.FACTOR_FOR_MAIN_TEXT_SIZE

    @override
    def draw_screen(self) -> None:
        """Draws the main menu screen for a single iteration
        """
        self.adjust_to_screen()
        self._screen.blit(self._scaled_picture, (0, 0))
        self._menu_text.draw()
        self._play_button.draw()
        self._info_button.draw()
        self._quit_button.draw()
    
    @property
    def background_picture(self) -> pygame.Surface:
        """Getter for background image surface

        Returns:
            _background_picture (pygame.Surface): the
            background picture used to draw
        """
        return self._background_picture
    
    @property
    def scaled_picture(self) -> pygame.Surface:
        """Getter for scaled picture variable

        Returns:
            scaled_picture (pygame.Surface): the
            background picture scaled to current
            screen size
        """
        return self._scaled_picture
    
    @property
    def main_text(self) -> GameText:
        """Getter for text variable

        Returns:
            _menu_text (GameText): the
            title card on main menu screen
        """
        return self._menu_text
    
    @property
    def play_button(self) -> GameButton:
        """Getter for play button variable

        Returns:
            _play_button (GameButton): the
            button connected to the play state
        """
        return self._play_button
    
    @property
    def info_button(self) -> GameButton:
        """Getter for info button variable

        Returns:
            _info_button (GameButton): the
            button connected to the info state
        """
        return self._info_button
    
    @property
    def quit_button(self) -> GameButton:
        """Getter for quit button variable

        Returns:
            _quit_button (GameButton): the
            button connected to quitting the
            game
        """
        return self._quit_button


class InfoScreen(Screen):
    """Class that will create the main menu screen
    """
    BACKGROUND_COLOR: str = "Black"
    X_FACTOR: float = 0.5

    Y_FACTOR_MAIN_TEXT: float = 0.08
    FACTOR_FOR_TEXT_SIZE: float = 0.3

    SIZE_FOR_LINES: int = 70
    Y_FACTOR_LINE_1: float = 0.25
    Y_FACTOR_LINE_2: float = 0.35
    Y_FACTOR_LINE_3: float = 0.45
    Y_FACTOR_LINE_4: float = 0.55
    
    Y_FACTOR_BACK_BUTTON: float = 0.85

    def __init__(self, screen: pygame.Surface) -> None:
        """Constructor for InfoScreen clas

        Args:
            screen (pygame.Surface): surface that will
            be drawn
        """
        super().__init__(screen)
        self._main_text: GameText = GameText(
            screen, "Chip's Core Escape:", self.X_FACTOR, self.Y_FACTOR_MAIN_TEXT,
            self.screen_width * self.FACTOR_FOR_TEXT_SIZE)
        
        self._body_text_line1: GameText = GameText(
            self.screen, " is a basic puzzle maze game.", self.X_FACTOR,
            self.Y_FACTOR_LINE_1, self.SIZE_FOR_LINES)
        
        self._body_text_line2: GameText = GameText(
            self._screen, "It features the player going through a maze",
            self.X_FACTOR, self.Y_FACTOR_LINE_2, self.SIZE_FOR_LINES)
        
        self._body_text_line3: GameText = GameText(
            self._screen, "having to avoid enemies while needing items",
            self.X_FACTOR, self.Y_FACTOR_LINE_3, self.SIZE_FOR_LINES)
        
        self._body_text_line4: GameText = GameText(
            self._screen, "to advance. It was developed as our final project.",
            self.X_FACTOR, self.Y_FACTOR_LINE_4, self.SIZE_FOR_LINES)
        
        self._back_button: GameButton = GameButton(
            screen, "Back", self.X_FACTOR, self.Y_FACTOR_BACK_BUTTON)
    
    @override
    def adjust_to_screen(self) -> None:
        """Adjusts variables depending on screen change
        """
        self.resize_screen_variables()
        self._main_text.size = self.screen_width * self.FACTOR_FOR_TEXT_SIZE

    @override
    def draw_screen(self) -> None:
        """Draws single iteration of the info screen
        """
        self.adjust_to_screen()
        self.screen.fill(self.BACKGROUND_COLOR)
        self._main_text.draw()

        self._body_text_line1.draw()
        self._body_text_line2.draw()
        self._body_text_line3.draw()
        self._body_text_line4.draw()

        self._back_button.draw()

    @property
    def main_text(self) -> GameText:
        """Getter for main text variable

        Returns:
            _main_text (GameText): title card
            on screen
        """
        return self._main_text
    
    @property
    def body_text_line1(self) -> GameText:
        """Getter for body text line 1 variable

        Returns:
            _body_text_line_1 (GameText): first
            line of the body of text displayed
        """
        return self._body_text_line1
    
    @property
    def body_text_line_2(self) -> GameText:
        """Getter for body text line 2 variable

        Returns:
            _body_text_line_2 (GameText): second
            line of the body of text displayed
        """
        return self._body_text_line2

    @property
    def body_text_line_3(self) -> GameText:
        """Getter for body text line 3 variable

        Returns:
            _body_text_line_3 (GameText): third
            line of the body of text displayed
        """
        return self._body_text_line3
    
    @property
    def body_text_line_4(self) -> GameText:
        """Getter for body text line 4 variable

        Returns:
            _body_text_line_4 (GameText): fourth
            line of the body of text displayed
        """
        return self._body_text_line4
    
    @property
    def back_button(self) -> GameButton:
        """Getter for the back button

        Returns:
            _back_button (GameButton): button
            that will change the state of game
            from info menu
        """
        return self._back_button
