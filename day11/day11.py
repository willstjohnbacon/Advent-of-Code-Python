def part1():
    for line in file.readlines():
        print("Input Line: ", line)
    return

def part2():
    file.seek(0)
    return



Testing = True
if Testing:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
