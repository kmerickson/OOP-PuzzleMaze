import pygame


class Text():  
    def __init__(self, font_dir: str, screen: pygame.Surface, screen_width: float,
                 screen_height: float, factor_of_x_pos: float, factor_of_y_pos: float,
                 color: str, size: float, text: str, outline: bool = False,
                 outline_size: float = 0, hover_color: str = None,
                 hover_outline: bool = False):
        self._screen: pygame.Surface = screen
        self._screen_width: float = screen_width
        self._screen_height: float = screen_height

        self._font_dir: str = font_dir
        self._size: float = size
        self._color: pygame.Color = pygame.Color(color)
        if hover_color is not None:
            self._hover_color: pygame.Color = pygame.Color(hover_color)
        else:
            self._hover_color = None
        self._hover_outline: bool = hover_outline
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

    def draw_hover_state(self) -> None:
        if self._hover_color is None and self._hover_outline is False:
            return
        self.draw_button(True)

    @property
    def size(self) -> float:
        """_summary_

        Returns:
            float: _description_
        """
        return self._size
    
    @size.setter
    def size(self, size: float) -> None:
        """_summary_

        Args:
            size (float): _description_
        """
        self._size = size
    def update_on_screen_resize(self, new_size: float, new_screen_width: float, new_screen_height):
        self._size = new_size
        self._screen_width = new_screen_width
        self._screen_height = new_screen_height
        self.draw_button()

    def draw_button(self, hover: bool = False) -> None:
        if (hover and self._hover_outline) or (not hover and self._outline):
            self._font_obj_outline = pygame.font.Font(
                self._font_dir,
                int(self._size + self._outline_size)
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
        
        color_to_use: str
        if hover:
            color_to_use = self._hover_color
        else:
            color_to_use = self._color
        self._font_obj = pygame.font.Font(
            self._font_dir,
            int(self._size)
        )

        self._text_obj = self._font_obj.render(
            self._text, True, color_to_use
           )

        self._text_rect = self._text_obj.get_rect(
            center=(
                    self._screen_width * self._factor_of_x_pos,
                    self._screen_height * self._factor_of_y_pos
            )
           )
        self._screen.blit(self._text_obj, self._text_rect)