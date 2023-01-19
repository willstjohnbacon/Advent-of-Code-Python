# -*- coding: utf-8 -*-
"""
This module implements a renderer that draws stacks of crates on a dock.
"""
from asciimatics.renderers.base import StaticRenderer

X = 0
Y = 1
DOCK_OFFSET = 3
LABEL_OFFSET = 1
COMMENTARY_OFFSET = 2


class Dock(StaticRenderer):
    """
    Renders stacks of crates on a dock.
    """

    def __init__(self, stacks):
        """
        :param stacks: The stacks of crates to be drawn on the dock
        """
        super(Dock, self).__init__()
        crates = render_crates(stacks)
        labels = render_labels(stacks)
        self._images = [crates + labels]

def render_labels(stacks):
    labels = ""

    for n in range(len(stacks)):
        labels += f" {n + 1}  "

    return labels

def render_crates(stacks):
    max_height = max(map(len, stacks))

    stack_render = ""

    for row_num in range(max_height - 1, -1, -1):
        for stack_num in range(len(stacks)):
            crate = "    " if row_num >= len(stacks[stack_num]) else f"[{stacks[stack_num][row_num]}] "
            stack_render += crate
        stack_render += "\n"

    return stack_render