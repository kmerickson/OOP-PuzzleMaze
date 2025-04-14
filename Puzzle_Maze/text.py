import pygame


class Text():  
    def __init__(self, font_dir: str, screen: pygame.Surface, screen_width: float,
                 screen_height: float, factor_of_x_pos: float, factor_of_y_pos: float,
                 color: str, size: float, text: str, outline: bool = False,
                 outline_size: float = 0):
        self._screen: pygame.Surface = screen
        self._screen_width: float = screen_width
        self._screen_height: float = screen_height

        self._font_dir: str = font_dir
        self._size: float = size
        self._color: pygame.Color = pygame.Color(color)
        self._text = text
        
        self._factor_of_x_pos: float = factor_of_x_pos
        self._x_pos: float = self._factor_of_x_pos * self._screen_width
        self._factor_of_y_pos: float = factor_of_y_pos
        self._y_pos: float = self._factor_of_y_pos * self._screen_height

        self._font_obj: pygame.font.Font | None = None
        self._text_obj: pygame.Surface | None = None
        self._text_rect: pygame.Rect | None = None
        
        self._outline: bool = outline
        self._outline_size: float = outline_size

        self._font_obj_outline: pygame.font.Font | None = None
        self._text_obj_outline: pygame.Surface | None = None
        self._text_rect_outline: pygame.Rect | None = None

    def draw_button(self) -> None:
        if (self._outline):
           self._font_obj_outline = pygame.font.Font(
            self._font_dir,
            self._size + self._outline_size
           ) 

           self._text_obj_outline = self._font_obj_outline.render(
            self._text, True, "Black"
           )

           self._text_rect_outline = self._text_obj_outline.get_rect(
            center=(
                    self._screen_width * self._factor_of_x_pos,
                    self._screen_height * self._factor_of_y_pos
            )
           )
           self._screen.blit(self._text_obj_outline, self._text_rect_outline)
           
        self._font_obj = pygame.font.Font(
            self._font_dir,
            self._size
        )

        self._text_obj = self._font_obj.render(
            self._text, True, self._color
           )

        self._text_rect = self._text_obj.get_rect(
            center=(
                    self._screen_width * self._factor_of_x_pos,
                    self._screen_height * self._factor_of_y_pos
            )
           )
        self._screen.blit(self._text_obj, self._text_rect)