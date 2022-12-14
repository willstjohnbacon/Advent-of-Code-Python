TESTING = False

def printCave(cave):
        for y in range(len(cave)):
            for x in range(len(cave[y])):
                print(cave[y][x], end='')
            print()

def flowSand(cave, min_width):
    sand_at_rest = 0

    while True:
        sand_posX = 500 - min_width
        sand_posY = 0

        if cave[sand_posY][sand_posX] == "o": #Cave has filled
            return sand_at_rest

        cave[sand_posY][sand_posX] = "o"

        sand_moved = True

        while sand_moved:
            new_posX = sand_posX
            new_posY = sand_posY

            if sand_posY + 1 == len(cave): #Sand is running into the endless abyss
                return sand_at_rest

            if cave[sand_posY + 1][sand_posX] == ".":
                new_posX = sand_posX
                new_posY = sand_posY + 1
            elif cave[sand_posY + 1][sand_posX - 1] == ".":
                new_posX = sand_posX - 1
                new_posY = sand_posY + 1
            elif cave[sand_posY + 1][sand_posX + 1] == ".":
                new_posX = sand_posX + 1
                new_posY = sand_posY + 1
            else:
                sand_moved = False
                sand_at_rest += 1

            cave[sand_posY][sand_posX] = "."
            cave[new_posY][new_posX] = "o"

            sand_posX = new_posX
            sand_posY = new_posY

def determineDimensions(formations):
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

    return min_width, max_width, depth

def mapCave (cave, formations, min_width):
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

def part1():
    if TESTING:
        file = open("sampleInput.txt", "r")
    else:
        file = open("input.txt", "r")

    file.seek(0)
    formations = [line.rstrip().split(" -> ") for line in file]

    min_width, max_width, depth = determineDimensions(formations)

    cave = [["." for x in range(max_width - min_width)] for y in range(depth)]
    cave[0][500 - min_width] = "+"

    mapCave(cave, formations, min_width)
    printCave(cave)

    sand_at_rest = flowSand(cave, min_width)
    printCave(cave)
    return sand_at_rest

def part2():
    if TESTING:
        file = open("sampleInput_part2.txt", "r")
    else:
        file = open("input_part2.txt", "r")

    file.seek(0)
    formations = [line.rstrip().split(" -> ") for line in file]

    min_width, max_width, depth = determineDimensions(formations)

    cave = [["." for x in range(max_width - min_width)] for y in range(depth)]
    cave[0][500 - min_width] = "+"

    mapCave(cave, formations, min_width)
    printCave(cave)

    sand_at_rest = flowSand(cave, min_width)
    printCave(cave)
    return sand_at_rest

print("Part 1: ", part1())
print("Part 2: ", part2())
