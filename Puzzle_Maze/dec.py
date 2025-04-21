from abc import ABC, abstractmethod
import pygame


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
    
    @abstractmethod
    def dynamically_draw(self):
        pass

    @abstractmethod
    def _adjust_to_new_screen_size(self):
        pass

    def resize_screen(self):
        self._screen_width, self._screen_height = self._screen.get_size()

    @property
    def screen(self):
        return self._screen
    
    @property
    def screen_width(self):
        return self._screen_width
    
    @property
    def screen_height(self):
        return self._screen_height
    
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
    def size(self):
        return self._size
    
    @size.setter
    def size(self, size):
        self._size = size

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

from abc import ABC, abstractmethod
from drawable import Drawable


class DrawableDecorator(Drawable):
    def __init__(self, drawable: Drawable):
        super().__init__(drawable.screen, drawable._factor_of_x_pos, 
                             drawable._factor_of_y_pos, drawable.image_dir)
        self._drawable = drawable

    
    @property
    def dec_rect(self):
        return self._dec_rect
    @property
    def drawable(self):
        return self._drawable
    
    @dec_rect.setter
    def dec_rect(self, rect):
        self._dec_rect = rect
    

    @property
    def size(self):
        drawable = self._drawable
        while isinstance(drawable, DrawableDecorator):
            drawable = drawable.drawable
        return drawable.size
    
    @size.setter
    def size(self, size):
        drawable = self._drawable
        while isinstance(drawable, DrawableDecorator):
            drawable = drawable.drawable
        
        drawable.size = size


    @property
    def dec_surface(self):
        return self._dec_surface
    
    @dec_surface.setter
    def dec_surface(self, surface):
        self._dec_surface = surface

from drawable import Drawable
import pygame


class Text(Drawable):
    def __init__(self, screen: pygame.Surface, factor_of_x_pos: float,
                    factor_of_y_pos: float, image_dir: str, size: int, text,
                    color):
            super().__init__(screen, factor_of_x_pos, factor_of_y_pos,
                             image_dir)
            self._size = size
            print("Here", self._size)
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
    
    def dynamically_draw(self):
        self._adjust_to_new_screen_size()
        self.draw()

    def _adjust_to_new_screen_size(self):
        self.resize_screen()
        self._font = pygame.font.Font(
                self.image_dir, int(self._size)
            )
        self.surface = self._font.render(self._text, True, self._color)
        self.rect = self.surface.get_rect(
                center=(
                    self.x_pos, self.y_pos
                )
            )

    @property
    def text(self):
        return self._text
    
from drawabledecorator import DrawableDecorator
from text import Text
import pygame


class Outline(DrawableDecorator):
    def __init__(self, drawable: Text, color: str, outline_size):
        super().__init__(drawable)
        self._color = color
        self._outline_size = outline_size
        self._font = pygame.font.Font(
                self.drawable.image_dir, int(self.size + self._outline_size)
            )
        self._surface = self._font.render(self.drawable.text, True,
                                                self._color)
        self._rect = self._surface.get_rect(
                center=(
                    self.drawable.x_pos, self.drawable.y_pos
                )
            )
        
    def draw(self):
            self.drawable.screen.blit(self._surface, self._rect)
            self.drawable.draw()
    
    def dynamically_draw(self):
        self._adjust_to_new_screen_size()
        self.drawable._adjust_to_new_size()
        self.draw()

    def _adjust_to_new_screen_size(self):
        self.drawable.resize_screen()
        self.drawable._adjust_to_new_screen_size()

        self._font = pygame.font.Font(
                self.drawable.image_dir, int(self.size) + self._outline_size
            )
        self.surface = self._font.render(self.drawable.text, True, self._color)
        self.rect = self.surface.get_rect(
                center=(
                    self.drawable.x_pos, self.drawable.y_pos
                )
            )

from drawabledecorator import DrawableDecorator
from text import Text
import pygame


class Button(DrawableDecorator):
    def __init__(self, image_dir: str, drawable):
        super().__init__(drawable)
        self._button_image_dir = image_dir
        self._surface: pygame.Surface = pygame.image.load(
            self._button_image_dir)
        self._button_width, self._button_height = self._surface.get_size()
        self._rect: pygame.Rect = self._surface.get_rect(
            center=(
                    self.drawable.x_pos, self.drawable.y_pos))
        self.size = self._button_height
        
    def draw(self):
        self.drawable.screen.blit(self._surface, self._rect)
        self.drawable.draw()
    
    def dynamically_draw(self):
        if self.drawable.screen.get_size() != (self.drawable.screen_width,
                                               self.drawable.screen_width):
            self._adjust_to_new_screen_size()
            self.size = self._button_height
            self.drawable._adjust_to_new_screen_size()
        self.draw()

    def _adjust_to_new_screen_size(self):
        screen_width, screen_height = self.drawable.screen.get_size()
        change_in_screen_width: float = screen_width / self.drawable.screen_width
        change_in_screen_height: float = screen_height / self.drawable.screen_height

        self._button_width = change_in_screen_width * self._button_width
        self._button_height = change_in_screen_height * self._button_height
        self.drawable.resize_screen()
    
        self._surface = pygame.transform.scale(
                self._surface,
                (self._button_width, self._button_height))
        self._rect = self._surface.get_rect(
            center=(
                    self.drawable.x_pos, self.drawable.y_pos
                    )
        )
