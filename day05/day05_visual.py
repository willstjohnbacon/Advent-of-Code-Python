from asciimatics.effects import Sprite, Print
from asciimatics.renderers import StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.paths import Path
import re

from Dock import Dock
from Crane import Crane
from MovingCrate import MovingCrate
from MovingCraneTrolley import MovingCraneTrolley
from MovingCraneHoist import MovingCraneHoist

TESTING = True

KEYPRESS_REQUIRED_BETWEEN_MOVES = -1 if TESTING else 0  # -1 for YES, 0 for NO
# KEYPRESS_REQUIRED_BETWEEN_MOVES = 0
MOVEMENT_SPEED_FACTOR = 3
INITIAL_FRAMES = 10

X = 0
Y = 1

LIFT = 1
ALIGN = 0
DROP = -1

DOCK_OFFSET = 3
LABEL_OFFSET = 1
COMMENTARY_OFFSET = 1
MAX_LIFT_HEIGHT = 26 if TESTING else 5
CRANE_TOP = MAX_LIFT_HEIGHT - 5
CRANE_CLEARANCE = 20
TROLLEY_HEIGHT = CRANE_TOP + 3

#TEMPORARY
previous_trolley_pos = 70

def print_crane(screen, dock_left, dock_floor, dock_width):
    crane_left = dock_left - CRANE_CLEARANCE

    return Print(
        screen,
        Crane(crane_left, dock_floor, dock_width, CRANE_TOP, CRANE_CLEARANCE),
        x=crane_left, y=CRANE_TOP,
        colour=Screen.COLOUR_YELLOW,
        clear=False,
        start_frame=0,
        stop_frame=5)


def print_stacks(screen, dock_left, stacks_top, stacks):
    return Print(
        screen,
        Dock(stacks),
        x=dock_left - 1, y=stacks_top - 1,
        colour=Screen.COLOUR_CYAN,
        clear=False,
        start_frame=0,
        stop_frame=5)


def print_description(screen, dock_floor, description):
    x_pos = (screen.width - len(description)) // 2 - 1

    return Print(
        screen,
        StaticRenderer([description]),
        x=x_pos, y=dock_floor + COMMENTARY_OFFSET,
        colour=Screen.COLOUR_WHITE,
        clear=False,
        transparent=False,
        start_frame=0,
        stop_frame=5)


def calculate_path(start_pos_x, start_pos_y, end_pos_x, end_pos_y, steps):
    path = Path()
    path.jump_to(start_pos_x, start_pos_y)
    path.move_straight_to(end_pos_x, end_pos_y, steps)
    path.wait(100)
    return path


def add_crane_animation_scene(screen, scenes, description, movement, stacks, crane_stack, num_crates, from_stack,
                              to_stack):
    #TEMPORARY
    global previous_trolley_pos

    max_stack_height = max(map(len, stacks))
    dock_width = len(stacks) * 4
    dock_left = (screen.width - dock_width) // 2
    dock_floor = screen.height - DOCK_OFFSET
    stacks_top = dock_floor - max_stack_height

    stack = stacks[from_stack if movement == LIFT else to_stack]
    stack_height = len(stack)

    if movement == LIFT:
        crate = stack[stack_height - 1]
        crate_start_pos_y = dock_floor - LABEL_OFFSET - stack_height
        crate_start_pos_x = dock_left + (from_stack * 4)
        crate_end_pos_x = crate_start_pos_x
        crate_end_pos_y = MAX_LIFT_HEIGHT + len(crane_stack)
        crate_movement_steps = abs(crate_start_pos_y - crate_end_pos_y)
        crate_path = calculate_path(crate_start_pos_x, crate_start_pos_y, crate_end_pos_x, crate_end_pos_y, crate_movement_steps)

        #Trolley moves above crate to be lifted
        trolley_steps = abs(crate_start_pos_x - previous_trolley_pos) // MOVEMENT_SPEED_FACTOR
        trolley_path = calculate_path(previous_trolley_pos, TROLLEY_HEIGHT, crate_start_pos_x, TROLLEY_HEIGHT, trolley_steps)

        hoist_steps = crate_movement_steps
        hoist_down_path = calculate_path(crate_start_pos_x, crate_end_pos_y - 1, crate_start_pos_x, crate_start_pos_y - 1, hoist_steps)
        hoist_up_path = calculate_path(crate_start_pos_x, crate_start_pos_y - 1, crate_start_pos_x, crate_end_pos_y - 1, hoist_steps)

        first_trolley_frame = INITIAL_FRAMES
        final_trolley_frame = first_trolley_frame + (trolley_steps * MOVEMENT_SPEED_FACTOR)
        first_hoist_down_frame = final_trolley_frame
        final_hoist_down_frame = first_hoist_down_frame + (hoist_steps * MOVEMENT_SPEED_FACTOR)
        first_crate_frame = final_hoist_down_frame
        final_crate_frame = first_crate_frame + (crate_movement_steps * MOVEMENT_SPEED_FACTOR)
        first_hoist_up_frame = final_hoist_down_frame
        final_hoist_up_frame = first_hoist_up_frame + (hoist_steps * MOVEMENT_SPEED_FACTOR)

    elif movement == DROP:
        crate = crane_stack[len(crane_stack) - 1]
        crate_start_pos_y = MAX_LIFT_HEIGHT + len(crane_stack) - 1
        crate_start_pos_x = dock_left + (to_stack * 4)
        crate_end_pos_x = crate_start_pos_x
        crate_end_pos_y = dock_floor - LABEL_OFFSET - stack_height - 1
        crate_movement_steps = abs(crate_start_pos_y - crate_end_pos_y)
        crate_path = calculate_path(crate_start_pos_x, crate_start_pos_y, crate_end_pos_x, crate_end_pos_y, crate_movement_steps)

        #Trolley does not move
        trolley_steps = 0
        trolley_path = calculate_path(crate_end_pos_x, TROLLEY_HEIGHT, crate_end_pos_x, TROLLEY_HEIGHT, trolley_steps)

        hoist_steps = crate_movement_steps
        hoist_down_path = calculate_path(crate_end_pos_x, crate_start_pos_y - 1, crate_end_pos_x, crate_end_pos_y - 1, hoist_steps)
        hoist_up_path = calculate_path(crate_end_pos_x, crate_end_pos_y - 1, crate_end_pos_x, crate_start_pos_y - 1, hoist_steps)

        first_trolley_frame = 0
        final_trolley_frame = 1
        first_hoist_down_frame = INITIAL_FRAMES
        final_hoist_down_frame = first_hoist_down_frame + (hoist_steps * MOVEMENT_SPEED_FACTOR)
        first_crate_frame = first_hoist_down_frame
        final_crate_frame = first_crate_frame + (crate_movement_steps * MOVEMENT_SPEED_FACTOR)
        first_hoist_up_frame = final_hoist_down_frame
        final_hoist_up_frame = first_hoist_up_frame + (hoist_steps * MOVEMENT_SPEED_FACTOR)

    else:  # ALIGN
        crate = crane_stack[len(crane_stack) - 1]
        crate_start_pos_y = MAX_LIFT_HEIGHT + len(crane_stack) - 1
        crate_start_pos_x = dock_left + (from_stack * 4)
        crate_end_pos_x = dock_left + (to_stack * 4)
        crate_end_pos_y = crate_start_pos_y
        crate_movement_steps = abs(crate_start_pos_x - crate_end_pos_x) // MOVEMENT_SPEED_FACTOR
        crate_path = calculate_path(crate_start_pos_x, crate_start_pos_y, crate_end_pos_x, crate_end_pos_y, crate_movement_steps)

        #Trolley moves above stack on which crate is to be dropped
        trolley_steps = abs(crate_start_pos_x - crate_end_pos_x) // MOVEMENT_SPEED_FACTOR
        trolley_path = calculate_path(crate_start_pos_x, TROLLEY_HEIGHT, crate_end_pos_x, TROLLEY_HEIGHT, trolley_steps)

        #Hoist does not move
        hoist_steps = 0
        hoist_down_path = calculate_path(crate_end_pos_x, TROLLEY_HEIGHT + 1, crate_end_pos_x, TROLLEY_HEIGHT + 1, hoist_steps)
        hoist_up_path = hoist_down_path

        first_trolley_frame = INITIAL_FRAMES
        final_trolley_frame = first_trolley_frame + (trolley_steps * MOVEMENT_SPEED_FACTOR)
        first_hoist_down_frame = final_trolley_frame
        final_hoist_down_frame = final_trolley_frame
        first_crate_frame = first_trolley_frame
        final_crate_frame = first_crate_frame + (crate_movement_steps * MOVEMENT_SPEED_FACTOR)
        first_hoist_up_frame = final_trolley_frame
        final_hoist_up_frame = final_trolley_frame

    previous_trolley_pos = crate_end_pos_x

    effects = [
                print_description(screen, dock_floor, description),
                print_crane(screen, dock_left, dock_floor, dock_width),
                print_stacks(screen, dock_left, stacks_top, stacks),
                MovingCraneTrolley(screen, trolley_path, start_frame=first_trolley_frame, stop_frame=final_trolley_frame),
                MovingCraneHoist(screen, hoist_up_path, start_frame=first_hoist_up_frame, stop_frame=final_hoist_up_frame),
                MovingCrate(screen, crate_path, f"[{crate}]", start_frame=first_crate_frame, stop_frame=final_crate_frame),
                MovingCraneHoist(screen, hoist_down_path, moving_up=False, start_frame=first_hoist_down_frame, stop_frame=final_hoist_down_frame),
            ]

    scenes.append(Scene(effects, clear=False, duration=KEYPRESS_REQUIRED_BETWEEN_MOVES if movement == DROP else 0))


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


def move(screen, scenes, description, stacks, crane_stack, num_crates, from_stack, to_stack):
    add_crane_animation_scene(screen, scenes, description, LIFT, stacks, crane_stack, num_crates, from_stack, to_stack)
    lift(stacks, crane_stack, num_crates, from_stack)

    add_crane_animation_scene(screen, scenes, description, ALIGN, stacks, crane_stack, num_crates, from_stack, to_stack)

    add_crane_animation_scene(screen, scenes, description, DROP, stacks, crane_stack, num_crates, from_stack, to_stack)
    drop(stacks, crane_stack, num_crates, to_stack)


def rearrange_crates(screen, scenes, stacks, crane_stack, move_ops):
    for num_crates, from_stack, to_stack in move_ops:
        description = f"Moving {num_crates} from {from_stack} to {to_stack}"

        for crate in range(0, num_crates):
            move(screen, scenes, description, stacks, crane_stack, 1, from_stack - 1, to_stack - 1)


def rearrange_crates_with_CrateMover_9001(screen, scenes, stacks, crane_stack, move_ops):
    for num_crates, from_stack, to_stack in move_ops:
        description = f"Moving {num_crates} from {from_stack} to {to_stack}"

        move(screen, scenes, description, stacks, crane_stack, num_crates, from_stack - 1, to_stack - 1)

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
    top_crates = get_top_crates(stacks)

    max_stack_height = max(map(len, stacks))
    dock_width = len(stacks) * 4
    dock_left = (screen.width - dock_width) // 2
    dock_floor = screen.height - DOCK_OFFSET
    stacks_top = dock_floor - max_stack_height

    effects = [print_description(screen, dock_floor, f"     The top crates are {top_crates}     "),
               print_stacks(screen, dock_left, stacks_top, stacks)]

    scenes.append(Scene(effects, clear=False, duration=-1))

    screen.play(scenes, stop_on_resize=True, repeat=False)

    return top_crates


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
