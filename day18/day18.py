TESTING = False

def part1():
    file.seek(0)
    lines = [line.rstrip() for line in file]

    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    min_z = float('inf')
    max_z = float('-inf')

    cubes = {}

    for line in lines:
        cube = [int(val) for val in line.split(",")]
        cubes.update({tuple(cube): 6})
        x, y, z = cube

        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        min_z = min(min_z, z)
        max_z = max(max_z, z)

    print(cubes)
    print(min_x, max_x, min_y, max_y, min_z, max_z)

    surfaces = [[[0 for z in range(0, max_z + 1)] for y in range(0, max_y + 1)] for x in range(0, max_x + 1)]
    print(surfaces)

    for cube in cubes:
        x, y, z = cube
        surfaces[x][y][z] = 6

    print(surfaces)

    for x in range(0, max_x + 1):
        for y in range(0, max_y + 1):
            for z in range(0, max_z + 1):
                if surfaces[x][y][z] > 0:
                    if tuple([x+1, y, z]) in cubes:
                        surfaces[x][y][z] -= 1
                    if tuple([x-1, y, z]) in cubes:
                        surfaces[x][y][z] -= 1
                    if tuple([x, y+1, z]) in cubes:
                        surfaces[x][y][z] -= 1
                    if tuple([x, y-1, z]) in cubes:
                        surfaces[x][y][z] -= 1
                    if tuple([x, y, z+1]) in cubes:
                        surfaces[x][y][z] -= 1
                    if tuple([x, y, z-1]) in cubes:
                        surfaces[x][y][z] -= 1

    print(surfaces)
    surface_area = 0

    for x in range(0, len(surfaces)):
        for y in range(0, len(surfaces[x])):
            for z in range(0, len(surfaces[x][y])):
                if surfaces[x][y][z] == 6:
                    print("ERROR:", (x, y, z))
                    # exit(1)

                surface_area += surfaces[x][y][z]

    return surface_area

def part2():
    file.seek(0)
    return


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
