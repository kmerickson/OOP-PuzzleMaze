import pygame, sys
from button import Button
import game

pygame.init()

class MenuScreens:
    """
    """
    DEFAULT_WIDTH = 1280
    DEFAULT_HEIGHT = 720
    SCREEN = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Chip's Core Escape")
    background_picture = pygame.image.load("assets/green_space.jpg")

    def __init__(self):
        picture = pygame.transform.scale(self.background_picture, (1280, 720))

    def get_font(self, size):
        return pygame.font.Font("assets/Cyberpunks.ttf", size)

    def get_dynamic_font(self, screen_width):
        font_size = screen_width // 10
        font = pygame.font.Font("assets/Cyberpunks.ttf", font_size)
        return font


    def play_screen(self):
        while True:

            game.game_loop()

            pygame.display.update()


    def draw_menu_text(self, text: str, width: int, height: int, color: str):
        menu = self.get_dynamic_font(width).render(text, True, color)
        menu_rect =  menu.get_rect(center=((width // 2), (height // 4)))
        self.SCREEN.blit(menu, menu_rect)

    def create_button(self, current_width, current_height):
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        play_button = Button("assets/Play Rect.png", current_width // 2, current_height // 2, "Play",
                             "assets/Cyberpunks.ttf", "White", self.SCREEN, current_width, current_height)
        quit_button = Button("assets/Play Rect.png", current_width // 2, ((current_height // 4) * 3), "Quit",
                             "assets/Cyberpunks.ttf", "White", self.SCREEN, current_width, current_height)
        #PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(current_width // 2, current_height // 2), 
                            #text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        #QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(current_width // 2, ((current_height // 4) * 3)), 
                            #text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        for button in [play_button, quit_button]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(self.SCREEN, current_width, current_height)
    
    def draw_background(self, width: int, height: int):
        picture = pygame.transform.scale(self.background_picture, (width, height))
        self.SCREEN.blit(picture, (0,0))

    def draw_main_menu_screen(self, current_width, current_height):
        self.draw_background(current_width, current_height)
        self.draw_menu_text("Chip's Core Escape", current_width, current_height, "White")
        #self.create_button(current_width, current_height)

    def main_menu(self):
        current_width, current_height = self.SCREEN.get_size()
        self.draw_main_menu_screen(current_width, current_height)
        play_button = Button("assets/Play Rect.png", current_width // 2, current_height // 2, "Play",
                             "assets/Cyberpunks.ttf", "White", self.SCREEN, current_width, current_height)
        quit_button = Button("assets/Play Rect.png", current_width // 2, ((current_height // 4) * 3), "Quit",
                             "assets/Cyberpunks.ttf", "White", self.SCREEN, current_width, current_height)
        while True:
            current_width, current_height = self.SCREEN.get_size()
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    current_width, current_height = self.SCREEN.get_size()
                    self.draw_main_menu_screen(current_width, current_height)
                    play_button.update(self.SCREEN, current_width, current_height, 0.5)
                    quit_button.update(self.SCREEN, current_width, current_height, 0.75)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(MENU_MOUSE_POS):
                        self.play_screen()
                    if quit_button.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()



menu = MenuScreens()
menu.main_menu()