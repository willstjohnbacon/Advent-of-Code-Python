from asciimatics.screen import Screen
from Animator import Animator, NONE, LIFT, ALIGN, DROP
import re

TESTING = True


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


def move(animator, description, stacks, crane_stack, num_crates, from_stack, to_stack):
    animator.add_scene(description, LIFT, stacks, crane_stack, num_crates, from_stack, to_stack)
    lift(stacks, crane_stack, num_crates, from_stack)

    animator.add_scene(description, ALIGN, stacks, crane_stack, num_crates, from_stack, to_stack)

    animator.add_scene(description, DROP, stacks, crane_stack, num_crates, from_stack, to_stack)
    drop(stacks, crane_stack, num_crates, to_stack)


def rearrange_crates(animator, stacks, crane_stack, move_ops):
    for num_crates, from_stack, to_stack in move_ops:
        description = f"Moving {num_crates} from {from_stack} to {to_stack}"

        for crate in range(0, num_crates):
            move(animator, description, stacks, crane_stack, 1, from_stack - 1, to_stack - 1)


def rearrange_crates_with_CrateMover_9001(animator, stacks, crane_stack, move_ops):
    for num_crates, from_stack, to_stack in move_ops:
        description = f"Moving {num_crates} from {from_stack} to {to_stack}"

        move(animator, description, stacks, crane_stack, num_crates, from_stack - 1, to_stack - 1)

    return stacks


def get_top_crates(stacks):
    answer = ''

    for stack in stacks:
        answer += stack[len(stack) - 1]

    return answer


def part1(screen):
    stacks, move_ops = read_input()

    animator = Animator(screen, stacks)

    rearrange_crates(animator, stacks, [], move_ops)

    top_crates = get_top_crates(stacks)
    animator.add_scene(f"       The top crates are {top_crates}       ", NONE, stacks, [], 0, 0, 0)
    animator.add_scene(f"             Press SPACE to exit             ", NONE, stacks, [], 0, 0, 0)

    animator.play()

    return top_crates


def part2(screen):
    stacks, move_ops = read_input()

    animator = Animator(screen, stacks)

    rearrange_crates_with_CrateMover_9001(animator, stacks, [], move_ops)

    top_crates = get_top_crates(stacks)
    animator.add_scene(f"       The top crates are {top_crates}       ", NONE, stacks, [], 0, 0, 0)
    animator.add_scene(f"             Press SPACE to exit             ", NONE, stacks, [], 0, 0, 0)

    animator.play()
    return get_top_crates(stacks)


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

# Screen.wrapper(part1)
Screen.wrapper(part2)
