TESTING = False

def readInput():
    file.seek(0)
    lines = [line.rstrip() for line in file]

    elves = []

    for y in range(0, len(lines)):
        for x in range(0, len(lines[0])):
            if lines[y][x] == "#":
                elves.append((y, x))

    # print(elves)
    return elves

def isIsolated(elfY, elfX, elves):
    for checkY in range(elfY - 1, elfY + 2):
        for checkX in range(elfX - 1, elfX + 2):
            if ((checkY, checkX) in elves) and ((checkY, checkX) != (elfY, elfX)):
                return False

    return True

def nearNeighbour(elfY, elfX, offsetY, offsetX, elves):
    if offsetY == 0:  # Checking E or W
        for checkY in range(elfY - 1, elfY + 2):
            if (checkY, elfX + offsetX) in elves:
                return True
    else:  # Checking N or S
        for checkX in range(elfX - 1, elfX + 2):
            if (elfY + offsetY, checkX) in elves:
                return True

    return False

def proposeNewPositions(elves, first_direction):
    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    proposals = []

    for elfY, elfX in elves:
        newPosY, newPosX = elfY, elfX

        if not isIsolated(elfY, elfX, elves):
            for check_num in range(0, 4):
                offsetY, offsetX = DIRECTIONS[(first_direction + check_num) % 4]

                if nearNeighbour(elfY, elfX, offsetY, offsetX, elves):
                    continue

                newPosY = elfY + offsetY
                newPosX = elfX + offsetX
                break

        # print(f"Elf at ({elfY}, {elfX}) proposes ({newPosY}, {newPosX})")
        proposals.append((newPosY, newPosX))

    return proposals

def moveToNewPositions(elves, proposals):
    new_elves = []
    elf_moved = False

    for current, proposed in zip(elves, proposals):
        if proposals.count(proposed) > 1:
            new_elves.append(current)
        else:
            if proposed != current:
                elf_moved = True
            new_elves.append(proposed)

    return new_elves, elf_moved

def countEmptyTiles(elves):
    minX = minY = float('inf')
    maxX = maxY = float('-inf')

    for elfY, elfX in elves:
        minY = min(minY, elfY)
        minX = min(minX, elfX)
        maxY = max(maxY, elfY)
        maxX = max(maxX, elfX)

    num_elves = len(elves)
    num_tiles = (maxX - minX + 1) * (maxY - minY + 1)

    return num_tiles - num_elves

def part1():
    first_direction = 0

    elves = readInput()

    for round_num in range(0, 10):
        print(f"Round {round_num}, first direction {first_direction}")
        print(elves)

        proposals = proposeNewPositions(elves, first_direction)
        # print(proposals)

        elves, _ = moveToNewPositions(elves, proposals)

        #First direction to check increments by one after each round (cyclical)
        first_direction = (first_direction + 1) % 4

    print(elves)

    return countEmptyTiles(elves)

def part2():
    first_direction = 0

    elves = readInput()

    round_num = 0
    elf_moved = True

### Adjust to run until no elves moved
    while elf_moved:
        round_num += 1

        print(f"Round {round_num}, first direction {first_direction}")
        # print(elves)

        proposals = proposeNewPositions(elves, first_direction)
        # print(proposals)

        elves, elf_moved = moveToNewPositions(elves, proposals)

        #First direction to check increments by one after each round (cyclical)
        first_direction = (first_direction + 1) % 4

    # print(elves)
    return round_num


if TESTING:
    file = open("sampleInput.txt", "r")
else:
    file = open("input.txt", "r")

print("Part 1: ", part1())
print("Part 2: ", part2())
