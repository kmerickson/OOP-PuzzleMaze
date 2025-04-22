import os
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import pygame, sys
from button import Button
import game
from text import Text
pygame.init()
#pygame.mixer.init()
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
        # pygame.mixer.music.load("assets/space-horror-music.mp3")
    def get_font(self, size):
        return pygame.font.Font("assets/Cyberpunks.ttf", size)

    def get_dynamic_font(self, screen_width):
        font_size = screen_width // 10
        font = pygame.font.Font("assets/Cyberpunks.ttf", font_size)
        return font


    def play_screen(self):
        #pygame.mixer.quit()
        #while True:

        game.game_loop() # changed, was in while loop

            #pygame.display.update()


    def draw_menu_text(self, text: str, width: int, height: int, color: str):
        menu = self.get_dynamic_font(width).render(text, True, color)
        menu_rect =  menu.get_rect(center=((width // 2), (height // 6)))
        self.SCREEN.blit(menu, menu_rect)

    def create_button(self, current_width, current_height):
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        play_button = Button("assets/button.png", 0.5, "Play",
                             "assets/Cyberpunks.ttf", "White", self.SCREEN, current_width, current_height)
        quit_button = Button("assets/button.png", 0.75 , "Quit",
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
    
    def hover_over_menu_text(self, menu_pos, width, height):
        font_and_size_obj = pygame.font.Font(
            "assets/Cyberpunks.ttf",
            (width // 10) + 7
            )
        text = font_and_size_obj.render(
            "Chip's Core Escape", True, "Black")
        
        text_rect = text.get_rect(
                center=(
                        width // 2, height // 6
                        )
                )
        self.SCREEN.blit(text, text_rect)
        self.draw_menu_text("Chip's Core Escape", width, height, "White")

    def main_menu(self):
        #pygame.mixer.music.play(loops=-1, start=0.0)
        current_width, current_height = self.SCREEN.get_size()
        self.draw_main_menu_screen(current_width, current_height)
        play_button = Button("assets/button.png", 0.45, "Play",
                             "assets/Cyberpunks.ttf", "White", self.SCREEN, current_width, current_height)
        options_button = Button("assets/button.png", 0.65, "Options",
                             "assets/Cyberpunks.ttf", "White", self.SCREEN, current_width, current_height)
        quit_button = Button("assets/button.png", 0.85, "Quit",
                             "assets/Cyberpunks.ttf", "White", self.SCREEN, current_width, current_height)
        while True:
            current_width, current_height = self.SCREEN.get_size()
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            self.hover_over_menu_text(MENU_MOUSE_POS, current_width, current_height)
            self.draw_main_menu_screen(current_width, current_height)
            play_button.react_to_user_position(MENU_MOUSE_POS)
            quit_button.react_to_user_position(MENU_MOUSE_POS)
            options_button.react_to_user_position(MENU_MOUSE_POS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    current_width, current_height = self.SCREEN.get_size()
                    self.draw_main_menu_screen(current_width, current_height)
                    play_button.update(current_width, current_height)
                    quit_button.update(current_width, current_height)
                    options_button.update(current_width, current_height)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.user_clicked_button(MENU_MOUSE_POS):
                        self.play_screen()
                    if options_button.user_clicked_button(MENU_MOUSE_POS):
                        pass
                    if quit_button.user_clicked_button(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()



menu = MenuScreens()
menu.main_menu()
