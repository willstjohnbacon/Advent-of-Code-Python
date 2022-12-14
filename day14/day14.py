TESTING = False

def printCave(cave):
        for y in range(len(cave)):
            for x in range(len(cave[y])):
                print(cave[y][x], end='')
            print()

def part1():
    file.seek(0)
    formations = [line.rstrip().split(" -> ") for line in file]

    min_width = 999999999
    max_width = 0
    depth = 0

    for formation in formations:
        for pointnum in range(len(formation)):
            x = int(formation[pointnum][0:3])
            y = int(formation[pointnum][4:])
            if x < min_width:
                min_width = x
            if x > max_width:
                max_width = x
            if y > depth:
                depth = y

    print(f"Cave span {min_width} to {max_width} and depth {depth}")

    max_width += 1
    depth += 1
    cave = [["." for x in range(max_width - min_width)] for y in range(depth)]

    cave[0][500 - min_width] = "+"

    for formation in formations:
        for pointnum in range(len(formation) - 1):
            x1 = int(formation[pointnum][0:3]) - min_width
            y1 = int(formation[pointnum][4:])
            x2 = int(formation[pointnum + 1][0:3]) - min_width
            y2 = int(formation[pointnum + 1][4:])

            if (x1 != x2) and (y1 != y2):
                print(f"ERROR: diagonal line in {formation}: ({x1},{y1}) -> ({x2},{y2}")
                exit(1)

            if (y1 == y2): #horizontal line
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    cave[y1][x] = "#"
            else: #vertical line
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    cave[y][x1] = "#"

    printCave(cave)
    return

def part2():
    file.seek(0)
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
