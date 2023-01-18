import re

TESTING = True

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
    num_stacks = float('-inf')

    for line in file.readlines():
        move_op = re.match("move (\d+) from (\d+) to (\d+)", line)

        if move_op:
            move_ops.append((int(move_op[1]), int(move_op[2]), int(move_op[3])))
        elif "[" in line:
            stack_info.append(line.rstrip())
        else:
            stack_nums = re.findall("\d+", line)
            num_stacks = max(num_stacks, len(stack_nums))

    print(f"There are {num_stacks} stacks")

    stacks = parse_stack_info(stack_info, num_stacks)

    return stacks, move_ops

def lift(stacks, crane_stack, crates_to_lift, stack_num):
    for crate in range(0, crates_to_lift):
        crane_stack.append(stacks[stack_num].pop())

def drop(stacks, crane_stack, crates_to_drop, stack_num):
    for crate in range(0, crates_to_drop):
        stacks[stack_num].append(crane_stack.pop())

def part1():
    stacks, move_ops = read_input()

    print(f"Stacks: {stacks}")
    print(f"Move Ops: {move_ops}")
    print()

    crane_stack = []

    for num_crates, from_stack, to_stack in move_ops:
        print(f"Moving {num_crates} from {from_stack} to {to_stack}")

        for crate in range(0, num_crates):
            lift(stacks, crane_stack, 1, from_stack - 1)
            drop(stacks, crane_stack, 1, to_stack - 1)

        print(stacks)

    answer = ''

    for stack in stacks:
        answer += stack[len(stack) - 1]

    return answer


def part2():
    stacks, move_ops = read_input()

    print(f"Stacks: {stacks}")
    print(f"Move Ops: {move_ops}")
    print()

    crane_stack = []

    for num_crates, from_stack, to_stack in move_ops:
        print(f"Moving {num_crates} from {from_stack} to {to_stack}")

        lift(stacks, crane_stack, num_crates, from_stack - 1)
        drop(stacks, crane_stack, num_crates, to_stack - 1)

        print(stacks)

    answer = ''

    for stack in stacks:
        answer += stack[len(stack) - 1]

    return answer


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
