import pygame
from abc import ABC, abstractmethod

class Drawable(ABC):
    def __init__(self, screen: pygame.Surface, factor_of_x_pos: float,
                 factor_of_y_pos: float, image_dir: str):
        self._screen = screen
        self._screen_width, self._screen_height = self._screen.get_size()
        self._factor_of_x_pos = factor_of_x_pos
        self._factor_of_y_pos = factor_of_y_pos
        self._rect = None
        self._surface = None
        self._image_dir = image_dir

    @abstractmethod
    def draw(self):
        pass
    
    def resize_screen(self):
        self._screen_width, self._screen_height = self._screen.get_size()

    @property
    def screen(self):
        return self._screen
    
    @property
    def x_pos(self):
        return self._screen_width * self._factor_of_x_pos
    
    @property
    def y_pos(self):
        return self._screen_height * self._factor_of_y_pos
    
    @property
    def image_dir(self):
        return self._image_dir
    
    @image_dir.setter
    def image_dir(self, image_dir):
        self._image_dir = image_dir

    @property
    def rect(self):
        return self._rect
    
    @rect.setter
    def rect(self, rect):
        self._rect = rect
    
    @property
    def surface(self):
        return self._surface
    
    @surface.setter
    def surface(self, surface):
        self._surface = surface

class DrawableDecorator(Drawable, ABC):
    def __init__(self, drawable: Drawable):
        self._drawable = drawable
        self._dec_surface = None
        self._dec_rect = None

    @abstractmethod
    def draw(self):
        pass
    
    @property
    def dec_rect(self):
        return self._dec_rect
    @dec_rect.setter
    def dec_rect(self, rect):
        self._dec_rect = rect
    
    @property
    def dec_surface(self):
        return self._dec_surface
    @dec_rect.setter
    def dec_surface(self, surface):
        self._dec_surface = surface

class Text(Drawable):
    def __init__(self, screen: pygame.Surface, factor_of_x_pos: float,
                    factor_of_y_pos: float, image_dir: str, size: int, text,
                    color):
            super().__init__(screen, factor_of_x_pos, factor_of_y_pos,
                             image_dir)
            self._size = size
            self._text = text
            self._color = color
            self._font = pygame.font.Font(
                self.image_dir, int(self._size)
            )
            self.surface = self._font.render(self._text, True, self._color)
            self.rect = self.surface.get_rect(
                center=(
                    self.x_pos, self.y_pos
                )
            )

    def draw(self):
        self.screen.blit(self.surface, self.rect)

    def resize_screen_with_text(self, new_size):
        super().resize_screen()
        self._size = new_size


class OutlineTextDecorator(DrawableDecorator):
    def __init__(self, drawable: Text, outline_color: str, outline_size):
        super().__init__(drawable)
        self._outline_color = outline_color
        self._outline_size = outline_size
        self._dec_font = pygame.font.Font(
                self.image_dir, int(drawable.size + outline_size)
            )
        self.dec_surface = self._dec_font.render(drawable.text, True, self._outline_color)
        self.dec_rect = self.dec_surface.get_rect(
                center=(
                    drawable.x_pos, drawable.y_pos
                )
            )
        
        def draw(self):
            self.drawable.screen.blit(self.dec_surface, self.dec_rect)
            self.drawable.draw()
