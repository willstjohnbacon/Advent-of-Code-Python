from asciimatics.effects import Sprite
from asciimatics.renderers import StaticRenderer
from asciimatics.screen import Screen


class MovingCrate(Sprite):
    """
    Plots a crate moving along the given path.
    """

    def __init__(self, screen, path, crate="[ ]", colour=Screen.COLOUR_WHITE, start_frame=0,
                 stop_frame=0):
        """
        See :py:obj:`.Sprite` for details.
        """
        super(MovingCrate, self).__init__(
            screen,
            renderer_dict={
                "default": StaticRenderer(images=[crate])
            },
            path=path,
            colour=colour,
            clear=True,
            start_frame=start_frame,
            stop_frame=stop_frame)
