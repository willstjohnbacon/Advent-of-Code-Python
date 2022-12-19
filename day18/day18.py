from collections import deque
cubes = {}
TESTING = False
def part1(cubes):
    file.seek(0)
    lines = [line.rstrip() for line in file]

    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    min_z = float('inf')
    max_z = float('-inf')

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

def get_neighbours(cube):
    x, y, z = cube
    return [
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    ]

def part2(cubes):
    cubes = frozenset(cubes)
    min_x, min_y, min_z, max_x, max_y, max_z = 0, 0, 0, 0, 0, 0
    for x, y, z in cubes:
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        min_z = min(min_z, z)
        max_z = max(max_z, z)
    min_x -= 1
    min_y -= 1
    min_z -= 1
    max_x += 1
    max_y += 1
    max_z += 1

    water_points = set()
    q = deque()
    q.append((min_x, min_y, min_z))
    while q:
        x, y, z = q.popleft()
        if (x, y, z) in water_points:
            continue
        water_points.add((x, y, z))
        neighbours = get_neighbours((x, y, z))
        for nx, ny, nz in neighbours:
            if min_x <= nx <= max_x and min_y <= ny <= max_y and min_z <= z <= max_z:
                if (nx, ny, nz) not in cubes:
                    q.append((nx, ny, nz))

    lava_points = set()
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                if (x, y, z) not in water_points:
                    lava_points.add((x, y, z))

    return part1(lava_points)


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1(cubes))
print("Part 2: ", part2(cubes))
