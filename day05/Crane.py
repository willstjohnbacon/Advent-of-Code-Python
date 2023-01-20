# -*- coding: utf-8 -*-
"""
This module implements a renderer that draws stacks of crates on a dock.
"""
from asciimatics.renderers.base import StaticRenderer


class Crane(StaticRenderer):
    """
    Renders a dockside crane
    """

    def __init__(self, crane_left, dock_floor, dock_width, crane_top, crane_clearance):
        super(Crane, self).__init__()
        crane = render_crane(crane_left, dock_floor, dock_width, crane_top, crane_clearance)
        self._images = [crane]


def render_crane(crane_left, dock_floor, dock_width, crane_top, crane_clearance):
    bridge_width = dock_width + (2 * crane_clearance) - 15
    tower_height = dock_floor - crane_top - 7

    crane = "  /XXX\_" + "_" * bridge_width + "/XXX\ \n" + \
            "XX|XXX|X" + "X" * bridge_width + "|XXX|XX \n" +\
            "  \XXX/ " + " " * bridge_width + "\XXX/ \n" + \
            ("   XxX  " + " " * bridge_width + " XxX \n") * tower_height +\
            "  /XxX\ " + " " * bridge_width + "/XxX\ \n" +\
            " /|XxX|\ " + " " * (bridge_width - 2) + "/|XxX|\ \n" +\
            "ooooooooo" + " " * (bridge_width - 3) + "ooooooooo"

    return crane
