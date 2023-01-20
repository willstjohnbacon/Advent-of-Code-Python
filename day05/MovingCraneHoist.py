from asciimatics.effects import Sprite
from asciimatics.renderers import StaticRenderer
from asciimatics.screen import Screen


class MovingCraneHoist(Sprite):
    """
    Plots the crane trolley moving along the given path.
    """

    def __init__(self, screen, path, moving_up=True, colour=Screen.COLOUR_YELLOW, start_frame=0,
                 stop_frame=0):
        """
        See :py:obj:`.Sprite` for details.
        """
        super(MovingCraneHoist, self).__init__(
            screen,
            renderer_dict={
                "default": StaticRenderer(images=["|\nƸ"])
            },
            path=path,
            colour=colour,
            clear=moving_up,
            start_frame=start_frame,
            stop_frame=stop_frame)
