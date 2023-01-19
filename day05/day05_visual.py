from asciimatics.effects import Sprite, Print
from asciimatics.renderers import StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.paths import Path
import re

from Dock import Dock

TESTING = True
KEYPRESS_REQUIRED_BETWEEN_MOVES = -1   # -1 for YES, 0 for NO

X = 0
Y = 1

LIFT = 1
ALIGN = 0
DROP = -1

DOCK_OFFSET = 3
LABEL_OFFSET = 1
COMMENTARY_OFFSET = 2
CRANE_TOP = 20


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


def print_stacks(screen, dock_left, stacks_top, stacks):
    return Print(
        screen,
        Dock(stacks),
        x=dock_left - 1, y=stacks_top - 1,
        colour=Screen.COLOUR_CYAN,
        clear=False,
        start_frame=0,
        stop_frame=5)


def add_crane_animation_scene(screen, scenes, movement, stacks, crane_stack, num_crates, from_stack, to_stack):
    max_stack_height = max(map(len, stacks))
    dock_width = len(stacks) * 4
    dock_left = (screen.width - dock_width) // 2
    dock_floor = screen.height - DOCK_OFFSET
    stacks_top = dock_floor - max_stack_height

    stack = stacks[from_stack if movement == LIFT else to_stack]
    stack_height = len(stack)

    if movement == LIFT:
        crate = stack[stack_height - 1]

        start_pos_y = dock_floor - LABEL_OFFSET - stack_height
        start_pos_x = dock_left + (from_stack * 4)

        end_pos_x = start_pos_x
        end_pos_y = CRANE_TOP + len(crane_stack)

        steps = abs(start_pos_y - end_pos_y)
    elif movement == DROP:
        crate = crane_stack[len(crane_stack) - 1]

        start_pos_y = CRANE_TOP + len(crane_stack) - 1
        start_pos_x = dock_left + (to_stack * 4)

        end_pos_x = start_pos_x
        end_pos_y = dock_floor - LABEL_OFFSET - stack_height - 1

        steps = abs(start_pos_y - end_pos_y)
    else:  #ALIGN
        crate = crane_stack[len(crane_stack) - 1]

        start_pos_y = CRANE_TOP + len(crane_stack) - 1
        start_pos_x = dock_left + (from_stack * 4)

        end_pos_x = dock_left + (to_stack * 4)
        end_pos_y = start_pos_y

        steps = abs(start_pos_x - end_pos_x)

    path = Path()
    path.jump_to(start_pos_x, start_pos_y)
    path.move_straight_to(end_pos_x, end_pos_y, steps)
    path.wait(100)

    final_frame = (steps * 5) + 5

    effects = [print_stacks(screen, dock_left, stacks_top, stacks),
               MovingCrate(screen, path, f"[{crate}]", start_frame=6, stop_frame=final_frame)]

    scenes.append(Scene(effects, clear=False, duration=KEYPRESS_REQUIRED_BETWEEN_MOVES if movement == DROP else 0))


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


def move(screen, scenes, stacks, crane_stack, num_crates, from_stack, to_stack):
    add_crane_animation_scene(screen, scenes, LIFT, stacks, crane_stack, num_crates, from_stack, to_stack)
    lift(stacks, crane_stack, num_crates, from_stack)

    add_crane_animation_scene(screen, scenes, ALIGN, stacks, crane_stack, num_crates, from_stack, to_stack)

    add_crane_animation_scene(screen, scenes, DROP, stacks, crane_stack, num_crates, from_stack, to_stack)
    drop(stacks, crane_stack, num_crates, to_stack)

def rearrange_crates(screen, scenes, stacks, crane_stack, move_ops):
    for num_crates, from_stack, to_stack in move_ops:
        draw_commentary(screen, f"Moving {num_crates} from {from_stack} to {to_stack}")

        for crate in range(0, num_crates):
            move(screen, scenes, stacks, crane_stack, 1, from_stack - 1, to_stack - 1)


def rearrange_crates_with_CrateMover_9001(screen, scenes, stacks, crane_stack, move_ops):
    for num_crates, from_stack, to_stack in move_ops:
        draw_commentary(screen, f"Moving {num_crates} from {from_stack} to {to_stack}")

        move(screen, scenes, stacks, crane_stack, num_crates, from_stack - 1, to_stack - 1)

    return stacks


def get_top_crates(stacks):
    answer = ''

    for stack in stacks:
        answer += stack[len(stack) - 1]

    return answer


def part1(screen):
    stacks, move_ops = read_input()

    scenes = []

    rearrange_crates(screen, scenes, stacks, [], move_ops)

    screen.play(scenes, stop_on_resize=True, repeat=False)

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
