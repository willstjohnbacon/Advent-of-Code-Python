from asciimatics.effects import Sprite, Print
from asciimatics.renderers import StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.paths import Path
from time import sleep
import re

from Dock import Dock

TESTING = True
X = 0
Y = 1
DOCK_OFFSET = 3
LABEL_OFFSET = 1
COMMENTARY_OFFSET = 2

class Plot(Sprite):
    """
    Sample Sprite that simply plots an "X" for each step in the path.  Useful
    for plotting a path to the screen.
    """

    def __init__(self, screen, path, crate="[ ]", colour=Screen.COLOUR_WHITE, start_frame=0,
                 stop_frame=0):
        """
        See :py:obj:`.Sprite` for details.
        """
        super(Plot, self).__init__(
            screen,
            renderer_dict={
                "default": StaticRenderer(images=[crate])
            },
            path=path,
            colour=colour,
            clear=True,
            start_frame=start_frame,
            stop_frame=stop_frame)


# def draw_stack_labels(screen, dock_start, stacks):
#     stack_numbers = ""
#
#     for n in range(len(stacks)):
#         stack_numbers += f" {n + 1}  "
#
#     screen.print_at(stack_numbers, dock_start[X], dock_start[Y])


# def draw_crates(screen, dock_start, stacks):
#     for stack_num, stack in enumerate(stacks):
#         x_pos = dock_start[X] + (stack_num * 4)
#
#         for level, crate in enumerate(stack):
#             y_pos = dock_start[Y] - level - LABEL_OFFSET
#             screen.print_at(f"[{crate}]", x_pos, y_pos)


def draw_stacks(screen, stacks):
    return
    # dock_width = len(stacks) * 4
    # dock_height = screen.height - DOCK_OFFSET
    # dock_start = ((screen.width - dock_width) // 2, dock_height)
    #
    # screen.clear_buffer(Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK,
    #                     dock_start[X], dock_start[Y] - dock_height, dock_width, dock_height)
    #
    # draw_stack_labels(screen, dock_start, stacks)
    # draw_crates(screen, dock_start, stacks)
    #
    # screen.refresh()
    # sleep(3) # replace with press key

def print_stacks(screen, dock_left, dock_top, stacks):
    return Print(
        screen,
        Dock(stacks),
        x=dock_left - 1, y=dock_top - 1,
        colour=Screen.COLOUR_CYAN,
        clear=False,
        start_frame=0,
        stop_frame=5)


def animate_crate_lift(screen, stacks, crane_stack, crates_to_lift, stack_num):
    dock_width = len(stacks) * 4
    dock_left = (screen.width - dock_width) // 2
    dock_bottom = screen.height - DOCK_OFFSET
    max_stack_height = max(map(len, stacks))
    dock_top = dock_bottom - max_stack_height

    stack = stacks[stack_num]
    stack_height = len(stack)
    crate = stack[stack_height - 1]
    crate_pos_y = dock_bottom - LABEL_OFFSET - stack_height
    crate_pos_x = dock_left + (stack_num * 4)

    scenes = []

    # Scene 1.
    path = Path()
    path.jump_to(crate_pos_x, crate_pos_y)
    path.move_straight_to(crate_pos_x, crate_pos_y - 10, 10)
    path.wait(30)

    effects = [
        print_stacks(screen, dock_left, dock_top, stacks),
        Plot(screen, path, f"[{crate}]", start_frame=10, stop_frame=300)
    ]

    scenes.append(Scene(effects))
    screen.play(scenes, stop_on_resize=True, repeat=False)


def draw_commentary(screen, message):
    message_row = screen.height - DOCK_OFFSET + COMMENTARY_OFFSET

    screen.clear_buffer(Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK, 0, message_row, screen.width, 1)

    screen.print_at(message, (screen.width - len(message)) // 2, message_row)

    screen.refresh()

def is_stack_line(line):
    return "[" in line


def is_move_line(line):
    return line.startswith("move")


def add_move_op(line, move_ops):
    move_op = re.match(r"move (\d+) from (\d+) to (\d+)", line)
    move_ops.append((int(move_op[1]), int(move_op[2]), int(move_op[3])))


def is_stack_num_line(line):
    return line.startswith(" 1")


def count_stacks(line):
    stack_nums = re.findall(r"\d+", line)
    num_stacks = len(stack_nums)
    return num_stacks


def parse_stack_info(stack_info, num_stacks):
    stacks = [[] for _ in range(0, num_stacks)]

    for row_num, row in enumerate(reversed(stack_info)):
        row = row.ljust(num_stacks * 4)

        for stack_num in range(0, num_stacks):
            crate = row[(stack_num * 4) + 1]

            if crate != " ":
                stacks[stack_num].append(crate)

    return stacks


def read_input():
    file.seek(0)

    stack_info = []
    move_ops = []
    num_stacks = "no"

    for line in file.readlines():
        if is_stack_line(line):
            stack_info.append(line.rstrip())
        elif is_move_line(line):
            add_move_op(line, move_ops)
        elif is_stack_num_line(line):
            num_stacks = count_stacks(line)

    stacks = parse_stack_info(stack_info, num_stacks)

    return stacks, move_ops


def lift(stacks, crane_stack, crates_to_lift, stack_num):
    for crate in range(0, crates_to_lift):
        crane_stack.append(stacks[stack_num].pop())


def drop(stacks, crane_stack, crates_to_drop, stack_num):
    for crate in range(0, crates_to_drop):
        stacks[stack_num].append(crane_stack.pop())


def move(screen, stacks, crane_stack, num_crates, from_stack, to_stack):
    animate_crate_lift(screen, stacks, crane_stack, num_crates, from_stack)
    lift(stacks, crane_stack, num_crates, from_stack)

    animate_crate_align(screen, stacks, crane_stack, num_crates, from_stack, to_stack)

    animate_crate_drop(screen, stacks, crane_stack, num_crates, to_stack)
    drop(stacks, crane_stack, num_crates, to_stack)


def rearrange_crates(screen, stacks, crane_stack, move_ops):
    for num_crates, from_stack, to_stack in move_ops:
        draw_commentary(screen, f"Moving {num_crates} from {from_stack} to {to_stack}")

        for crate in range(0, num_crates):
            move(screen, stacks, crane_stack, 1, from_stack - 1, to_stack - 1)

        # draw_stacks(screen, stacks)


def rearrange_crates_with_CrateMover_9001(screen, stacks, crane_stack, move_ops):
    for num_crates, from_stack, to_stack in move_ops:
        draw_commentary(screen, f"Moving {num_crates} from {from_stack} to {to_stack}")

        move(screen, stacks, crane_stack, num_crates, from_stack - 1, to_stack - 1)

        # draw_stacks(screen, stacks)

    return stacks


def get_top_crates(stacks):
    answer = ''

    for stack in stacks:
        answer += stack[len(stack) - 1]

    return answer


def part1(screen):
    stacks, move_ops = read_input()

    # draw_stacks(screen, stacks)

    rearrange_crates(screen, stacks, [], move_ops)

    return get_top_crates(stacks)


# def part2():
#     stacks, move_ops = read_input()
#
#     print(f"Stacks: {stacks}")
#     print(f"Move Ops: {move_ops}")
#     print()
#
#     rearrange_crates_with_CrateMover_9001(screen, stacks, [], move_ops)
#
#     return get_top_crates(stacks)


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")


Screen.wrapper(part1)