
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
    file.seek(0)
    return


Testing = False
if Testing:
    file = open("sampleInput.txt", "r")

else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
