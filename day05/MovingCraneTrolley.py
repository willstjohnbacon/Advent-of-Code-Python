from asciimatics.effects import Sprite
from asciimatics.renderers import StaticRenderer
from asciimatics.screen import Screen


class MovingCraneTrolley(Sprite):
    """
    Plots the crane trolley moving along the given path.
    """

    def __init__(self, screen, path, colour=Screen.COLOUR_YELLOW, start_frame=0,
                 stop_frame=0):
        """
        See :py:obj:`.Sprite` for details.
        """
        super(MovingCraneTrolley, self).__init__(
            screen,
            renderer_dict={
                "default": StaticRenderer(images=["ovo\n |\n Ƹ"])
            },
            path=path,
            colour=colour,
            clear=True,
            start_frame=start_frame,
            stop_frame=stop_frame)
