"""
"""
from typing_extensions import override
from drawable import Drawable


class DrawableDecorator(Drawable):
    """The base decorator class for to fulfill the
        decorator design pattern
    """

    def __init__(self, drawable: Drawable) -> None:
        """Constructor for the Drawable Decorator class

            Args:
            drawable (Drawable): The object to decorate
        """
        super().__init__(drawable.screen, drawable._factor_of_x_pos,
                         drawable._factor_of_y_pos, drawable.image_dir,
                         drawable.size, drawable.data)
        self._drawable = drawable

    @override
    def draw(self) -> None:
        """Implementation of draw function from base class
        """
        self.drawable.draw()

    @override
    def dynamically_draw(self) -> None:
        """Implementation of dynamically_draw function from base class
        """
        self.drawable.dynamically_draw()

    @override
    def _adjust_to_changes(self) -> None:
        """Implementation of _adjust_to_changes function from base class
        """
        self.drawable._adjust_to_changes()

    @property
    def drawable(self) -> Drawable:
        """Getter for drawable variable

        Returns:
            _drawable (Drawable):
            Either concrete component or another
            decorator
        """
        return self._drawable

    @drawable.setter
    def drawable(self, drawble: Drawable) -> None:
        """Setter for drawable variable

        Args:
            drawable (Drawable):
            Either concrete component or another
            decorator
        """
        self._drawable = drawble
        self._drawable.resize_screen()

    @property
    def original_size(self) -> float:
        """Getter to get the original size
           property from the first concrete component
           used in decorator chain

        Returns:
            size (float): the size property from the first
            concrete component used in decorator chain
        """
        drawable = self._drawable
        while isinstance(drawable, DrawableDecorator):
            drawable = drawable.drawable
        return drawable.size

    @original_size.setter
    def original_size(self, size: float) -> None:
        """Setter for the original size property

        Args:
            size (float): value to set the size of
            the first concrete component used in
            decorator chain
        """
        drawable = self._drawable
        while isinstance(drawable, DrawableDecorator):
            drawable = drawable.drawable

        drawable.size = size
