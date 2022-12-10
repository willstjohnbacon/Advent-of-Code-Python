
def part1():
    program = [line.split() for line in file]
    cycle = 0
    register = 1
    signal_strength = 0
    for command in program:
        for c in range(1 if command[0] == "noop" else 2):
            cycle += 1
            if cycle in (20, 60, 100, 140, 180, 220):
                signal_strength += cycle * register
        if command[0] == "addx":
            register += int(command[1])
    return signal_strength

def part2():
    program = [line.split() for line in file]
    cycle = 0
    register = 1
    signal_strength = 0
    display = []
    row = ""
    for instruction in program:
        for c in range(1 if instruction[0] == "noop" else 2):
            cycle += 1
            row += "#" if len(row) in range(register - 1, register + 2) else "."
            if len(row) == 40:
                display.append(row)
                row = ""
            if cycle in (20, 60, 100, 140, 180, 220):
                signal_strength += cycle * register
        if instruction[0] == "addx":
            register += int(instruction[1])
    # Use the * to print the lines on different lines
    return print(*display, sep="\n")


Testing = False
if Testing:
    file = open("sampleInput.txt", "r")

else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
file.close()
file = open("input.txt", "r")
print("Part 2: ", part2())
